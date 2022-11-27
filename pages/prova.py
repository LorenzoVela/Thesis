from itertools import count
from tkinter import PAGES
import webbrowser
import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
from pandas_profiling import *
import json
from time import sleep

from streamlit_extras.switch_page_button import switch_page
#def app():


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_900,h_470/https://www.analyticsinsight.net/wp-content/uploads/2019/12/Data-Analytics-will-Drive-the-Growth-of-IoT-1024x535.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#add_bg_from_url() 

st.title("[prova]Questa è un'app di prova test1")
st.markdown("Test Markdown")

def uploading_csv():
    st.header("📁Upload your dataset:")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.session_state['df'] = df
        return df
    else:
        ()

x = st.session_state['x']

df = uploading_csv()

def profile_csv(df):
    profile = ProfileReport(df)
    profile.to_file("newProfile.json")
    with open("newProfile.json", 'r') as f:
        report = json.load(f)
    st.session_state['profile'] = profile
    st.session_state['report'] = report


message = st.empty()
dfCol = []
if df is not None:
    if x == 0:
        message.success("File uploaded correctly! Please wait, profiling in progress..")
        profile_csv(df)
        message.success("Profiling completed!")
        print("Test")
        st.session_state['x'] = 1
        for col in df.columns:
            dfCol.append(col)
        st.session_state['dfCol'] = dfCol
    else:
        message.success("Redirecting...")
    #profile = ProfileReport(df)
    #profile.to_file("newProfile.json")
    #with open("newProfile.json", 'r') as f:
    #    report = json.load(f)
    #message.empty()
    #st.session_state['profile'] = profile
    #st.session_state['report'] = report
    #st.write(df.head())
        #firstRows = st.checkbox("Select to show a preview of your dataset:", value=False, key=10)
        #if firstRows == True:
        #    st.write(df.head())  
    button = st.button("Continue")
    if button:
        switch_page("Homepage")

