import streamlit as st
from scripts.Failure_proba2 import calculate_failure
from PIL import Image
import os


# st.markdown("# Page 4 ❄️")
# st.sidebar.markdown("# Page 4 ❄️")

def failure_probability():
    Failure_probability = st.button("Calculation of the failure probability ")
    if Failure_probability:
        gamma = st.session_state.config['gamma']
        status=st.text("calculating using gamma "+str(gamma))
        fig, fig1 = calculate_failure(gamma)
        if not fig:
            st.warning("Error "+str(fig1))
        else:
            st.write(fig)
            st.write(fig1)
            status.text("done calculation")

# failure_probability()

