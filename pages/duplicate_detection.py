import json
import time
import functional_dependencies
import jellyfish
import numpy as np
import pandas as pd
import pandas_profiling
import streamlit as st
from pandas_profiling import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.echo_expander import echo_expander
from streamlit_extras.toggle_switch import st_toggle_switch
from streamlit_extras.stoggle import stoggle
from random import *
import os
import streamlit_nested_layout
import webbrowser
import streamlit.components.v1 as components
import recordlinkage
from recordlinkage.index import Block
from sklearn.metrics.pairwise import cosine_similarity
import jaro


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
    height:7em;
    width:7em;
}
</style>""", unsafe_allow_html=True)


df = st.session_state['df']
dfCol = st.session_state['dfCol']
profile = st.session_state['profile']
report = st.session_state['report']
correlations = profile.description_set["correlations"]
phik_df = correlations["phi_k"]

st.title("Duplicates detection")
slate1 = st.empty()
body1 = slate1.container()
with body1:
    with st.expander("Expand to understand more over the technique that is being used to detect duplicates", expanded=False):
        st.write("The technique that is being used to limit the number of comparisons is the blocking technique. The dataset will be partioned in blocks, in this case a block will be composed by tuples that have the same values for the attribute/s selected below.")
    listCol = df.columns
    listCol = listCol.insert(0, "None")
    colToDrop = st.multiselect("Select one or more columns that will be used to match possible duplicates", listCol, "None")
    if "None" not in colToDrop:
        Blocker = Block(on=colToDrop)
        candidate_links = Blocker.index(df)
        numOfCouples = len(candidate_links)
        st.write(f"There are **{numOfCouples}** couples of rows that have the same values for this set of column/s")
        st.dataframe(candidate_links)
        setCompare = set(df.columns.drop(colToDrop))
        i = 0
        for item in candidate_links:
            i += 1
            #st.write(df.iloc[[item[0], item[1]]])
            row1 = df.iloc[item[0]][setCompare]
            row2 = df.iloc[item[1]][setCompare]
            jaroNum = 0
            numCol = 0
            for col in setCompare:
                #if df.iloc[item[0]][col].isna() == False and df.iloc[item[1]][col].isna() == False:
                    numCol += 1
                    jaroNum += jaro.jaro_winkler_metric(str(df.iloc[item[0]][col]), str(df.iloc[item[1]][col]))
                    #st.write(jaroNum, col)
            sim = jaroNum/numCol
            st.write(i, jaroNum/numCol)
            if sim > 0.95:
                st.write(df.iloc[[item[0], item[1]]])


st.markdown("---")
if st.button("Homepage"):
    switch_page("Homepage")