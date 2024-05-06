from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.dist_map.dist_map_controller import dist_map_callbacks
from plugins.dist_map.dist_map_model.dist_map_model import DistMapModel
from plugins.dist_map.dist_map_view.dist_map_view import DistMapView


class DistMapController(AbstractController):
    def __init__(self):
        self.view = DistMapView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = DistMapModel(input_data)
        self.model.process_data_model()

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        dist_map_callbacks.register_dist_map_callbacks(self, app)
