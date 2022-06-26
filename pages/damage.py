
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
#from config import m, material_param_delta0, C, k, scale_sizes, PROCESSED_DATA_PATH,BASE_PATH

scale_sizes = ["100", "80", "60", "40"]

def Process_data():

    st.title("Processing data Page")
    uploaded_files = st.file_uploader("Choose a  file", accept_multiple_files=True)
    hasText=False
    "test".lower
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith(".rpt"):
            destination = os.path.abspath(config.RAW_DATA_PATH)
        elif uploaded_file.name.lower().endswith(".txt"):
            hasText=True
            destination = os.path.abspath(config.EXPERIMENTAL_PATH)
        #st.write("type:", uploaded_file)
        bytes_data= uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        #st.write(bytes_data)
        #move_folder = os.path.join(BASE_PATH, uploaded_file.name)
        with open(os.path.join(destination,uploaded_file.name), 'w', encoding='utf-8') as f:
            f.write(bytes_data.decode('utf-8'))
    os.sync()


    process_button = st.button("Process the data")

    if process_button:

        # Create a text element and let the reader know the data is loading.
        data_load_state = st.text("[INFO]: Processing data ...")

        FE_paths, EXP_paths = data_utils.get_paths()
        fe_raw_paths, fe_processed_paths = FE_paths
        print("got paths", fe_raw_paths, fe_processed_paths)
        if not fe_raw_paths and not fe_processed_paths:
            st.write("no file to process, please provide file using upload component above")
        else:
            if not EXP_paths or (not EXP_paths[0] and not EXP_paths[1]):
                st.warning("No test result provided. We'll use Test_results_different_scales_CHP.")
                import shutil
                print("=== copy "+config.DEMO_PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv"+" ==> "+config.PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv")
                shutil.copy(config.DEMO_PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv", config.PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv")
                os.sync()
                config.get_nf()
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
        print("[INFO]: Estimating w ...")
        config.get_nf()
        FE_paths, EXP_paths = data_utils.get_paths()
        _, fe_processed_paths = FE_paths

        fe_vol_paths = [v_path for v_path in fe_processed_paths if "_"+data_utils.VOL_EXT in v_path]
        fe_ss_paths = [s_path for s_path in fe_processed_paths if "_"+data_utils.SS_EXT in s_path]
        fe_paths = (fe_ss_paths, fe_vol_paths)

        # Method 2:
        # w_df = damage_parameter.estimate_w_met2(fe_paths)
        # Method 5:
        output_results_path = os.path.sep.join(
            [config.BASE_PATH, "processed", "parameters"]
        )
        print("result should go to "+output_results_path)
        m = st.session_state.config['k']*st.session_state.config['bn_mean']
        print(fe_paths, m, st.session_state.config)
        w_df = damage_parameter.estimate_w_met5(fe_paths, m, st.session_state.config['c'], st.session_state.config['k'], scale_sizes, config.material_param_delta0)
        w_df.to_csv(os.path.join(output_results_path, "met_5.csv"), index=None)


        w_estimate_state = st.text("[INFO]: Estimation done!")

        st.subheader("Estimation results:")
        st.dataframe(w_df)

def estimate_process():
    Process_data()
    Estimation_damage()
