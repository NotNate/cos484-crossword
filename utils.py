import puz
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