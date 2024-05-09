from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.scatter_map.scatter_map_controller import scatter_map_callbacks
from plugins.scatter_map.scatter_map_model.scatter_map_model import ScatterMapModel
from plugins.scatter_map.scatter_map_view.scatter_map_view import ScatterMapView

class ScatterMapController(AbstractController):
    def __init__(self):
        self.view = ScatterMapView()
        self.model = None
    
    def initialize_data(self, input_data):
        self.model = ScatterMapModel(input_data)
        self.model.process_data_model()

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        scatter_map_callbacks.register_scatter_map_callbacks(self, app)
