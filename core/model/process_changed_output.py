import copy
from common.samples import sample_elements
from core.model import conversion_functions


def calculate_load_time(vehicle_data, depot_info, weight_load, cbm_load):
    vehicle_load_time_weight = vehicle_data["loadTimePerTon"] * weight_load / 1000000
    vehicle_load_time_cbm = vehicle_data["loadTimePerCbm"] * cbm_load / 1000000
    depot_load_time_weight = depot_info["loadTimePerTon"] * weight_load / 1000000
    depot_load_time_cbm = depot_info["loadTimePerCbm"] * cbm_load / 1000000
    load_time = depot_info["fixedLoadTime"] + max(vehicle_load_time_weight, vehicle_load_time_cbm,
                                                  depot_load_time_weight, depot_load_time_cbm)

    return load_time


def calculate_unload_time(vehicle_data, customer_info, weight_load, cbm_load):
    vehicle_unload_time_weight = vehicle_data["unloadTimePerTon"] * weight_load / 1000000
    vehicle_unload_time_cbm = vehicle_data["unloadTimePerCbm"] * cbm_load / 1000000
    customer_unload_time_weight = customer_info["unloadTimePerTon"] * weight_load / 1000000
    customer_unload_time_cbm = customer_info["unloadTimePerCbm"] * cbm_load / 1000000
    unload_time = customer_info["fixedUnloadTime"] + max(vehicle_unload_time_weight, vehicle_unload_time_cbm,
                                                         customer_unload_time_weight, customer_unload_time_cbm)

    return unload_time


def extract_all_requests_and_vehicles(input_data, routes_info):
    all_elements, all_vehicles = dict(), dict()
    depot_code = input_data["depots"][0]["depotCode"]
    request_number, vehicle_number = 1, 1
    for route in routes_info["routes"]:
        vehicle_key = f"vehicle-{vehicle_number}"
        vehicle_data = next((v for v in input_data["vehicles"] if v["vehicleCode"] == route["vehicle_code"]), None)
        all_vehicles[vehicle_key] = dict()
        all_vehicles[vehicle_key]["vehicle_code"] = route["vehicle_code"]
        all_vehicles[vehicle_key]["vehicle_cbm"] = route["vehicle_cbm"]
        all_vehicles[vehicle_key]["vehicle_weight"] = route["vehicle_weight"]
        all_vehicles[vehicle_key]["vehicle_data"] = vehicle_data
        vehicle_number += 1
        for element in route["elements"]:
            if element["location_type"] == "CUSTOMER":
                request_key = f"request-{request_number}"
                all_elements[request_key] = conversion_functions.convert_request_format(depot_code, element, "scheduled")
                request_number += 1
    for request in routes_info["unscheduled_requests"]:
        request_key = f"request-{request_number}"
        all_elements[request_key] = conversion_functions.convert_request_format(depot_code, request, "unscheduled")
        request_number += 1
    return all_elements, all_vehicles


def get_necessary_elements():
    necessary_elements = dict()
    necessary_elements["route_start_element"] = copy.deepcopy(sample_elements.ROUTE_START_INFO)
    necessary_elements["depot_loading_element"] = copy.deepcopy(sample_elements.ROUTE_DEPOT_LOADING)
    necessary_elements["route_end_element"] = copy.deepcopy(sample_elements.ROUTE_END_INFO)
    return necessary_elements


def update_element(current_element, new_element):
    current_element["cd_code"] = new_element["cd_code"] if "cd_code" in new_element.keys() else new_element["customer_code"]
    current_element["location_code"] = new_element["location_code"]
    current_element["arrival_time"] = new_element["leaving_time"]
    current_element["leaving_time"] = new_element["leaving_time"]


def update_route_basic_info(current_route, init_route):
    current_route["additional_cost"] = init_route["additional_cost"]
    current_route["bounding_box"] = init_route["bounding_box"]
    current_route["main_cost"] = init_route["main_cost"]
    current_route["moq_status"] = init_route["moq_status"]
    current_route["total_cost"] = init_route["total_cost"]
    current_route["total_item_cost"] = init_route["total_item_cost"]
