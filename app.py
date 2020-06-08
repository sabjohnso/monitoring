"""
An application for the visualization of COVID19 data
"""

import subprocess
import os
import json
import numpy as np


import plotly

import dash
import dash_core_components as cc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output




from runtime_config import RuntimeConfig
from base_driver import BaseDriver
import data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

module_path = os.path.dirname(__file__)
def complete_package_path(tail):
    return module_path + '/' + tail if module_path != '' else tail

config_basename = 'config.json'
with open(complete_package_path(config_basename), 'r') as config_file:
    default_config = json.load(config_file)

states_and_territories_basename = 'USStatesAndTerritories.json'
with open(complete_package_path(states_and_territories_basename), 'r') as states_and_territories_file:
    states_and_territories = json.load(states_and_territories_file)

theme = {
    'dark' : True,
       'detail' : '#007439',
      'primary' : '#00EA64',
    'secondary' : '#6E6E6E'
}

class Main(BaseDriver):
    def __init__(self, argv):
        super().__init__()
        self.runtime_config_ = RuntimeConfig(argv).args
        self.__setup()
        
        self.daily = data.DailyReports(
            default_config['dataRoot'] + '/' + default_config['dataRelpath'],
            ['labelSequence1.json', 'labelSequence1WithCoords.json', 'labelSequence2.json'])
        self.__layout()
        self.__register_callbacks()
        self.__run()

    def setupStatePlot(self):
            pass

    def __run(self):
        self.app.run_server(
            port = self.runtime_config_["port"],
            debug = self.runtime_config_["debug"])

    def __setup(self):
        self.app = dash.Dash(__name__, external_stylesheets =external_stylesheets)

    def __app_components(self):
        return [html.Br(),
                html.H1(children = 'COVID-19 Deaths'),
                html.Div(children = '''Visualization of cummulative COVID-19 deaths'''),
                cc.Checklist(
                    options = [{'label' : state_or_territory,
                                'value' : state_or_territory}
                               for state_or_territory in
                               states_and_territories if
                               states_and_territories[state_or_territory]['isState']]
                ),
                cc.Dropdown(
                    id = 'state-dropdown',
                    options =[{'label' : state, 'value' : state} for state in data.STATES],
                    value = 'Texas'),
                cc.Graph(id = 'cumulative-deaths'),
                cc.Slider(
                    id = 'start-date-slider',
                    min = 0,
                    max = len(self.daily.dates),
                    value = 0,
                    marks={str(day) : str(day) for day in range(len(self.daily.dates))},
                    step = 1)
                ]


    def __register_callbacks(self):
        @self.app.callback(
            Output('cumulative-deaths', 'figure'),
            [Input('state-dropdown', 'value'), Input('start-date-slider', 'value')])
        def updateSelected(selected_state, start_date):
            x = np.array([i for i in range(len(self.daily.dates))])
            y = np.array(self.daily.filteredDeaths(data.makeStatePredicate(selected_state)))
            figure = {
                "data": [{
                    "x": x[start_date :],
                    "y": y[start_date :],
                    "type": "scatter",
                    "mode" : "lines",
                    "line" : {"width" : 2}
                }],
                "layout" :{'margin': {'l': 20, 'r': 10, 'b': 20, 't': 10}}}
            return figure

        @self.app.callback(
            Output('top-level', 'children'),
            [Input('daq-light-dark-theme', 'value')])
        def toggle_darkness(dark_theme):
            if(dark_theme): theme.update(dark = True)
            else: theme.update(dark = False)
            return daq.DarkThemeProvider(theme = theme, children = self.__app_components())

        @self.app.callback(
            Output('app', 'style'),
            [Input('daq-light-dark-theme', 'value')])
        def change_bg(dark_theme):
            if(dark_theme):
                return {'background-color': '#303030', 'color': 'white'}
            else:
                return {'background-color': 'white', 'color': 'black'}
        

    def __layout(self):
        self.app.layout = html.Div(
            id = 'top-level',
            children = [
                html.Br(),
                html.Div( children = 
                          [html.Div(id = 'app', children = [daq.DarkThemeProvider(theme = theme, children = self.__app_components())],                              
                           daq.ToggleSwitch(
                               id='daq-light-dark-theme',
                               label = ['Light', 'Dark'],
                               style = {'width' : '250px', 'margin': 'auto'},
                               value = False)
        

            



            
                                             


class ExceptionHandler(BaseDriver):
    def __init__(self, argv, e):
        super().__init__(1)
        print("COVID19 Encountered and error:\n", e)


def main(argv, exit):
    try:
        exit(Main(argv).ExitCode)
    except Exception as e:            
        exit(ExceptionHandler(argv, e).ExitCode)


if __name__ == '__main__':
    import sys
    main(sys.argv, sys.exit)
    
