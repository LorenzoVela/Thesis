import json
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
import streamlit.components.v1 as components
import recordlinkage
from recordlinkage.index import Block
from sklearn.metrics.pairwise import cosine_similarity
import jaro
from streamlit_extras.no_default_selectbox import selectbox


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
    height:auto;
    width:auto;
}
</style>""", unsafe_allow_html=True)

def clean0 ():
    slate2.empty()
    st.session_state['y'] = 0

def clean1 ():
    slate1.empty()
    st.session_state['y'] = 1

def clean10 ():
    slate1.empty()
    st.session_state['y'] = 2

def cleanHome ():
    slate2.empty()
    switch_page("Homepage")

df = st.session_state['df']
dfCol = st.session_state['dfCol']
profile = st.session_state['profile']
report = st.session_state['report']
correlations = profile.description_set["correlations"]
phik_df = correlations["phi_k"]

st.title("Duplicates detection")
slate1 = st.empty()
body1 = slate1.container()
slate2 = st.empty()
body2 = slate2.container()
with body1:
    if st.session_state['y'] == 0:
        setColToDropWeights = set()
        with st.expander("Expand to understand more over the technique that is being used to detect duplicates", expanded=False):
            st.write(f"The technique that is being used for the **record linkage** is the blocking technique. The dataset will be partioned in blocks, in this case a block will be composed by tuples that have the same values for the attribute/s selected below.")
            st.write(f"For the **similarity** is being used the jaro-winkler metric. Is a string edit distance between two sequences. In this case the algorithm is slightly modified: to calculate the similarity between two rows every attribute can have a weight between 0 and 2.")
        listCol = df.columns
        colToDrop = st.multiselect("Select one or more columns that will be used to match possible duplicates", listCol, key="multiselect")
    #threshold selection, would be nice with a slider -> pay attention to the refresh(could be better to use the stremlit one)
        numOfCouples = 0
        max = ((len(df.index) * (len(df.index) - 1)) / 5)
        if len(colToDrop) > 0:
            try:
                Blocker = Block(on=colToDrop)
                candidate_links = Blocker.index(df)
                numOfCouples = len(candidate_links)
            except:
                st.error("Please select something.")
            if numOfCouples >= max:
                st.error(f"This set is not eligile for blocking because generates too many comparisons (**{numOfCouples}**). Please, change the blocking set.")
            elif numOfCouples > 0 and numOfCouples < max:
                st.info(f"There are **{numOfCouples}** couples of rows that have the same values for this set of column/s. These are two samples:")
                st.write(df.iloc[[candidate_links[1][0], candidate_links[1][1]]].style.apply(lambda x: ['background-color: lightgreen' if x.name in colToDrop else '' for i in x], axis=0))
                st.write(df.iloc[[candidate_links[3][0], candidate_links[3][1]]].style.apply(lambda x: ['background-color: lightgreen' if x.name in colToDrop else '' for i in x], axis=0))
                #st.write(df.iloc[[candidate_links[1][0], candidate_links[1][1]]])
                #st.dataframe(candidate_links)
                #setCompare = set(df.columns.drop(colToDrop))
                setCompareTemp = list(df.columns.drop(colToDrop))
                weights = []
                setCompare = []
                #st.write(setCompare)
                for col in df.columns:
                    if col in setCompareTemp and (len(pd.unique(df[col])) == len(df.index) or len(pd.unique(df[col])) == 1):
                        setCompareTemp.remove(col)
                    else:
                        ()
                #st.info("Select the weights for every column that will be used to calculate the similarity. For the similarity calculation are excluded the columns that have been selected for blocking and the columns that have the same value for all the rows.")
                st.markdown("---")
                st.write(f"Automatically removing from the set used to calculate the similarity all the columns that have a unique values, the columns with a different value for each row")
                colToDropWeights = st.multiselect("Select one or more additional column that won't be used as weight to calculate the string similarity", setCompareTemp)    
                if len(colToDropWeights) > 0:
                    setColToDropWeights = set(colToDropWeights)
                    setCompare = [x for x in setCompareTemp if x not in setColToDropWeights]
                else:
                    setCompare = setCompareTemp
                st.markdown("---")
                st.subheader("Select the weights")
                st.write("")
                #st.write("setCompareTemp", setCompareTemp,"setCompare", setCompare,"setCol", setColToDropWeights)
                columnsWeight = st.columns([1 for i in range(len(setCompare))], gap="small")
                for i in range(len(setCompare)):
                    with columnsWeight[i]:
                        label = str(setCompare[i])
                        weight = st.number_input(label, 0.0, 100.0, 1.0, 0.25)
                        weights.append([weight, label])
                st.markdown("---")
                threshold = st.slider("Select a similarity threshold above to display the pairs of possible duplicate rows", 0.01, 1.00, value=0.9, step=0.01)
                if threshold < 0.9:
                    st.warning("Pay attention because the computation can take up to some minutes!")
                st.write("")
                drop = st.checkbox("Check to drop the rows that has more null values within the same couple. To perform this no conflicts should be present.")
                st.write("")
                st.write("")
                st.session_state['weights'] = weights
                st.session_state['threshold'] = threshold
                st.session_state['setCompare'] = setCompare
                st.session_state['candidate_links'] = candidate_links
                st.session_state['drop'] = drop
                columns = st.columns([1,10,1], gap='small')
                with columns[0]:
                    if st.button("Go!", on_click=clean1):
                        ()
                with columns[2]:
                    if st.button("Clear selection", on_click=clean10):
                        ()
            elif len(colToDrop) > 0:
                st.error("One of the attribute chosen is not eligible for blocking, given the fact that is unique for every row.")
        else:
            ()
with body2:
    if st.session_state['y'] == 1:
        drop = st.session_state['drop']
        candidate_links = st.session_state['candidate_links'] 
        setCompare = st.session_state['setCompare']
        threshold = st.session_state['threshold']
        weights = st.session_state['weights']
        #st.write(weights)
        #st.write(setCompare)
        i = 0
        count = 0
        changed = 0
        for item in candidate_links:
            i += 1
            st.write([item[0]], len(df.index))
            row1Null = df.iloc[item[0]].isna().sum(axis=0)
            row2Null = df.iloc[item[1]].isna().sum(axis=0)
            jaroNum = 0
            totalWeight = 0
            for col, weight in zip(setCompare, weights):
                if str(weight[1]) == col:
                    totalWeight += weight[0]
                    jaroNum += (jaro.jaro_winkler_metric(str(df.iloc[item[0]][col]), str(df.iloc[item[1]][col])) * weight[0])
                    #st.write(jaroNum, col)
            #st.write("Sum of all the wighted similarities", jaroNum)
            #st.write("Sum of all the weights" , totalWeight)
            sim = jaroNum/totalWeight
            st.write("Similarity of couple ", i, " is ", sim)
            if sim == 1:
                st.write(df.iloc[[item[1], item[0]]])
                count += 1
                st.write("Given that these 2 rows are equal, it's arbitrarily dropped the second one. NO information is lost")
                df.drop([item[0]], axis=0, inplace=True)
            elif sim >= threshold:     #with 0.7 -> 40second
                st.write(df.iloc[[item[1], item[0]]])
                count += 1
                #st.write(df.iloc[[item[0]]][setCompare])
                #st.write("Null values in row 1 ", row1Null)
                #st.write("Null values in row 2 ", row2Null)
                if (row1Null + row2Null) > 0:
                    if drop:
                        result = {}
                        row1 = df.iloc[item[0]]
                        row2 = df.iloc[item[1]]
                        flag = "YES"
                        #provare sempre a droppare row1
                        for attr in setCompare:
                            if str(row1[attr]) in ['<NA>', 'nan']:
                                result[attr] = row2[attr]
                                #st.write(result[attr], "row1 was null")
                            elif str(row2[attr]) in ['<NA>', 'nan']:
                                result[attr] = row1[attr]
                                #st.write(result[attr], "row2 was null")
                            elif str(row1[attr]) == str(row2[attr]):
                                result[attr] = row1[attr]
                                #st.write(result[attr], "None of them was null")
                            else:
                                flag = "NO"
                                break
                        #st.write(f"**{flag}**  {result}")
                        if flag == "YES":
                            df.loc[item[0], setCompare] = [result[col] for col in setCompare]
                            st.write("The two previous rows will be replaced with this one. No information is lost")
                            st.write(df.iloc[[item[0]]])
                            df.drop([item[1]], axis=0, inplace=True)
                            changed += 1
            #if i == 40:
            #    break
            st.markdown("---")
        st.write(changed)
        st.info(f"There are **{count}** couples of rows that have a similarity equal or higher to the threshold of {threshold}")
        st.write("")
        if st.button("Back",on_click=clean0):
            ()

if st.session_state['y'] == 2:
    st.session_state['y'] = 0
    st.session_state.multiselect = []
    st.experimental_rerun()

st.markdown("---")
if st.button("Homepage", on_click=cleanHome):
    ()