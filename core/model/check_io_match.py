def extract_input_obj_codes(input_data):
    input_obj_codes = dict()
    input_obj_codes["input_customer_codes"] = [cus["customerCode"] for cus in input_data["customers"]]
    input_obj_codes["input_vehicle_codes"] = [veh["vehicleCode"] for veh in input_data["vehicles"]]
    input_obj_codes["input_depot_codes"] = [dep["depotCode"] for dep in input_data["depots"]]
    input_obj_codes["input_location_codes"] = [loc["locationCode"] for loc in input_data["locations"]]

    return input_obj_codes


def extract_output_obj_codes(output_data):
    output_customer_codes = []
    output_vehicle_codes = []
    output_depot_codes = []
    output_location_codes = []

    output_routes = output_data["solutions"][0]["routes"]
    output_unscheduled_reqs = output_data["solutions"][0]["unscheduled_requests"]

    for route in output_routes:
        output_vehicle_codes.append(route["vehicle_code"])
        for element in route["elements"]:
            output_location_codes.append(element["location_code"])
            if element["location_type"] == "DEPOT":
                output_depot_codes.append(element["cd_code"])
            elif element["location_type"] == "CUSTOMER":
                output_customer_codes.append(element["cd_code"])

    for req in output_unscheduled_reqs:
        output_location_codes.append(req["pickup_location_code"])
        output_location_codes.append(req["delivery_location_code"])
        output_depot_codes.append(req["depot_code"])
        output_customer_codes.append(req["customer_code"])

    output_obj_codes = dict()
    output_obj_codes["output_customer_codes"] = output_customer_codes
    output_obj_codes["output_vehicle_codes"] = output_vehicle_codes
    output_obj_codes["output_depot_codes"] = output_depot_codes
    output_obj_codes["output_location_codes"] = output_location_codes

    return output_obj_codes


def check_input_output_match(input_data, output_data):
    input_obj_codes = extract_input_obj_codes(input_data)
    output_obj_codes = extract_output_obj_codes(output_data)

    cus_match = set(output_obj_codes["output_customer_codes"]).issubset(set(input_obj_codes["input_customer_codes"]))
    veh_match = set(output_obj_codes["output_vehicle_codes"]).issubset(set(input_obj_codes["input_vehicle_codes"]))
    dep_match = set(output_obj_codes["output_depot_codes"]).issubset(set(input_obj_codes["input_depot_codes"]))
    loc_match = set(output_obj_codes["output_location_codes"]).issubset(set(input_obj_codes["input_location_codes"]))

    io_match = cus_match and veh_match and dep_match and loc_match

    return io_match
