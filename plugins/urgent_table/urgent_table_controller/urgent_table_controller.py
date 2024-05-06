import dash
import json
from dash import dcc, html, Input, Output, State
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
from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.urgent_table.urgent_table_model.urgent_table_model import UrgentTableModel
from plugins.urgent_table.urgent_table_view.urgent_table_view import UrgentTableView
# from plugins.base_plugin.base_model import AbstractModel

class UrgentTableController(AbstractController):
    def __init__(self):
        self.view = UrgentTableView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = UrgentTableModel(input_data, output_data, output_data["solutions"][0]["unscheduled_requests"])

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        @app.callback(
            Output('display-urgent-table', 'children'),
            Input('vis-init-routes-button', 'n_clicks'),
            Input('get-updated-routes-button', 'n_clicks'),
            Input('urgent-table-switch', 'on'),
            State('json-output-store', 'data'),
        )
        def update_urgent_table(init_routes_button, updated_routes_button, switch, new_output_data):
            if self.model and switch:
                ctx = dash.callback_context
                trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

                if not new_output_data or trigger_id == 'vis-init-routes-button':
                    urgent_table_input_data = self.model.process_data_model(self.model.routes_data)
                    return self.view.draw_urgent_table(urgent_table_input_data) # type: ignore

                new_output_data = json.loads(new_output_data)
                new_routes_data = new_output_data["solutions"][0]["unscheduled_requests"]
                new_urgent_table_input_data = self.model.process_data_model(new_routes_data)
                return self.view.draw_urgent_table(new_urgent_table_input_data)
            else:
                return None
            
        @app.callback(
        Output('urgent-table-cover', 'style'),
        Input('urgent-table-switch', 'on')
        )
        def urgent_table_display(switch):
            if switch:
                return {}
            else:
                return {'display': 'none'}