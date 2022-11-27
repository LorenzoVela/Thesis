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
    height:4em;
    width:4em;
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
    else:
        ()

if st.button("Back to Homepage"):
    switch_page("Homepage")

