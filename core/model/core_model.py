import json


class CoreModel:
    def __init__(self):
        self.input_data = {}
        self.output_data = {}
        self.routes_data = []
        self.unscheduled_req_data = []
        self.new_output_data = None
        self.new_routes_data = None
        self.new_unscheduled_req_data = None
        self.io_match = True

    def get_updated_output(self, new_output_data):
        self.new_output_data = new_output_data
        self.new_routes_data = new_output_data["solutions"][0]["routes"]
        self.new_unscheduled_req_data = new_output_data["solutions"][0]["unscheduled_requests"]

    def init_uploaded_data_files(self, input_data, output_data):
        self.input_data = input_data
        self.output_data = output_data
        self.routes_data = output_data["solutions"][0]["routes"]
        self.unscheduled_req_data = output_data["solutions"][0].get("unscheduled_requests", None)
