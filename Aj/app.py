import streamlit as st
import pandas as pd
import janitor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# df = pd\
#     .read_csv('../derived_data.csv')\
#     .clean_names()\
#     .filter(['internal_id', 'text_only_transcript', 'people', 'places', 'topics'])\
#     .assign(text_only_transcript = lambda x: x['text_only_transcript']\
#             .replace({'\\|': ' ', 
#                     '\\[\\[': ' ', 
#                     '\\]\\]': ' ', 
#                     '\\r': ' ', 
#                     '\\n': ' ', 
#                     '\\t': ' '}, regex=True))\
#     .reset_index(drop=True)\
#     .fillna({'People': '', 'Topics': '', 'Clean Text': ''})\
#     .dropna()\
#     .assign(topics = lambda x: x['topics'].apply(lambda x: ' '.join(x.split('|'))))\
#     .assign(people = lambda x: x['people'].apply(lambda x: ' '.join(x.split('|'))))\
#     .assign(places = lambda x: x['places'].apply(lambda x: ' '.join(x.split('|'))))

# df.to_csv('ww_data_appclean.csv')
# Beginning Stuff

import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))

# def create_tfidf_matrix(data, stop_words='english'):
#     tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
#     tfidf_matrix = tfidf_vectorizer.fit_transform(data)
#     return tfidf_matrix


# tfidf_matrix_people = create_tfidf_matrix(df['people'])
# tfidf_matrix_topics = create_tfidf_matrix(df['topics'])
# tfidf_matrx_places = create_tfidf_matrix(df['places'])
# tfidf_matrix_text = create_tfidf_matrix(df['text_only_transcript'])

# people_similarity = cosine_similarity(tfidf_matrix_people)
# topics_similarity = cosine_similarity(tfidf_matrix_topics)
# places_similarity = cosine_similarity(tfidf_matrx_places)
# text_similarity = cosine_similarity(tfidf_matrix_text)

# ppl_df = pd.DataFrame(people_similarity).clean_names()
# ppl_df.columns = ppl_df.columns.astype(str)
# ppl_df.to_parquet('people_similarity.parquet')
# ###
# topics_df = pd.DataFrame(topics_similarity).clean_names()
# topics_df.columns = topics_df.columns.astype(str)
# topics_df.to_parquet('topics_similarity.parquet')
# ###
# places_df = pd.DataFrame(places_similarity).clean_names()
# places_df.columns = places_df.columns.astype(str)
# places_df.to_parquet('places_similarity.parquet')
# ###
# text_df = pd.DataFrame(text_similarity).clean_names()
# text_df.columns = text_df.columns.astype(str)
# text_df.to_parquet('text_similarity.parquet')

df = pd.read_csv('ww_data_appclean.csv')

# people_similarity = pd.read_parquet('people_similarity.parquet')
# topics_similarity = pd.read_parquet('topics_similarity.parquet')
# places_similarity = pd.read_parquet('places_similarity.parquet')
text_similarity = pd.read_parquet('text_similarity.parquet')



def get_row_number_by_internal_id(df, internal_id):
    return df.query('internal_id == @internal_id').index[0]

def get_recommendations(df, row_number, similarity_matrix, threshold=0.2, num_recommendations=3):
    sim_scores = list(enumerate(similarity_matrix[str(row_number)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [item for item in sim_scores if item[1] > threshold]
    recommended_ids = [df.iloc[item[0]]['internal_id'] for item in sim_scores if item[0] != row_number]
    return recommended_ids[:num_recommendations]




# Choose internal_id to analyze

st.sidebar.write("Choose internal_id to analyze:")
internal_id = st.sidebar.number_input("internal_id", min_value=df['internal_id'].min(), max_value=df['internal_id'].max(), value=42, step=1)

#Show transcript
st.sidebar.write("Transcript:")
try:
    text_transcript = df.query('internal_id == @internal_id')['text_only_transcript'].values[0]
    st.sidebar.markdown(text_transcript)
except IndexError:
    pass
    

col1, col2, col3 = st.columns(3)

with col1:
    st.write("People:")
    try:
        people_list = df.query('internal_id == @internal_id')['people'].values[0]
        st.write(people_list)
    except IndexError:
        st.error('OOPSY', icon="🥵")


with col2:
    st.write("Places:") 
    try:
        places_list = df.query('internal_id == @internal_id')['places'].values[0]
        st.write(places_list)
    except IndexError:
        st.error('Sorry, we could not find that journal entry', icon="🚨")

with col3:
    st.write("Topics:")
    try:
        topics_list = df.query('internal_id == @internal_id')['topics'].values[0]
        st.write(topics_list)
    except IndexError:
        st.error('WOOPSY', icon="🥵")

row_id = get_row_number_by_internal_id(df, internal_id)

similar_text   = get_recommendations(df, row_id, text_similarity  )
# similar_people = get_recommendations(df, row_id, people_similarity)
# similar_topics = get_recommendations(df, row_id, topics_similarity)
# similar_places = get_recommendations(df, row_id, places_similarity)

st.header("Best Matches Overall")

col1a, col2a, col3a = st.columns(3)

with col1a:
    st.write("First Match:")
    st.write(df[["text_only_transcript"]].loc[int(similar_text[0]),].item())
         
with col2a:
    st.write("Second Match:")
    st.write(df[["text_only_transcript"]].loc[int(similar_text[1]),].item())

with col3a:
    st.write("Third Match:")
    st.write(df[["text_only_transcript"]].loc[int(similar_text[2]),].item())



