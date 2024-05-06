def convert_distance_time_matrices(distances):
    dist_dict, time_dict = dict(), dict()
    for entry in distances:
        src, dest = entry["srcCode"], entry["destCode"]
        if src not in dist_dict:
            dist_dict[src] = {}
        if src not in time_dict:
            time_dict[src] = {}
        dist_dict[src][dest] = entry["distance"]
        time_dict[src][dest] = entry["travelTime"]
        dist_dict[src][src] = 0
        time_dict[src][src] = 0
    return dist_dict, time_dict


def convert_request_format(depot_code, request, request_type):
    # Common extraction for both scheduled and unscheduled data
    items = request.get('items', [])
    # Extracting data based on whether it's an unscheduled request or a route element
    if request_type == "unscheduled":
        customer_code = request.get('customer_code', '')
        delivery_location_code = request.get('delivery_location_code', '')
        total_cbm = request.get('cbm', 0)
        total_weight = request.get('weight', 0)
    else:
        customer_code = request.get('cd_code', '')
        delivery_location_code = request.get('location_code', '')
        total_cbm = sum(item['cbm'] for item in items)
        total_weight = sum(item['weight'] for item in items)
    # Building the formatted_request structure
    formatted_request = {
        "customer_code": customer_code,
        "depot_code": depot_code,
        "pickup_location_code": depot_code,  # Assuming this is the same for all
        "delivery_location_code": delivery_location_code,
        "location_code": delivery_location_code,
        "items": items,
        "total_cbm": total_cbm,
        "total_weight": total_weight,
    }
    return formatted_request


def convert_scheduled_request(request):
    return {
        "cd_code": request["customer_code"],
        "location_code": request["location_code"],
        "location_type": "CUSTOMER",
        "items": request["items"]
    }


def convert_unscheduled_request(request):
    converted_request = {
        "customer_code": request["customer_code"],
        "depot_code": request["depot_code"],
        "pickup_location_code": request["pickup_location_code"],  # Assuming this is the same for all
        "delivery_location_code": request["delivery_location_code"],
        "items": request["items"],
        "cbm": request["total_cbm"],
        "weight": request["total_weight"],
        "order_code": "N/A"
    }
    return converted_request