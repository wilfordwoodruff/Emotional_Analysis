import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

correct_password = "passwordWWP2023"
password = st.sidebar.text_input("Enter Password:", "", type="password")

def authenticate(password_attempt):
    return password_attempt == correct_password

# Keep all important secrets within password IF statement
if authenticate(password):
    # Upload the data
    df = pd.read_csv("Log-adjusted Hume scores.csv")
    emotion_mapping = pd.read_csv("emotion_categories_updated.csv")
    emotion_mapping = emotion_mapping.set_index('HUME')['10CATEGORIES'].to_dict()    


    # df = df.melt(id_vars='ROW')

    # df["emotion"] = df["variable"].map(emotion_mapping)

    # df = df.groupby('emotion')\
    #     .agg(score=pd.NamedAgg(column = 'value', aggfunc = np.mean))\
    #     .reset_index(drop=True)\
    #     .assign(score = lambda x: round(x.score, 2))

    selected_user = st.sidebar.selectbox("Select User ID:", df['ROW'])
    user_data = df[df['ROW'] == selected_user].drop(columns='ROW')

    st.title("Exploring emotions in the Wilford Woodruff Papers (WWP)")

    #Plotly Radar Chart (all emotions)
    fig = px.line_polar(user_data, r=user_data.values.flatten(), theta=user_data.columns, line_close=True, template='ggplot2')
    st.plotly_chart(fig, use_container_width=True)

    #Plotly Radar Chart (emo categories)
    #fig2 = px.line_polar(user_data, r=user_data.values.flatten(), theta=user_data.columns, line_close=True, template='plotly_dark')
    #st.plotly_chart(fig2, use_container_width=True)

    # Need new dataset with emotions hooked up to article
    # text = df[df['ROW'] == 1].drop(columns='ROW')
    




else:
    st.sidebar.error("Incorrect Password. Please try again.")

