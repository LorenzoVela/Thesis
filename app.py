import os
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="[app]Titolo del tab", layout="wide", initial_sidebar_state="collapsed")

st.title("Welcome to the introduction page")

start_button = st.button("Let's start the analysis")
st.session_state['x'] = 0
if start_button:
    switch_page("prova")
    #if st.button("prova"):
####################
### IMPORT PAGES ### 
####################

#from multipage import MultiPage
#from pages import prova, prova2

# Create an instance of the app 
#app = MultiPage() 


#################
### ADD PAGES ###
#################

#app.add_page("[app]Questa è la pagina di prova", prova.app)
#st.markdown("<style> li {display: unset}</style>", unsafe_allow_html=True)
#app.add_page("[app]Questa è la seconda pagina di prova", prova2.app)
#app.add_page("Presentation Page", presentation_page.app)
#app.add_page("Data Wrangling Page", automatic_data_wrangling.app)


############
### MAIN ###
############

#app.run()






##################
### IMPORT CSS ###
##################

#with open("style.css") as f:
    #st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
    #st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#st.markdown("<style> li {display: none;}</style>", unsafe_allow_html=True)
