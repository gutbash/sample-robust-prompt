import csv
from os import environ
from model.openai import OpenAI
from message.message import SystemMessage, UserMessage, ModelMessage
import asyncio

# Set your OpenAI API key
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")

# Read data from the CSV file
def read_data_from_csv(file_name):
    data = []
    with open(file_name, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

# Write data to a new CSV file
def write_data_to_csv(file_name, data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Main function to process data
async def process_data(input_file, output_file):
    
    openai = OpenAI(OPENAI_API_KEY)
    
    # Read data from the input CSV
    data = read_data_from_csv(input_file)

    # Iterate over each row
    for i, row in enumerate(data[1:], start=1):  # Skip the header row
        prompt = row[4]  # Fetch the prompt from the "Prompt" column
        for trial in range(1, 6):  # Generate 5 trials
            
            messages = [
                UserMessage(prompt),
            ]
            
            response = await openai.arun(messages)
            new_row = [
                response,  # ChatGPT response
                row[1],    # Class
                row[2],    # ID
                row[3],    # Created
                row[4],    # Prompt
                row[5],    # QuestionID
                row[6],    # Stderr
                row[7],    # Stdout
                row[8],    # UserEmail
                row[9],    # UserIp
                trial      # Trial Number
            ]
            data.append(new_row)

    # Write the new data into a new CSV file
    write_data_to_csv(output_file, data)

# Input and Output file names
input_file = 'input_data.csv'
output_file = 'output_data.csv'

# Call the main function to process the data
asyncio.run(process_data(input_file, output_file))