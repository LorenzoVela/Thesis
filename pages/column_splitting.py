import streamlit as st
import time
import pandas as pd
import numpy as np
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.switch_page_button import switch_page


m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 254, 239);
    height:4em;
    width:4em;
}
</style>""", unsafe_allow_html=True)

wrangler_df = st.session_state['df']
#dfCol = st.session_state['dfCol']
st.title("Column splitting")
st.subheader("Column Splitting")
st.markdown(
    "This wrangling operation let you split a column composed of multiple values.")
st.info(
    "👀Please select the column first, then the delimiter and then call your new columns whatever you want!")
dfCol = []
for col in wrangler_df.columns:
    if "," in str(wrangler_df[col][0]) or " " in str(wrangler_df[col][0]):
        dfCol.append(col)
if (len(dfCol) > 0):
    columnChosen = st.radio("Columns with possible splitting:", dfCol, key=104)
    splittingDelimiter = st.selectbox("Select the delimiter of " + columnChosen,
                                        (" ", ","), 0)
    if splittingDelimiter == " ":
        if " " not in str(wrangler_df[columnChosen][0]):
            st.error(
                "Sorry, there are no tuples in column " + columnChosen + " that agree with your pattern.\nPlease update column or delimiter!")
        else:
            st.success("Possibile wrangling!")

            firstColumn = st.text_input(
                "Insert the name of the new column before the splitter: ")
            secondColumn = st.text_input(
                "Insert the name of the new column after the splitter: ")
            split1 = wrangler_df[columnChosen].str.split(expand=True)

            applySplit = st.checkbox("Click here to apply", value=False, key=15)

            if applySplit == True:
                wrangler_df[[firstColumn, secondColumn]] = wrangler_df[
                    columnChosen].str.split(splittingDelimiter, n=1, expand=True)
                st.success(
                    "🎉Congrats!\nYou splitted column " + columnChosen + " into the two new columns: " + firstColumn + ", " + secondColumn)

                deleteSplittedColumn = st.radio(
                    "Do you want to delete your splitted column " + columnChosen + "?",
                    ("Yes", "No"), 1, key=105)

                if deleteSplittedColumn == "Yes":
                    wrangler_df = wrangler_df.drop(columnChosen, axis=1)
                    st.info("Column " + columnChosen + " has been removed!")
                else:
                    st.info("Column " + columnChosen + " hasn't been removed!")

                #wrangler_df_csv = convert_df(wrangler_df)

                showSplit = st.checkbox(
                    "Click here to show the new wrangled-dataset", value=False,
                    key=16)
                if showSplit:
                    st.write(wrangler_df.head())

                operationApllied = True

    if splittingDelimiter == ",":
        if "," not in str(wrangler_df[columnChosen][0]):
            st.error(
                "Sorry, there are no tuples in column " + columnChosen + " that agree with your pattern.\nPlease update column or delimiter!")
        else:
            st.success("Possibile wrangling!")

            firstColumn = st.text_input(
                "Insert the name of the new column before the splitter: ")
            secondColumn = st.text_input(
                "Insert the name of the new column after the splitter: ")
            split1 = wrangler_df[columnChosen].str.split(expand=True)

            applySplit = st.checkbox("Click here to apply", value=False, key=17)
            if applySplit == True:
                wrangler_df[[firstColumn, secondColumn]] = wrangler_df[
                    columnChosen].str.split(splittingDelimiter, n=1, expand=True)
                st.success(
                    "🎉Congrats!\nYou splitted column " + columnChosen + " into the two new columns: " + firstColumn + ", " + secondColumn)

                deleteSplittedColumn = st.radio(
                    "Do you want to delete your splitted column " + columnChosen + "?",
                    ("Yes", "No"), 1, key=106)
                if deleteSplittedColumn == "Yes":
                    wrangler_df = wrangler_df.drop(columnChosen, axis=1)
                    st.info("Column " + columnChosen + " has been removed!")
                else:
                    st.info("Column " + columnChosen + " hasn't been removed!")

                #wrangler_df_csv = convert_df(wrangler_df)
                showSplit = st.checkbox("Click here to show your splitted dataset",
                                        value=False, key=18)
                if showSplit:
                    st.write(wrangler_df.head())

                operationApllied = True
else:
    st.error(
        "Sorry, there are no tuples in your dataset that agree with your pattern. Please select another wrangling operation!")

if st.button("Done!"):
        switch_page("Homepage")

