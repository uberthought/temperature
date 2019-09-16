#!/usr/bin/python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time
from datetime import datetime, timedelta

import csv

import numpy as np

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(id='time-div', style={'font-size': '75px', 'text-align': 'center'}),
    html.Div(id='temperature-div', style={'font-size': '75px', 'text-align': 'center'}),
    dcc.Graph(id='example-graph', style={'height': '300px'}),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=1)
])

@app.callback(
    dash.dependencies.Output(component_id='time-div', component_property='children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_time_div(n_intervals):
    return str(datetime.now().strftime('%-I:%M%p'))

@app.callback(
    dash.dependencies.Output(component_id='temperature-div', component_property='children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_temperature_div(n_intervals):
    with open('/home/pi/temperature/temperature.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        row = list(reader)[-1]
        temperature0 = float(row[1])
        temperature0 = temperature0 * 1.8 + 32

    return '{0:.1f}'.format(temperature0) + 'F'

@app.callback(
    dash.dependencies.Output(component_id='example-graph', component_property='figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph(n_intervals):

    with open('/home/pi/temperature/temperature.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        oldest = str(datetime.now() - timedelta(days=7))

        timestamps = []
        temperatures = []
        last_temperature = 0

        for row in reader:
            try:
                timestamp = row[0]
                temperature = float(row[1])

                if timestamp < oldest:
                    continue
                if abs(last_temperature - temperature) > 50:
                    continue
                if abs(temperature) > 1.0 and abs(last_temperature + temperature) < 0.2:
                    continue

                last_temperature = temperature

                timestamps.append(timestamp)
                temperatures.append(temperature * 1.8 + 32)
            except ValueError:
                continue

#        l = 20
#        box = np.ones(l)/l
#        temperatures = np.convolve(temperatures, box, mode='valid')
#        timestamps = timestamps[l:]
        
    return {
        'data': [
            go.Scatter(x = timestamps, y = temperatures, name = 'temperature', yaxis='y1', line = dict(color='black')),
        ],
        'layout': go.Layout(yaxis=dict(title='temperature'))
    }

if __name__ == '__main__':
    app.run_server(debug=False, host='192.168.1.189')
