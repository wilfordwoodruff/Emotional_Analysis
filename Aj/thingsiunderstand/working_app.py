
import pandas as pd
import polars as pl
import numpy as np
import janitor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import streamlit as st

os.chdir(os.path.dirname(os.path.abspath(__file__)))

lmao = st.text_input("Enter Password:", value="", type="password")

def every_thing():

    # Define the data
    @st.cache_data
    def load_in_data():
        wwtext = pl.read_csv("wwtext_df.csv")
        people = pl.read_csv("people_df.csv")
        places = pl.read_csv("places_df.csv")
        topics = pl.read_csv("topics_df.csv")

        return wwtext, people, places, topics

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

    with st.status("Loading and calculating..."):
        st.write("Defining data...")
        df_display = make_df_display()
        wwtext, people, places, topics = load_in_data()
        st.write("Finished!")

    def grab_from_internal_id(internal_id, column_name):
        return df_display\
            .filter(pl.col("internal_id") == internal_id)\
            [column_name]\
            .to_list()[0]

    def return_text(df, place, var="text_only_transcript"):
        return df_display\
                .filter(pl.col("internal_id") == list(df.filter(pl.col("internal_id") == input_number)\
                .transpose())[0][place])\
                [var]\
                .to_list()[0]


    # Sidebar:

    st.sidebar.title("Woodruff Similarity Algorithm")

    input_number = st.sidebar.number_input("Choose internal_id to analyze:",
                                            min_value=df_display['internal_id'].min(),
                                            max_value=df_display['internal_id'].max(),
                                            value=42,
                                            step=1)


    side_col1, side_col2, side_col3 = st.sidebar.columns(3)

    with side_col1:
        st.sidebar.write("Topics:")
        st.sidebar.write(f":blue[{grab_from_internal_id(input_number, 'topics')}]")

    with side_col2:
        st.sidebar.write("People:")
        st.sidebar.write(f":red[{grab_from_internal_id(input_number, 'people')}]")

    with side_col3:
        st.sidebar.write("Places:")
        st.sidebar.write(f":green[{grab_from_internal_id(input_number, 'places')}]")

    st.sidebar.write("Transcript:")
    st.sidebar.write(grab_from_internal_id(input_number, "text_only_transcript"))



















        

    # ######################
    # # Main Page
    # ######################

    st.title("Woodruff Similarity Algorithm")





    tab1, tab2, tab3, tab4 = st.tabs(["Overall", "People", "Topics", "Places"])



    with tab1:

        ###
        st.header("1st Best Match Overall")

        st.write(f"Internal ID:{return_text(wwtext, 1, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(wwtext, 1, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(wwtext, 1, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(wwtext, 1, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(wwtext, 1, "text_only_transcript"))

        ###
        st.header("2nd Best Match Overall")

        st.write(f"Internal ID:{return_text(wwtext, 2, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(wwtext, 2, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(wwtext, 2, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(wwtext, 2, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(wwtext, 1, "text_only_transcript"))

        ###
        st.header("3rd Best Match Overall")

        st.write(f"Internal ID:{return_text(wwtext, 3, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(wwtext, 3, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(wwtext, 3, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(wwtext, 3, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(wwtext, 3, "text_only_transcript"))


    with tab2:

        ###
        st.header("1st Best Match Overall")

        st.write(f"Internal ID:{return_text(people, 1, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(people, 1, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(people, 1, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(people, 1, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(people, 1, "text_only_transcript"))

        ###
        st.header("2nd Best Match Overall")

        st.write(f"Internal ID:{return_text(people, 2, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(people, 2, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(people, 2, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(people, 2, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(people, 1, "text_only_transcript"))

        ###
        st.header("3rd Best Match Overall")

        st.write(f"Internal ID:{return_text(people, 3, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(people, 3, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(people, 3, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(people, 3, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(people, 3, "text_only_transcript"))

    with tab3:

        ###
        st.header("1st Best Match Overall")

        st.write(f"Internal ID:{return_text(topics, 1, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(topics, 1, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(topics, 1, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(topics, 1, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(topics, 1, "text_only_transcript"))

        ###
        st.header("2nd Best Match Overall")

        st.write(f"Internal ID:{return_text(topics, 2, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(topics, 2, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(topics, 2, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(topics, 2, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(topics, 1, "text_only_transcript"))

        ###
        st.header("3rd Best Match Overall")

        st.write(f"Internal ID:{return_text(topics, 3, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(topics, 3, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(topics, 3, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(topics, 3, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(topics, 3, "text_only_transcript"))

    with tab4:

        ###
        st.header("1st Best Match Overall")

        st.write(f"Internal ID:{return_text(places, 1, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(places, 1, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(places, 1, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(places, 1, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(places, 1, "text_only_transcript"))

        ###
        st.header("2nd Best Match Overall")

        st.write(f"Internal ID:{return_text(places, 2, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(places, 2, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(places, 2, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(places, 2, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(places, 1, "text_only_transcript"))

        ###
        st.header("3rd Best Match Overall")

        st.write(f"Internal ID:{return_text(places, 3, 'internal_id')}")

        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)

        with col1_tab1:
            st.write("Topics:")
            st.write(f":blue[{return_text(places, 3, 'topics')}]")

        with col2_tab1:
            st.write("People:")
            st.write(f":red[{return_text(places, 3, 'people')}]")

        with col3_tab1:
            st.write("Places:")
            st.write(f":green[{return_text(places, 3, 'places')}]")

        st.write("Transcript:")
        st.markdown(return_text(places, 3, "text_only_transcript"))

if lmao == "password":
    every_thing()