#%%
import requests
import pandas as pd
full = pd.read_csv('../../derived_data.csv')
hume_api_key = 'hRRgvtBFS46E9qOZg28eGZiAFzZxeiHwxGmvbV49GRTLNHpo'

#%%
from utilities import print_emotions, print_sentiment

from hume import HumeBatchClient
from hume.models.config import LanguageConfig

client = HumeBatchClient(hume_api_key)
url = ''
config = LanguageConfig(sentiment={})
job = client.submit_job(url, [config])

print("Running...", job)

job.await_complete()
print("Job completed with status: ", job.get_status())
# %%
full_predictions = job.get_predictions()
for source in full_predictions:
    source_name = source["source"]["url"]
    predictions = source["results"]["predictions"]
    for prediction in predictions:
        language_predictions = prediction["models"]["language"]["grouped_predictions"]
        for language_prediction in language_predictions:
            for chunk in language_prediction["predictions"]:
                print(chunk["text"])
                print_emotions(chunk["emotions"])
                print("~ ~ ~")
                print_sentiment(chunk["sentiment"])
                print()
# %%
job.download_predictions("full_text.json")
#job.download_artifacts("full_text.zip")
print(f"\nPredictions downloaded to predictions.json")
# %%
import pandas as pd

data = {
    'Word': ['word1', 'word2', 'NEW_ENTRY', 'word3', 'word4', 'NEW_ENTRY', 'word5', 'word6', 'NEW_ENTRY'],
    'Score': [1.0, 2.0, 0.0, 3.0, 4.0, 0.0, 2.5, 1.5, 0.0]
}

results = pd.DataFrame(data)

print(results)

#df = pd.read_json('full_text.json')

# Initialize variables for grouping
current_group = 0
group_scores = []

# Create a new column 'Group' to identify groups based on 'Word' column
results['Entry'] = 0

# Iterate through the rows and assign groups
for index, row in results.iterrows():
    if row['Word'] == 'NEW_ENTRY':
        current_group += 1
    results.at[index, 'Entry'] = current_group

# Filter out rows with 'NEW_ENTRY' in 'Word' column
df = results[results['Word'] != 'NEW_ENTRY']

# Group by 'Group' and calculate the average score for each group
result = df.groupby('Entry').mean().reset_index()

# Reset index for the result DataFrame
result.reset_index(drop=True, inplace=True)

# Print the result
print(result)

# %%
