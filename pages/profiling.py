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

df = st.session_state['df']
#profile = st.session_state['profile']
pr = df.profile_report()
pr.to_file("testProfile.json")
st_profile_report(pr)

if st.button("Done!"):
        switch_page("Homepage")

