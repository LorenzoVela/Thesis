import time
import numpy as np
import pandas as pd
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox
import os
from pandas_profiling import *
import json
import numpy as np

def update_selectbox_style():
    st.markdown(
        """
        <style>
            .stSelectbox [data-baseweb="select"] div[aria-selected="true"] {
                white-space: normal; overflow-wrap: anywhere;
                :first-child{
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
            span[data-baseweb="tag"] {
                background-color: indianred !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

update_multiselect_style()
update_selectbox_style()



m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 254, 239);
    height:4em;
    width:auto;
}
</style>""", unsafe_allow_html=True)

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


profile = st.session_state['profile']
report = st.session_state['report']
df = st.session_state['df']


st.title("Column splitting")
slate = st.empty()
body = slate.container()
with body:
    if st.session_state['y'] == 0:  #choose the values to replace
        st.subheader("Dataset preview")
        st.write(df.head(200))
        dfPreview = df.copy()
        columns = list(df.columns)
        for col in columns:
            if df[col].dtype == "float64":
                columns.remove(col)
        column = st.selectbox("Select the column to be splitted", columns)
        delimiters = [" ", ",", ";", " ' ", "{", "}", "[", "]", "(", ")", " \ ", "/", "-", "_", ".", "|"]
        if column != None:
            colPreview = df[column].copy()
            importantDelimiters = []
            importantCounters = []
            for item in delimiters:
                counter = 0
                for i in range(int(len(df.index))):  #search for a delimiter in the column
                    x = str(colPreview[i]).find(item)
                    if x > 0:
                        counter += 1
                if counter >= (len(df.index)/20):  #if is present at least in 5% of the lines then we should propose it!
                    importantDelimiters.append(item)
                    importantCounters.append(counter)
            
            for i in range(0, len(importantDelimiters)):
                if importantDelimiters[i] == " ":
                    importantDelimiters[i] = "First space appearance"
            importantDelimiters.insert(0,"None")
            importantCounters.insert(0, "None")
            delimiter = st.selectbox("Select the delimiter ", importantDelimiters)
            if delimiter != "None":
                num = importantCounters[(importantDelimiters.index(delimiter))]
                percentage = num / len(df.index) * 100
                infoString = f"This delimiter appears {num} times (" + str("%0.2f" %(percentage)) + "%) within this column"
                for i in range(len(df.index)):
                    if delimiter == "First space appearance":
                        if " " in str(colPreview[i]):
                            flag = 0
                            string = str(colPreview[i]).split(" ", 1)
                            break
                    else:
                        #infoString = f"This delimiter appears {importantCounters[(importantDelimiters.index(delimiter))]} times within this column"
                        if delimiter in str(colPreview[i]):
                            flag = 1
                            string = str(colPreview[i]).split(delimiter, 1)
                            break
                st.info(infoString)
                if len(string) == 1:
                    st.error("It's not possible to split this column")
                else:
                    data = [string]
                    st.write(f"One-line preview of the first splittable row, **you're strongly recommended to do not apply splitting to numeric columns**")
                    oneLinePreview = pd.DataFrame(data, columns=['First column', 'Second column'])
                    st.write(oneLinePreview)
                    firstColumn = st.text_input("Insert the name of the new 'First column'")
                    secondColumn = st.text_input("Insert the name of the new 'Second column'")
                    columnsLower = [element.lower() for element in columns]
                    firstColumnLower = firstColumn.lower()
                    secondColumnLower = secondColumn.lower()
                    if firstColumn == "" or secondColumn == "":
                        st.write("null")
                    elif firstColumnLower == secondColumnLower:
                        st.write("name not distinct")
                    elif firstColumnLower in columnsLower or secondColumnLower in columnsLower:
                        st.write("contained in the dataset")
                    else:
                        #st.write("ok")
                        st.warning("The splitting will be applying where possible. You'll be shown with a preview of the new dataset")
                        if st.button("Go!", on_click=clean1):
                            ()





st.markdown("---")
if st.button("Done!"):
        switch_page("Homepage")

