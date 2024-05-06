import dash
import json
from dash import dcc, html, Input, Output, State
from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.fishbone_table.fishbone_table_model.fishbone_table_model import FishboneTableModel
from plugins.fishbone_table.fishbone_table_view.fishbone_table_view import FishboneTableView


class FishboneTableController(AbstractController):
    def __init__(self):
        self.view = FishboneTableView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = FishboneTableModel(input_data, output_data, output_data["solutions"][0]["routes"])

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        @app.callback(
            Output('display-fishbone-table', 'children'),
            Input('vis-init-routes-button', 'n_clicks'),
            Input('get-updated-routes-button', 'n_clicks'),
            Input('fishbone-table-switch', 'on'),
            State('json-output-store', 'data'),
        )
        def update_fishbone_table(init_routes_button, updated_routes_button, switch, new_output_data):
            if self.model and switch:
                ctx = dash.callback_context
                trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

                if not new_output_data or trigger_id == 'vis-init-routes-button':
                    fishbone_table_input_data = self.model.process_data_model(self.model.routes_data)
                    return self.view.draw_fishbone_table(fishbone_table_input_data)

                new_output_data = json.loads(new_output_data)
                new_routes_data = new_output_data["solutions"][0]["routes"]
                new_fishbone_table_input_data = self.model.process_data_model(new_routes_data)
                return self.view.draw_fishbone_table(new_fishbone_table_input_data)
            else:
                return None

        @app.callback(
            Output('fishbone-table-cover', 'style'),
            Input('fishbone-table-switch', 'on')
        )
        def fishbone_table_display(switch):
            if switch:
                return {}
            else:
                return {'display': 'none'}