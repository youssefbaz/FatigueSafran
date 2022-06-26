import streamlit as st
from pages.damage import estimate_process
from pages.compute_bayesian import Bayesian
from pages.failure_proba import failure_probability
from pages.custom_variables import value
from pages.doc import show_pdf
from scripts import config

st.set_page_config(page_title='Safran')
st.write(config.BASE_PATH)
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
    "1 - Custom Variables": value,
    "2 - Procesing data and Estimation of damage parameter": estimate_process,
    #"Processing data:": Estimation_damage,
    #"Estimation of damage": Estimation_damage,
    "3 - Compute the Bayesian": Bayesian,
    "4 - Calculate a failure probability": failure_probability,
    "Documentation":show_pdf
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


