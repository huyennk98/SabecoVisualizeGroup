unit_weight = "grams"
unit_volume = "ml"
unit_cost = "VND"
class ConstraintTableModel:

    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data
        self.output_data = output_data
        self.routes_data = routes_data

    @staticmethod
    def check_weight_constraint():
        pass

    @staticmethod
    def check_volume_constraint():
        pass

    @staticmethod
    def check_items_value_constraint():
        pass

    @staticmethod
    def process_data_model(routes_data):
        '''
        Từ route_index và JSON Data Input & Output, tạo ra dữ liệu nhỏ chứa chuyến
        xe được chọn để tạo ra constraint table
        '''
        input_for_view = {
            "data": [],
            "style_info": {
                "header": {
                    'font': dict(color='white', size=18),
                    "fill_color": "navy"
                },
                "cells": {
                    'height': 32,
                    'font': dict(color='black', size=16),
                    "fill_color": [["white", "lightgrey"] * len(routes_data)]},
                "figure_height": 1000,
                "figure_title": " "
                }
        }

        for route_idx, route in enumerate(routes_data):
            route_info = {
                "Route": "Route " + str(route_idx + 1),
                "Vehicle Code": route["vehicle_code"],
                f"Total Weight ( {unit_weight} ) ": f"PASS ({route['total_weight_load']})" if route["total_weight_load"] <= route["vehicle_weight"] else "FAIL",
                f"Total Volume ( {unit_volume} ) ": f"PASS ({route['total_cbm_load']})" if route["total_cbm_load"] <= route["vehicle_cbm"] else "FAIL",
                f"Item Cost ( {unit_cost}) " : route["total_item_cost"],
                "Status": "PASS" if route["moq_status"] else "FAIL",
            }
            input_for_view['data'].append(route_info)

        return input_for_view
