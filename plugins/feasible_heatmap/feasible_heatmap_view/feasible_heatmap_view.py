import dash_bootstrap_components as dbc
import dash_daq as daq
import json
from components.feasible_heatmap import feasible_heatmap
from dash import dcc, html
from plugins.base_plugin.constants import base_display_const


class FeasibleHeatmapView:
    def __init__(self):
        self.dropdown_options = {
            "vehicle_options": [],
            "request_options": []
        }
        self.heatmap_data = {}
        self.display_settings = {}
        self.layout_settings = {}

    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/dist_map/config/plugin_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)

    def get_feasible_display_settings(self):
        self.display_settings["chart_title"] = "Feasible Heatmap: Vehicle-Requests based on Customer Weight Limit"
        self.display_settings["x_axis_settings"] = dict(title='Request Order Codes')
        self.display_settings["y_axis_settings"] = dict(title='Vehicle Codes', autorange='reversed')
        self.display_settings["margins"] = dict(l=150, r=50, t=50, b=150)
        self.display_settings["color_scale"] = [[0, 'red'], [1, 'blue']]
        self.display_settings["show_scale"] = True
        self.display_settings["hover_info"] = "text"
        self.display_settings["chart_height"] = base_display_const.FIGURE_HEIGHT

    def create_heatmap_data(self, feasible_matrix, vehicle_codes, request_codes):
        heatmap_data = {}
        heatmap_data["x_axis_data"] = request_codes
        heatmap_data["y_axis_data"] = vehicle_codes
        heatmap_data["z_axis_data"] = feasible_matrix
        self.heatmap_data = heatmap_data

    def create_visualization(self, feasible_matrix, vehicle_codes, request_codes):
        self.get_feasible_display_settings()
        self.create_heatmap_data(feasible_matrix, vehicle_codes, request_codes)
        feas_heatmap = feasible_heatmap.create_feasible_heatmap(self.heatmap_data, self.display_settings)
        return feas_heatmap

    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='feasible-heatmap-switch',
            label={"label": "Feasible Heatmap",
                   "style": {"font-size": "24px"}},
            # label="Request Bar Chart",
            labelPosition="top",
            on=False
        )

    def create_dropdown_options(self, input_data):
        return {
            "vehicle_options": [{'label': v["vehicleCode"], 'value': v["vehicleCode"]} for v in input_data["vehicles"]],
            "request_options": [{'label': r["orderCode"], 'value': r["orderCode"]} for r in input_data["requests"]],
        }

    def create_dropdowns(self):
        return {
            "vehicle_dropdown": dcc.Dropdown(id='vehicles-dropdown',
                                             options=self.dropdown_options["vehicle_options"],
                                             multi=True,
                                             placeholder="Click Here to Select Vehicles"
                                             ),
            "request_dropdown": dcc.Dropdown(id='requests-dropdown',
                                             options=self.dropdown_options["request_options"],
                                             multi=True,
                                             placeholder="Click Here to Select Requests"
                                             ),
        }

    def create_control_board(self):
        dropdowns = self.create_dropdowns()

        control_board = [
            dbc.Row(html.Div([html.Label(html.B("Select Vehicles:"))])),
            dbc.Row(dropdowns["vehicle_dropdown"]),
            dbc.Row(html.Div([html.Br(), html.Label(html.B("Select Requests:"))])),
            dbc.Row(dropdowns["request_dropdown"]),
        ]

        return control_board

    def create_display_area(self):
        return dbc.Card(id='display-feasible-heatmap')

    def create_plugin_layout(self):
        control_board = self.create_control_board()
        display_area = self.create_display_area()
        return dbc.Card(
            dbc.Row([
                dbc.Col(control_board, width=base_display_const.CONTROL_BOARD_WIDTH),
                dbc.Col(display_area, width=base_display_const.VISUALIZATION_WIDTH)
            ]),
            id='feasible-heatmap-cover'
        )
