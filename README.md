# COS484 Final Project
This is the code directory for the COS484 final project.

## Environment setup
For this project, conda was used.

1. `conda create --name xword python=3.8`
2. `conda activate xword`
3. `pip install -r requirements.txt`

You'll next need to generate an OpenAI key to use for the project. Please create a file called `.env` and place the key in this format:
```
KEY="YOURKEYGOESHERE"
```

In order to run on an example puzzle, you'll first need the `.puz` file associated with that particular mini puzzle.

From there, the process goes as follows:
1. `python utils.py puzzle.puz puzzle.json`
2. `python generate_clues.py puzzle.json clue_output.json ./database/CLUEDATABASE`
3. `python solver.py puzzle.json clue_output.json puzzle_answers.json`
4. `python eval.py puzzle.puz puzzle_answers.json`

This is the entire process of converting the puzzle to the necessary grid, generating the clues for each clue in hte puzzle, solving it (or not) based on the constraints, and then evaluating it.