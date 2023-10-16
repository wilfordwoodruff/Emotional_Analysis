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
job.download_artifacts("full_text.zip")
print(f"\nPredictions downloaded to predictions.json")
# %%