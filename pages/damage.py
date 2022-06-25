
import streamlit as st
from time import sleep
import os
import re
from scripts import data_utils
from time import sleep
from scripts import data_utils
from scripts import damage_parameter
from scripts import config

# st.markdown("# Page 2 ❄️")
# st.sidebar.markdown("# Page 2 ❄️")
destination = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/raw/finite_elements"))
#from config import m, material_param_delta0, C, k, scale_sizes, PROCESSED_DATA_PATH,BASE_PATH

BASE_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../data"))

scale_sizes = ["100", "80", "60", "40"]

def Process_data():

    st.title("Processing data Page")
    uploaded_files = st.file_uploader("Choose a  file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        #st.write("type:", uploaded_file)
        bytes_data= uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        #st.write(bytes_data)
        #move_folder = os.path.join(BASE_PATH, uploaded_file.name)
        with open(os.path.join(destination,uploaded_file.name), 'w', encoding='utf-8') as f:
            f.write(bytes_data.decode('utf-8'))

    process_button = st.button("Process the data")

    if process_button:
        # Create a text element and let the reader know the data is loading.
        data_load_state = st.text("[INFO]: Processing data ...")

        FE_paths, EXP_paths = data_utils.get_paths()
        fe_raw_paths, fe_processed_paths = FE_paths
        print("process ", FE_paths, EXP_paths)
        data_utils.process_data(FE_paths, EXP_paths)
        for test_path in fe_processed_paths:
            print(" reading "+test_path)
            data = data_utils.read_processed_data(test_path)

            data_load_state.text("[INFO]: Processed done!")

            # Read data for each scale
            file_name = os.path.basename(test_path)
            scale_size = re.findall(r"\d+", file_name)
            st.subheader(f"Processed sample {scale_size}:")
            st.write(file_name)
            print("read", scale_size, " from ", file_name)
            st.dataframe(data.head(10))

def Estimation_damage():
    st.title("Estimation damage Parameter")
    estimate_button = st.button("Estimate damage and effective damage parameter")

    if estimate_button:
        w_estimate_state = st.text("[INFO]: Estimating w ...")

        sleep(1)

        FE_paths, EXP_paths = data_utils.get_paths()
        _, fe_processed_paths = FE_paths

        fe_vol_paths = [v_path for v_path in fe_processed_paths if "_Vol" in v_path]
        fe_ss_paths = [s_path for s_path in fe_processed_paths if "_SS" in s_path]
        fe_paths = (fe_ss_paths, fe_vol_paths)

        # Method 2:
        # w_df = damage_parameter.estimate_w_met2(fe_paths)
        # Method 5:
        output_results_path = os.path.sep.join(
            [BASE_PATH + "/processed", "parameters", "damage_parameter"]
        )
        m = st.session_state.config['k']*st.session_state.config['bn_mean']
        w_df = damage_parameter.estimate_w_met5(fe_paths, m, st.session_state.config['c'], st.session_state.config['k'], scale_sizes, config.material_param_delta0)
        w_df.to_csv(os.path.join(output_results_path, "met_5.csv"), index=None)


        w_estimate_state = st.text("[INFO]: Estimation done!")

        st.subheader("Estimation results:")
        st.dataframe(w_df)

def estimate_process():
    Process_data()
    Estimation_damage()
