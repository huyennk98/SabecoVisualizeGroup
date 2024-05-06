from core.view import drag_and_drop_cards


def create_drag_and_drop_section(input_data, routes_info, unscheduled_req_info):
    color_info = drag_and_drop_cards.map_province_to_color(input_data)
    layout_components, unscheduled_reqs = [], []
    request_number = 1

    # Get the routes and scheduled requests of each route
    for route_id, route in enumerate(routes_info):
        # Non-draggable vehicle info as a separate element
        vehicle_label = drag_and_drop_cards.make_vehicle_label(route_id+1, route)
        request_cards = []
        for element in route['elements']:
            if element["location_type"] == "CUSTOMER":
                req_card, tooltip = drag_and_drop_cards.make_request_card("scheduled", element, request_number,
                                                                    color_info)
                request_cards.extend([req_card, tooltip]) # Add the request card & tooltip to the list
                request_number += 1

        # Create a sub-container for just the request cards to allow horizontal layout
        requests_container = drag_and_drop_cards.make_requests_container(route_id+1, request_cards)

        # Container of the whole route (Vehicle + Associated Requests)
        route_container = drag_and_drop_cards.make_route_container(route_id+1, vehicle_label, requests_container)

        layout_components.append(route_container)

    # Get the unscheduled requests & their container
    for request in unscheduled_req_info:
        req_card, tooltip = drag_and_drop_cards.make_request_card("unscheduled", request, request_number,
                                                            color_info)
        unscheduled_reqs.extend([req_card, tooltip]) # Add the request card & tooltip to the list
        request_number += 1

    # Create a sub-container for just the request cards to allow horizontal layout
    unscheduled_reqs_container = drag_and_drop_cards.make_unscheduled_requests_container(unscheduled_reqs)

    # Container of the unscheduled requests (Label + Unscheduled Request Cards)
    unscheduled_reqs_zone = drag_and_drop_cards.make_unscheduled_requests_zone(unscheduled_reqs_container)

    layout_components.append(unscheduled_reqs_zone)

    return layout_components
