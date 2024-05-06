import dash
import json
from dash import dcc, html, Input, Output, State
from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.loading_3d_check_table.loading_3d_check_table_model.loading_3d_check_table_model import Loading3DCheckTableModel
from plugins.loading_3d_check_table.loading_3d_check_table_view.loading_3d_check_table_view import Loading3DCheckTableView


class Loading3DCheckTableController(AbstractController):
    def __init__(self):
        self.view = Loading3DCheckTableView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = Loading3DCheckTableModel(input_data, output_data, output_data["solutions"][0]["routes"])

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        @app.callback(
            Output('display-loading-3d-check-table', 'children'),
            Input('vis-init-routes-button', 'n_clicks'),
            Input('get-updated-routes-button', 'n_clicks'),
            Input('loading-3d-check-table-switch', 'on'),
            State('json-output-store', 'data'),
        )
        def update_loading_3d_check_table(init_routes_button, updated_routes_button, switch, new_output_data):
            if self.model and switch:
                ctx = dash.callback_context
                trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

                if not new_output_data or trigger_id == 'vis-init-routes-button':
                    loading_3d_check_table_input_data = self.model.processing_data_to_view(self.model.routes_data)
                    return self.view.draw_weight_limit_table(loading_3d_check_table_input_data)

                new_output_data = json.loads(new_output_data)
                new_routes_data = new_output_data["solutions"][0]["routes"]
                new_loading_3d_check_table_input_data = self.model.processing_data_to_view(new_routes_data)
                return self.view.draw_weight_limit_table(new_loading_3d_check_table_input_data)
            else:
                return None

        @app.callback(
            Output('loading-3d-check-table-cover', 'style'),
            Input('loading-3d-check-table-switch', 'on')
        )
        def loading_3d_check_table_display(switch):
            if switch:
                return {}
            else:
                return {'display': 'none'}
