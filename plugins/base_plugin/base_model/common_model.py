from collections import defaultdict
from datetime import datetime


# Function to add offset to lat/lng if there are overlapping locations
def add_offset(lat, lng, index, base_offset=0.001):
    """
    Modify lat, lng to prevent duplication customer/ hub by adding index * base_offset.
    If there are 3 duplicated points, index = 0, 1, 2.
    Output:
        New lat & lng of the current point

    Example:
        >>> add_offset(10.0, 20.0, 2)
        (10.002, 20.002)
    """
    offset = base_offset * index
    return lat + offset, lng + offset

def list_of_dicts_to_plain_dict(list_dict, keyword, valuename):
    """
    Transform list of dict into plain dict via keyword and valuename
    Input: [{
            "factoryAddress": "165",
            "pdAdress": "PD-165",
            "match": 1
            },
            {
            "factoryAddress": "168",
            "pdAdress": "PD-168",
            "match": 1
            }]
    Output: {"165": "PD-165", "168": "PD-168"]}
    """

    return {
        element[keyword]: element[valuename] for element in list_dict
    }

def list_of_dicts_to_dict_of_dicts(list_dict, keyword):
    """
    Transform list of dict into dict of dict via value of a key.
    Input: [{ "locationCode":"ABC",
                "lat": 10.2,
                "lng": 105.1}]
    Output: { "ABC": {"lat": 10.2,
                    "lng": 105.1}}
    """

    return {
        element[keyword]: {
            key: value for key, value in element.items() if key != keyword
        } for element in list_dict
    }

def list_of_dicts_to_dict_of_list(list_dict, keyword, valuename):
    """
    Transform list of dict into dict of list via via keyword and valuename
    Input: [{
            "depotAddress": "D165",
            "pdAdress": "PD-165",
            "match": 1
            },
            {
            "depotAddress": "D165.2",
            "pdAdress": "PD-165",
            "match": 1
            }]
    Output: {"PD-165": ["D165", "D165.2"]}
    """

    return {
        component[keyword]: [
            element[valuename] for element in list_dict if component[keyword] == element[keyword]
        ] for component in list_dict
    }

def reverse_plain_dict_to_dict_of_list(input_dict):
    reverse_dict = {}
    for key, value in input_dict.items():
        reverse_dict.setdefault(value, []).append(key)
    return reverse_dict

def add_province_to_requests(requests, customers):
    """
    Adds province information to each request based on the customer's location code.

    This function modifies the input list of requests by adding a 'province' key to each
    request dictionary. The province is determined based on the customer's location code.
    If the location code is not found, 'Unknown' is set as the province.

    Args:
        requests (List[Dict]): A list of request dictionaries. Each request should have
                               a 'deliveryLocationCode'.
        customers (List[Dict]): A list of customer dictionaries. Each customer dictionary
                                must have 'locationCode' and 'province' keys.
    """
    # Map location codes to provinces
    location_to_province = {customer['locationCode']: customer['province'] for customer in customers}

    # Add province information to each request
    for request in requests:
        delivery_location = request.get('deliveryLocationCode')
        request['province'] = location_to_province.get(delivery_location, 'Unknown')

def calculate_total_loads(requests):
    """
    Calculates and adds the total weight and volume for each request in the provided list.

    This function iterates through each request, summing the weights and volumes of items
    and then adds those sums as 'totalWeight' and 'totalVolume' entries in each request dictionary.
    The input list of requests is modified in-place.

    Args:
        requests (List[Dict]): A list of request dictionaries. Each request dictionary should
                               contain an 'items' key, which is a list of items. Each item is
                               expected to have a 'weight' and 'cbm' key.
    """
    for request in requests:
        # Calculate the total weight and volume for each request
        total_weight = sum(item["weight"] for item in request['items'])
        total_volume = sum(item["cbm"] for item in request['items'])

        # Update the request dictionary with the calculated totals
        request['totalWeight'] = total_weight
        request['totalVolume'] = total_volume

def get_unique_provinces_from_requests(requests):
    """
    Extracts a sorted list of unique provinces from a list of requests.

    This function goes through each request in the provided list, extracts the
    'province' value, and then returns a sorted list of unique province names.

    Args:
        requests (List[dict]): A list of dictionaries, where each dictionary represents
                               a request and contains a 'province' key.

    Returns:
        List[str]: A sorted list of unique province names extracted from the requests.
    """
    # Extract unique provinces using a set comprehension and sort the result
    unique_provinces = sorted({request['province'] for request in requests})

    return unique_provinces

def group_customers_by_province(customers):
    """
    Groups customers by their respective provinces.

    This function takes a list of customer dictionaries and returns a dictionary mapping
    provinces to lists of customers belonging to those provinces.

    Args:
        customers (List[Dict]): A list of customer dictionaries, each containing at least
                                a 'province' key.

    Returns:
        Dict[str, List[Dict]]: A dictionary mapping provinces to lists of customers from
                               that province.
    """
    provinces_to_customers = defaultdict(list)

    for customer in customers:
        province = customer['province']
        provinces_to_customers[province].append(customer)

    return provinces_to_customers

def group_requests_by_customer(requests):
    """
    Groups and summarizes delivery requests by location.

    Each request dictionary should contain 'deliveryLocationCode', 'totalWeight',
    and 'totalVolume'. The function returns a dictionary mapping each delivery location
    to its aggregated requests and summaries.

    Args:
        requests (List[Dict]): A list of request dictionaries.

    Returns:
        Dict[str, Dict]: A dictionary mapping delivery locations to their requests
                         and aggregated summaries (total weight and volume).
    """

    customers_to_requests = defaultdict(lambda: {
        'requests': [],
        'totalWeight': 0,
        'totalVolume': 0
    })

    for request in requests:
        location = request['deliveryLocationCode']
        customers_to_requests[location]['requests'].append(request)
        customers_to_requests[location]['totalWeight'] += request['totalWeight']
        customers_to_requests[location]['totalVolume'] += request['totalVolume']

    return customers_to_requests


def convert_ton_string_to_kg(ton_string):
    # Convert "5T" to 5000 (kg)
    # Tại sao lại có cặp try-except này? Trường hợp mà khách hàng không cấm tải => Cho limited_weight lên rất lớn
    try:
        return int(float(ton_string.upper().replace('T', '')) * 1000)
    except:
        return 1000000


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Function to convert string time to datetime
def str_to_datetime(timestring):
    return datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
