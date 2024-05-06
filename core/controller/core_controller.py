import dash
import dash_bootstrap_components as dbc
import importlib
import inspect
import json
import zipfile
import gzip
import dash_daq as daq
import logging
import sys
from core.controller import callbacks
from core.model import check_io_match
from core.model.core_model import CoreModel
from core.view.core_view import CoreView
from core.view import drag_and_drop_zone
from dash import dcc, html, Input, Output, State
from plugins.base_plugin.base_controller.abstract_controller import AbstractController


class CoreController:
    def __init__(self):
        self.model = CoreModel()
        self.view = CoreView()
        self.plugins_config = []
        self.plugin_objects = []
        self.tabs_switches = {
            "Input Visualization": [],
            "Output Visualization": []
        }
        self.tabs_plugins = {
            "Input Visualization": [],
            "Output Visualization": []
        }

    @staticmethod
    #load danh sách plugin
    def load_plugins_config():
        with open('plugins/config_plugins/plugins_list.json') as json_plugin_config:
            plugin_config = json.load(json_plugin_config)
        return plugin_config['plugins']

    def get_plugins(self):
        """
        load tung plugin va cho vao plugin objects list
        :return:
        """
        if self.plugins_config:
            for plugin_name in self.plugins_config:
                controller_module = importlib.import_module("plugins." + f"{plugin_name}." +
                                                            f"{plugin_name}_controller." + f"{plugin_name}_controller")
                for name, obj in inspect.getmembers(controller_module, inspect.isclass):
                    if issubclass(obj, AbstractController) and obj is not AbstractController:
                        self.plugin_objects.append(obj())
                        break

    def init_layout(self, app):
        """
        create layout
        """

        self.plugins_config = self.load_plugins_config()
        self.get_plugins()

        for plugin_obj in self.plugin_objects:
            plugin_obj.register_plugin_callbacks(app)
            plugin_layout_settings = plugin_obj.get_plugin_layout_settings()
            plugin_tab = plugin_layout_settings["tab"]
            plugin_switch = plugin_obj.get_plugin_switch()
            plugin_layout = plugin_obj.get_plugin_layout()
            self.tabs_switches[plugin_tab].append(plugin_switch)
            self.tabs_plugins[plugin_tab].append(plugin_layout)

        return self.view.create_layout(self.tabs_switches, self.tabs_plugins)

    def register_execution_callback(self, app):
        @app.callback(
            Output('validate-io-message-box', 'children'),
            Output('drag-and-drop-zone', 'children'),
            Input('render-vis-button', 'n_clicks'),
            State('input-data-storage', 'children'),
            State('output-data-storage', 'children')
        )
        def execute(render_vis_button, input_data, output_data):
            if not input_data or not output_data:
                return None, html.Div("Please upload Input & Output files")

            logging.basicConfig(level=logging.INFO, filename="logs/program_logs.log", filemode='w',
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            self.model.io_match = check_io_match.check_input_output_match(json.loads(input_data),
                                                                          json.loads(output_data))

            if not self.model.io_match:
                logging.error("Input and output data mismatch!")
                return (dbc.Alert("Input & Output files mismatch! Cannot test!", color="danger"),
                        "Input and output data mismatch!")
            else:
                logging.info("Input and output data match!")

            if not render_vis_button:
                return (dbc.Alert("Input & Output files match! Program continues!", color="success"),
                        html.Div("Please click on the Render Visualization Button"))

            self.model.init_uploaded_data_files(json.loads(input_data), json.loads(output_data))

            for plugin_obj in self.plugin_objects:
                plugin_obj.initialize_data(self.model.input_data, self.model.output_data)

            return (dbc.Alert("Input & Output files match! Program continues!", color="success"),
                    drag_and_drop_zone.create_drag_and_drop_section(self.model.input_data, self.model.routes_data,
                                                                    self.model.unscheduled_req_data))

    def register_core_callbacks(self, app):
        callbacks.register_theme_change_callback(self, app)
        callbacks.register_input_file_upload_callback(self, app)
        callbacks.register_output_file_upload_callback(self, app)
        callbacks.bind_js_callback_to_drag_drop_zone(self, app)
        callbacks.register_update_output_callback(self, app)
        callbacks.register_last_clicked_visualization_button(self, app)
