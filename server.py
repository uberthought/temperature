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
    html.Div(id='text-div', style={'font-size': '75px', 'text-align': 'center'}),
    dcc.Graph(id='temperature-graph', style={'height': '400px'}),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=1)
])

@app.callback(
    dash.dependencies.Output(component_id='text-div', component_property='children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_time_div(n_intervals):
    time = str(datetime.now().strftime('%-I:%M%p'))

    with open('/home/pi/temperature/temperature.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            try:
                temperature0 = float(row[2])
                temperature1 = float(row[1])
            except ValueError:
                continue
        temperature0 = temperature0 * 1.8 + 32
        temperature1 = temperature1 * 1.8 + 32

    temperature0 = '{0:.1f}'.format(temperature0)
    temperature1 = '{0:.1f}'.format(temperature1)

    return '{} {}/{}F'.format(time, temperature0, temperature1)

@app.callback(
    dash.dependencies.Output(component_id='temperature-graph', component_property='figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph(n_intervals):

    with open('/home/pi/temperature/temperature.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        oldest = str(datetime.now() - timedelta(days=7))

        timestamps = []
        temperature0s = []
        temperature1s = []

        for row in reader:
            try:
                timestamp = row[0]
                temperature0 = float(row[2])
                temperature1 = float(row[1])

                if timestamp < oldest:
                    continue

                timestamps.append(timestamp)
                temperature0s.append(temperature0 * 1.8 + 32)
                temperature1s.append(temperature1 * 1.8 + 32)
            except ValueError:
                continue

        #l = 9
        #box = np.ones(l)/l
        #temperatures = np.convolve(temperatures, box, mode='valid')
        #timestamps = timestamps[l:]
        
    return {
        'data': [
            go.Scatter(x = timestamps, y = temperature1s, name = 'fridge', line = dict(color='gray')),
            go.Scatter(x = timestamps, y = temperature0s, name = 'freezer', line = dict(color='black')),
        ],
        'layout': go.Layout(yaxis=dict(title='temperature'))
    }

if __name__ == '__main__':
    app.run_server(debug=False, host='192.168.1.189')
