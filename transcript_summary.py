from openai import OpenAI
import os
import json
import tkinter as tk
from tkinter import filedialog


# Set your OpenAI API key here
api_key = ""

client = OpenAI(api_key=api_key)


# Function to process the transcript and return the response
def process_transcript(transcript):
# Example JSON structure for the response
    example_json_response = json.dumps({
        "Main topic": "Example Topic",
        "Brief Summarization": "Example Summarization",
        "List of Keywords": ["Keyword1", "Keyword2"],
        "List of Names": ["Name1", "Name2"],
        "List of important terms or jargon with brief definitions": [
            {"term": "Term1", "definition": "Definition1"},
            {"term": "Term2", "definition": "Definition2"},

        ],
        "List of concepts that may be difficult to interpret": [
            {"concept": "Concept1", "brief explanation": "Explanation1"},
            {"concept": "Concept2", "brief explanation": "Explanation2"}
        ]
    }, indent=4)

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "Please analyze the transcript and provide the following information in JSON format as shown in the example:\n" + example_json_response
            },
            {
                "role": "user",
                "content": transcript
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
    
    

# Function to select files and process them
def select_files_and_process():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # File dialog to select one or more .txt files
    file_paths = filedialog.askopenfilenames(
        title='Select one or more text files', 
        filetypes=[('Text Files', '*.txt')]
    )

    for file_path in file_paths:
        print('Processing' + file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            transcript = file.read()

        # Process the transcript
        response_content = process_transcript(transcript)

        # Save the response in a JSON file with the same base name as the text file
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        json_file_path = f"{base_name}_analysis.json"
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(response_content)

        print(f"Analysis saved in {json_file_path}")

# Run the file selection and processing
select_files_and_process()