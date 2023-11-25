import openai
import csv
import requests
import time

## ADJUST AS NECESSARY:

api_key = "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"

input_file_path = "Desktop/School/current semester/Consulting Wilford Woodruff/RUN WITH GPT.csv"
column_to_read = 2  # Change this to 2 to read the third column 
output_file_path = "Desktop/School/current semester/Consulting Wilford Woodruff/GPT RESULTS RAW.csv"

start_row = 301       # Change this to start from a different row
end_row = 5000        # Change this to specify the number of rows to analyze
# Will do start row to end row - 1 (ex: if start row = 10, end row = 20, will do 10-19)


### THE CODE DOES THE REST

openai.api_key = api_key

def analyze_emotions(text, prompt, i):
    response = None
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.0,  # Set temperature to 0 for deterministic output
            max_tokens=1000  
        )
    except:
        print(f"API request for row '{i}' timed out. Skipping.")
        return "Timeout or Error"
    

    return response['choices'][0]['message']['content']


with open(input_file_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # Read the header row

    with open(output_file_path, "a", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)

        for i, row in enumerate(reader):
            if i < start_row:
                continue
            if i >= end_row:
                break

            journal_entry = row[column_to_read]  # Read the specified column

            emo = ['Neutral', 'Enthusiasm', 'Joy', 'Hope', 'Satisfaction', 'Sad', 'Anger', 'Fear']
            prompt = f"You are a helpful assistant that analyzes emotions. Analyze the text and respond in the following format [{emo[0]} : score_1, {emo[1]} : score_2, {emo[2]} : score_3, {emo[3]} : score_4, {emo[4]} : score_5, {emo[5]} : score_6, {emo[6]} : score_7, {emo[7]} : score_8]. Match the format EXACTLY, giving a score (1 to 10) for each of the 8 emotions. ONLY analyze these emotions."
            emotions_analysis = analyze_emotions(journal_entry, prompt, i)
            time.sleep(.5)
            print(i)
            # Write the analysis results to the second column
            row.append(emotions_analysis)
            writer.writerow(row)
