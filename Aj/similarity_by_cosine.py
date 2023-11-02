import pandas as pd
import numpy as np
import janitor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df =  pd\
    .read_csv("../derived_data.csv")\
    .clean_names()

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['text_only_transcript'])

cosine_similarities = cosine_similarity(tfidf_matrix)

n_closest = 3
closest_texts = {}
for i, similarities in enumerate(cosine_similarities):
    closest_indices = np.argsort(similarities)[-n_closest-1:-1][::-1]
    closest_texts[i] = closest_indices.tolist()

df_close = pd\
    .DataFrame(closest_texts)\
    .T\
    .rename(columns={0:"Closest_1",
                     1:"Closest_2",
                     2:"Closest_3"})

similarity_by_cosine = pd.concat([df, df_close], axis=1)

similarity_by_cosine.to_csv("similarity_by_cosine.csv")