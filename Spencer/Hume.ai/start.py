#%%
import requests
import pandas as pd
full = pd.read_csv('../../derived_data.csv')

uuids = ['49e2ab1c-4e61-4a90-b109-4c216e9fd7a4',
'683a68cc-fda4-43ca-a6cb-360fff93ddc8',
'7685247d-8215-474a-b75b-174c146558f3',
'bfac4c8c-b683-476d-9692-20987d1bf12e',
'a7eef15d-e36b-4653-98ff-296ec93ea2aa',
'fb4934b2-7830-41f9-b070-31126ebc5134',
'd7edb0ef-4712-40e5-ad0c-8a1442236363',
'6f45867c-6f95-4ad9-85aa-d19862fd783e',
'de3368c0-8ad2-498a-891a-987d3cbf3785',
'093763d7-fd65-417d-8993-99e97d74e2a1',
'dbc5a49a-539c-41a8-82fd-7ad957fe42aa']

pages = full[full['UUID'].isin(uuids)]
hume_api_key = 'hRRgvtBFS46E9qOZg28eGZiAFzZxeiHwxGmvbV49GRTLNHpo'
#%%

#Turn 10 pages into txt files for URL link
import os
output_directory = 'text_files'
os.makedirs(output_directory, exist_ok=True)


series = pages['Text Only Transcript']
for index, text_item in enumerate(series):
    filename = f'UUID:{index + 1}.txt'
    filepath = os.path.join(output_directory, filename)
    
    with open(filepath, 'w') as file:
        file.write(text_item)

    print(f'Saved {filename}')

#%%

urls = []
for i in range(2):
    urls.append('https://raw.githubusercontent.com/wilfordwoodruff/Emotional_Analysis/main/Spencer/Hume.ai/text_files/text_item_' + str(i+1) + '.txt')

#%%
from utilities import print_emotions, print_sentiment

from hume import HumeBatchClient
from hume.models.config import LanguageConfig

client = HumeBatchClient(hume_api_key)
#urls = ['']
config = LanguageConfig(sentiment={})
job = client.submit_job(urls, [config])

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
job.download_predictions("two_files.json")
job.download_artifacts("two_files.zip")
print(f"\nPredictions downloaded to predictions.json")
# %%
scores= pd.read_excel('journal_1_averages.xlsx')
scores = scores.transpose().reset_index()
scores.columns = ['Emotion','Score']
scores.sort_values('Score',ascending=False)



#%%
#Copied from Website, havent used
from hume import HumeBatchClient
from hume.models.config import FaceConfig

client = HumeBatchClient(hume_api_key)
filepaths = [
  "faces.zip",
  "david_hume.jpeg",
]
config = FaceConfig()
job = client.submit_job(None, [config], files=filepaths)

print(job)
print("Running...")

details = job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")