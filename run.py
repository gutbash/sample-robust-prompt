import csv
from os import environ
from model.openai import OpenAI
from message.message import SystemMessage, UserMessage, ModelMessage
import asyncio
from pathlib import Path

# Set your OpenAI API key
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")

# Read data from the CSV file
def read_data_from_csv(file_name: Path) -> list[list[str]]:
    data = []
    with open(file_name, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

# Write data to a new CSV file
def write_data_to_csv(file_name: Path, data: list[list[str]]):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Main function to process data
async def process_data(input_file: Path, output_file: Path, limit: int = None, trials: int = 5):
    
    # Initialize the OpenAI model
    openai = OpenAI(
        OPENAI_API_KEY,
        model="gpt-4-turbo",
        temperature=0.2,
    )
    
    # Read data from the input CSV
    data = read_data_from_csv(input_file)
    new_data = []
    new_data.append([
        "model_response",  # Model Response
        "class_id",   # Class ID
        "created",   # Created
        "prompt",    # Prompt
        "question_id",  # Question ID
        "stderr",    # Stderr
        "stdout",    # Stdout
        "user_email", # User Email
        "user_ip",    # User IP
        "completion_object",  # Completion Object
        "trial_id",     # Trial Number
    ])

    # Iterate over each row
    for i, row in enumerate(data[1:], start=1):  # Skip the header row
        if limit is not None and i > limit:
            break
        prompt = row[3]  # Fetch the prompt from the "Prompt" column
        for trial in range(1, trials + 1):  # Generate 5 trials
            
            messages = [
                UserMessage(prompt),
            ]
            
            response, completion = await openai.arun(messages)
            
            # convert python code block to plain
            response = response.replace("```python", "```")
            # extract code block and save to response
            response = response.split("```")[1]
            
            new_row = [
                response,  # model response
                row[1],    # Class ID
                row[2],    # Created
                prompt,    # Prompt
                row[4],    # QuestionID
                row[5],    # Stderr
                row[6],    # Stdout
                row[7],    # UserEmail
                row[8],    # UserIp
                completion,  # Completion Object
                trial,      # Trial Number
            ]
            new_data.append(new_row)

    # Write the new data into a new CSV file
    write_data_to_csv(output_file, new_data)

# Input and Output file names
input_file = Path('data/input/attempts-2023-07-29T08_36_51.352Z.csv')
output_file = Path('data/output/attempts-2023-07-29T08_36_51.352Z-sampled.csv')

# Call the main function to process the data
asyncio.run(process_data(input_file, output_file, limit=1, trials=3))