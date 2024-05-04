import os
from datetime import datetime, timedelta
import concurrent.futures
import subprocess

# Define the command template
command_template = "xword-dl {} --date {}"

# Define the download function
def download_puzzle(puzzle_type, date):
    date_str = date.strftime("%m/%d/%y")
    command = command_template.format(puzzle_type, date_str)
    subprocess.run(command, shell=True)
    return f"Downloaded {puzzle_type} puzzle for {date_str}"

def main():
    # Create a directory for puzzles if it doesn't exist
    base_directory = 'puzzles'
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Input start and end dates from the user
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    puzzle_type = input("Enter puzzle type (e.g., 'nyt', 'wsj'): ")

    # Convert input strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Create a subdirectory for the puzzle type
    puzzle_directory = os.path.join(base_directory, puzzle_type)
    if not os.path.exists(puzzle_directory):
        os.makedirs(puzzle_directory)

    # Change the working directory to the puzzle type directory
    os.chdir(puzzle_directory)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        futures = [executor.submit(download_puzzle, puzzle_type, date) for date in dates]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    print("All puzzles downloaded successfully.")

if __name__ == "__main__":
    main()
