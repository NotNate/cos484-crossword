from ast import literal_eval
from tabulate import tabulate
import json
import z3
import argparse
import utils

class CrosswordPuzzleSolver:
    def __init__(self, grid_file, clues_file, output_file):
        self.grid_file = grid_file
        self.grid_data = utils.load_grid(grid_file)
        self.clues_file = clues_file
        self.output_file = output_file

    def get_clues(self):
        with open(self.clues_file) as fp:
            return literal_eval(json.load(fp))

    def generate_grid(self):
        clues = self.get_clues()
        start_pos = {}

        max_coord = 0
        for clue in self.grid_data:
            start_pos[tuple(self.grid_data[clue]["start"])] = clue

            max_coord = max(max_coord, self.grid_data[clue]["start"][0], self.grid_data[clue]["start"][1])

        max_coord += 1

        grid = [[None for _ in range(max_coord)] for _ in range(max_coord)]

        for x in range(max_coord):
            for y in range(max_coord):
                if (x, y) in start_pos:
                    pos_data = self.grid_data[start_pos[(x, y)]]
                    for i in range(pos_data["length"]):
                        if pos_data["direction"] == "A":
                            if isinstance(grid[x][y + i], z3.z3.ArithRef):
                                grid[x][y + i] = (z3.Int(f"col_{x}_{y + i}"), z3.Int(f"row_{x}_{y + i}"))
                            else:
                                grid[x][y + i] = z3.Int(f"cell_{x}_{y + i}")
                        elif pos_data["direction"] == "D":
                            if isinstance(grid[x + i][y], z3.z3.ArithRef):
                                grid[x + i][y] = (z3.Int(f"col_{x + i}_{y}"), z3.Int(f"row_{x + i}_{y}"))
                            else:
                                grid[x + i][y] = z3.Int(f"cell_{x + i}_{y}")

        return grid, start_pos, max_coord

    def encode_clues(self):
        clues = self.get_clues()
        encoded_clues = {}

        for clue in clues:
            encoded_clues[clue] = [[ord(ch) for ch in guess.lower()] for guess in clues[clue]]

        return encoded_clues

    def generate_guess_constraints(self):
        encoded_clues = self.encode_clues()
        grid, start_pos, max_coord = self.generate_grid()

        guess_constraints = []

        for x in range(max_coord):
            for y in range(max_coord):
                if (x, y) in start_pos:
                    pos_data = self.grid_data[start_pos[(x, y)]]
                    clue = start_pos[(x, y)]

                    if clue in encoded_clues and encoded_clues[clue]:
                        all_guess_constraints = []

                        for guess_encoded in encoded_clues[clue]:
                            single_guess_constraint = []
                            x_i, y_i = x, y

                            for ch in guess_encoded:
                                if isinstance(grid[x_i][y_i], tuple):
                                    cell_val = grid[x_i][y_i][0] if pos_data["direction"] == "D" else grid[x_i][y_i][1]
                                else:
                                    cell_val = grid[x_i][y_i]

                                single_guess_constraint.append(z3.And(cell_val == ch))

                                x_i += 1 if pos_data["direction"] == "D" else 0
                                y_i += 1 if pos_data["direction"] == "A" else 0

                            all_guess_constraints.append(z3.And(single_guess_constraint))

                        guess_constraints.append(z3.Or(all_guess_constraints))

        return z3.And(guess_constraints)

    def generate_intersection_constraints(self):
        grid, _, max_coord = self.generate_grid()

        intersection_constraints = []

        for x in range(max_coord):
            for y in range(max_coord):
                if isinstance(grid[x][y], tuple):
                    col_val, row_val = grid[x][y]
                    intersection_constraints.append(z3.And(col_val == row_val))

        return z3.And(intersection_constraints)

    def solve(self):
        solver = z3.Solver()
        solver.add(self.generate_guess_constraints())
        solver.add(self.generate_intersection_constraints())
        solver.check()

        return solver.model()

    def display_solution(self):
        solution = self.solve()
        grid, start_pos, max_coord = self.generate_grid()
        clues = self.get_clues()
        answer_pairs = {}

        for x in range(max_coord):
            for y in range(max_coord):
                if (x, y) in start_pos:
                    clue = start_pos[(x, y)]
                    answer = ""
                    pos_data = self.grid_data[clue]
                    x_i, y_i = x, y

                    for _ in range(pos_data["length"]):
                        if isinstance(grid[x_i][y_i], tuple):
                            cell_val = grid[x_i][y_i][0] if pos_data["direction"] == "D" else grid[x_i][y_i][1]
                        else:
                            cell_val = grid[x_i][y_i]

                        num = solution[cell_val]
                        ch = chr(num.as_long())
                        answer += ch

                        x_i += 1 if pos_data["direction"] == "D" else 0
                        y_i += 1 if pos_data["direction"] == "A" else 0

                    answer_pairs[clue] = answer

        self.save_answer_pairs(answer_pairs)

        for x in range(max_coord):
            for y in range(max_coord):
                if isinstance(grid[x][y], tuple):
                    cell_val = grid[x][y][0]
                elif grid[x][y] is not None:
                    cell_val = grid[x][y]
                else:
                    continue

                num = solution[cell_val]
                ch = chr(num.as_long())
                grid[x][y] = ch

        return tabulate(grid)

    def save_answer_pairs(self, answer_pairs):
        with open(self.output_file, 'w') as fp:
            json.dump(answer_pairs, fp, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('grid_file', help='Path to the crossword grid JSON file')
    parser.add_argument('clues_file', help='Path to the clues JSON file')
    parser.add_argument('output_file', help='Path to the output file for saving clues and answers')
    args = parser.parse_args()

    solver = CrosswordPuzzleSolver(args.grid_file, args.clues_file, args.output_file)
    print(solver.display_solution())
    correct, total = utils.compare_answers("nymold.puz", args.output_file)
    print(f"Correct: {correct}, Total: {total}")