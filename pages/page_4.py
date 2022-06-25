import streamlit as st
from scripts.Failure_proba2 import twoD_array
from scripts.Failure_proba2 import threeD_array
from PIL import Image
import os


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))


# st.markdown("# Page 4 ❄️")
# st.sidebar.markdown("# Page 4 ❄️")

def failure_probability():
    Failure_probability = st.button("Calculation of the failure probability ")
    if Failure_probability:
        gamma = st.session_state.config['gamma']
        twoD_array()

        threeD_array(gamma)
        print("done calculation")
        st.write("done")
# failure_probability()

