from plugins.base_plugin.base_model import common_model

class ScatterMapModel:
    def __init__(self, data):
        self.input_data = data
        self.lat_lng_dict = {}
        self.map_center = None
        self.scatter_map_data = {}



    def get_map_center(self, locations_data):
        self.map_center = None if not locations_data else {
            "lat": sum(loc['lat'] for loc in locations_data) / len(locations_data),
            "lng": sum(loc['lng'] for loc in locations_data) / len(locations_data)
        }
    
    def create_scatter_map_data(self, input_data):

        scatter_map_data = {
            "factories": [],
            "depots": [],
            "customers": []
        }

        for factory in input_data["depots"]:
            fac_data = {}
            fac_data["factory_code"] = factory["factoryCode"]
            fac_data["lat"] = self.lat_lng_dict[factory["factoryCode"]]["lat"]
            fac_data["lng"] = self.lat_lng_dict[factory["factoryCode"]]["lng"]
            scatter_map_data["factories"].append(fac_data)

        for depot in input_data["depots"]:
            depot_data = {}
            depot_data["depot_code"] = depot["depotCode"]
            depot_data["lat"] = self.lat_lng_dict[depot["depotCode"]]["lat"]
            depot_data["lng"] = self.lat_lng_dict[depot["depotCode"]]["lng"]
            scatter_map_data["depots"].append(depot_data)      

        for customer in input_data["customers"]:
            cus_data = {}
            cus_data["customer_code"] = customer["customerCode"]
            cus_data["lat"] = self.lat_lng_dict[customer["customerCode"]]["lat"]
            cus_data["lng"] = self.lat_lng_dict[customer["customerCode"]]["lng"]
            scatter_map_data["customers"].append(cus_data)

        self.scatter_map_data = scatter_map_data

    def process_data_model(self):
        self.lat_lng_dict = common_model.list_of_dicts_to_dict_of_dicts(self.input_data["locations"], "locationCode")
        self.get_map_center(self.input_data["locations"])
        self.create_scatter_map_data(self.input_data)
