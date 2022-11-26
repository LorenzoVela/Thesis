from cgitb import small
import os
import webbrowser
import streamlit as st
import time
import pandas as pd
import numpy as np
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="prova2 title", layout="wide", initial_sidebar_state="collapsed")

#def app():

df = st.session_state['df']
#st.write(df.head())

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 254, 239);
    height:6em;
    width:6em;
}
</style>""", unsafe_allow_html=True)



st.title("Homepage")
#st.markdown("- 💱 **Renaming**: you can rename one or more columns")
#st.info("You can operate one or more wrangling operations together. Remember to let the tool know (from the sidebar) that you finished your operations in order to generate the download .csv button.")
#st.error("⚠️REMEMBER: when you are one the wrangling page do NOT call back the data profiling page. You will lost every operation done!")
st.write(" ")
st.write(" ")
st.write(" ")

col1_1, col1_2, col1_3, col1_4, col1_5, col1_6, col1_7, col1_8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
with col1_1:
    if(st.button("Profiling")):
        switch_page("profiling")
with col1_2:
    if(st.button("Reccomended actions")):
        switch_page("reccomended_actions")
with col1_3:
    if st.button("Dataset Info"):
        switch_page("dataset_info")
        #st.write(df.head())
with col1_4:
    if st.button("Columns splitting"):
        switch_page("column_splitting")
with col1_5:
    st.button("🎂")
with col1_6:
    st.button("🎶")
with col1_7:
    st.button("🎉")
with col1_8:
    st.button("🐱‍🐉")

    


st.write(" ")
st.write(" ")

col3_1, col3_2 = st.columns(2)
with col3_1:
    with st.expander("Show starting of dataset"):
        st.write(df.head())
with col3_2:
    with st.expander("Show tail of dataset"):
        st.write(df.tail())
    
        