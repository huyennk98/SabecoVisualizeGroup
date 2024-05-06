import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output


def register_feasible_heatmap_callbacks(self, app):
    @app.callback(
        Output('vehicles-dropdown', 'options'),
        Output('requests-dropdown', 'options'),
        Output('feasible-heatmap-cover', 'style'),
        Input('feasible-heatmap-switch', 'on')
    )
    def create_feasible_heatmap_options(switch):
        if self.model and switch:
            dropdown_options = self.view.create_dropdown_options(self.model.input_data)
            return dropdown_options["vehicle_options"], dropdown_options["request_options"], {}
        return [], [], {'display': 'none'}

    @app.callback(
        Output('display-feasible-heatmap', 'children'),
        [Input('vehicles-dropdown', 'value'),
        Input('requests-dropdown', 'value')]
    )
    def update_feasible_heatmap(selected_vehicles, selected_requests):
        if selected_vehicles is None or selected_requests is None:
            return "Please select both vehicles  and requests to generate the heatmap!"

        all_vehicles = self.model.input_data["vehicles"]
        all_requests = self.model.input_data["requests"]

        # Filter the vehicles and requests based on the selection
        filtered_vehicles = [v for v in all_vehicles if v["vehicleCode"] in selected_vehicles]
        filtered_requests = [r for r in all_requests if r["orderCode"] in selected_requests]
        filtered_vehicle_codes = [v['vehicleCode'] for v in filtered_vehicles]
        filtered_request_codes = [r['orderCode'] for r in filtered_requests]

        # Generate the feasibility matrix
        feasible_matrix = self.model.generate_feasible_matrix(self.model.input_data["customers"],
                                                              filtered_vehicles,
                                                              filtered_requests)

        # Create the heatmap figure
        heatmap_fig = self.view.create_visualization(feasible_matrix,
                                                     filtered_vehicle_codes,
                                                     filtered_request_codes)

        # Return the heatmap figure wrapped in a dcc.Graph component
        return dcc.Graph(figure=heatmap_fig)
