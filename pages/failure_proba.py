import streamlit as st
from scripts.Failure_proba2 import calculate_failure
from PIL import Image
import os
from scripts import data_utils
from scripts import config
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))


# st.markdown("# Page 4 ❄️")
# st.sidebar.markdown("# Page 4 ❄️")

def failure_probability():
    Failure_probability = st.button("Calculation of the failure probability ")
    if Failure_probability:
        gamma = st.session_state.config['gamma']
        status=st.text("calculating using gamma "+str(gamma))

        _, EXP_paths = data_utils.get_paths()
        if not EXP_paths or (not EXP_paths[0] and not EXP_paths[1]):
            st.warning("No test result provided. We'll use Test_results_different_scales_CHP.")
            import shutil
            print("=== copy "+config.DEMO_PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv"+" ==> "+config.PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv")
            shutil.copy(config.DEMO_PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv", config.PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv")
            os.sync()
            config.get_nf()
        fig, fig1 = calculate_failure(gamma)
        if not fig:
            st.warning("Error "+str(fig1))
        else:
            st.write(fig)
            st.write(fig1)
            status.text("done calculation")

# failure_probability()

