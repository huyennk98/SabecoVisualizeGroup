import datetime
from plugins.base_plugin.base_model import common_model


class TransportationConstraintTableModel:
    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data  # JSON Input File
        self.output_data = output_data  # JSON Output
        self.routes_data = routes_data  # Custom Route
        ''' Convert location (customers and depots) and vehicle to dict for easy access to Time Windows'''
        self.locations_dict = common_model.list_of_dicts_to_dict_of_dicts(input_data["customers"], "locationCode")
        self.locations_dict.update(common_model.list_of_dicts_to_dict_of_dicts(input_data["depots"], "locationCode"))
        self.vehicles_dict = common_model.list_of_dicts_to_dict_of_dicts(input_data["vehicles"], "vehicleCode")

    @staticmethod
    def parse_time(time_str):
        return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    def check_weight_limit_constraint(self, weight_limit, route):
        return not weight_limit or route["vehicle_weight"] <= weight_limit

    def check_vehicle_priority_constraint(self, vehicle_code, priority_vehicle_list):
        return

    def processing_data_to_view(self, routes_data):
        transportation_constraint_table_input = {
            "data": [],
            "style_info": {
                "header": {"fill_color": "navy",
                           'font': dict(color='white', size=18)},
                "cells": {'height': 32, 'font': dict(color='black', size=16),
                          "fill_color": "limegreen"},
                "figure_title": "Annotations:<br>LC: Location Code<br>WL: Weight Limit",
                "figure_height": 1000
            },
            "cell_colors": []
        }

        max_points_of_route = max([len(route['elements']) for route in routes_data])

        for route_idx, route in enumerate(routes_data):
            vehicle_weight = round(route["vehicle_weight"]/1000000, 2)
            row_data = {"Route": f"Route {route_idx + 1}",
                        "Vehicle Weight (Tons)": f"{vehicle_weight:.2f}"}
            row_colors = ["limegreen", "lightblue"]
            weight_limit_string = ""
            for ele_idx, element in enumerate(route["elements"]):
                loc_code = element["location_code"]
                weight_limit = None

                if "cType" in self.locations_dict[loc_code].keys():
                    weight_limit_string = self.locations_dict[loc_code]["cType"]["typeOfCustomerByLimitedWeight"]
                    if weight_limit_string != "no value":
                        weight_limit = int(float(weight_limit_string[:-1])*1000000)

                weight_limit_key = f"Location {ele_idx + 1}"
                row_data[weight_limit_key] = "LC: " + loc_code + "<br>"
                row_data[weight_limit_key] += "WL: " + weight_limit_string if weight_limit else "No WL"

                # Determine the cell color based on the condition
                cell_color = "lightgrey" if (not weight_limit or route["vehicle_weight"] <= weight_limit) else "red"
                row_colors.append(cell_color)

            if len(route['elements']) < max_points_of_route:
                row_colors.extend(["lightgrey"] * (max_points_of_route - len(route['elements'])))
                for i in range(len(route['elements'])+1, max_points_of_route + 1):
                    row_data[f"Location {i}"] = ""

            transportation_constraint_table_input["data"].append(row_data)
            transportation_constraint_table_input["cell_colors"].append(row_colors)

        # Now fishbone_table_input is prepared with the data and cell_colors according to the requirements
        transportation_constraint_table_input["cell_colors"] = list(
            map(list, zip(*transportation_constraint_table_input["cell_colors"])))  # Transpose the cell colors

        return transportation_constraint_table_input
