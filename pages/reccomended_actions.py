from tkinter.font import BOLD
from turtle import color
import streamlit as st
import time
import pandas as pd
import numpy as np
import pandas_profiling
from pandas_profiling import *
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.switch_page_button import switch_page
from annotated_text import annotated_text
import json
import os
df = st.session_state['df']

#if os.path.exists("newProfile.json"):
#  os.remove("newProfile.json")
#else:
#  print("The file does not exist")
if st.button("Done!"):
        switch_page("Homepage")

