import numpy as np
import pandas as pd
from lmfit import Model, Parameters
import plotly.express as px


'''
J_c : the known parameter that record from the data
J_0 : the parameter that we want to find
delta : (∆) themral satability
t : the pulse width

J_c = J_0 * (1- 1/∆ * exp(t * 1ns))

what we have is the J_c and t, trying to fit the data of J_0 and ∆
'''
duration = np.float64([3e-4,5e-4,7e-4,9e-4,1e-3,2e-3,4e-3,8e-3,10e-3,20e-3,50e-3])

def thermal_activation_equation(t_pulse,J_0,delta):
    return J_0*(1-1/delta*np.log(1e9*t_pulse))


class thermal_activation_model:
    def __init__(self,duration,J_c):

        test = Model(thermal_activation_equation)
        params = Parameters()
        params.add('J_0', value=1e-3)
        params.add('delta', value=30)

        self.result = test.fit(J_c,params,t_pulse = duration)
    
    def fitting(self):
        return self.result.best_fit
    
    def fit_params(self):
        return self.result.params

    def fit_J_0(self):
        return self.result.params['J_0'].value

    def fit_delta(self):
        return self.result.params['delta'].value