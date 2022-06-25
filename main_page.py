import streamlit as st
from pages.page_2 import estimate_process
from pages.page_3 import Bayesian
from pages.page_4 import failure_probability
from pages.page_5 import value
from pages.page_6 import show_pdf
from scripts import config

st.set_page_config(page_title='Safran')
def main_page():

    st.text("Steps to Follow ")

    st.text(" Step 1/custom variables to start the process")
    st.text(" Step 2/Process Data and estimate the damage parameter")
    st.text(" Step 3/Compute the bayesian")
    st.text(" Step 4/Calculate the Probability of failure ")

    if not 'config' in st.session_state:
        st.session_state.config = config.default_params


page_names_to_funcs = {
    "Main Page": main_page,
    "Procesing data and Estimation of damage parameter": estimate_process,
    #"Processing data:": Estimation_damage,
    #"Estimation of damage": Estimation_damage,
    "Compute the Bayesian": Bayesian,
    "Calculate a failure probability": failure_probability,
    "Custom Variables": value,
    "Documentation":show_pdf
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


