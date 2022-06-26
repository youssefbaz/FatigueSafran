import numpy as np
import pymc3 as pm
import arviz as az
import os

az.rcParams["plot.matplotlib.show"] = True
from scipy.stats import norm, kstest, ks_2samp
import scipy.stats as stats
import matplotlib.pyplot as plt
from scripts import config
#import config
#import met


## input data:

# 1st option: plug it to the other script
# Bn initialization values are taken from the Experimental_data script:
# from Experimental_data_safran import Bn_positive, Bn_positive_mean, Bn_positive_std
# bn_init = Bn_positive_mean
# bn_std_init = Bn_positive_std
# otherwise take as constant:
config.RANDOM_SEED
# DIFFERENTIATE INITIAL BN FROM EXP DATA IN THE LIKELIHOOD AND THE BN IN THE PRIOR WHICH AR HE BELIEFS
# Constants (to put as parameters later on)
def m_weibull_logp(bn, gamma, sigma, sigma_eps, N0_w, Nf_list):
    t = len(Nf_list)
    nf0 = N0_w * (np.log(2) ** (1 / bn)) / gamma
    return (1 / (((2 * np.pi) ** (t / 2)) * sigma_eps ** t)) * np.exp(
        -1 / (2 * sigma ** 2) * sum([(np.log(i) - np.log(nf0)) ** 2 for i in Nf_list]))

def checkN0_w(N0_w,gamma):
#    print("got", gamma,config.gamma_dict[gamma], type(config.gamma_dict[gamma]), type(N0_w))
 #   if round(N0_w, 3) == round(config.gamma_dict[gamma], 3):
  #      print("N0_w is aligned with the given values of gamma")
    return round(N0_w, 3) == round(config.gamma_dict[gamma], 3)

class Modified_Weibull(pm.Continuous):
    def __init__(self, bn, **likelihood_params):
        super().__init__()
        self.bn = bn
        self.mode = bn
        self.likelihood_params
        for key, value in likelihood_params.items():
            setattr(self, key, value)

    def logp(self, value=0):
        bn = self.bn
        return m_weibull_logp(bn - value, **self.likelihood_params)

class FatigueLife_BayesianCalibration:
    def __init__(self, sample_size, observations, bn_init_values, step_method=None, seed=config.RANDOM_SEED,
                 **likelihood_params):
        self.sample_size = sample_size
        self.seed = seed
        self.observations = observations
        self.bn_init_mean = bn_init_values[0]
        self.bn_init_std = bn_init_values[1]
        self.step_method = step_method
        for key, value in likelihood_params.items():
            setattr(self, key, value)
        # self.inference_data = self.get_posterior_samples()

    def get_posterior_samples_and_fig(self):
        with pm.Model() as m:
            bn = pm.TruncatedNormal("bn", mu=config.bn_priors[0], sigma=config.bn_priors[1], lower=0.001)
            #likelihood_bn = Modified_Weibull("slope", bn=bn,
            #                                 **likelihood_params,
            #                                 observed=self.observations)
            if self.step_method == "Metropolis":
                step = pm.Metropolis()
                idata = pm.sample(self.sample_size, cores=4, step=step, chains=2)
            else:
                idata = pm.sample(self.sample_size, cores=4,
                                  chains=2)  # automatic determination of the step by the model
            s = az.summary(idata)
            print(s)

            trace = az.plot_trace(idata)
            fig_trace = trace.ravel()[0].figure
            posterior = az.plot_posterior(idata)

            fig_trace.savefig(config.IMAGES_PATH+"/image_trace.png")
            #fig_posterior.savefig(BASE_PATH+"/image_posterior.png")
            posterior.figure.savefig(config.IMAGES_PATH+"/image_posterior.png")
            #az.plot_trace(idata)
            #az.plot_posterior(idata)
            return idata, s, fig_trace, posterior.figure

def calculate_bayesian(settings):
    #N0_w=948.22
    print("calculate bayesian using ", config.met)
    if not config.met:
        print(" empry met, try reloading")
        config.get_met()
    N0_w = config.met['40']
    print(N0_w)
    print('calculate_bayesian')
    print(settings)
    # checkN0_w(N0_w, settings['gamma'])
    likelihood_params = {
        'gamma': settings['gamma'],
        'sigma': settings['bn_std'],
        'sigma_eps': config.sigma_eps,
        'N0_w': N0_w,
        'Nf_list': config.Nf_list,
        'observed_Nf': config.observed_Nf
    }

    A, s, fig_trace, fig_posterior = FatigueLife_BayesianCalibration(sample_size=5000, step="Metropolis", observations=config.observed_Nf,
                                           bn_init_values=[settings['bn_mean'],settings['bn_std']]).get_posterior_samples_and_fig()

    x = A["bn"]

    # define scoring for bn normality:
    # define a normal distribution to compare with
    normal = norm(loc=config.bn_priors[0], scale=config.bn_priors[1])
    norm_rvs = normal.rvs(size=5000, random_state=config.RANDOM_SEED)
    norm_rvs = norm_rvs[norm_rvs > 0]

    # Use the Kolmogorov Smirnov test from scipy, using the 2 sample formula (as the normal rvs is not the standard normal)
    # The sample size is really big for this method: even when we use the "asymp" mode, so we split the sample into bits and look at the K stat and p value
    # sample being huge the p value ends up being ridiculously small even for distribution that are really close to each other (size increases the nb of discrepencies
    # and to be able to understand such a p value we should compare it with an also ridculously small probability:

    l = np.arange(start=1, stop=5000, step=180)
    k = []
    for i in range(len(l) - 1):
        k.append(ks_2samp(x[l[i]:l[i + 1]], norm_rvs[l[i]:l[i + 1]], alternative="two-sided", mode="asymp")[1])
    print(k)
    print(np.average(k))
    k_ = np.array(k)
    print(len(k))
    print(len(k_[k_ < 0.005]))

    return fig_trace, fig_posterior

#if __name__=="__main__":
#    calculate_bayesian()

