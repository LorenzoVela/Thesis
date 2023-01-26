import time

import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox


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

st.title("Null values handling")
with st.expander("", expanded=True):
    st.write("In this page you're allowed to select a column in order to replace its null values. You can also decide to drop the entire column too.")
    column = selectbox("Choose a column", dfCol)
    #column = st.multiselect("Replace all the values with", dfCol)
    if column != None:
        nullNum = df[column].isna().sum()
        percentageNull = nullNum/len(df.index)*100
        st.write("This column has ", nullNum, " null values (" + "%0.2f" %(percentageNull) + "%)")
        st.write("If you want to proceed click next, otherwise you can either select another column or come back to the Homepage")
        if st.button("Next"):
            st.session_state['from'] = 1
            st.session_state['y'] = 0
            st.session_state['arg'] = df[column].copy(deep=False)
            switch_page("null_values")
with st.expander("", expanded=True):
    if column == None:
        st.info("If you want to replace all the null values of the dataset in 2 click, select here with which value")
        col = st.columns([1,1,1.5])
        with col[0]:
            fillingOpStr = st.radio("Filling options for columns of type object:",("", "Following Value", "Previous Value","Mode", "Custom Value"), index=0,key=107)
        with col[1]:
            fillingOpNum = st.radio(f"Filling options for numeric columns :",("", "Min", "Max", "Avg", "0", "Mode"),index=0)
        if fillingOpNum != "" and fillingOpStr != "":
            dfPreview = df.copy()
            for col in df.columns:
                if dfPreview[col].dtype != "Variable.S_TYPE_UNSUPPORTED":
                    if dfPreview[col].dtype == "object":
                        ()#missing the switch between the 4 different types of filling for str
                    elif dfPreview[col].dtype == "float64" or dfPreview[col].dtype == "Int64":
                        ()#missing the switch between the 5 different types of filling for num



if st.button("Back to Homepage"):
    switch_page("Homepage")

