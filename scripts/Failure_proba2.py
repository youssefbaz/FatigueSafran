import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import pandas as pd
from scripts import data_utils
import os

# in windows if we want to save fig 
#pio.kaleido.scope.mathjax = None or Downgrad kaleido
def calculate_failure(gamma):
    # from Experimental_data_safran import experimental_df
    _, EXP_paths = data_utils.get_paths()
    _, expmtl_processed_paths = EXP_paths
    # Test_results_different_scales_CHP.txt
    print("exp:", expmtl_processed_paths, EXP_paths)
    #if not expmtl_processed_paths:
    #    return False, "no processed files found. have runned the steps before ?"

    experimental_df = data_utils.read_processed_data(expmtl_processed_paths[0])


    # print(experimental_df)

    # import experimental data
    dfs = [x for _, x in experimental_df.groupby('Specimen')]
    nfs = [sorted([*i['LCF']]) for i in dfs]


    # sort the Nf life from shortest to longest:
    Pf_experimental = pd.DataFrame(data=list(np.concatenate(nfs).flat), columns=["LCF"])
    Pf_experimental["Specimen"] = experimental_df["Specimen"]

    # from Bayesian_inference2.0 import bn_mean
    bn_mean = 1.45

    # gamma and N0_w parameter: coming from damage parameter calculation
    # version interpolating the value for 60%
    gamma_dict = {'100%': [6.63, 73475],
                  '80%': [3.86, 88986],
                  '60%': [2.78, 112400],
                  '40%': [1.74, 146151]}

    # gamma dict with N0_w obtained from damage parameter with the raw value for 60%: extreme value to be questioned
    gamma_dict_raw = {'100%': [6.63, 73475],
                      '80%': [3.86, 88986],
                      '60%': [2.78, 573302],
                      '40%': [1.74, 146151]}

    # gamma dict with N0_w obtained with the log method
    gamma_dict_exp = {'100%': [6.63, 1207.382681482064],
                      '80%': [3.86, 1248.88990432624],
                      '60%': [2.78, 1287.2670811429887],
                      '40%': [1.74, 1378.0689937821892]}

    # observed_Nf = [10275, 19773, 50119, 171907, 5196, 25347, 50573, 100453, 11348, 12533, 15287, 135323, 17504, 19773,35562, 38922, 42793, 50119, 55855, 69058, 78364, 101364]

    observed_Nf = [*experimental_df["LCF"]]

    # axis for the graphs: number of cycles
    Nf_axis = np.linspace(start=1000, stop=1500000, num=1000)

    # secondary axis for surface graphs representing the stress level / damage parameter:

    N0_w_axis = np.linspace(start=20000, stop=150000, num=1000)


    def failure_proba(gamma, N0_w, Nf, bn):
        """
        Cumulative Probability formula for a Weibull variable : here x = Nf/(gamma*N0_w), function of Nf.
        Formula is coded manually to account for these parameters : N0_w and gamma that modify the standard Weibull
        :param gamma: parameter acknoledging for size effect ( derived from microcrack length ratio), scalar
        :param N0_w: effective number of cycle as a function of the damage parameter, accounts for the stress level, scalar
        :param Nf: nb of cycles: np array
        :param bn: Weibull shape parameter, scalar
        :return: a cumulative probability distribution between 0 and 1
        """
        assert isinstance(bn, float), "Bn must be a scalar value"
        assert bn > 0, "Bn parameter must be positive"
        assert isinstance(Nf, np.ndarray), "Nf must be of type: numpy array"
        assert gamma > 0, "Gamma parameter must be positive"
        return 1 - np.exp(-(Nf / (gamma * N0_w)) ** bn)


    def exp_proba(size=40):
        df = experimental_df.copy()
        df = df.loc[df["Specimen"] == size]
        n = len(df)
        df["Exp_proba"] = [(i - 0.3) / (n + 0.4) for i in range(1, n + 1)]
        df = df[["LCF", "Exp_proba"]]
        return df


    # make the reference proba df for 2D: code to be refined, quick code

    pf = np.array([failure_proba(gamma=gamma_dict[i][0],
                                 N0_w=gamma_dict[i][1],
                                 Nf=Nf_axis, bn=bn_mean) for i in gamma_dict.keys()])
    df_pf = pd.DataFrame(data=pf.T, columns=["Pf_100", "Pf_80", "Pf_60", "Pf_40"])
    df_pf.index = Nf_axis


    def failure_surface(gamma, N0_w, Nf, bn):
        a1 = 1 / (gamma * N0_w)
        return 1 - np.exp(-np.outer(Nf, a1) ** bn)


    def threeD_array(gamma):
        # specify the gamma among the reference gamma dict
        z_data = failure_surface(gamma=gamma, N0_w=N0_w_axis, Nf=Nf_axis, bn=bn_mean)
        fig = go.Figure(data=[go.Surface(x=N0_w_axis, y=Nf_axis, z=z_data, colorscale="earth")])
        fig.update_layout(title="Failure Probability Surface for gamma = {:.2f}".format(gamma), autosize=False,
                          width=600, height=600, margin=dict(l=90, r=70, b=90, t=120),
                          scene=dict(yaxis=dict(dtick=1, type='log')))
        fig.update_xaxes(title_text="Number of cycles in logarithmic scale", type="log")
        fig.update_yaxes(title_text="Damage parameter through N0(w)")
        #fig.show()
        return fig
        # plt.savefig(config.IMAGES_PATH + "/threeD-new.png")

    def twoD_array():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Nf_axis, y=df_pf["Pf_40"], mode='lines', name='40%', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=Nf_axis, y=df_pf["Pf_60"], mode='lines', name='60%', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=Nf_axis, y=df_pf["Pf_80"], mode='lines', name='80%', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=Nf_axis, y=df_pf["Pf_100"], mode='lines', name='100%', line=dict(color='red')))
        ep_40 = exp_proba()
        ep_60 = exp_proba(60)
        ep_80 = exp_proba(80)
        ep_100 = exp_proba(100)
        fig.add_trace(
            go.Scatter(x=ep_40["LCF"], y=ep_40["Exp_proba"], mode='markers', name="exp_40%", marker=dict(color='green')))
        fig.add_trace(
            go.Scatter(x=ep_60["LCF"], y=ep_60["Exp_proba"], mode='markers', name="exp_60%", marker=dict(color='blue')))
        fig.add_trace(
            go.Scatter(x=ep_80["LCF"], y=ep_80["Exp_proba"], mode='markers', name="exp_80%", marker=dict(color='orange')))
        fig.add_trace(
            go.Scatter(x=ep_100["LCF"], y=ep_100["Exp_proba"], mode='markers', name="exp_100%", marker=dict(color='red')))
        fig.update_xaxes(title_text="Number of cycles in logarithmic scale", type="log")
        fig.update_yaxes(showline=True, gridcolor='grey', linewidth=0.1)
        fig.update_layout(plot_bgcolor="white", title="Failure probability for different gamma sizes")
       # fig.show()
        return fig

        # plt.savefig(config.IMAGES_PATH + "/twoD-test-sauv.png")
        # fig.write_image(config.IMAGES_PATH + "/twoDtiiuet.png")
        print('done')
    return (twoD_array(),threeD_array(gamma))
if __name__ == "__main__":
    # gamma for the 3D array graph should be imported from the user input page
    calculate_failure(1.75)







