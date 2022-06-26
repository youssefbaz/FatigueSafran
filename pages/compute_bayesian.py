
import streamlit as st
from scripts.Bayesian_inference import calculate_bayesian
from PIL import Image
import os
from scripts.config import *

#import scripts.likelihood_params from config

# st.markdown("# Page 3 ❄️")
# st.sidebar.markdown("# Page 3 ❄️")
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))

def Bayesian():
    calculation_bayesian = st.button("Calculation of the Bayesian inference")

    if calculation_bayesian:

        calcul_state = st.text("[INFO]: Calculating...")
        fig_trace, fig_posterior = calculate_bayesian(st.session_state.config)
        if not fig_trace:
            st.warning(fig_posterior)
            return

        #image1 = Image.open(BASE_PATH+"/image_trace.png")
        #st.image(image1, caption='image trace')
        st.write(fig_trace)
        #image2 = Image.open(BASE_PATH+"/image_posterior.png")
        #st.image(image2, caption='image trace')
        st.write(fig_posterior)

        calcul_state = st.text("[INFO]: Calculating done")

# Bayesian()