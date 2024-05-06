import dash_bootstrap_components as dbc
import itertools
from common.styles import card_styles, colors


# NOTE: UPDATE LẠI PHẦN NÀY (ĐỂ TÁCH PHẦN XỬ LÝ DATA RA KHỎI VIEW, SẼ UPDATE LẠI Ở PHẦN OUTPUT_PROCESSING TRONG MODEL)
# => THIẾT KẾ DATA MODEL CHO CẨN THẬN ĐỂ TRÁNH NHẬP NHẰNG
# Cải thiện lại data dist_map_model để viết lại hàm này
def map_province_to_color(input_data):
    province_colors = colors.BOOTSTRAP_COLOR_ARRAY
    unique_provinces = sorted({customer['province'] for customer in input_data['customers']})

    province_colors_dict = dict()
    for index, province in enumerate(unique_provinces):
        # Use modulo operator to cycle through colors_array
        color = province_colors[index % len(province_colors)]
        province_colors_dict[province] = color

    color_info = dict()
    color_info["dict_province"] = {customer['province']: customer['cType']['typeOfCustomerByArea'] for customer in
                                   input_data['customers']}
    # color_info["province_color_map"] = {province: color for province, color in zip(unique_provinces, province_colors)}
    color_info["province_color_map"] = province_colors_dict
    color_info["province_mapping"] = {customer['locationCode']: customer['province'] for customer in
                                      input_data["customers"]}

    return color_info

# Cải thiện lại data dist_map_model để viết lại hàm này
def get_request_tooltip_message(request_type, request, request_number, province):
    delivery_location_code = request['location_code'] if request_type == "scheduled" else (
        request)['delivery_location_code']
    request_cbm = sum([item["cbm"] for item in request["items"]])
    request_weight = sum([item["weight"] for item in request["items"]])

    tooltip_message = (
        f"Request #{request_number} Information: \n"
        f"1. Delivery Location Code: {delivery_location_code} \n"
        f"2. Province: {province} \n"
        f"3. Weight: {request_weight / 1000} kg \n"
        f"4. Cbm: {request_cbm / 1000000} m3"
    )

    return tooltip_message


def get_vehicle_tooltip_message(vehicle_index, vehicle_info):
    vehicle_code = vehicle_info["vehicle_code"]
    vehicle_cbm = vehicle_info["vehicle_cbm"]
    vehicle_weight = vehicle_info["vehicle_weight"]

    tooltip_message = (
        f"Vehicle #{vehicle_index} Information: \n"
        f"1. Vehicle Code: {vehicle_code} \n"
        f"2. Vehicle Weight: {vehicle_weight / 1000} kg \n"
        f"3. Vehicle Cbm: {vehicle_cbm / 1000000} m3"
    )

    return tooltip_message


def make_request_card(request_type, request, request_number, color_info):
    # Make request card
    request_location = request['location_code'] if request_type == "scheduled" else request['delivery_location_code']
    province = color_info["province_mapping"].get(request_location, 'default')
    card_color = color_info["province_color_map"].get(province)  # Default color if province not found
    updated_card_style = card_styles.REQUEST_CARD_STYLE.copy()
    request_card = dbc.Card(
        f"Request #{request_number}",
        className='draggable-card',
        color=card_color,
        id=f"request-{request_number}",
        style=updated_card_style
    )

    # Create tooltip
    tooltip_message = get_request_tooltip_message(request_type, request, request_number, province)
    tooltip = dbc.Tooltip(tooltip_message, className="tooltip_inner", target=f"request-{request_number}")

    return request_card, tooltip


def make_requests_container(route_index, request_cards):
    return dbc.Card(id=f'route-{route_index}', className='route-draggable-area', children=request_cards,
                    style=card_styles.ROUTE_CONTAINER_STYLE)


def make_unscheduled_requests_container(request_cards):
    return dbc.Card(id='unscheduled-reqs-container', className='route-draggable-area', children=request_cards,
                    style=card_styles.ROUTE_CONTAINER_STYLE)


def make_route_container(route_index, vehicle_label, requests_container):
    container_children = [dbc.Col(vehicle_label, width="auto"), dbc.Col(requests_container, width=True)]

    return dbc.Card(id=f'container-{route_index}', children=dbc.Row(container_children),
                    style={'alignItems': 'left', 'display': 'flex', 'justifyContent': 'start'})


def make_unscheduled_requests_zone(requests_container):
    container_children = [dbc.Col(make_unscheduled_label(), width="auto"), dbc.Col(requests_container, width=True)]

    return dbc.Card(id='unscheduled-reqs-zone', children=dbc.Row(container_children),
                    style={'alignItems': 'left', 'display': 'flex', 'justifyContent': 'start'})


def make_vehicle_label(route_index, route_info):
    vehicle_info = dbc.Card(
        f"Vehicle #{route_index}",
        id=f"vehicle-{route_index}",
        style=card_styles.VEHICLE_CARD_STYLE
    )

    vehicle_tooltip_message = get_vehicle_tooltip_message(route_index, route_info)
    vehicle_tooltip = dbc.Tooltip(vehicle_tooltip_message, className="tooltip_inner", target=f"vehicle-{route_index}")

    vehicle_label = dbc.Card(
        id=f'vehicle-container-{route_index}',
        className='vehicle-container',
        children=[vehicle_info, vehicle_tooltip],  # Vehicle info followed by request cards,
        style=card_styles.ROUTE_CONTAINER_STYLE
    )

    return vehicle_label


def make_unscheduled_label():
    unscheduled_reqs_info = dbc.Card(f"Unscheduled Requests", id="unscheduled-requests",
                                     style=card_styles.VEHICLE_CARD_STYLE)

    unscheduled_tooltip = dbc.Tooltip("These requests haven't been assigned to any vehicle yet!",
                                      className="tooltip_inner", target="unscheduled-requests")

    unscheduled_reqs_info_container = dbc.Card(id="unscheduled-requests-container",
                                               className='unscheduled-requests-container',
                                               children=[unscheduled_reqs_info, unscheduled_tooltip],
                                               style=card_styles.ROUTE_CONTAINER_STYLE)

    return unscheduled_reqs_info_container
