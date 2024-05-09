import dash_bootstrap_components as dbc
import dash_daq as daq
import math
import json
from dash import dcc, html

from components.scatter_map import scatter_map
from plugins.base_plugin.constants import base_data_const, base_display_const
from plugins.base_plugin.base_view import common_view
from plugins.dist_map.constants import display_const

class ScatterMapView:
    def __init__(self):
        self.MAX_POPUP_BUBBLE_WIDTH = 300
        self.color_array = ["blue", "green", "purple", "orange", "beige",
                            "darkblue", "darkgreen", "cadetblue", "darkred",
                            "lightred", "pink", "darkpurple", "lightblue",
                            "lightgreen", "gray", "black", "lightgray"]
        self.scatter_markers = []
        self.display_settings = {}
        self.layout_settings = {}


    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/scatter_map/config/plugin_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)
    
    def scatter_map_display_setting(self, map_center):
        self.display_settings = {
            'accesstoken': 'pk.eyJ1Ijoic29sa2FyYW1tYWFyIiwiYSI6ImNrc2JqdWM4eTA3aXYzMG9kOGd2NTZxdHEifQ.M8vfidWZ-3C7SEI2w4EjLg',
            'style': 'mapbox://styles/mapbox/streets-v11',
            'zoom': 8,
            'center': {'lat': map_center["lat"], 'lon': map_center["lng"]}  # Tọa độ trung tâm bản đồ
        }

    def create_markers_for_scatter_map(self, scatter_map_data):
        markers_array = []

        for depot_info in scatter_map_data["depots"]:
            depot_marker_info = {}
            depot_marker_info["location"] = [depot_info["lat"], depot_info["lng"]]
            depot_marker_info["color"] = "red"
            depot_marker_info["text"] = depot_info["depot_code"]
            depot_marker_info["opacity"] = 0.8

            markers_array.append(depot_marker_info)  

        for fac_info in scatter_map_data["factories"]:
            fac_marker_info = {}
            fac_marker_info["location"] = [fac_info["lat"], fac_info["lng"]]
            fac_marker_info["color"] = "green"
            fac_marker_info["text"] = fac_info["factory_code"]
            fac_marker_info["opacity"] = 0.8

            markers_array.append(fac_marker_info)  
              
        for cus_info in scatter_map_data["customer"]:
            cus_marker_info = {}
            cus_marker_info["location"] = [cus_info["lat"], cus_info["lng"]]
            cus_marker_info["color"] = "red"
            cus_marker_info["text"] = cus_info["customer_code"]
            cus_marker_info["opacity"] = 0.8

            markers_array.append(cus_marker_info)  
        
        self.scatter_markers = markers_array

    def create_visualization(self, map_center, scatter_map_data):
        self.scatter_map_display_setting(map_center)
        self.create_markers_for_scatter_map(scatter_map_data)
        scatter_mapbox = scatter_map.create_scatter_map(self.display_settings, self.scatter_markers)

        return scatter_mapbox
    
    # Plugin Layout Creation
    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='scatter-map-switch',
            label={"label": "Scatter Map",
                   "style": {"font-size": "24px"}},
            labelPosition="top",
            on=False
        )
    
    def create_display_area(self):
        return dcc.Graph(id='display-scatter-map')

    def create_plugin_layout(self):
        # control_board = self.create_control_board()
        display_area = self.create_display_area()
        return dbc.Card(
            dbc.Row([
                # dbc.Col(control_board, width=base_display_const.CONTROL_BOARD_WIDTH),
                dbc.Col(display_area, width=base_display_const.VISUALIZATION_WIDTH)
            ]),
            id="scatter-map-cover"
        )

