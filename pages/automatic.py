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

droppedList = []

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
        droppedList.append(["rows", nullToDelete])
        if st.session_state['once'] == True:
            with st.spinner(text=stringDropAutomaticLoad):
                time.sleep(5)
        st.success(stringDropAutomaticConfirmed)
        with st.expander("Why I did it?"):
            st.write("Incomplete rows are one of the principal sources of poor information. Even by applying the imputing technique within these rows would just be almost the same as incresing the dataset's size with non-real samples.")
            if st.checkbox(stringDropRollback, value=False) == True:
                droppedList = droppedList[ : -1]
        st.markdown("---")
    for i in range(0, len(correlationList)):
        if correlationList[i][0] in dfAutomatic.columns and correlationList[i][1] in dfAutomatic.columns: 
            if correlationSum[correlationList[i][0]] > correlationSum[correlationList[i][1]]:
                x = 0
                y = 1
            else:
                x = 1
                y = 0
            strDropAutomaticCorrLoad = "Dropping column " + correlationList[i][x] + "because of it's high correlation with column " + correlationList[i][y]
            strDropAutomaticCorrConfirmed = f"Successfully dropped column **{correlationList[i][x]}** because of its high correlation with column {correlationList[i][y]}"
            strDropCorrRollback = f"Rollback the drop of column **{correlationList[i][x]}**"
            dfAutomatic = dfAutomatic.drop(correlationList[i][x], axis=1)
            droppedList.append(["column", correlationList[i][x]])
            if st.session_state['once'] == True:
                with st.spinner(text=strDropAutomaticCorrLoad):
                    time.sleep(2.5)
            st.success(strDropAutomaticCorrConfirmed)
            with st.expander("Why I did it?"):
                st.write("When two columns has an high correlation between each other, this means that the 2 of them together have almost the same amount of information with respect to have only one of them. ANyway some columns can be useful, for example, to perform aggregate queries. If you think it's the case with this column you should better rollback this action and keep it!")
                if st.checkbox(strDropCorrRollback, key=correlationSum[correlationList[i][x]]) == True:
                    st.write("Ciao0")
                    droppedList = droppedList[ : -1]
            #st.markdown("<p id=page-bottom>You have reached the bottom of this page!!</p>", unsafe_allow_html=True)
            st.markdown("---")
    for col in dfAutomatic.columns:
        k = randint(1,100)
        if len(pd.unique(dfAutomatic[col])) == 1:
            strDropAutomaticDistLoad = "Dropping column " + col + " because has the same value for all the rows, that is " + str(dfAutomatic[col][1])
            strDropAutomaticDistConfirmed = f"Successfully dropped column **{col}** because has the same value for all the rows, that is {dfAutomatic[col][1]}"
            strDropDistRollback = f"Rollback the drop of column **{col}**"
            dfAutomatic = dfAutomatic.drop(col, axis=1)
            droppedList.append(["column", col])
            if st.session_state['once'] == True:
                with st.spinner(text=strDropAutomaticDistLoad):
                    time.sleep(2.5)
            st.success(strDropAutomaticDistConfirmed)
            with st.expander("Why I did it?"):
                st.write("The fact that all the rows of the dataset had the same value for this attribute, doesn't bring any additional information with respect to removing the attribute. A dumb example could be: imagine a table of people with name, surname, date of birth...Does make sense to add a column called 'IsPerson'? No, because the answer would be the same for all the rows, we already know that every row here represent a person.")
                if st.checkbox(strDropDistRollback, key=k) == True:
                    st.write("Ciao0")
                    droppedList = droppedList[ : -1]
        st.markdown("---")
    st.write("Click to apply all the selected actions and rollbacks, you'll be shown with a preview of the new dataset. You'll still have a chance to comeback.")
    if st.button("Confirm"):
        ()
        #st.write(droppedList)
        #st.session_state['y'] = 2
        #st.experimental_rerun()
    st.session_state['once'] = False
elif st.session_state['y'] == 2:
    ()
st.markdown("---")
if st.button("Back To Homepage"):
        switch_page("homepage")

