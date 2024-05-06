import datetime
from plugins.base_plugin.base_model import common_model


class Loading3DCheckTableModel:
    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data  # JSON Input File
        self.output_data = output_data  # JSON Output
        self.routes_data = routes_data  # Custom Route
        ''' Convert location (customers and depots) and vehicle to dict for easy access to Time Windows'''
        self.locations_dict = common_model.list_of_dicts_to_dict_of_dicts(input_data["customers"], "locationCode")
        self.locations_dict.update(common_model.list_of_dicts_to_dict_of_dicts(input_data["depots"], "locationCode"))
        self.vehicles_dict = common_model.list_of_dicts_to_dict_of_dicts(input_data["vehicles"], "vehicleCode")

    def create_fault_items_list(self):
        fault_items = []

        for route in self.routes_data:
            for element in route["elements"]:
                if element["location_type"] == "DEPOT":
                    for item in element["items"]:
                        check_item_loading_status = any(idx > len(item["size"]) for idx in item["size_index"])
                        if check_item_loading_status:
                            fault_items.append(item)

        return fault_items

    def processing_data_to_view(self, routes_data):
        loading_3d_check_table_input = {
            "data": [],
            "style_info": {
                "header": {"fill_color": "navy",
                           'font': dict(color='white', size=18)},
                "cells": {'height': 32, 'font': dict(color='black', size=16),
                          "fill_color": "limegreen"},
                "figure_title": "",
                "figure_height": 1000
            },
            "cell_colors": []
        }

        fault_items = self.create_fault_items_list()

        for item in fault_items:
            item_info = {
                "Item Code": item["item_code"],
                "Weight": item["weight"],
                "Cbm": item["cbm"],
                "Error": True
            }
            loading_3d_check_table_input["data"].append(item_info)

        # Now fishbone_table_input is prepared with the data and cell_colors according to the requirements
        loading_3d_check_table_input["cell_colors"] = list(
            map(list, zip(*loading_3d_check_table_input["cell_colors"])))  # Transpose the cell colors

        return loading_3d_check_table_input
