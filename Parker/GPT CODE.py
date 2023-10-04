import openai
import csv

api_key = "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"
openai.api_key = api_key

def analyze_emotions(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes emotions. This is the list of all possible emotions: (Emotions: Anger, Anticipation, Joy, Fear, Disgust, Positive, Negative, Sadness, Surprise, and Trust). Make a bulleted list of ONLY FIVE words/phrases that evoke emotion from the text and then. MOST IMPORTANT PART: return the top 3 emotions with scores in EXACTLY this format ['emotion_1 : score_1', 'emotion_2 : score_2', 'emotion_3 : score_3']:"},
            {"role": "user", "content": text},
        ],
        temperature=0.0,  # Set temperature to 0.0 for deterministic output
        max_tokens=300  # Limit the response length
    )
    return response['choices'][0]['message']['content']

with open("Desktop/Consulting Wilford Woodruff/WW_cleaned.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  
    for i, row in enumerate(reader):
        if i >= 5:  # Analyzes the first 5 entries
            break

        journal_entry = row[0]
        emotions_analysis = analyze_emotions(journal_entry)

        print("Emotions:")
        print(emotions_analysis)
        print("=" * 50)
