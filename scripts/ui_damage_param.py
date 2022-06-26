import streamlit as st
from time import sleep
import os
import re


import data_utils
import damage_parameter

st.title("SAFRAN")


process_button = st.button("Process the data")


if process_button:
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text("[INFO]: Processing data ...")

    sleep(1)

    fe_raw_paths, fe_processed_paths = data_utils.get_paths()
    # data_utils.process_data(fe_raw_paths, fe_processed_paths)

    test_path = fe_processed_paths[0]
    data = data_utils.read_processed_data(test_path)

    data_load_state.text("[INFO]: Processed done!")

    # Read data for each scale
    file_name = os.path.basename(test_path)
    scale_size = re.findall(r"\d+", file_name)
    st.subheader(f"Processed sample {scale_size}:")
    st.dataframe(data.head(10))


estimate_button = st.button("Estimate damage and effective damage parameter")


if estimate_button:

    w_estimate_state = st.text("[INFO]: Estimating w ...")

    sleep(1)

    _, fe_processed_paths = data_utils.get_paths()

    fe_vol_paths = [v_path for v_path in fe_processed_paths if "_"+data_utils.VOL_EXT in v_path]
    fe_ss_paths = [s_path for s_path in fe_processed_paths if "_"+data_utils.SS_EXT in s_path]
    fe_paths = (fe_ss_paths, fe_vol_paths)

    w_df = damage_parameter.estimate_w(fe_paths)

    w_estimate_state = st.text("[INFO]: Estimation done!")

    st.subheader("Estimation results:")
    st.dataframe(w_df)
