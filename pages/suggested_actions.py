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
    height: 3.5em;
    width:auto;
}
</style>""", unsafe_allow_html=True)

df = st.session_state['df']
dfCol = st.session_state['dfCol']
profile = st.session_state['profile']
report = st.session_state['report']
correlations = profile.description_set["correlations"]
phik_df = correlations["phi_k"]

st.title("Suggested actions")
slate1 = st.empty() 
body1 = slate1.container()

slate2 = st.empty()
body2 = slate2.container()

def clean1 ():
    slate1.empty()
    st.session_state['y'] = 1
    #st.session_state['2'] = True
    #st.session_state['toBeProfiled'] = True
    #st.experimental_rerun()

def clean2 ():
    slate2.empty()
    st.session_state['y'] = 2
    st.session_state['toBeProfiled'] = True
    #st.experimental_rerun()

def element_not_in_tuples(element, tuple_list):
    for tup in tuple_list:
        if element not in tup:
            return True
    return False

droppedList = []

ind = 1
correlationList = []
for col in phik_df.columns:
    if ind < (len(phik_df.columns) - 1):
        for y in range(ind, len(phik_df.columns)):
            x = float(phik_df[col][y])*100
            if x > 85:
                correlationList.append([col, str(phik_df.columns[y]), x])
        ind += 1

correlationSum = {}
for y in range(0, len(phik_df.columns)):
    x = 0
    z = 0
    for column in phik_df.columns:
        z = float(phik_df[column][y])
        x += z 
    correlationSum.update({str(phik_df.columns[y]) : x})


with body1:
    if st.session_state['y'] == 0:
        with st.expander("Dataset preview", expanded=False):
            st.write(df.head(100))
        with st.expander("Incomplete Rows", expanded=True):
            colNum = len(df.columns)
            threshold = round(0.4 * colNum) #if a value has 40% of the attribute = NaN it's available for dropping
            nullList = df.isnull().sum(axis=1).tolist()
            nullToDelete = []
            dfToDelete = df.copy()
            rangeList = list(range(len(nullList)))
            for i in range(len(nullList)):
                if nullList[i] >= threshold:
                    nullToDelete.append(i)
            if len(nullToDelete) > 0:
                notNullList = [i for i in rangeList if i not in nullToDelete]
                dfToDelete.drop(notNullList, axis=0, inplace=True)
                percentageNullRows = len(nullToDelete) / len(df.index) * 100
                infoStr = "This dataset has " + str(len(nullToDelete)) + " rows (" + str("%0.2f" %(percentageNullRows)) + "%) that have at least " + str(threshold) + " null values out of " + str(len(df.columns))
                st.info(infoStr)
                with st.expander("Expand to see all the incomplete rows"):
                    st.dataframe(dfToDelete)
                if st.checkbox("Drop these rows from the dataset", key=-1):
                    droppedList.append(["rows", nullToDelete])
            else:
                numm = colNum - threshold 
                successString = "The dataset has all the rows with at least " + str(numm) + " not null values out of " + str(len(df.columns))
                st.success(successString)
        with st.expander("Correlated columns", expanded=True):
            if len(correlationList) > 0:
                for i in range(0, len(correlationList)):
                    if correlationList[i][0] in df.columns and correlationList[i][1] in df.columns: 
                        strDropCorr =f"Columns **{correlationList[i][0]}** and  **{correlationList[i][1]}** are highly correlated. You're suggested to drop one of the two"
                        st.info(strDropCorr)
                        choice = st.radio("Select below", ["None", correlationList[i][0], correlationList[i][1]], index=0)
                        if choice != "None":    
                            droppedList.append(["column", choice])
            else:
                st.success("All the columns are acceptably independent!")
            st.markdown("---")
        st.session_state['droppedList'] = droppedList #update the array before doing the action    
        if len(droppedList) > 0:
            st.warning("After you apply the changes selected, a preview of the new dataset will be displayed")
            if st.button("Go!", on_click=clean1):
                ()
        st.markdown("---")
        if st.button("Homepage"):
            switch_page("Homepage")
with body2:
    if st.session_state['y'] == 1:
        
        #here we should perform all the actions in "droppedList" and profile again the dataset
        
        dfPreview = df.copy()
        successMessage = st.empty()
        successString = "Please wait while the dataframe is profiled again with all the applied changes.."
        for item in st.session_state['droppedList']:
            if item[0] == "rows":
                dfPreview = dfPreview.drop(item[1], axis=0, inplace=True)
            elif item[0] == "column":
                if item[1] in dfPreview.columns:
                    dfPreview = dfPreview.drop(item[1], axis=1)
        st.write(dfPreview.head(50))
        st.warning("This action will be permanent")
        col1, col2, col3 = st.columns([1,1,10], gap='small')
        st.session_state['newdf'] = dfPreview.copy()
        with col1:
            if st.button("Save!", on_click=clean2):
                ()
                #st.session_state['y'] = 2
                #st.session_state['toBeProfiled'] = True
                #st.experimental_rerun()
        with col2:
            if st.button("Back"):
                st.session_state['y'] = 0
                #st.session_state['toBeProfiled'] = True     
                st.experimental_rerun()
        st.markdown("---")
        if st.button("Homepage"):
            switch_page("Homepage")
if st.session_state['y'] == 2:
    if st.session_state['toBeProfiled'] == True:
        df = st.session_state['newdf']
        successMessage = st.empty()
        successString = "Please wait while the dataframe is profiled again with all the applied changes.."
        successMessage.success(successString)
        with st.spinner(" "):
            profileAgain(df)
        successMessage.success("Profiling updated!")
        st.session_state['toBeProfiled'] = False
        st.subheader("New dataset")
        st.write(df.head(50))
    st.markdown("---")
    if st.button("Homepage"):
        switch_page("Homepage")
