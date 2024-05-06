from plugins.base_plugin.base_model import common_model


class DistMapModel:
    def __init__(self, data):
        self.input_data = data
        self.lat_lng_dict = {}
        self.map_center = None
        self.cus_to_req_dict = {}
        self.unique_provinces = []
        self.dist_map_data = {}
        self.list_of_loads = {
            "weights": [],
            "volumes": []
        }

    def get_map_center(self, locations_data):
        self.map_center = None if not locations_data else {
            "lat": sum(loc['lat'] for loc in locations_data) / len(locations_data),
            "lng": sum(loc['lng'] for loc in locations_data) / len(locations_data)
        }

    def get_unique_provinces(self, requests):
        unique_provinces = sorted({request['province'] for request in requests})
        self.unique_provinces = unique_provinces

    def get_list_of_loads(self, cus_to_req_dict):
        self.list_of_loads["weights"] = [loc_group['totalWeight'] for loc_group in cus_to_req_dict.values()]
        self.list_of_loads["volumes"] = [loc_group['totalVolume'] for loc_group in cus_to_req_dict.values()]

    def create_dist_map_data(self, input_data, cus_to_req_dict):

        dist_map_data = {
            "depots": [],
            "customers": []
        }

        for depot in input_data["depots"]:
            depot_data = {}
            depot_data["depot_code"] = depot["depotCode"]
            depot_data["lat"] = self.lat_lng_dict[depot["depotCode"]]["lat"]
            depot_data["lng"] = self.lat_lng_dict[depot["depotCode"]]["lng"]
            dist_map_data["depots"].append(depot_data)

        for customer in input_data["customers"]:
            cus_data = {}
            location_code = customer["locationCode"]
            cus_data["location_code"] = location_code
            cus_data["lat"] = self.lat_lng_dict[location_code]["lat"]
            cus_data["lng"] = self.lat_lng_dict[location_code]["lng"]
            cus_data["weight"] = cus_to_req_dict[location_code]["totalWeight"]
            cus_data["volume"] = cus_to_req_dict[location_code]["totalVolume"]
            cus_data["province"] = customer["province"]
            dist_map_data["customers"].append(cus_data)

        self.dist_map_data = dist_map_data


    def process_data_model(self):
        common_model.calculate_total_loads(self.input_data["requests"])
        common_model.add_province_to_requests(self.input_data["requests"]
                                              , self.input_data["customers"])
        self.lat_lng_dict = common_model.list_of_dicts_to_dict_of_dicts(self.input_data["locations"], "locationCode")
        self.get_map_center(self.input_data["locations"])
        self.cus_to_req_dict = common_model.group_requests_by_customer(self.input_data["requests"])
        self.get_list_of_loads(self.cus_to_req_dict)
        self.get_unique_provinces(self.input_data["requests"])
        self.get_list_of_loads(self.cus_to_req_dict)
        self.create_dist_map_data(self.input_data, self.cus_to_req_dict)
