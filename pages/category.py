import time

import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page

def update_multiselect_style():
    st.markdown(
        """
        <style>
            .stMultiSelect [data-baseweb="tag"] {
                height: fit-content;
            }
            .stMultiSelect [data-baseweb="tag"] span[title] {
                white-space: normal; max-width: 100%; overflow-wrap: anywhere;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


update_selectbox_style()
update_multiselect_style()

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 254, 239);
    height:4em;
    width:4em;
}
</style>""", unsafe_allow_html=True)


dfCol = st.session_state['arg'] #dfCol is a series here
profile = st.session_state['profile']
report = st.session_state['report']
df = st.session_state['df']
string = "Managing categories of column " + dfCol.name
st.title(string)
col1, col2, col3 = st.columns(3, gap='small')
distinctList = pd.unique(dfCol)
distinctNum = len(distinctList)
percentageDistinct = distinctNum/len(dfCol.index)*100
with col1:
    st.write(dfCol.head())
with col2:
    if distinctNum != 1:
        st.write("This column has ", distinctNum, " different distinct values (" + "%0.2f" %(percentageDistinct) + "%)")
    else:
        st.write("This column has only one unique value that is: ")
list = report["variables"][dfCol.name]["value_counts"]
with st.expander("Value counter"):
    st.write(list)

with st.expander("Values replacer"):
    if st.session_state['y'] == 0:
        old_values = st.multiselect("Replace all the values with",distinctList)
        new_value = st.selectbox("With the value", distinctList)
        st.session_state['old_values'] = old_values
        st.session_state['new_value'] = new_value
        if new_value in old_values:
            errorString = "You're choosing to replace " + new_value + " with " + new_value + ", try again"
            st.error(errorString)
            st.session_state['bool'] = True
        else:
            if st.button("Preview"):
                st.session_state['y'] = 1
                st.experimental_rerun()
    elif st.session_state['y'] == 1:
        changedValues = newDistinctNum = newPercentageDistinct = 0
        old_values = st.session_state['old_values']
        new_value = st.session_state['new_value']
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.write("Old column")
            st.write(dfCol.head(20))
            
        with col1_2:
            dfColCopy = dfCol.copy(deep=True)
            for i in range(len(dfCol.index)):
                if str(dfCol[i]) in old_values:
                    dfColCopy[i] = new_value
                    changedValues += 1
            st.session_state['dfColCopy'] = dfColCopy
            st.write("New column")
            st.write(dfColCopy.head(20))
            newDistinctList = pd.unique(dfColCopy)
            newDistinctNum = len(newDistinctList)
            newPercentageDistinct = newDistinctNum/len(dfCol.index)*100
        strChanged = str(changedValues)
        successString = strChanged + " values has been replaced successfully with " + new_value
            
            #TODO valutare st.metric!!

        message1 = st.empty()
        message1.success(successString)
        st.write("New number of distinct values is ", newDistinctNum)
        st.write("New percentage of distict values is " + "%0.2f" %(newPercentageDistinct) + "%")
        if st.radio("Do you want to apply these changes?", ["No", "Yes"], horizontal=True) == "Yes":
            st.session_state['y'] = 2
            st.experimental_rerun()
        else:
            ()

    elif st.session_state['y'] == 2:
        dfColCopy = st.session_state['dfColCopy']
        df[dfCol.name] = dfColCopy.values
        message2 = st.empty()
        message2.success("Replacement completed, dataset preview")
        st.write(df.head(20))
        st.session_state['df'] = df
        if st.button("Replace another value"):
            st.session_state['y'] == 0
            st.experimental_rerun()
    else:
        ()
if st.button("Back to Dataset Info!"):
        switch_page("dataset_info")

