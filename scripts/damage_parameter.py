'''import numpy as np
import pandas as pd
import os
import re
from scripts import data_utils


from scripts.config import scale_sizes, m, material_param_delta0


def estimate_w_met2(fe_paths):
    """
    Estimate the damage and effective damage parameter.

    Parameters:
        fe_paths (tuple): Path of the SS and Vol files.

    Returns:
        w_df (dataframe): Pandas data frame with the estimation results.
    """

    # Store all the data needed for the estimation
    #  one key for each scale
    w_dict_met2 = {}

    # Store the final results
    w_list2 = []

    fe_ss_paths, fe_vol_paths = fe_paths

    for ss_path, vol_path in zip(fe_ss_paths, fe_vol_paths):

        # Computations of w:

        file_name = os.path.basename(ss_path)
        scale_size = re.findall(r"\d+", file_name)[0]

        fe_ss_df = data_utils.read_processed_data(ss_path)

        # We need to exponential because the record type is logarithmic strain
        fe_ss_df["strain_max"] = np.exp(fe_ss_df["LE_max"])
        fe_ss_df["strain_min"] = 0.1 * fe_ss_df["strain_max"]

        fe_ss_df["sigma_max"] = fe_ss_df["S_max"]

        fe_ss_df["w"] = (0.9 * fe_ss_df["strain_max"]) * fe_ss_df["sigma_max"]

        fe_ss_df.drop(["LE_max", "S_max"], axis=1, inplace=True)

        # Adding the volumne

        fe_vol_df = data_utils.read_processed_data(vol_path)

        fe_vol_df.rename(columns={"E_vol": "V"}, inplace=True)

        ss_vol_df = pd.merge(
            fe_ss_df, fe_vol_df, how="inner", on="label", validate="1:1"
        )

        # Compute w_i*V_i

        ss_vol_df["wV"] = ss_vol_df["w"] * ss_vol_df["V"]

        w_dict_met2[scale_size] = ss_vol_df

    for scale in scale_sizes:
        # Computation

        # w_effective:
        w_effective = (sum(w_dict_met2[scale].wV ** m) / sum(w_dict_met2[scale].V)) ** (
            1 / m
        )

        # average other parameters
        strain_max_avg = np.mean(w_dict_met2[scale].strain_max)
        strain_min_avg = np.mean(w_dict_met2[scale].strain_min)
        sigma_max_avg = np.mean(w_dict_met2[scale].sigma_max)
        w_avg = np.mean(w_dict_met2[scale].w)

        scale_info = [
            scale,
            strain_max_avg,
            strain_min_avg,
            sigma_max_avg,
            w_avg,
            w_effective,
        ]

        w_list2.append(scale_info)

    w_df = pd.DataFrame(
        w_list2,
        columns=[
            "scale_size",
            "strain_max_avg",
            "strain_min_avg",
            "sigma_max_avg",
            "w_avg",
            "w_effective",
        ],
    )

    return w_df


# Using methodology #5


def estimate_w_met5(fe_paths):
    """
    Estimate the damage and effective damage parameter.

    Parameters:
        fe_paths (tuple): Path of the SS and Vol files.

    Returns:
        w_df (dataframe): Pandas data frame with the estimation results.
    """

    # Store all the data needed for the estimation
    #  one key for each scale
    w_dict_met5 = {}

    # Store the final results
    w_list5 = []

    fe_ss_paths, fe_vol_paths = fe_paths

    for ss_path, vol_path in zip(fe_ss_paths, fe_vol_paths):

        # Computations of w:

        file_name = os.path.basename(ss_path)
        scale_size = re.findall(r"\d+", file_name)[0]

        fe_ss_df = data_utils.read_processed_data(ss_path)

        # We need to exponential because the record type is logarithmic strain
        fe_ss_df["strain_max"] = np.exp(fe_ss_df["LE_max"])
        fe_ss_df["strain_min"] = np.min(fe_ss_df["strain_max"])

        fe_ss_df["sigma_max"] = fe_ss_df["S_max"]
        fe_ss_df["w"] = (fe_ss_df["strain_max"] - fe_ss_df["strain_min"]) * fe_ss_df[
            "sigma_max"
        ]

        fe_ss_df.drop(["LE_max", "S_max"], axis=1, inplace=True)

        # Adding the volumne

        fe_vol_df = data_utils.read_processed_data(vol_path)

        fe_vol_df.rename(columns={"E_vol": "V"}, inplace=True)

        ss_vol_df = pd.merge(
            fe_ss_df, fe_vol_df, how="inner", on="label", validate="1:1"
        )

        # Compute w_i*V_i

        ss_vol_df["wV"] = ss_vol_df["w"] * ss_vol_df["V"]

        w_dict_met5[scale_size] = ss_vol_df

    for scale in scale_sizes:

        # Adjust w computation:
        w_dict_met5[scale]["w"] = w_dict_met5[scale]["w"] - material_param_delta0
        w_dict_met5[scale]["wV"] = w_dict_met5[scale]["w"] * w_dict_met5[scale]["V"]

        # Computation

        # w_effective:
        w_effective = (sum(w_dict_met5[scale].wV ** m) / sum(w_dict_met5[scale].V)) ** (
            1 / m
        )

        # average other parameters
        strain_max_avg = np.mean(w_dict_met5[scale].strain_max)
        strain_min_avg = np.mean(w_dict_met5[scale].strain_min)
        sigma_max_avg = np.mean(w_dict_met5[scale].sigma_max)
        w_avg = np.mean(w_dict_met5[scale].w)

        scale_info = [
            scale,
            strain_max_avg,
            strain_min_avg,
            sigma_max_avg,
            w_avg,
            w_effective,
        ]

        w_list5.append(scale_info)

    w_df = pd.DataFrame(
        w_list5,
        columns=[
            "scale_size",
            "strain_max_avg",
            "strain_min_avg",
            "sigma_max_avg",
            "w_avg",
            "w_effective",
        ],
    )

    return w_df
'''
import numpy as np
import pandas as pd
import os
import re
import math
from scripts import data_utils


def estimate_w_met1(fe_paths, C, k):
    w_list1 = []

    fe_ss_paths, _ = fe_paths

    for ss_path in fe_ss_paths:

        # Read data for each scale
        file_name = os.path.basename(ss_path)
        scale_size = re.findall(r"\d+", file_name)[0]

        fe_ss_df = data_utils.read_processed_data(ss_path)

        # We need to exponential because the record type is logarithmic strain
        strain_max = math.exp(fe_ss_df["LE_max"].max())
        strain_min = math.exp(fe_ss_df["LE_max"].min())

        # Computation of parameters
        sigma_max = fe_ss_df["S_max"].max()

        w = (strain_max - strain_min) * sigma_max
        w_effective = w

        # Computing N0_w
        N0_w = C / np.power(w_effective, k)

        scale_info = [
            scale_size,
            strain_max,
            strain_min,
            sigma_max,
            w,
            w_effective,
            N0_w,
        ]

        w_list1.append(scale_info)

    w_df = pd.DataFrame(
        w_list1,
        columns=[
            "scale_size",
            "strain_max",
            "strain_min",
            "sigma_max",
            "w",
            "w_effective",
            "N0_w",
        ],
    )

    return w_df


def estimate_w_met2(fe_paths, m, c, k, scale_sizes, strain_ratio=0.1):
    """
    Estimate the damage and effective damage parameter.

    Parameters:
        fe_paths (tuple): Path of the SS and Vol files.

    Returns:
        w_df (dataframe): Pandas data frame with the estimation results.
    """

    # Store all the data needed for the estimation
    #  one key for each scale
    w_dict_met2 = {}

    # Store the final results
    w_list2 = []

    fe_ss_paths, fe_vol_paths = fe_paths

    for ss_path, vol_path in zip(fe_ss_paths, fe_vol_paths):

        # Computations of w:

        file_name = os.path.basename(ss_path)
        scale_size = re.findall(r"\d+", file_name)[0]

        fe_ss_df = data_utils.read_processed_data(ss_path)

        # We need to exponential because the record type is logarithmic strain
        # fe_ss_df["strain_max"] = np.exp(fe_ss_df["LE_max"])
        # fe_ss_df["strain_max"] = np.power(10, fe_ss_df["LE_max"])
        fe_ss_df["strain_max"] = fe_ss_df["LE_max"]
        fe_ss_df["strain_min"] = strain_ratio * fe_ss_df["strain_max"]

        fe_ss_df["sigma_max"] = fe_ss_df["S_max"]

        fe_ss_df["w"] = ((1 - strain_ratio) * fe_ss_df["strain_max"]) * fe_ss_df[
            "sigma_max"
        ]

        fe_ss_df.drop(["LE_max", "S_max"], axis=1, inplace=True)

        # Adding the volumne

        fe_vol_df = data_utils.read_processed_data(vol_path)

        fe_vol_df.rename(columns={"E_vol": "V"}, inplace=True)

        ss_vol_df = pd.merge(
            fe_ss_df, fe_vol_df, how="inner", on="label", validate="1:1"
        )

        # Compute w_i*V_i

        ss_vol_df["wV"] = ss_vol_df["w"] * ss_vol_df["V"]

        w_dict_met2[scale_size] = ss_vol_df

    for scale in scale_sizes:
        # Computation

        # w_effective:
        w_effective = (sum(w_dict_met2[scale].wV ** m) / sum(w_dict_met2[scale].V)) ** (
            1 / m
        )

        # average other parameters
        strain_max_avg = np.mean(w_dict_met2[scale].strain_max)
        strain_min_avg = np.mean(w_dict_met2[scale].strain_min)
        sigma_max_avg = np.mean(w_dict_met2[scale].sigma_max)
        w_avg = np.mean(w_dict_met2[scale].w)

        # Computing N0_w
        N0_w = c / np.power(w_effective, k)

        scale_info = [
            scale,
            strain_max_avg,
            strain_min_avg,
            sigma_max_avg,
            w_avg,
            w_effective,
            N0_w,
        ]

        w_list2.append(scale_info)

    w_df = pd.DataFrame(
        w_list2,
        columns=[
            "scale_size",
            "strain_max_avg",
            "strain_min_avg",
            "sigma_max_avg",
            "w_avg",
            "w_effective",
            "N0_w",
        ],
    )

    return w_df


# Using methodology 3


def estimate_w_met3(fe_paths, m, C, k, scale_sizes, material_param_delta0):

    # Create a data frame with the info of each scale size

    w_dict_met3 = {}
    w_list3 = []

    fe_ss_paths, fe_vol_paths = fe_paths

    for ss_path, vol_path in zip(fe_ss_paths, fe_vol_paths):

        # Computations of w:

        file_name = os.path.basename(ss_path)
        scale_size = re.findall(r"\d+", file_name)[0]

        fe_ss_df = data_utils.read_processed_data(ss_path)

        # We need to exponential because the record type is logarithmic strain
        fe_ss_df["strain_max"] = np.exp(fe_ss_df["LE_max"])
        fe_ss_df["strain_min"] = np.min(fe_ss_df["strain_max"])

        fe_ss_df["sigma_max"] = fe_ss_df["S_max"]
        fe_ss_df["w"] = (fe_ss_df["strain_max"] - fe_ss_df["strain_min"]) * fe_ss_df[
            "sigma_max"
        ]

        fe_ss_df.drop(["LE_max", "S_max"], axis=1, inplace=True)

        # Adding the volumne

        fe_vol_df = data_utils.read_processed_data(vol_path)

        fe_vol_df.rename(columns={"E_vol": "V"}, inplace=True)

        ss_vol_df = pd.merge(
            fe_ss_df, fe_vol_df, how="inner", on="label", validate="1:1"
        )

        # Compute w_i*V_i

        ss_vol_df["wV"] = ss_vol_df["w"] * ss_vol_df["V"]

        w_dict_met3[scale_size] = ss_vol_df

    for scale in scale_sizes:

        # Adjust w computation:
        w_dict_met3[scale]["w"] = w_dict_met3[scale]["w"] - material_param_delta0
        w_dict_met3[scale]["wV"] = w_dict_met3[scale]["w"] * w_dict_met3[scale]["V"]

        # Computation

        # w_effective:
        w_effective = (sum(w_dict_met3[scale].wV ** m) / sum(w_dict_met3[scale].V)) ** (
            1 / m
        )

        # average other parameters
        strain_max_avg = np.mean(w_dict_met3[scale].strain_max)
        strain_min_avg = np.mean(w_dict_met3[scale].strain_min)
        sigma_max_avg = np.mean(w_dict_met3[scale].sigma_max)
        w_avg = np.mean(w_dict_met3[scale].w)

        # Computing N0_w
        N0_w = C / np.power(w_effective, k)

        scale_info = [
            scale,
            strain_max_avg,
            strain_min_avg,
            sigma_max_avg,
            w_avg,
            w_effective,
            N0_w,
        ]

        w_list3.append(scale_info)

    w_df = pd.DataFrame(
        w_list3,
        columns=[
            "scale_size",
            "strain_max_avg",
            "strain_min_avg",
            "sigma_max_avg",
            "w_avg",
            "w_effective",
            "N0_w",
        ],
    )

    return w_df


# Using methodology #4


def estimate_w_met4(fe_paths, C, k, material_param_delta0):

    w_df4 = estimate_w_met1(fe_paths, C, k)
    w_df4["w"] = w_df4["w"] - material_param_delta0
    w_df4["w_effective"] = w_df4["w"]
    w_df4["N0_w"] = C / np.power(w_df4["w_effective"], k)

    return w_df4


# Using methodology #5


def estimate_w_met5(fe_paths, m, c, k, scale_sizes, material_param_delta0):
    """
    Estimate the damage and effective damage parameter.

    Parameters:
        fe_paths (tuple): Path of the SS and Vol files.

    Returns:
        w_df (dataframe): Pandas data frame with the estimation results.
    """

    # Store all the data needed for the estimation
    #  one key for each scale
    w_dict_met5 = {}

    # Store the final results
    w_list5 = []

    fe_ss_paths, fe_vol_paths = fe_paths

    for ss_path, vol_path in zip(fe_ss_paths, fe_vol_paths):

        # Computations of w:

        file_name = os.path.basename(ss_path)
        scale_size = re.findall(r"\d+", file_name)[0]

        fe_ss_df = data_utils.read_processed_data(ss_path)

        # We need to exponential because the record type is logarithmic strain
        fe_ss_df["strain_max"] = np.exp(fe_ss_df["LE_max"])
        fe_ss_df["strain_min"] = np.min(fe_ss_df["strain_max"])

        fe_ss_df["sigma_max"] = fe_ss_df["S_max"]
        fe_ss_df["w"] = (fe_ss_df["strain_max"] - fe_ss_df["strain_min"]) * fe_ss_df[
            "sigma_max"
        ]

        fe_ss_df.drop(["LE_max", "S_max"], axis=1, inplace=True)

        # Adding the volumne

        fe_vol_df = data_utils.read_processed_data(vol_path)

        fe_vol_df.rename(columns={"E_vol": "V"}, inplace=True)

        ss_vol_df = pd.merge(
            fe_ss_df, fe_vol_df, how="inner", on="label", validate="1:1"
        )

        # Compute w_i*V_i

        ss_vol_df["wV"] = ss_vol_df["w"] * ss_vol_df["V"]

        w_dict_met5[scale_size] = ss_vol_df

    for scale in scale_sizes:

        # Adjust w computation:
        w_dict_met5[scale]["w"] = w_dict_met5[scale]["w"] - material_param_delta0
        w_dict_met5[scale]["wV"] = w_dict_met5[scale]["w"] * w_dict_met5[scale]["V"]

        # Computation

        # w_effective:
        w_effective = (sum(w_dict_met5[scale].wV ** m) / sum(w_dict_met5[scale].V)) ** (
            1 / m
        )

        # average other parameters
        strain_max_avg = np.mean(w_dict_met5[scale].strain_max)
        strain_min_avg = np.mean(w_dict_met5[scale].strain_min)
        sigma_max_avg = np.mean(w_dict_met5[scale].sigma_max)
        w_avg = np.mean(w_dict_met5[scale].w)

        # Computing N0_w
        N0_w = c / np.power(w_effective, k)

        scale_info = [
            scale,
            strain_max_avg,
            strain_min_avg,
            sigma_max_avg,
            w_avg,
            w_effective,
            N0_w,
        ]

        w_list5.append(scale_info)

    w_df = pd.DataFrame(
        w_list5,
        columns=[
            "scale_size",
            "strain_max_avg",
            "strain_min_avg",
            "sigma_max_avg",
            "w_avg",
            "w_effective",
            "N0_w",
        ],
    )

    return w_df


if __name__ == "__main__":
    from config import m, material_param_delta0, C, k, scale_sizes, PROCESSED_DATA_PATH,BASE_PATH

    FE_paths, EXP_paths = data_utils.get_paths()
    _, fe_processed_paths = FE_paths

    fe_vol_paths = [v_path for v_path in fe_processed_paths if "_Vol" in v_path]
    fe_ss_paths = [s_path for s_path in fe_processed_paths if "_SS" in s_path]
    fe_paths = (fe_ss_paths, fe_vol_paths)

    # Method 1:
    w_df1 = estimate_w_met1(fe_paths, C, k)
    # Method 2:
    w_df2 = estimate_w_met2(fe_paths, m, C, k, scale_sizes, strain_ratio=0.1)
    # Method 3:
    w_df3 = estimate_w_met5(fe_paths, m, C, k, scale_sizes, material_param_delta0)
    # Method 4:
    w_df4 = estimate_w_met5(fe_paths, m, C, k, scale_sizes, material_param_delta0)
    # Method 5:
    w_df5 = estimate_w_met5(fe_paths, m, C, k, scale_sizes, material_param_delta0)

    # Saving the results
    output_results_path = os.path.sep.join(
        [BASE_PATH+"/processed", "parameters", "damage_parameter"]
    )

    print("[INFO]: *Saving Results: ", output_results_path + "/met_1.csv")
    w_df1.to_csv(os.path.join(output_results_path, "met_1.csv"), index=None)
    print("[INFO]: *Saving Results: ", output_results_path + "/met_2.csv")
    w_df2.to_csv(os.path.join(output_results_path, "met_2.csv"), index=None)
    print("[INFO]: *Saving Results: ", output_results_path + "/met_3.csv")
    w_df3.to_csv(os.path.join(output_results_path, "met_3.csv"), index=None)
    print("[INFO]: *Saving Results: ", output_results_path + "/met_4.csv")
    w_df4.to_csv(os.path.join(output_results_path, "met_4.csv"), index=None)
    print("[INFO]: *Saving Results: ", output_results_path + "/met_5.csv")
    w_df5.to_csv(os.path.join(output_results_path, "met_5.csv"), index=None)
