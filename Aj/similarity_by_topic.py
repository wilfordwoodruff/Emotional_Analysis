import pandas as pd
import numpy as np
import janitor
from scipy.spatial import distance_matrix




df = pd\
    .read_csv("../derived_data.csv")\
    .dropna(subset=["Topics"])\
    .clean_names()\
    .drop(columns=['document_type', 'parent_id', 'order', 'parent_name','uuid', 'name', 'website_url', 'short_url', 'image_url','original_transcript', 'text_only_transcript', 'people', 'places','first_date', 'dates'])\
    .reset_index(drop=True)

topics = pd\
    .Series("|"
            .join(df["topics"].astype(str))
            .split("|"))\
    .replace('nan',np.nan)\
    .dropna()\
    .reset_index()\
    .rename(columns={0:"Topics"})\
    .groupby("Topics", as_index=False)\
    .count()\
    .sort_values("index", ascending=False)\
    .query("Topics != 'Utah' & Topics != '' ")\
    .assign(cdf_ithink=lambda x: x["index"].cumsum() / x["index"].sum())\
    .query("cdf_ithink<.75")\
    .clean_names()\
    .reset_index(drop=True)

    
for topic in topics["topics"]:
    df[topic] = df["topics"].str.contains(topic)

df = df\
    .drop(columns="topics")\
    .clean_names()\
    .replace({True:1,False:0})\
    .drop(columns=["internal_id"])



dist_matrix = distance_matrix(df.values, df.values)

n_closest = 3 
closest_rows = {}
for i, distances in enumerate(dist_matrix):
    closest_indices = np.argsort(distances)[1:n_closest + 1]
    closest_rows[i] = closest_indices.tolist()

df['Closest_Rows'] = pd.Series(closest_rows)

for i in range(n_closest):
    df[f'Closest_{i+1}'] = df['Closest_Rows'].apply(lambda x: x[i])

df_close = df\
        .drop('Closest_Rows', axis=1)\
        .filter(items=["Closest_1", "Closest_2", "Closest_3"])\
        .reset_index(drop=True)

df_papers = pd\
    .read_csv("../derived_data.csv")\
    .dropna(subset=["Topics"])\
    .clean_names()\
    .reset_index(drop=True)


similarity_by_topic = pd\
        .concat([df_papers, df_close], axis=1)\
        .reset_index(drop=False)\
        .rename(columns={'index':"aj_id"})

similarity_by_topic.to_csv("similarity_by_topic.csv")