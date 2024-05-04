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