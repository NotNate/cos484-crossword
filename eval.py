import argparse
import puz
import json

def compare_answers(puz_file, json_file):
    # Load crossword puzzle from .puz file
    puzzle = puz.read(puz_file)
    numbering = puzzle.clue_numbering()

    # Load clue answer pairs from JSON file
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Initialize counters for correct and total answers
    correct_answers = 0
    total_answers = 0
    incorrect_letters = 0
    total_letters = 0
    incorrect_details = []

    # Compare answers
    for clue in numbering.across:
        answer = ''.join(puzzle.solution[clue['cell'] + i] for i in range(clue['len']))
        clue_text = ' '.join(word.capitalize() for word in clue['clue'].split())
        if clue_text in json_data:
            total_answers += 1
            total_letters += len(answer)
            json_answer = json_data[clue_text].lower()
            if answer.lower() == json_answer:
                correct_answers += 1
            else:
                correct_letters = sum(a == b for a, b in zip(answer.lower(), json_answer))
                incorrect_letters += abs(len(answer) - correct_letters)
                incorrect_details.append({
                    "clue": clue_text,
                    "correct": answer,
                    "incorrect": json_answer
                })

    for clue in numbering.down:
        answer = ''.join(puzzle.solution[clue['cell'] + i * numbering.width] for i in range(clue['len']))
        clue_text = ' '.join(word.capitalize() for word in clue['clue'].split())
        if clue_text in json_data:
            total_answers += 1
            total_letters += len(answer)
            json_answer = json_data[clue_text].lower()
            if answer.lower() == json_answer:
                correct_answers += 1
            else:
                correct_letters = sum(a == b for a, b in zip(answer.lower(), json_answer))
                incorrect_letters += abs(len(answer) - correct_letters)
                incorrect_details.append({
                    "clue": clue_text,
                    "correct": answer,
                    "incorrect": json_answer
                })

    return correct_answers, total_answers, incorrect_letters, total_letters, incorrect_details

def main():
    parser = argparse.ArgumentParser(description='Compare clue answer pairs from a .puz puzzle with a JSON file.')
    parser.add_argument('puz_file', help='Path to the .puz file')
    parser.add_argument('json_file', help='Path to the JSON file containing clue answer pairs')
    args = parser.parse_args()

    correct, total, incorrect_letters, total_letters, incorrect_details = compare_answers(args.puz_file, args.json_file)
    if incorrect_details:
        print("Incorrect answers:")
        for incorrect in incorrect_details:
            print(f"Clue: {incorrect['clue']}")
            print(f"Correct: {incorrect['correct']}")
            print(f"Yours: {incorrect['incorrect']}\n")

    print(f"Correct answers: {correct} out of {total}")
    print(f"Correct letters: {incorrect_letters} out of {total_letters}")

if __name__ == "__main__":
    main()
