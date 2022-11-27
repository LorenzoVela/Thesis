import time

import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.st_keyup import st_keyup


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
with st.expander("", expanded=True):
    st.write("In this page you're allowed to select a column in which apply some splitting/changes to its values")
    column = selectbox("Choose a column", dfCol)
    col1, col2, col3 = st.columns(3, gap="small")
    if column != None:
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
                    st.session_state['y'] = 5
                    st.experimental_rerun()
            
    else: #column is none
        ()
    if st.session_state['y'] == 5:
        
        #TODO
        #update the dataframe
        #do the profile again
        #remove the old report
        #load the new one
        
        #copyPreview = st.session_state['copyPreview']
        #df[column] = copyPreview.values
        #st.session_state['df'] = df
        st.success("Column updated successfully!")
    if st.button("Back to column selection"):
        st.session_state['y'] = 0
        st.experimental_rerun()

if st.button("Back to Homepage"):
    switch_page("Homepage")

