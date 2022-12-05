import time
import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.st_keyup import st_keyup
import os
import json
from pandas_profiling import *


def profileAgain(df):
    if os.path.exists("newProfile.json"):
        os.remove("newProfile.json")
    profile = ProfileReport(df)
    profile.to_file("newProfile.json")
    with open("newProfile.json", 'r') as f:
        report = json.load(f)
    st.session_state['profile'] = profile
    st.session_state['report'] = report
    st.session_state['df'] = df
    newColumns = []
    for item in df.columns:
        newColumns.append(item)
    st.session_state['dfCol'] = newColumns




m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 254, 239);
    height:auto;
    width:auto;
}
</style>""", unsafe_allow_html=True)

st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)


profile = st.session_state['profile']
report = st.session_state['report']
df = st.session_state['df']
dfCol = st.session_state['dfCol']

st.title("Filter column values")
with st.expander("Manual", expanded=False):
    st.write("In this page you're allowed to select a column in which apply some splitting/changes to its values")
    column = selectbox("Choose a column", dfCol)
    if column != None:
        unique = df.duplicated(subset=column).value_counts()[0]
        st.write("Unique rows: ", unique)
        st.write("Duplicate rows", len(df.index) - unique)
        #st.write("Unique rows: ", df.duplicated(subset=column).value_counts())
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            st.write('Old column')
            st.write(df[column].head(30))
        with col2:
            if st.session_state['y'] == 0:
                st.write("Edit menu")
                action = selectbox("Action", ["Remove", "Add"])
                if action == "Add":
                    where = selectbox("Where", ["Start of the value", "End of the value"])
                    if where == "Start of the value":
                        inputString = st.text_input("Provide the string")
                        st.session_state['string'] = inputString
                        if st.button("Go!"):
                            st.session_state['y'] = 1
                            st.experimental_rerun()
                    elif where == "End of the value":
                        inputString = st.text_input("Provide the string")
                        st.session_state['string'] = inputString
                        if st.button("Go!"):
                            st.session_state['y'] = 2
                            st.experimental_rerun()
                elif action == "Remove":
                    inputString = st.text_input("Provide the string")
                    st.session_state['string'] = inputString
                    if st.button("Go!"):
                        st.session_state['y'] = 3
                        st.experimental_rerun()
                else:
                    ()
            elif st.session_state['y'] == 1: #add start
                string = st.session_state['string']
                copyPreview = df[column].copy()
                for i in range(len(df.index)):
                    copyPreview[i] = string + str(copyPreview[i])
                st.session_state['copyPreview'] = copyPreview
                st.session_state['y'] = 4
                st.experimental_rerun()
            elif st.session_state['y'] == 2: #add end
                string = st.session_state['string']
                copyPreview = df[column].copy()
                for i in range(len(df.index)):
                    copyPreview[i] = str(copyPreview[i]) + string 
                st.session_state['copyPreview'] = copyPreview
                st.session_state['y'] = 4
                st.experimental_rerun()
            elif st.session_state['y'] == 3: #remove
                string = st.session_state['string']
                copyPreview = df[column].copy()
                for i in range(len(df.index)):
                    if string in str(copyPreview[i]):
                        copyPreview[i] = str(copyPreview[i]).replace(string,'')
                st.session_state['copyPreview'] = copyPreview
                st.session_state['y'] = 4
                st.experimental_rerun()
            elif st.session_state['y'] == 4:
                st.write("New column")
                copyPreview = st.session_state['copyPreview']
                st.write(copyPreview.head(30))
                if st.button("Save"):
                    st.session_state['toBeProfiled'] = True
                    st.session_state['y'] = 5
                    st.experimental_rerun()
            
    else: #column is none
        ()
    if st.session_state['y'] == 5:
        copyPreview = st.session_state['copyPreview']
        df[copyPreview.name] = copyPreview.values
        successMessage = st.empty()
        successString = "Column successfully updated! Please wait while the dataframe is profiled again.."
        successMessage.success(successString)
        if st.session_state['toBeProfiled'] == True:
            profileAgain(df)
        st.session_state['toBeProfiled'] = False
        st.session_state['y'] = 1
        successMessage.success("Profiling updated!")
        newUnique = copyPreview.duplicated().value_counts()[0]
        st.write("Unique rows of the new column: ", newUnique)
        st.write("Duplicate rows of the new column: ", len(df.index) - newUnique)
        #st.write("Non unique rows: ", copyPreview.duplicated().sum())
        if st.button("Continue with the filtering"):
            st.session_state['y'] = 0
            st.experimental_rerun()
            #st.write("Non unique rows: ", df.duplicated(subset=copyPreview.name).value_counts()[1])
            #st.write("Unique rows: ", df.duplicated(subset=copyPreview.name).value_counts()[0])

with st.expander("Automatic", expanded=False):
    st.write("In this page you're allowed to select a column in which apply some splitting/changes to its values")
    column = selectbox("Choose a columnn", dfCol)
    delimiters = [",", ";", " ' ", "{", "}", "[", "]", "(", ")", " \ ", "/", "-", "_", ".", "|"]
    if column != None:
        counter = 0
        importantDelimiters = []
        copyPreview = df[column].copy()
        unique = df.duplicated(subset=column).value_counts()[0]
        st.write("Unique rows: ", unique)
        st.write("Duplicate rows", len(df.index) - unique)
        #st.write("Unique rows: ", df.duplicated(subset=column).value_counts())
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            st.write('Old column')
            st.write(df[column].head(30))
        with col2:
            if st.session_state['y'] == 0:
                st.write("Edit menu")
                for item in delimiters:
                    counter = 0
                    for i in range(int(len(df.index)/10)):  #search for a delimiter in the first 10% of the dataset
                        x = str(copyPreview[i]).find(item)
                        if x > 0:
                            counter += 1
                    if counter >= (len(df.index)/50):  #if in the first 10%, is present at least the 20% then we should propose it!
                        importantDelimiters.append(item)
                st.write(importantDelimiters)
                
                





if st.button("Back to Homepage"):
    switch_page("Homepage")

