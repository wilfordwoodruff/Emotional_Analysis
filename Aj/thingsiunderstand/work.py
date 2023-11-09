import pandas as pd
import polars as pl
import numpy as np
import janitor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import streamlit as st

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define the data
@st.cache_data
def sim_maker(_df, var):

    """
    This makes a similarity matrix for a given col (var) in the dataframe.
    """

    def create_tfidf_matrix(data, stop_words='english'):
        tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
        tfidf_matrix = tfidf_vectorizer.fit_transform(data)
        return tfidf_matrix

    tfidf_matrix_var = create_tfidf_matrix(df[f'{var}'])
    var_similarity = cosine_similarity(tfidf_matrix_var)

    var_df = pd.DataFrame(var_similarity)

    # Specify the columns to INTERNAL ID
    var_df.columns = df["internal_id"].to_pandas().astype(str)
    var_df.columns.name = None

    # Specify the rows to INTERNAL ID
    var_df["internal_id"] = df["internal_id"]

    return var_df

@st.cache_data
def make_df_display():
    df_display = pl\
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
            pl.col("people").fill_null(""),
            pl.col("places").fill_null(""),
            pl.col("topics").fill_null("")])\
        .with_columns([
            pl\
                .col("text_only_transcript")\
                .str\
                .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", " "),
            pl\
                .col("people")\
                .str\
                .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", ", "),
            pl\
                .col("places")\
                .str\
                .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", ", "),
            pl\
                .col("topics")\
                .str\
                .replace_all(r"\||\[\[|\]\]|\\r|\\t|\\n", ", ")])
    
    return df_display

@st.cache_data
def make_df():
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

    return df

with st.status("Loading and calculating..."):
    st.write("Defining data...")
    
    df_display = make_df_display()

    df = make_df()

    # Modified DF
    
    st.write("Defining similarity matrices...")

    raw_text_sims = sim_maker(df, 'text_only_transcript')
    # raw_people_sims = sim_maker(df, 'people')
    # raw_places_sims = sim_maker(df, 'places')
    # raw_topics_sims = sim_maker(df, 'topics')

    st.write("Finished!")


def results_df_maker(internal_id, 
                     var_df, 
                     keep_columns=["internal_id", "text_only_transcript"]):

    """
    This takes the similarity matrix and returns the top 3 results.
    """

    results_text = pl\
        .DataFrame(
            var_df\
                .query(f"internal_id == {internal_id}")\
                .drop("internal_id", axis=1))\
        .transpose()\
        .rename({"column_0": "similarity"})\
        .with_columns(df["internal_id"].alias("internal_id"))\
        .sort('similarity', descending=True)\
        .head(4)\
        .tail(3)

    results_df = df_display\
        .filter(pl.col("internal_id")\
                .is_in(results_text["internal_id"].to_list()))\
        .select(keep_columns)
    
    return results_df

def grab_from_internal_id(internal_id, column_name):
    return df_display\
        .filter(pl.col("internal_id") == internal_id)\
        [column_name]\
        .to_list()[0]

######################
# Sidebar
######################

input_number = st.sidebar.number_input("Choose internal_id to analyze:", 
                min_value=df['internal_id'].min(),
                max_value=df['internal_id'].max(), 
                value=42, 
                step=1)

st.sidebar.write("Topics:")
st.sidebar.write(f":blue[{grab_from_internal_id(input_number, 'topics')}]")
st.sidebar.write("People:")
st.sidebar.write(f":red[{grab_from_internal_id(input_number, 'people')}]")
st.sidebar.write("Places:")
st.sidebar.write(f":green[{grab_from_internal_id(input_number, 'places')}]")
st.sidebar.write("Transcript:")
st.sidebar.write(grab_from_internal_id(input_number, "text_only_transcript"))

######################
# Main Page
######################

st.title("Woodruff Similarity Algorithm")

results_df = results_df_maker(input_number, raw_text_sims, ["internal_id", "text_only_transcript"])


col1, col2, col3 = st.tabs(["1st", "2nd", "3rd"])

with col1:
    id = results_df["internal_id"].to_list()[0]
    st.write(f"Internal ID:{id}")
    st.write("Topics:")
    st.write(f":blue[{grab_from_internal_id(id, 'topics')}]")
    st.write("People:")
    st.write(f":red[{grab_from_internal_id(id, 'people')}]")
    st.write("Places:")
    st.write(f":green[{grab_from_internal_id(id, 'places')}]")
    st.write("Transcript:")
    st.write(grab_from_internal_id(id, "text_only_transcript"))

with col2:
    id = results_df["internal_id"].to_list()[1]
    st.write(f"Internal ID:{id}")
    st.write("Topics:")
    st.write(f":blue[{grab_from_internal_id(id, 'topics')}]")
    st.write("People:")
    st.write(f":red[{grab_from_internal_id(id, 'people')}]")
    st.write("Places:")
    st.write(f":green[{grab_from_internal_id(id, 'places')}]")
    st.write("Transcript:")
    st.write(grab_from_internal_id(id, "text_only_transcript"))

with col3:
    id = results_df["internal_id"].to_list()[2]
    st.write(f"Internal ID:{id}")
    st.write("Topics:")
    st.write(f":blue[{grab_from_internal_id(id, 'topics')}]")
    st.write("People:")
    st.write(f":red[{grab_from_internal_id(id, 'people')}]")
    st.write("Places:")
    st.write(f":green[{grab_from_internal_id(id, 'places')}]")
    st.write("Transcript:")
    st.write(grab_from_internal_id(id, "text_only_transcript"))