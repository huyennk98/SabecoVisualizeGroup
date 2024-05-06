import dash_bootstrap_components as dbc
import dash_daq as daq
import json
from dash import dcc, html
from components.table import table
from plugins.base_plugin.constants import base_display_const


class Loading3DCheckTableView:
    def __init__(self):
        self.layout_settings = {}

    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/loading_3d_check_table/loading_3d_check_table_config/loading_3d_check_table_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)

    # Plugin Layout Creation
    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='loading-3d-check-table-switch',
            label={"label": "Loading 3D Check Table",
                   "style": {"font-size": "24px"}},
            labelPosition="top",
            on=False
        )

    def create_plugin_layout(self):
        return dbc.Card(
            dbc.Row([
                dbc.Col(dbc.Card(id='display-loading-3d-check-table'), width=base_display_const.MAX_VISUALIZATION_WIDTH)
            ]),
            id="loading-3d-check-table-cover"
        )

    def draw_weight_limit_table(self, input_data):
        return [html.H2("Loading 3D Check Table"),
        dcc.Graph(figure=table.create_general_table_from_json(input_data))]
