import pandas as pd
import polars as pl
import numpy as np
import janitor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import streamlit as st

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pl\
    .read_csv('../../derived_data.csv')\
    .rename({
        'Internal ID': 'internal_id',
        'Document Type': 'document_type',
        'Parent ID': 'parent_id',
        'Order': 'order',
        'Parent Name': 'parent_name',
        'UUID': 'uuid',
        'Name': 'name',
        'Website URL': 'website_url',
        'Short URL': 'short_url',
        'Image URL': 'image_url',
        'Original Transcript': 'original_transcript',
        'Text Only Transcript': 'text_only_transcript',
        'People': 'people',
        'Places': 'places',
        'First Date': 'first_date',
        'Dates': 'dates',
        'Topics': 'topics'})\
    .select(['internal_id', 'text_only_transcript', 'people', 'places', 'topics'])\
    .with_columns([
        pl.col("text_only_transcript").fill_null(""),
        pl.col("people").fill_null(""),
        pl.col("places").fill_null(""),
        pl.col("topics").fill_null("")])\
    .with_columns([
        pl\
            .col("text_only_transcript")\
            .str\
            .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|January|February|March|April|May|June|July|August|September|October|November|December", " "),

        pl\
            .col("people")\
            .str\
            .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", " ")\
            .alias("text_people"),
        pl\
            .col("places")\
            .str\
            .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", " ")\
            .alias("text_places"),
        pl\
            .col("topics")\
            .str\
            .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", " ")\
            .alias("text_topics")])

def sim_maker(df, var):

    """
    This makes a similarity matrix for a given col (var) in the dataframe.
    """

    def create_tfidf_matrix(data, stop_words='english'):
        tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
        tfidf_matrix = tfidf_vectorizer.fit_transform(data)
        return tfidf_matrix

    tfidf_matrix_var = create_tfidf_matrix(df[var])
    var_similarity = cosine_similarity(tfidf_matrix_var)

    return var_similarity

ndarray_wwtext = sim_maker(df, 'text_only_transcript')
ndarray_people = sim_maker(df, 'text_people')
ndarray_places = sim_maker(df, 'text_places')
ndarray_topics = sim_maker(df, 'text_topics')


def closest_indices_df(ndarray, n_top=4):
    df_var = pd.DataFrame(ndarray)
    df_var.columns = list(df['internal_id'])
    df_var.index = list(df['internal_id'])

    top_three = df_var.apply(lambda x: x.nlargest(n_top).index.tolist(), axis=1)
    top_three_df = pd.DataFrame(top_three.tolist())
    top_three_df = top_three_df.rename(columns={0: 'internal_id', 1: 'closest_1', 2: 'closest_2', 3: 'closest_3'})

    return top_three_df

wwtext_df_sort = closest_indices_df(ndarray_wwtext)
people_df_sort = closest_indices_df(ndarray_people)
places_df_sort = closest_indices_df(ndarray_places)
topics_df_sort = closest_indices_df(ndarray_topics)

wwtext_df_sort.to_csv("wwtext_df.csv", index=False)
people_df_sort.to_csv("people_df.csv", index=False)
places_df_sort.to_csv("places_df.csv", index=False)
topics_df_sort.to_csv("topics_df.csv", index=False)

