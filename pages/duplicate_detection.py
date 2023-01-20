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
#st.subheader("In this page you'll visualize all the information of every column")

indexer = recordlinkage.Index()
#df['DescrizioneVia'] = df['DescrizioneVia'].apply(str.upper)
Blocker = Block(on=['DescrizioneVia', 'Civico'])
candidate_links = Blocker.index(df)
st.write(df.info())
st.write(len(candidate_links))
st.dataframe(candidate_links)
setCompare = set(df.columns.drop(['DescrizioneVia', 'Civico']))
i = 0
for item in candidate_links:
    st.write(df.iloc[[item[0], item[1]]])
    row1 = df.iloc[item[0]][setCompare]
    row2 = df.iloc[item[1]][setCompare]
    jaroNum = 0
    numCol = 0
    for col in setCompare:
        #if df.iloc[item[0]][col].isna() == False and df.iloc[item[1]][col].isna() == False:
            numCol += 1
            i += 1
            jaroNum += jaro.jaro_winkler_metric(str(df.iloc[item[0]][col]), str(df.iloc[item[1]][col]))
            st.write(jaroNum, col)
    st.write(jaroNum/numCol)
    if i == 50:
        break


st.markdown("---")
if st.button("Homepage"):
    switch_page("Homepage")