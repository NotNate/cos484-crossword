import argparse
import puz
import json

def convert_puz_to_dict(fname):
    puzzle = puz.read(fname)
    numbering = puzzle.clue_numbering()

    crossword_grid = {}

    # Processing across clues
    for clue in numbering.across:
        clue_text = ' '.join(word.capitalize() for word in clue['clue'].split())
        start_x = clue['cell'] % puzzle.width
        start_y = clue['cell'] // puzzle.width
        crossword_grid[clue_text] = {
            "start": (start_y, start_x),
            "direction": "A",
            "length": clue['len']
        }

    # Processing down clues
    for clue in numbering.down:
        clue_text = ' '.join(word.capitalize() for word in clue['clue'].split())
        start_x = clue['cell'] % puzzle.width
        start_y = clue['cell'] // puzzle.width
        crossword_grid[clue_text] = {
            "start": (start_y, start_x),
            "direction": "D",
            "length": clue['len']
        }

    return crossword_grid

def load_grid(grid_path):
    with open(grid_path) as fp:
        return json.load(fp)

def main():
    parser = argparse.ArgumentParser(description="Convert .puz crossword file to JSON format")
    parser.add_argument("input", help="Input .puz file")
    parser.add_argument("output", help="Output .json file")
    args = parser.parse_args()

    crossword_dict = convert_puz_to_dict(args.input)
    with open(args.output, 'w') as f:
        json.dump(crossword_dict, f, indent=4)

if __name__ == "__main__":
    main()
