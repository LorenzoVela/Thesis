import time
import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox
import os
from pandas_profiling import *
import json
import numpy as np




def update_selectbox_style():
    st.markdown(
        """
        <style>
            .stSelectbox [data-baseweb="select"] div[aria-selected="true"] {
                white-space: normal; overflow-wrap: anywhere;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

update_selectbox_style()


m = st.markdown("""
<style>
div.stButton > button:first-child {
    line-height: 1.2;
    background-color: rgb(255, 254, 239);
    height:4em;
    width:auto;
}
</style>""", unsafe_allow_html=True)

def color_survived(val):
    color = 'palegreen'
    return f'background-color: {color}'

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


profile = st.session_state['profile']
report = st.session_state['report']
df = st.session_state['df']
st.title("Column renaming")

if st.session_state['y'] == 0:  #choose the values to replace
    dfPreview = df.copy()
    columns = list(df.columns)
    oldName = st.selectbox("Select the column to be renamed", columns)
    newName = st.text_input("Insert the new name and press enter")

    if (len(newName) > 0) and (newName not in columns):
        col11, col22, col33 = st.columns([1,1,7], gap='small')
        dfPreview = dfPreview.rename(columns={oldName:newName})
        st.session_state['dfPreview'] = dfPreview
        with col11:
            if st.button("Show preview"):
                st.session_state['y'] = 1
                st.experimental_rerun()
        with col22:
            if st.button("Save"):
                st.session_state['toBeProfiled'] = True
                st.session_state['y'] = 2
                st.experimental_rerun()
elif st.session_state['y'] == 1:  #show the preview
    dfPreview = st.session_state['dfPreview']
    st.subheader("Preview of the new dataset")
    st.write(dfPreview.head(50))
    col1, col2, col3 = st.columns([1,1,10], gap='small')
    with col1:
        if st.button("Save"):
            st.session_state['toBeProfiled'] = True
            st.session_state['y'] = 2
            st.experimental_rerun()
    with col2:
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

elif st.session_state['y'] == 2:  
    df = st.session_state['dfPreview']
    successMessage = st.empty()
    if st.session_state['toBeProfiled'] == True:
        with st.spinner("The column has been renamed! Please wait while the dataframe is profiled again.."):
            profileAgain(df)
    st.session_state['toBeProfiled'] = False
    successMessage.success("Profiling updated!")
    if st.button("Rename another column"):
        st.session_state['y'] = 0
        st.experimental_rerun() 
else:
    ()
st.markdown("---")
if st.button("Homepage"):
        switch_page("Homepage")

