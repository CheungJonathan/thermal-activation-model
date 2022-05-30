import numpy as np
import pandas as pd
from lmfit import Model, Parameters
import plotly.graph_objects as go

class hysteresis_model:
    def __init__(self,current,hall_voltage,read_current):
        
        self.current = current
        self.hall_voltage = hall_voltage/read_current
        self.m = 3
        self.n = 3

        self.a = np.linspace(-np.pi/2,np.pi*3/2,len(self.current))
        
        self.b_x = max(self.current)
        self.b_y = (max(self.hall_voltage)-min(self.hall_voltage))/2 

    def x_function(self,a,b_x):
        return b_x*np.sin(a)

    def y_function(self,a,a_data,b_y,c):
        extra = -np.power(a_data,self.n)*np.power(self.b_x,self.m-self.n)/(np.power(self.b_x*self.b_x-a_data*a_data,self.m/2))
        return 2*b_y*(np.heaviside(extra*np.power(np.cos(a),self.m)+np.power(np.sin(a),self.n),1)-0.5) + c

    
    def process(self):
        std_all = []
        test = Model(self.y_function)

        for i in range(100):
            a_data = self.b_x * 0.01 * (i+1)

            if a_data < self.b_x:

                params = Parameters()
                # params.add('x', value=0)
                params.add('a_data', value=a_data,min=0, max=self.b_x)
                params.add('b_y', value=self.b_y)
                params.add('c', value=self.b_y)

                result = test.fit(np.float32(self.hall_voltage),params,a=self.a,method='least_squares')
                std_all.append(np.std(self.hall_voltage-result.best_fit))

        self.a_percentage = std_all.index(min(std_all))+1

        std_all = []
        for i in range(500,2000,1):

            test = Model(self.y_function)

            a_data = self.b_x * 0.01 * self.a_percentage

            params = Parameters()

            ini_a = np.float32(self.a*0.001*i)
            # params.add('x', value=0)
            params.add('a_data', value=a_data,min=0, max=self.b_x)
            params.add('b_y', value=self.b_y)
            params.add('c', value=self.b_y)

            result = test.fit(np.float32(self.hall_voltage),params,a=ini_a,method='least_squares')
            std_all.append(np.std(self.hall_voltage-result.best_fit))

        self.x_delay = std_all.index(min(std_all))+500
        
    def final_fit (self):
        test = Model(self.y_function)

        a_data = self.b_x * 0.01 * self.a_percentage

        params = Parameters()

        ini_a = np.float32(self.a*0.001*self.x_delay)

        # params.add('x', value=0)
        params.add('a_data', value=a_data,min=0, max=self.b_x) 
        params.add('b_y', value=self.b_y)
        params.add('c', value=self.b_y)

        result = test.fit(np.float32(self.hall_voltage),params,a=ini_a,method='least_squares')
        print(result.fit_report())
        self.best_fit = result.best_fit
        return self.best_fit
    
    def analyse(self):

        switching_point = []
        for i in range(len(self.best_fit)-1):
            data = self.best_fit[i+1]-self.best_fit[i]
            if data != 0:
                self.switching_point.append(i)
        coresisty = (np.abs(self.current[self.switching_point[1]])+np.abs(self.current[self.switching_point[0]]))/2
        return coresisty, switching_point



        