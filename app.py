"""
An application for the visualization of COVID19 data
"""

import subprocess


import dash
import dash_core_components as cc
import dash_html_components as hc

import base_driver
from base_driver import BaseDriver

# import runtime_config
from runtime_config import RuntimeConfig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class Main(BaseDriver):
    def __init__(self, argv):
        super().__init__()
        self.runtime_config_ = RuntimeConfig(argv).args
        self.setup_()
        self.layout_()
        self.run()


    def run(self):
        self.app.run_server(
            port = self.runtime_config_["port"],
            debug = self.runtime_config_["debug"])
        

    
    def setup_(self):
        self.app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

    def layout_(self):
        self.app.layout = hc.Div(children = [
            hc.H1(children = 'Hello Dash'),
            hc.Div(children = '''
            Dash: A web application framework for Python.
            '''),
            cc.Graph(
                id = 'example-graph',
                figure = {
                    'data' : [
                        {'x': [1, 2, 3], 'y':[4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'y': [1, 2, 3], 'y':[2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout' : {
                        'title': 'Dash Data Visulaization'
                    }
                }
            )
        ])


            

class ExceptionHandler(BaseDriver):
    def __init__(self, e):
        super().__init__(1)
        print("COVID19 Encountered and error:\n", e)


def main(argv, exit):
    try:
        driver = Main(argv)
        driver.run()
        exit(driver.ExitCode)
    except Exception as e:
        exHandler = ExceptionHandler(e)
        exit(exHandler.ExitCode)


if __name__ == '__main__':
    import sys
    main(sys.argv, sys.exit)
