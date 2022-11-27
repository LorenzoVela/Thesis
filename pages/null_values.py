import time

import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page


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

parentPage = st.session_state['from']
dfCol = st.session_state['arg'] #dfCol is a series here
profile = st.session_state['profile']
report = st.session_state['report']
df = st.session_state['df']

string = "Managing null values of column " + dfCol.name
st.title(string)
col1_1, col2_1, col3_1 = st.columns(3, gap='small')
#dfColNew = dfCol.to_frame()
nullNum = dfCol.isna().sum()
percentageNull = nullNum/len(dfCol.index)*100
with col1_1:
    st.write(dfCol.head())
with col2_1:
    st.write("This column has ", nullNum, " null values (" + "%0.2f" %(percentageNull) + "%)")

with st.expander("Which action you want to perform?", expanded=True):
    if st.session_state['y'] == 0:
        col1_2, col2_2, col3_2, col4_2, col5_2 = st.columns([0.4,1,1,1,1], gap='small')
        with col1_2:
            if st.button("Drop"):
                st.session_state['y'] = 1
                st.experimental_rerun()
        with col2_2:
            if st.button("Fill"):
                st.session_state['y'] = 2
                st.experimental_rerun()

    elif st.session_state['y'] == 1: #drop case
        st.warning("Do you really want to drop the entire column?")
        if st.radio("", ["", "No", "Yes"], horizontal=True) == "Yes":
            st.session_state['y'] = 3
            st.experimental_rerun()
        else:
            ()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 2: #fill case
        if df[dfCol.name].dtype == "object":
            fillingOpObj = st.radio("Filling options for " + dfCol.name + ":",("", "Following Value", "Previous Value","Mode", "Custom Value"), index=0,key=107)
            if fillingOpObj == "Following Value":
                st.session_state['y'] = 4
                st.experimental_rerun()
            elif fillingOpObj == "Previous Value":
                st.session_state['y'] = 5
                st.experimental_rerun()
            elif fillingOpObj == "Mode":
                st.session_state['y'] = 6
                st.experimental_rerun()
            elif fillingOpObj == "Custom Value":
                st.session_state['y'] = 7
                st.experimental_rerun()
        elif df[dfCol.name].dtype == "float64":
            fillingOpNum = st.radio("Filling options for " + dfCol.name + ":",("", "Min", "Max", "Avg", "0", "Mode"),index=0)
            if fillingOpNum == "Min":
                st.session_state['y'] = 13
                st.experimental_rerun()
            elif fillingOpNum == "Max":
                st.session_state['y'] = 8
                st.experimental_rerun()
            elif fillingOpNum == "Avg":
                st.session_state['y'] = 9
                st.experimental_rerun()
            elif fillingOpNum == "Mode":
                st.session_state['y'] = 10
                st.experimental_rerun()
            elif fillingOpNum == "0":
                st.session_state['y'] = 11
                st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 3: #drop confirmed
        df.drop[dfCol.name]
        st.write(df.head(20))
        st.session_state['df'] = df
        st.success("Column dropped successfully")
    
    elif st.session_state['y'] == 4: #Replace object with following value
        copyPreview = dfCol.copy()
        copyPreview.fillna(method="bfill", inplace=True)
        col1_4, col2_4 = st.columns(2)
        with col1_4:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_4:
            st.write("New column")
            st.write(copyPreview.head(30)) 
        radio4 = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 4)
        if  radio4 == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio4 == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 5: #Replace object with previous value
        copyPreview = dfCol.copy()
        copyPreview.fillna(method="ffill", inplace=True)
        col1_5, col2_5 = st.columns(2)
        with col1_5:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_5:
            st.write("New column")
            st.write(copyPreview.head(30)) 
        radio5 = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 5)
        if  radio5 == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio5 == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 6: #Replace object with mode value
        copyPreview = dfCol.copy()
        copyPreview.fillna(copyPreview.mode(), inplace=True)
        col1_6, col2_6 = st.columns(2)
        with col1_6:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_6:
            st.write("New column")
            st.write(copyPreview.head(30)) 
        radio5 = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 6)
        if  radio5 == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio5 == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 7: #Replace object with custom value
        copyPreview = dfCol.copy()
        customValue = st.text_input("Please insert the custom value you want to use:")
        if len(customValue) != 0:
            copyPreview.replace([np.nan], customValue, inplace=True)
            col1_7, col2_7 = st.columns(2)
            with col1_7:
                st.write("Old column")
                st.write(dfCol.head(30))
            with col2_7:
                st.write("New column")
                st.write(copyPreview.head(30)) 
            radio5 = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 7)
            if  radio5 == "Yes":
                st.session_state['copyPreview'] = copyPreview
                st.session_state['y'] = 12
                st.experimental_rerun()
            elif radio5 == "No":
                st.session_state['y'] = 2
                st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()
    
    elif st.session_state['y'] == 8: #Replace num with max value
        copyPreview = dfCol.copy()
        maxValue = report["variables"][dfCol.name]["max"]
        maxValue2 = "{:.2f}".format(maxValue)
        st.info("Replaced all the missing values with the maximum value: " + maxValue2)
        copyPreview.replace([np.nan], maxValue,inplace=True)
        col1_8, col2_8 = st.columns(2)
        with col1_8:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_8:
            st.write("New column")
            st.write(copyPreview.head(30))
        radio = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 8)
        if  radio == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 9: #Replace num with avg value
        copyPreview = dfCol.copy()
        avgValue = report["variables"][dfCol.name]["mean"]
        avgValue2 = "{:.2f}".format(avgValue)
        st.info("Replaced all the missing values with the average: " + avgValue2)
        copyPreview.replace([np.nan], avgValue2,inplace=True)
        col1_9, col2_9 = st.columns(2)
        with col1_9:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_9:
            st.write("New column")
            st.write(copyPreview.head(30))
        radio = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 9)
        if  radio == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 10: #Replace num with mode value
        copyPreview = dfCol.copy()
        strMode = str(copyPreview.mode()[0])
        infoString = "Replaced all the missing values with the mode value: " + strMode
        st.info(infoString)
        copyPreview.fillna(copyPreview.mode()[0], inplace=True)
        col1_10, col2_10 = st.columns(2)
        with col1_10:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_10:
            st.write("New column")
            st.write(copyPreview.head(30))
        radio = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 10)
        if  radio == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    elif st.session_state['y'] == 11: #Replace num with 0 value
        copyPreview = dfCol.copy()
        st.info("Replaced all the missing values with value 0")
        copyPreview.replace([np.nan], 0,inplace=True)
        col1_11, col2_11 = st.columns(2)
        with col1_11:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_11:
            st.write("New column")
            st.write(copyPreview.head(30))
        radio = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 11)
        if  radio == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun() 

    elif st.session_state['y'] == 12: #Save state
        
        #TODO
        #update the dataframe
        #do the profile again
        #remove the old report
        #load the new one
        #dfCol = st.session_state['copyPreview']
        #df[dfCol.name] = dfCol.values

        nullCount = str(dfCol.isnull().sum())
        successString = "Now the column has now " + nullCount + " null values"
        st.success(successString)
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()
        #st.write(df.head(20))
        #st.session_state['df'] = df

    elif st.session_state['y'] == 13: #Replace num with min value
        copyPreview = dfCol.copy()
        minValue = report["variables"][dfCol.name]["min"]
        minValue2 = "{:.2f}".format(minValue)
        st.info("Replaced all the missing values with the maximum value: " + minValue2)
        copyPreview.replace([np.nan], minValue,inplace=True)
        col1_13, col2_13 = st.columns(2)
        with col1_13:
            st.write("Old column")
            st.write(dfCol.head(30))
        with col2_13:
            st.write("New column")
            st.write(copyPreview.head(30))
        radio = st.radio("Do you want to apply these changes?", ["", "No", "Yes"], horizontal=True, index=0, key = 13)
        if  radio == "Yes":
            st.session_state['copyPreview'] = copyPreview
            st.session_state['y'] = 12
            st.experimental_rerun()
        elif radio == "No":
            st.session_state['y'] = 2
            st.experimental_rerun()
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()

    else:
        st.error("Something went wrong")
        if st.button("Back"):
            st.session_state['y'] = 0
            st.experimental_rerun()
if parentPage == 0:
    if st.button("Back to Dataset Info!"):
        switch_page("dataset_info")

if parentPage == 1:
    if st.button("Back to Homepage"):
        switch_page("Homepage")


