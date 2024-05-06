from plugins.base_plugin.base_model import common_model


class FeasibleHeatmapModel:
    def __init__(self, data):
        self.input_data = data

    def generate_feasible_matrix(self, customers_data, vehicles_data, requests_data):
        # Create a mapping for customer weight limits based on location code
        customer_weight_limits = {customer['locationCode']:
                                  common_model.convert_ton_string_to_kg(customer['cType']['typeOfCustomerByLimitedWeight'])
                                  for customer in customers_data}

        # Create a mapping for vehicle weights based on vehicle code
        vehicle_weights = {vehicle['vehicleCode']:
                           common_model.convert_ton_string_to_kg(vehicle['vType']['typeOfVehicleByCostToDeploy'])
                           for vehicle in vehicles_data}

        # Initialize the feasibility matrix
        feasible_matrix = []

        # Iterate over each vehicle and request to determine feasibility
        for vehicle in vehicles_data:
            vehicle_row = []
            vehicle_weight = vehicle_weights[vehicle['vehicleCode']]

            for request in requests_data:
                customer_location = request['deliveryLocationCode']
                customer_weight_limit = customer_weight_limits.get(customer_location, float('inf'))

                # Determine if the vehicle can deliver to the customer based on weight limit
                is_feasible = 1 if vehicle_weight <= customer_weight_limit else 0
                vehicle_row.append(is_feasible)

            feasible_matrix.append(vehicle_row)

        return feasible_matrix

    def process_data_model(self):
        pass
