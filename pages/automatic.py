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
#st.markdown("<p><a id=scroll-to-bottom>Scroll to bottom</a></p>", unsafe_allow_html=True)
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
    percentageNullRows = len(nullToDelete) / len(df.index) * 100

st.title("Automatic")
st.subheader("Original dataset preview")
st.dataframe(df.head(50))
st.markdown("---")
if st.session_state['y'] == 0:
    st.write("Click the button to perform automatically all the actions that the system finds suitable for your dataset, later you'll have the possibility to check the preview of the new dataset and to rollback action by action.")
    if st.button("Go!"):
        st.session_state['y'] = 1
        st.session_state['once'] = True
        st.experimental_rerun()
elif st.session_state['y'] == 1:
    box = st.empty()
    dfAutomatic = df.copy()
    if len(nullToDelete) > 0:
        stringDropAutomaticLoad = "Dropping the " + str(len(nullToDelete)) + " rows (" + str("%0.2f" %(percentageNullRows)) + "%) that have at least " + str(threshold) + " null values out of " + str(len(df.columns))
        stringDropRollback = "Rollback the drop of " + str(len(nullToDelete)) + " incomplete rows"
        stringDropAutomaticConfirmed = f"Successfully dropped **{str(len(nullToDelete))}** **rows** (" + str("%0.2f" %(percentageNullRows)) + "%) that had at least " + str(threshold) + " null values out of " + str(len(df.columns))
        dfAutomatic.drop(nullToDelete, axis=0, inplace=True)
        if st.session_state['once'] == True:
            with st.spinner(text=stringDropAutomaticLoad):
                time.sleep(5)
        st.success(stringDropAutomaticConfirmed)
        with st.expander("Why I did it?"):
            st.write("Incomplete rows are one of the principal sources of poor information. Even by applying the imputing technique within these rows would just be almost the same as incresing the dataset's size with non-real samples.")
            if st.checkbox(stringDropRollback, value=False) == True:
                ()
        st.markdown("---")
    for i in range(0, len(correlationList)):
        if correlationList[i][0] in dfAutomatic.columns and correlationList[i][1] in dfAutomatic.columns: 
            if correlationSum[correlationList[i][0]] > correlationSum[correlationList[i][1]]:
                strDropAutomaticLoad0 = "Dropping column " + correlationList[i][0] + "because of it's high correlation with column " + correlationList[i][1]
                strDropAutomaticConfirmed0 = f"Successfully dropped column **{correlationList[i][0]}** because of its high correlation with column {correlationList[i][1]}"
                strDropRollback0 = f"Rollback the drop of column **{correlationList[i][0]}**"
                dfAutomatic = dfAutomatic.drop(correlationList[i][0], axis=1)
                if st.session_state['once'] == True:
                    with st.spinner(text=strDropAutomaticLoad0):
                        time.sleep(2.5)
                st.success(strDropAutomaticConfirmed0)
                with st.expander("Why I did it?"):
                    st.write("a")
                    if st.checkbox(strDropRollback0, key=correlationSum[correlationList[i][0]]) == True:
                        st.write("Ciao0")
            else:
                strDropAutomaticLoad1 = "Dropping column " + correlationList[i][1] + " because of its high correlation with column " + correlationList[i][0]
                strDropAutomaticConfirmed1 = f"Successfully dropped column **{correlationList[i][1]}** because of its high correlation with column {correlationList[i][0]}"
                strDropRollback1 = f"Check to restore the column **{correlationList[i][1]}**"
                dfAutomatic = dfAutomatic.drop(correlationList[i][1], axis=1)
                if st.session_state['once'] == True:
                    with st.spinner(text=strDropAutomaticLoad1):
                        time.sleep(2.5)
                st.success(strDropAutomaticConfirmed1)
                with st.expander("Why I did it?"):
                    st.write("a")
                    if st.checkbox(strDropRollback1, key=correlationSum[correlationList[i][1]]) == True:
                        st.write("Ciao1")
            #st.markdown("<p id=page-bottom>You have reached the bottom of this page!!</p>", unsafe_allow_html=True)
            st.markdown("---")
    st.write("Click to apply all the selected actions and rollbacks, you'll be shown with a preview of the new dataset. You'll still have a chance to comeback.")
    if st.button("Confirm"):
        st.session_state['y'] = 2
        st.experimental_rerun()
    st.session_state['once'] = False
elif st.session_state['status'] == 2:
    ()
st.markdown("---")
if st.button("Back To Homepage"):
        switch_page("homepage")

