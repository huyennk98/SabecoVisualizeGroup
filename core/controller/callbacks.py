import base64
import copy
import dash
import json
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash import html, Input, Output, State, no_update
from dash.dependencies import ClientsideFunction
from datetime import datetime, timedelta
from common.samples import sample_elements
from core.model import conversion_functions, process_changed_output, read_file_functions


def register_theme_change_callback(self, app):
    @app.callback(
        [Output('theme', 'href')],
        [Input(ThemeChangerAIO.ids.radio("theme"), 'value')],
        prevent_initial_call=True
    )
    def update_theme(theme):
        if theme is None:
            raise dash.exceptions.PreventUpdate
        return theme

def register_input_file_upload_callback(self, app):
    @app.callback(
        [Output('input-data-storage', 'children'),
         Output('input-upload-message-box', 'children')],
        [Input('upload-input-data', 'contents')],
        [State('upload-input-data', 'filename')]
    )
    def upload_input_file(contents, filename):
        if contents is None:
            return None, html.Div()

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        if (filename.endswith('.json') or filename.endswith('.zip') or filename.endswith('.gz') or
                filename.endswith('.gzip')):
            input_data_file = read_file_functions.read_json_from_archive(filename, decoded)
            return json.dumps(input_data_file), dbc.Alert(
                                                    html.Span([
                                                        "Input file uploaded and parsed successfully! ",
                                                        html.Span("✓", style={"color": "green",
                                                                              "fontSize": "24px",
                                                                              "fontWeight": "900",
                                                                              "marginRight": "5px"}),
                                                    ]),
                                                    color="secondary"
                                                )
        else:
            return None, dbc.Alert("Invalid input file type. Please upload a .json or .zip / .gz / .gzip file "
                                   "containing .json files.", color="danger")

def register_output_file_upload_callback(self, app):
    @app.callback(
        [Output('output-data-storage', 'children'),
         Output('output-upload-message-box', 'children')],
        [Input('upload-output-data', 'contents')],
        [State('upload-output-data', 'filename')]
    )
    def upload_output_file(contents, filename):
        if contents is None:
            return None, html.Div()

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        if (filename.endswith('.json') or filename.endswith('.zip') or filename.endswith('.gz') or
                filename.endswith('.gzip')):
            output_data_file = read_file_functions.read_json_from_archive(filename, decoded)
            return json.dumps(output_data_file), dbc.Alert(
                                                    html.Span([
                                                        "Output file uploaded and parsed successfully! ",
                                                        html.Span("✓", style={"color": "green",
                                                                              "fontSize": "24px",
                                                                              "fontWeight": "900",
                                                                              "marginRight": "5px"}),
                                                    ]),
                                                    color="secondary"
                                                )
        else:
            return None, dbc.Alert("Invalid output file type. Please upload a .json or .zip / .gz / .gzip file "
                                   "containing .json files.", color="danger")


def bind_js_callback_to_drag_drop_zone(self, app):
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='change_draggable_zone'
        ),
        Output('drag-and-drop-data-store', 'data'),
        [Input("drag-and-drop-zone", "id")] + [Input("get-updated-routes-button", "n_clicks")]
    )

def register_last_clicked_visualization_button(self, app):
    @app.callback(
        Output('last-clicked-vis-button', 'children'),
        Input('vis-init-routes-button', 'n_clicks'),
        Input('get-updated-routes-button', 'n_clicks')
    )
    def get_last_clicked_visualization_button(init_routes_button, updated_routes_button):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'vis-init-routes-button':
            return 'vis-init-routes-button'
        elif trigger_id == 'get-updated-routes-button':
            return 'get-updated-routes-button'

# Update JSON Output after drag-and-drop
# HÀM CALLBACK NÀY KHÁ LẰNG NHẰNG! CÓ CÁCH NÀO ĐỂ REFACTOR LẠI HAY THIẾT KẾ LẠI ĐỂ TINH GỌN HƠN?
# Thiết kế core dist_map_model ntn để hàm này đỡ phải rối ntn?
def register_update_output_callback(self, app):
    @app.callback(
        Output('json-output-store', 'data'),
        Input('drag-and-drop-data-store', 'data')
    )
    def update_routes(stored_data):
        if not self.model.output_data:
            raise dash.exceptions.PreventUpdate

        # Parsing the data received from the client-side callback
        updated_data = json.loads(stored_data)

        # Process necessary data here!
        depot_info = self.model.input_data["depots"][0]
        dist_matrix, time_matrix = conversion_functions.convert_distance_time_matrices(self.model.input_data["distances"])
        all_requests, all_vehicles = process_changed_output.extract_all_requests_and_vehicles(self.model.input_data,
                                                                                              self.model.output_data["solutions"][0])

        # Initialize important route elements
        route_start_info = sample_elements.ROUTE_START_INFO
        route_depot_loading = sample_elements.ROUTE_DEPOT_LOADING
        route_end_info = sample_elements.ROUTE_END_INFO

        # Add some ìnormation here
        route_start_info["arrival_time"] = depot_info["workingTime"]["start"]
        route_start_info["cd_code"] = depot_info["depotCode"]
        route_start_info["leaving_time"] = depot_info["workingTime"]["start"]
        route_start_info["location_code"] = depot_info["locationCode"]

        route_depot_loading["arrival_time"] = depot_info["workingTime"]["start"]
        route_depot_loading["cd_code"] = depot_info["depotCode"]
        route_depot_loading["location_code"] = depot_info["locationCode"]

        # Initialize a list to hold messages for the message board
        new_routes, unscheduled_reqs = [], []
        new_solution, new_output = dict(), dict()
        new_output["solutions"] = []

        # Iterate over each route and extract request and vehicle information
        for route, requests in updated_data.items():
            if route != "unscheduled-reqs-container":
                cumulative_distance, cumulative_time = 0, 0
                all_items_buffer, request_buffer = [], []
                data_storage_temp, last_request_info = dict(), None
                route_index = int(route.split('-')[1])  # Extract route index (e.g., 'route-1')

                # Getting necessary elements & vehicle info
                route_core_elements = process_changed_output.get_necessary_elements()
                vehicle_info = all_vehicles[f'vehicle-{route_index}']

                for request_id in requests:
                    request_info = all_requests[request_id]
                    all_items_buffer.extend(request_info['items'])

                route_weight_load = sum(item['weight'] for item in all_items_buffer)
                route_cbm_load = sum(item['cbm'] for item in all_items_buffer)
                load_time = process_changed_output.calculate_load_time(vehicle_info["vehicle_data"],
                                                                       depot_info, route_weight_load, route_cbm_load)

                arrival_time_obj = datetime.strptime(route_core_elements["depot_loading_element"]["arrival_time"],
                                                     "%Y-%m-%d %H:%M:%S")
                leaving_time_obj = arrival_time_obj + timedelta(seconds=load_time)
                route_depot_loading_info = copy.deepcopy(route_depot_loading)

                route_depot_loading_info["leaving_time"] = leaving_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                route_depot_loading_info["items"] = all_items_buffer
                route_depot_loading_info["cbm_load"] = route_cbm_load
                route_depot_loading_info["weight_load"] = route_weight_load

                for request_id in requests:
                    request_info = all_requests[request_id]

                    request_info = conversion_functions.convert_scheduled_request(request_info)
                    customer_code = request_info["location_code"]
                    request_weight = sum(item['weight'] for item in request_info["items"])
                    request_cbm = sum(item['cbm'] for item in request_info["items"])
                    customer_info = next((c for c in self.model.input_data["customers"] if c["locationCode"] == customer_code),
                                         None)
                    unload_time = process_changed_output.calculate_unload_time(vehicle_info["vehicle_data"],
                                                                               customer_info, request_weight, request_cbm)

                    # Calculate arrival and leaving time
                    if last_request_info is None:  # First request
                        arrival_time_obj = datetime.strptime(route_depot_loading_info["leaving_time"],
                                                             "%Y-%m-%d %H:%M:%S") + timedelta(
                            seconds=time_matrix[route_depot_loading_info["location_code"]][customer_code])
                        cumulative_distance += dist_matrix[route_depot_loading_info["location_code"]][customer_code]
                    else:  # Subsequent requests
                        arrival_time_obj = datetime.strptime(last_request_info["leaving_time"],
                                                             "%Y-%m-%d %H:%M:%S") + timedelta(
                            seconds=time_matrix[last_request_info["location_code"]][customer_code])
                        cumulative_distance += dist_matrix[last_request_info["location_code"]][customer_code]

                    leaving_time_obj = arrival_time_obj + timedelta(seconds=unload_time)
                    request_info["arrival_time"] = arrival_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                    request_info["leaving_time"] = leaving_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                    request_info["distance"] = int(cumulative_distance * 1000)
                    request_info["cbm_load"] = route_cbm_load - request_cbm
                    request_info["weight_load"] = route_weight_load - request_weight

                    request_buffer.append(request_info)

                    route_weight_load -= request_weight
                    route_cbm_load -= request_cbm
                    last_request_info = request_info

                route_ending_info = copy.deepcopy(route_end_info)

                if not last_request_info:
                    process_changed_output.update_element(route_ending_info, route_depot_loading_info)
                    route_ending_info["cd_code"] = route_depot_loading_info["cd_code"]
                    route_ending_info["location_code"] = route_depot_loading_info["location_code"]
                    route_ending_info["arrival_time"] = route_depot_loading_info["leaving_time"]
                    route_ending_info["leaving_time"] = route_depot_loading_info["leaving_time"]
                else:
                    process_changed_output.update_element(route_ending_info, last_request_info)
                    route_ending_info["cd_code"] = last_request_info["cd_code"]
                    route_ending_info["location_code"] = last_request_info["location_code"]
                    route_ending_info["arrival_time"] = last_request_info["leaving_time"]
                    route_ending_info["leaving_time"] = last_request_info["leaving_time"]
                    route_ending_info["distance"] = int(cumulative_distance * 1000)

                start_timestamp = datetime.strptime(route_start_info["arrival_time"], "%Y-%m-%d %H:%M:%S")
                end_timestamp = datetime.strptime(route_ending_info["leaving_time"], "%Y-%m-%d %H:%M:%S")

                route = dict()
                process_changed_output.update_route_basic_info(route, self.model.routes_data[route_index - 1])
                route["elements"] = [route_start_info, route_depot_loading_info]
                route["elements"].extend(request_buffer)
                route["elements"].append(route_ending_info)
                route["total_distance"] = int(cumulative_distance * 1000)  # Example
                route["total_duration"] = int((end_timestamp - start_timestamp).total_seconds())  # Example
                route["total_cbm_load"] = route_depot_loading_info["cbm_load"]
                route["total_weight_load"] = route_depot_loading_info["weight_load"]
                route["vehicle_code"] = vehicle_info["vehicle_code"]
                route["vehicle_cbm"] = vehicle_info["vehicle_cbm"]
                route["vehicle_weight"] = vehicle_info["vehicle_weight"]

                new_routes.append(route)

            else:
                for req in requests:
                    unscheduled_reqs.append(conversion_functions.convert_unscheduled_request(all_requests[req]))

        new_solution["routes"] = new_routes
        new_solution["unscheduled_requests"] = unscheduled_reqs
        new_output["solutions"].append(new_solution)

        return json.dumps(new_output)
