import dash_bootstrap_components as dbc
import dash_daq as daq
import json
from dash import dcc, html
from components.table import table
from plugins.base_plugin.constants import base_display_const


class TransportationConstraintTableView:
    def __init__(self):
        self.layout_settings = {}

    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/transportation_constraint_table/transportation_constraint_table_config/'
                  'transportation_constraint_table_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)

    # Plugin Layout Creation
    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='transportation-constraint-table-switch',
            label={"label": "Transportation Constraint Table",
                   "style": {"font-size": "24px"}},
            labelPosition="top",
            on=False
        )

    def create_plugin_layout(self):
        return dbc.Card(
            dbc.Row([
                dbc.Col(dbc.Card(id='display-transportation-constraint-table'),
                        width=base_display_const.MAX_VISUALIZATION_WIDTH)
            ]),
            id="transportation-constraint-table-cover"
        )

    def draw_transportation_constraint_table(self, input_data):
        return [html.H2("Transportation Constraint Table"),
                dcc.Graph(figure=table.create_general_table_from_json(input_data))]
