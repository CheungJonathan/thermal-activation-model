
import time
from turtle import xcor
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
 
file_name = 'analy_c_pulse_channel_22.csv'
fig = go.Figure()
df = pd.read_csv(file_name)
x = [3e-4,5e-4,7e-4,9e-4,1e-3,2e-3,4e-3,8e-3,10e-3,20e-3,50e-3]
y_1 = df['point_1']
y_2 = df['point_1']

fig = px.scatter( x=x, y=y_1,log_x=True)
# fig.add_trace(go.Scatter(x=x,y=y_1,mode ='markers+lines',log_x = True))

fig.update_layout(
        template="simple_white",
        plot_bgcolor='white',
        xaxis_title='Pulse duration (s)',
        yaxis_title='Critical current (A)',
        font=dict(
        size=18,
        color="RebeccaPurple"))
        
fig.show()