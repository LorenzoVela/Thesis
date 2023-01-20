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
    if(st.button("Pandas Profiling", key=1)):
        switch_page("profiling")
with col1_2:
    if st.button("Dataset Info", key=2):
        st.session_state['status'] = 0
        switch_page("dataset_info")
with col1_3:
    if st.button("Values Management", key=3):
        st.session_state['y'] = 0
        switch_page("value_filtering")
with col1_4:
    if st.button("Null values handling", key=4):
        switch_page("null_values_selection")
with col1_5:
    st.button("--", key=5)
        #switch_page("")
with col1_6:
    if(st.button("Automate profiling", key=6)):
        st.session_state['y'] = 0
        st.session_state['widget'] = 500
        switch_page("automatic")
with col1_7:
    if st.button("Show Entire dataset", key=7):
        switch_page("visualize_dataset")
with col1_8:
    if st.button("Download dataset", key=8):
        switch_page("download_dataset")

st.write(" ")

col2_1, col2_2, col2_3, col2_4, col2_5, col2_6, col2_7, col2_8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
with col2_1:
     if st.button("Suggested actions", key=9):
        st.session_state['Once'] = True
        st.session_state['y'] = 0
        switch_page("suggested_actions") 
with col2_2:
     if st.button("Column renaming", key=10):
        st.session_state['y'] = 0
        switch_page("column_renaming")
with col2_3:
     if st.button("Column splitting", key=11):
        st.session_state['avoid'] = 0
        st.session_state['y'] = 0
        switch_page("column_splitting")  
with col2_4:
    if st.button("Column by column", key=12):
        st.session_state['counter'] = 0
        switch_page("col_by_col")
with col2_5:
    if st.button("Columns merging", key=13):
        st.session_state['y'] = 0
        switch_page("column_merging")
with col2_6:
    if st.button("Column dropping", key=14):
            st.session_state['avoid'] = 0
            st.session_state['y'] = 0
            switch_page("column_dropping")
with col2_7:
    if st.button("Duplicate detection", key=15):
        switch_page("duplicate_detection")


    


st.write(" ")
st.write(" ")

col3_1, col3_2 = st.columns(2)
with col3_1:
    with st.expander("Show starting of dataset"):
        st.write(df.head())
with col3_2:
    with st.expander("Show tail of dataset"):
        st.write(df.tail())
    
        