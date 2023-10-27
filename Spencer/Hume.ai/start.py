#%%
import requests
import pandas as pd
import os
full = pd.read_csv('../../derived_data.csv')
hume_api_key = os.getenv('HUME_WWP_API') #('HUME_MY_API')#

#%%
from utilities import print_emotions, print_sentiment

from hume import HumeBatchClient
from hume.models.config import LanguageConfig

client = HumeBatchClient(hume_api_key)

def HumePerPage(page_num):
    url = 'https://github.com/wilfordwoodruff/Emotional_Analysis/blob/main/Spencer/Entries%20in%20200s/output_file_'+str(page_num)+'.txt'
    config = LanguageConfig(sentiment={})
    job = client.submit_job([url], [config])

    print("Running...", job)

    job.await_complete()
    print("Job ", page_num, " completed with status: ", job.get_status())
    job.download_artifacts("wwp"+str(page_num)+".zip")
#%%

#%%
for i in range(150):
    HumePerPage(i)
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
    #job.download_predictions("BIG3.json")
    job.download_artifacts("BIG3.zip")
    print(f"\nPredictions downloaded to predictions.json")
# %%
client.get_job('0aa7ca3f-0622-4806-924a-f050bbbee28e')

#%%
json_result = pd.read_json("C:/Users/spenc/Downloads/predictions-e39a5cb7-9016-4bed-b85d-498c53bdb8d9.json")

# Use the explode function to split the "predictions" list into rows
json_result = json_result.explode("results")
json_result = json_result['source'].explode('source')

# Reset the index for a clean DataFrame
json_result = json_result.reset_index(drop=True)
json_result.head()
