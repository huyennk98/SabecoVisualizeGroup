import numpy as np

formula_one = "Step 1 : mark = max_distance(depot, location[i])"
formula_two = "Step 2 : Fishbone(location[i]) = distance(depot, location[i]) + distance(location[i], mark) - distance(depot, mark)"
formula_three = "Step 3: Check Fishbone(location[i]) <= Max Fishbone of Route"

class FishboneTableModel:
    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data        # JSON Input File
        self.output_data = output_data      # JSON Output
        self.routes_data = routes_data      # Routes Data
        self.fishbone_config = input_data["algoParams"]['fishboneThresholds']

    def get_distance_matrix(self, distances_data):
        distance_matrix = {}
        for dis_info in distances_data:
            distance_matrix[dis_info['srcCode'], dis_info['destCode']] =  dis_info['distance']
            distance_matrix[dis_info['srcCode'], dis_info['srcCode']] =  0
        return distance_matrix

    def check_fishbone(self, route_max_distance):
        for fishbone_idx in range(len(self.fishbone_config)):
            if self.fishbone_config[fishbone_idx]["maxDistance"]>= route_max_distance:
                return self.fishbone_config[fishbone_idx]
        return self.fishbone_config[-1]

    def get_fishbone_data(self, routes_data, distance_matrix):
        fishbone_data = []
        for route in routes_data:
            route_info = {"location_codes":[], "fish_bone":[]}
            for element in route['elements']:
                route_info['location_codes'].append(element['location_code'])
            location_codes = route_info['location_codes']
            sorted_location_codes = sorted(location_codes, key=lambda point : distance_matrix[location_codes[0], point])
            route_info["farthest"] = sorted_location_codes[-1]
            route_info['fish_bone'] = [distance_matrix[location_codes[0],point]+distance_matrix[point, sorted_location_codes[-1]] - distance_matrix[location_codes[0],sorted_location_codes[-1]] for point in location_codes]
            route_info["fish_bone_info"] = self.check_fishbone(distance_matrix[location_codes[0],sorted_location_codes[-1]])
            fishbone_data.append(route_info)
        return fishbone_data

    def get_fishbone_matrix(self, fishbone_data, routes_data):
        max_points_of_route = max([len(route['elements']) for route in routes_data])
        fishbone_matrix = -1 * np.ones((len(self.routes_data), max_points_of_route))
        for route_idx, route in enumerate(fishbone_data):
            for element_idx in range(len(route["fish_bone"])):
                fishbone_matrix[route_idx, element_idx] = 0 if route["fish_bone"][element_idx] < 0 else route["fish_bone"][element_idx]
        return fishbone_matrix

    def get_max_fishbone(self, fishbone_data):
        return [route_info['fish_bone_info']['maxFishbone'] for route_info in fishbone_data]

    def process_data_model(self, routes_data):
        fishbone_table_input = {
            "data": [],
            "style_info": {
                "header": {'font': dict(color='white', size=18),
                           "fill_color": "navy"},
                "cells": {'height': 32, 'font': dict(color='black', size=16),
                          "fill_color": "limegreen"},
                "figure_title": dict(
                    text=formula_one + "<br>" + formula_two + "<br>" + formula_three
                ),
                "figure_height": 1000
            },
            "cell_colors": [],
        }

        # Preprocess Data
        distance_matrix = self.get_distance_matrix(self.input_data["distances"])
        fishbone_data = self.get_fishbone_data(routes_data, distance_matrix)

        # Get Core Data
        fishbone_matrix = self.get_fishbone_matrix(fishbone_data, routes_data)
        max_fishbone_list = self.get_max_fishbone(fishbone_data)

        # Populate the input_json 'data' with the correct structure
        for route_idx, row in enumerate(fishbone_matrix):
            max_fishbone_value = max_fishbone_list[route_idx]
            row_data = {"Route": f"Route {route_idx+1}", "Max Fishbone (km)": f"{max_fishbone_value:.2f}"}
            row_colors = ["limegreen", "lightblue"]  # Default color for the "Route" & "Max Fishbone" column

            for col_idx, value in enumerate(row):
                cell_key = f"Location {col_idx+1}"
                row_data[cell_key] = f"{value:.2f}" if value != -1 else ""

                # Determine the cell color based on the condition
                cell_color = "red" if value > max_fishbone_value else "lightgrey"
                row_colors.append(cell_color)

            fishbone_table_input["data"].append(row_data)
            fishbone_table_input["cell_colors"].append(row_colors)

        # Now fishbone_table_input is prepared with the data and cell_colors according to the requirements
        fishbone_table_input["cell_colors"] = list(map(list, zip(*fishbone_table_input["cell_colors"])))  # Transpose the cell colors

        return fishbone_table_input
