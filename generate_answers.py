import json
import math
import re
from collections import Counter
from nltk.corpus import stopwords
import gpt3
import utils
import argparse

class ClueGenerator:
    def __init__(self):
        self.stop_words = set(stopwords.words('english') + [""])

    def _calculate_cosine_similarity(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def _preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return [word for word in text.split() if word not in self.stop_words]

    def _load_dictionary(self, all_solution_path):
        with open(all_solution_path, encoding="latin-1") as fp:
            return fp.readlines()

    def _map_clues_to_guesses(self, clues, dict_guesses):
        clue_mapping = {clue: [] for clue in clues}
        all_lengths = list(set(clues.values()))
        clue_statements = list(clues.keys())
        clue_vecs = {clue: self._preprocess_text(clue) for clue in clue_statements}

        for guess in dict_guesses:
            guess_word = guess.split()[0]
            if len(guess_word) not in all_lengths:
                continue
            guess_statement = " ".join(guess.split()[4:])
            guess_vec = Counter(self._preprocess_text(guess_statement))

            for clue in clue_statements:
                if len(guess_word) == clues[clue]:
                    clue_vec = Counter(clue_vecs[clue])
                    similarity = self._calculate_cosine_similarity(guess_vec, clue_vec)
                    if similarity > 0.6:
                        clue_mapping[clue].append(guess_word.lower())

        for clue in clues:
            clue_mapping[clue] = list(set(clue_mapping[clue]))

        return clue_mapping

    def _all_solution(self, clues, all_solution_path):
        dict_guesses = self._load_dictionary(all_solution_path)
        clue_mapping = self._map_clues_to_guesses(clues, dict_guesses)
        return clue_mapping

    def _fetch_words(self, clues, clue_pairings, clues_path):
        all_solved = self._all_solution(clues, clue_pairings)

        for clue in all_solved.keys():
            backup_answers = gpt3.get_answer(clue, clues[clue], amount=20)
            all_solved[clue] += list(backup_answers)
            all_solved[clue] = list(set(all_solved[clue]))

        print("Storing answers to clues...")
        with open(clues_path, "w") as fp:
            json.dump(str(all_solved), fp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('grid_path', help='Path to the grid JSON file')
    parser.add_argument('clues_path', help='Path to store the clues JSON file')
    parser.add_argument('clue_pairings', help='Path to the clue-answer pairing file')
    args = parser.parse_args()

    grid = utils.load_grid(args.grid_path)
    clues = {clue: grid[clue]["length"] for clue in grid}

    ClueGenerator()._fetch_words(clues, args.clue_pairings, args.clues_path)