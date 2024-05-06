import dash
import json
from dash import dcc, html, Input, Output, State
from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.timeline_table.timeline_table_model.timeline_table_model import TimelineTableModel
from plugins.timeline_table.timeline_table_view.timeline_table_view import TimelineTableView


class TimelineTableController(AbstractController):
    def __init__(self):
        self.view = TimelineTableView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = TimelineTableModel(input_data, output_data, output_data["solutions"][0]["routes"])

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        @app.callback(
            Output('display-timeline-table', 'children'),
            Input('vis-init-routes-button', 'n_clicks'),
            Input('get-updated-routes-button', 'n_clicks'),
            Input('timeline-table-switch', 'on'),
            State('json-output-store', 'data'),
        )
        def update_timeline_table(init_routes_button, updated_routes_button, switch, new_output_data):
            if self.model and switch:
                ctx = dash.callback_context
                trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

                if not new_output_data or trigger_id == 'vis-init-routes-button':
                    timeline_table_input_data = self.model.processing_data_to_view(self.model.routes_data)
                    return self.view.draw_timeline_table(timeline_table_input_data)

                new_output_data = json.loads(new_output_data)
                new_routes_data = new_output_data["solutions"][0]["routes"]
                new_timeline_table_input_data = self.model.processing_data_to_view(new_routes_data)
                return self.view.draw_timeline_table(new_timeline_table_input_data)
            else:
                return None

        @app.callback(
            Output('timeline-table-cover', 'style'),
            Input('timeline-table-switch', 'on')
        )
        def timeline_table_display(switch):
            if switch:
                return {}
            else:
                return {'display': 'none'}