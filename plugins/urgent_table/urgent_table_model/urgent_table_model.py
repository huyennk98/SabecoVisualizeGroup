from plugins.base_plugin.base_model.common_model import list_of_dicts_to_dict_of_dicts


class UrgentTableModel():
    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data        # JSON Input File
        self.output_data = output_data      # JSON Output
        self.routes_data = routes_data      # Custom Route'
        self.requests_dict = list_of_dicts_to_dict_of_dicts(input_data["requests"], "orderCode")
        self.dropped_reqs = output_data["solutions"][0]["unscheduled_requests"]

    def create_urgent_dropped_reqs(self, dropped_reqs):
        urgent_items = []

        # Duyệt qua từng đơn hàng chưa phân bổ
        for request in  dropped_reqs:
        # Lấy danh sách items của đơn hàng hiện tại
            items = request["items"]
        # Duyệt qua từng item trong danh sách
            for item in items:
                # Kiểm tra nếu trạng thái urgent_status của item là True
                if item["urgent_status"]:
                # Thêm item vào danh sách urgent_items
                    urgent_items.append(item)

        return urgent_items
    
    def process_data_model(self, routes_data):
        input_json = {
            "data": [],
            "style_info": {
                "header": {"fill_color": "navy"},
                "cells": {"fill_color": "lightgrey"}
            }
        }
        urgent_items = self.create_urgent_dropped_reqs(self.dropped_reqs)

        # Header bảng (tùy chỉnh theo yêu cầu)
        headers = ["Item Code", "Quantity", "Cbm", "Weight"]  # Bạn có thể thêm các header khác

        # Duyệt qua các item urgent và tạo dữ liệu hàng bảng
        for item in urgent_items:
            item_info = {
                "Item Code": item["item_code"],
                "Quantity": item["quantity"],
                "Cbm": item["cbm"],
                "Weight": item["weight"],
            }
            input_json["data"].append(item_info)


        return input_json
