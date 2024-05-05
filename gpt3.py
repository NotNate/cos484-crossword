import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def recommend_crossword_answers(clue, length, amount):
    # Retrieve API key from environment variable
    api_key = os.getenv("KEY")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        # LEFT AS DEFAULT FOR TESTING, CHANGE WITH YOUR FINETUNED VERSION
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a crossword clue answer recommender. Given a length, you will return crossword answers that may match the answer to the clue of a certain length, and return in JSON format.\n\nPlease ensure they are the correct length, and do not output things of the wrong length.\n\nExample:\nCLUE: Pool activity \nLENGTH: 4\n\nOutput:\n{{\"swim\", \"dive\", \"wade\" ... }}"
            },
            {"role": "user", "content": f'CLUE:{clue}\nLENGTH:{length}\nAMOUNT:{amount}'},
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content

def filter_crossword_answers(output, length):
    # Convert the output JSON string to a set
    answers = set(output.strip('{}').replace('"', '').split(', '))

    # Filter out words that don't match the original length
    filtered_answers = [word for word in answers if len(word) == length]

    return filtered_answers

def get_answer(clue, length, amount):
    output = recommend_crossword_answers(clue, length, amount)
    return filter_crossword_answers(output, length)
