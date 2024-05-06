import dash_bootstrap_components as dbc
import dash_daq as daq
import math
import json
from dash import dcc, html
from components.folium_map import folium_map, marker_element
from plugins.base_plugin.constants import base_data_const, base_display_const
from plugins.base_plugin.base_view import common_view
from plugins.dist_map.constants import display_const


class DistMapView:
    def __init__(self):
        self.MAX_POPUP_BUBBLE_WIDTH = 300
        self.color_array = ["blue", "green", "purple", "orange", "beige",
                            "darkblue", "darkgreen", "cadetblue", "darkred",
                            "lightred", "pink", "darkpurple", "lightblue",
                            "lightgreen", "gray", "black", "lightgray"]
        self.folium_markers = []
        self.display_settings = {}
        self.layout_settings = {}
        self.province_colors = {}

    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/dist_map/config/plugin_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)

    def folium_map_display_settings(self, map_center):
        self.display_settings = {
            "center": [map_center["lat"], map_center["lng"]],  # Tượng trưng, sẽ load vào sau
            "zoom": 10,  # Có thể thay đổi zoom linh động ở đây
            "display_scalebar": True,
            "tiles": "CartoDB Positron"
        }

    def calculate_circle_size(self, load, loads_list, latitude):
        """
        Calculates the size of the circle representing a load on a distribution map.

        This function considers the load's value relative to other loads, the local latitude
        deformation factor, and predefined constants to calculate an appropriate circle size.
        It ensures the size is between predefined minimum and maximum radii.

        Args:
            load (float): The load value for which the circle size is being calculated.
            location_loads (List[float]): A list of all load values for the location.
            latitude (float): The latitude of the load's location in degrees.

        Returns:
            float: The calculated circle size.
        """
        local_deformation = math.cos(math.radians(latitude))
        max_load, min_load = max(loads_list), min(loads_list)

        # Check if all loads are the same
        if max_load == min_load:
            # Return a default or average size since all loads are equal
            return max(display_const.MIN_RADIUS, display_const.MAX_RADIUS * local_deformation)

        normalized_load = (load - min_load) / (max_load - min_load)
        return max(display_const.MIN_RADIUS, normalized_load * display_const.LOAD_PER_CM * local_deformation)

    def create_depot_popup_content(self, depot_info):
        depot_code = depot_info["depot_code"]
        return f"Depot - Depot Code: {depot_code}"

    def create_cus_popup_content(self, cus_info):
        """
        Creates a popup bubble with information about a specific delivery location.

        Args:
            location_code (str): The code for the delivery location.
            location_group (Dict): A dictionary containing 'totalWeight' and 'totalVolume' for locations.

        Returns:
            folium.Popup: A popup bubble object containing the formatted information.
        """
        # Format the message for the popup bubble
        cus_code = cus_info["location_code"]
        weight_in_tons = cus_info['weight'] / base_data_const.TONS_TO_GRAMS
        volume_in_cbm = cus_info['volume'] / base_data_const.CBM_TO_ML
        return (
            f"1. Delivery Location Code: {cus_code}<br>"
            f"2. Total Weight: {weight_in_tons:.2f} Tons<br>"
            f"3. Total Volume: {volume_in_cbm:.2f} Cbm"
        )

    def create_markers_for_dist_map(self, dist_map_data, map_type, list_of_loads):
        markers_array = []

        for depot_info in dist_map_data["depots"]:
            depot_marker_info = {}
            depot_marker_info["location"] = [depot_info["lat"], depot_info["lng"]]
            depot_marker_info["color"] = "red"
            depot_marker_info["fill"] = True
            depot_marker_info["radius"] = display_const.DEPOT_CIRCLE_RADIUS
            depot_marker_info["icon"] = "industry"
            depot_marker_info["prefix"] = "fa"
            depot_marker_info["opacity"] = 0.8
            depot_marker_info["fixed_size"] = True
            depot_marker_info["popup"] = {
                "content": self.create_depot_popup_content(depot_info),
                "width": display_const.MAX_POPUP_BUBBLE_WIDTH
            }

            if map_type in ["circle-weight", "circle-volume"]:
                depot_marker = marker_element.create_circle_marker_element(depot_marker_info)
            else:
                depot_marker = marker_element.create_plain_marker_element(depot_marker_info)

            markers_array.append(depot_marker)

        for cus_info in dist_map_data["customers"]:
            cus_load = cus_info["volume"] if map_type == "circle-volume" else cus_info["weight"]
            loads_list = list_of_loads["volumes"] if map_type == "circle-volume" else list_of_loads["weights"]
            cus_marker_info = {}
            cus_marker_info["location"] = [cus_info["lat"], cus_info["lng"]]
            cus_marker_info["color"] = self.province_colors[cus_info["province"]]
            cus_marker_info["fill"] = True
            cus_marker_info["radius"] = self.calculate_circle_size(cus_load, loads_list, cus_info["lat"])
            cus_marker_info["icon"] = "users"
            cus_marker_info["prefix"] = "fa"
            cus_marker_info["opacity"] = 0.8
            cus_marker_info["fixed_size"] = True
            cus_marker_info["popup"] = {
                "content": self.create_cus_popup_content(cus_info),
                "width": display_const.MAX_POPUP_BUBBLE_WIDTH
            }

            if map_type in ["circle-weight", "circle-volume"]:
                cus_marker = marker_element.create_circle_marker_element(cus_marker_info)
            else:
                cus_marker = marker_element.create_plain_marker_element(cus_marker_info)

            markers_array.append(cus_marker)

        self.folium_markers = markers_array

    def create_convex_hull_for_map(self):
        pass

    def create_visualization(self, map_center, dist_map_data, map_type, unique_provinces,
                             list_of_loads):
        self.province_colors = common_view.assign_colors_to_provinces(unique_provinces, self.color_array)
        self.folium_map_display_settings(map_center)
        self.create_markers_for_dist_map(dist_map_data, map_type, list_of_loads)
        dist_map = folium_map.create_folium_map(self.display_settings, self.folium_markers, [], [])

        # Return HTML String of the Distribution Map
        return dist_map._repr_html_()

    # Plugin Layout Creation
    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='dist-map-switch',
            label={"label": "Distribution Map",
                   "style": {"font-size": "24px"}},
            labelPosition="top",
            on=False
        )

    def create_radio_buttons_options(self):
        return [{'label': '  Bubble Map, by Weight', 'value': 'circle-weight'},
                {'label': '  Bubble Map, by Volume', 'value': 'circle-volume'},
                {'label': '  Plain Map', 'value': 'plain'}]

    def create_radio_buttons(self):
        radio_buttons_options = self.create_radio_buttons_options()
        return {
            "chart_category": dcc.RadioItems(id='radio-map-category', value='plain',
                                             options=radio_buttons_options,
                                             style={'paddingLeft': '50px'})
        }

    def create_control_board(self):
        radio_buttons = self.create_radio_buttons()

        control_board = [
            dbc.Row(html.Div([html.Label(html.B("Select Distribution Map Type:"))])),
            dbc.Row(radio_buttons["chart_category"])
        ]

        return control_board

    def create_display_area(self):
        return dbc.Card(id='display-dist-map')

    def create_plugin_layout(self):
        control_board = self.create_control_board()
        display_area = self.create_display_area()
        return dbc.Card(
            dbc.Row([
                dbc.Col(control_board, width=base_display_const.CONTROL_BOARD_WIDTH),
                dbc.Col(display_area, width=base_display_const.VISUALIZATION_WIDTH)
            ]),
            id="dist-map-cover"
        )
