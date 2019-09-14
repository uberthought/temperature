#!/usr/bin/python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import time
from datetime import datetime

import csv

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Button('Refresh', id='refresh'),
    html.Div(id='time-div', style={'font-size': '125px', 'text-align': 'center'}),
    html.Div(id='date-div', style={'font-size': '50px', 'text-align': 'center'}),
    html.Div(id='temperature-div', style={'font-size': '125px', 'text-align': 'center'}),
    dcc.Graph(id='example-graph'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=1)
])

@app.callback(
    dash.dependencies.Output(component_id='time-div', component_property='children'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('refresh', 'n_clicks')])
def update_time_div(n_intervals, n_clicks):
    return str(datetime.now().strftime('%-I:%M%p'))

@app.callback(
    dash.dependencies.Output(component_id='date-div', component_property='children'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('refresh', 'n_clicks')])
def update_date_div(n_intervals, n_clicks):
    return str(datetime.now().strftime('%b %d %Y'))

@app.callback(
    dash.dependencies.Output(component_id='temperature-div', component_property='children'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('refresh', 'n_clicks')])
def update_temperature_div(n_intervals, n_clicks):
    with open('temperature.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        row = list(reader)[-1]
        temperature0 = float(row[1])
        humidity0 = float(row[2])
        temperature0 = temperature0 * 1.8 + 32

    temperature_str = '{0:.1f}'.format(temperature0)
    humidity_str = '{0:.1f}'.format(humidity0)

    return '{}F/{}%'.format(temperature_str, humidity_str)

@app.callback(
    dash.dependencies.Output(component_id='example-graph', component_property='figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('refresh', 'n_clicks')])
def update_graph(n_intervals, n_clicks):

    timestamps = []
    temperatures = []
    humidities = []

    with open('temperature.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        foo = list(reader)
        for row in foo:
            timestamp0 = row[0]
            temperature0 = float(row[1])
            humidity0 = float(row[2])

            temperature0 = temperature0 * 1.8 + 32

            timestamps.append(timestamp0)
            temperatures.append(temperature0)
            humidities.append(humidity0)

    return {
        'data': [
            go.Scatter(x = timestamps, y = humidities, name = 'humidity', yaxis='y1', line = dict(color='blue')),
            go.Scatter(x = timestamps, y = temperatures, name = 'temperature', yaxis='y2', line = dict(color='red')),
        ],
        'layout': go.Layout(
            title='Double Y Axis Example',
            yaxis=dict(title='temperature'),
            yaxis2=dict(
                title='humidity',
                overlaying='y',
                side='right'
            )
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.1.189')
