def experimental_df(gamma_dict, observed_fn):
    import numpy as np
    import os
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    # from scripts import config
    import plotly.express as px

    import plotly.express as px
    import streamlit as st
    # imports: to plug in :

    # gamma dict: gamma parameter is obtained from the microscrack lenght ratio: params to work on in the next steps with more

    #gamma_dict = {'40%': [1.74, 1],
    #              '60%': [2.78, 1.60],
    #              '80%': [3.86, 2.21],
    #              '100%': [6.63, 2.89]}

    # import bn from bayesian calibration


    # observed Nf: to be imported from experimental data script

    # observed_Nf = [10275, 19773, 50119, 171907, 5196, 25347, 50573, 100453, 11348, 12533, 15287, 135323, 17504, 19773,
    #               35562, 38922, 42793, 50119, 55855, 69058, 78364, 101364]
    # config.observed_Nf
    Nf_axis = np.linspace(start=10.e3, stop=10.e5, num=1000)
    # gamma>0 cause gamma = ln(af/ai) with af: final crack length and ai: initial crack length
    # in theory gamma can be <1 but in practice maybe need a higher ratio: make gamma begin at 0.95 to see

    gamma_axis = np.linspace(start=0.95, stop=8, num=1000)
    gamma_array = [i[0] for i in gamma_dict.values()]
    # N0_w : characteristic fatigue life, is a function of the damage parameter:
    N0_w_axis = np.linspace(start=20000, stop=100000, num=1000)


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


    def failure_surface(gamma, N0_w, Nf, bn):
        # 1 axis is Nf, then you can choose tp plot against either a range of gamma, or a range of N0_w: same formula
        """

        :param gamma:
        :param N0_w:
        :param Nf:
        :param bn:
        :return:
        """
        a1 = 1 / (gamma * N0_w)

        return 1 - np.exp(-np.outer(Nf, a1) ** bn)

    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))

    def twoD_array():
        pf_100 = failure_proba(gamma=gamma_dict['100%'][0], N0_w=79000, Nf=Nf_axis, bn=1.443)
        pf_80 = failure_proba(gamma=gamma_dict['80%'][0], N0_w=79000, Nf=Nf_axis, bn=1.443)
        pf_60 = failure_proba(gamma=gamma_dict['60%'][0], N0_w=79000, Nf=Nf_axis, bn=1.443)
        pf_40 = failure_proba(gamma=gamma_dict['40%'][0], N0_w=79000, Nf=Nf_axis, bn=1.443)

        plt.plot(Nf_axis, pf_40, Nf_axis, pf_60, Nf_axis, pf_80, Nf_axis, pf_100)
        plt.xlim(1.e3, 1.e6)
        plt.ylim(0, 1.05)
        plt.legend(["Pf 40%", "Pf 60%", "Pf 80%", "Pf 100%"])
        plt.xlabel('Number of cycles in millions')
        #plt.show()
        plt.savefig(BASE_PATH+"/twoD.png")



    def threeD_array():
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        print(gamma_dict['100%'][0])
        # try with N0_w
        # X, Y = np.meshgrid(Nf_axis, N0_w_axis)
        # againt gamma:
        X, Y = np.meshgrid(gamma_axis, Nf_axis)
        pf_100 = failure_surface(gamma=gamma_axis, N0_w=79000, Nf=Nf_axis, bn=1.443)

        surface = ax.plot_surface(X, Y, pf_100, cmap=cm.summer,
                                  linewidth=0, antialiased=False)
        ax.set_zlim(0, 1.1)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter('{x:.02f}')
        fig.colorbar(surface, shrink=0.5, aspect=5)

        #plt.show()

        plt.savefig(BASE_PATH+"/threeD.png")

    return plt


#if __name__ == "__main__":
#    twoD_array()
#    threeD_array()
