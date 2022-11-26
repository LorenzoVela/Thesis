from tkinter.font import BOLD
from turtle import color
import streamlit as st
import time
import pandas as pd
import numpy as np
import pandas_profiling
from pandas_profiling import *
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.switch_page_button import switch_page
from annotated_text import annotated_text
import json

df = st.session_state['df']

profile = ProfileReport(df)
profile.to_file("newProfile.json")
with open("newProfile.json", 'r') as f:
    report = json.load(f)

rep = profile.to_file("Test.json")

defNullThreshold = 15

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 254, 239);
    height:4em;
    width:4em;
}
</style>""", unsafe_allow_html=True)


dfCol = st.session_state['dfCol']
nullCount = []
for col in dfCol: 
    nullPercentage = int(df[col].isna().sum())/len(df.index)*100
    strCol = "Percentage of null values in column " + col + "is " + "%0.2f" %(nullPercentage) + "%"
    if nullPercentage > defNullThreshold:
        st.write(strCol)
        annotated_text(strCol, ("Action required","","#faa"))
    else:
        st.write(strCol)
count = 0
with st.expander("Warnings from pandas profiling"):
    warningMessages = report["messages"]
    for mex in warningMessages:
        st.write(mex)
if st.button("Done!", count):
        switch_page("Homepage")

