import dash_bootstrap_components as dbc
import dash_daq as daq
import json
from dash import dcc, html
from components.table import table
from plugins.base_plugin.constants import base_display_const
import copy
import folium
import json
import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import random
from datetime import datetime
from collections import defaultdict
from folium.plugins import BeautifyIcon
from dash import Dash, dcc, html, Input, Output
from folium.map import Popup
from branca.element import Template, MacroElement

class RequestDeliveryTimeTableView:
    def __init__(self):
        self.layout_settings = {}
    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/request_delivery_time_table/request_delivery_time_table_config/request_delivery_time_table_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)

    # Plugin Layout Creation
    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='request-delivery-time-table-switch',
            label={"label": "Request Delivery Time Table",
                   "style": {"font-size": "24px"}},
            labelPosition="top",
            on=False
        )
    
    def create_plugin_layout(self):
        return dbc.Card(
            dbc.Row([
                dbc.Col(dbc.Card(id='display-request-delivery-time-table'), width=base_display_const.MAX_VISUALIZATION_WIDTH)
            ]), 
            id="request-delivery-time-table-cover")

    def draw_request_delivery_time_table(self, input_data):
        # data_input_for_a_route = processing_data(self, route_index)
        return [html.H2("Request Delivery Time Table"),
                dcc.Graph(figure=table.create_general_table_from_json(input_data))]