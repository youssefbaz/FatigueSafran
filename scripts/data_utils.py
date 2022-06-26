
# Data manipulation
import numpy as np
import pandas as pd
from scripts import config
#import  config

# OS interface
import os
import glob


def create_finite_element_df(file_path, output_path, skiprows=19, skipfooter=9):
    """
    Create .csv (sep = ;) files from the original data .rpt files.
    Parameters:
        file_path (str): Path of the .rpt file
        output_path (str): Path where the .csv will be saved
        skiprows (int): Number of rows skipped from the .rpt file (default 19)
        skipfooter (int): Number of end-rows ignored from the .rp file (default 9)
    Returns:
        None
    """
    if "SS" in file_path:
        names = ["label", "LE_max", "S_max"]
        dtype = {"label": np.int64, "LE_max": np.float64, "S_max": np.float64}
    else:
        names = ["label", "E_vol"]
        dtype = {"label": np.int64, "E_vol": np.float64}

    finite_element_df = pd.read_fwf(
        file_path,
        delimiter="    ",
        skiprows=skiprows,
        names=names,
        index_col=False,
        dtype=dtype,
        skipfooter=skipfooter,
    )

    # Make this change in order to fix the label column:
    finite_element_df["label"] = finite_element_df.index + 1

    finite_element_df.to_csv(output_path, index=None, sep=";")


def create_experimental_df(input_path, output_path):
    """
    Create .csv (sep = ;) files from the original data .txt files.
    Parameters:
        file_path (str): Path of the .txt file
        output_path (str): Path where the .csv will be saved
    Returns:
        None
    """

    experimental_df = pd.read_csv(
        input_path,
        skiprows=1,
        sep="\t",
        names=["LCF", "Specimen"],
        header=0,
        dtype={"LCF": np.float64, "Specimen": np.int64},
    )

    experimental_df.to_csv(output_path, index=None, sep=";")


def read_processed_data(file_path, file_sep=";"):
    """
    Read a .csv file with a given separator.
    Parameters:
        file_path (str): Path of the .csv file
        file_sep (str): csv separator (default ;)
    Returns:
        processed_df (dataframe): Pandas data frame with the .csv content.
    """
    processed_df = pd.read_csv(file_path, delimiter=file_sep)
    return processed_df






def get_paths():
    # Get FE rpt files paths:
    fe_raw_path = config.RAW_DATA_PATH
    print("[INFO]: *.rpt files path: ", fe_raw_path)
    fe_raw_paths = glob.glob(os.path.join(fe_raw_path, "*.rpt"))

    # Creating processed paths
    fe_processed_paths = [
        path.replace("raw", "processed").replace("rpt", "csv") for path in fe_raw_paths
    ]

    print("[INFO]: Files to process: ", *fe_raw_paths, sep="\n")

    # Get Experimental data .txt files paths:

    exp_raw_path = config.EXPERIMENTAL_PATH# os.path.sep.join([output_path, "experimental"])
    print("[INFO]: *.txt files path: ", exp_raw_path)
 
    expmtl_raw_paths = glob.glob(
        os.path.join(exp_raw_path, "*.txt")
    )
 
    # Creating processed paths
    expmtl_processed_path = [
        path.replace(config.EXPERIMENTAL_PATH, config.PROCESSED_DATA_EXP).replace("txt", "csv")
        for path in expmtl_raw_paths
    ]
 
    print("[INFO]: Files to process: ", *expmtl_raw_paths, sep="\n")

    FE_paths = (fe_raw_paths, fe_processed_paths)
    EXP_paths = (expmtl_raw_paths, expmtl_processed_path)

    return FE_paths, EXP_paths


def process_data(FE_paths, EXP_paths):
    # Process FE data
    fe_raw_paths, fe_processed_paths = FE_paths

    print("[INFO]: Processing FE data ...")
    for i in range(len(fe_raw_paths)):
        print(f"Processing: {fe_processed_paths[i]}")
        create_finite_element_df(fe_raw_paths[i], fe_processed_paths[i])

    # Process Experimental data
    print("[INFO]: Processing Experimenta data ...")

    expmtl_raw_paths, expmtl_processed_paths = EXP_paths

    for i in range(len(expmtl_raw_paths)):
        print(f"Processing: {expmtl_raw_paths[i]}")
        create_experimental_df(expmtl_raw_paths[i], expmtl_processed_paths[i])

    print("[INFO]: Processed done!")


if __name__ == "__main__":
    FE_paths, EXP_paths = get_paths(gamma)
    process_data(FE_paths, EXP_paths)
