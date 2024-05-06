from plugins.base_plugin.base_model.common_model import list_of_dicts_to_dict_of_dicts


class RequestDeliveryTimeTableModel():
    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data        # JSON Input File
        self.output_data = output_data      # JSON Output
        self.routes_data = routes_data      # Custom Route'

    #add to function for process data model

    
    def process_data_model(self, routes_data):
        pass
