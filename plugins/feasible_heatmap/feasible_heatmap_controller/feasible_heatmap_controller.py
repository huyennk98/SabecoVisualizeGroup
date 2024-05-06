from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.feasible_heatmap.feasible_heatmap_controller import feasible_heatmap_callbacks
from plugins.feasible_heatmap.feasible_heatmap_model.feasible_heatmap_model import FeasibleHeatmapModel
from plugins.feasible_heatmap.feasible_heatmap_view.feasible_heatmap_view import FeasibleHeatmapView

class FeasibleHeatmapController(AbstractController):
    def __init__(self):
        self.view = FeasibleHeatmapView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = FeasibleHeatmapModel(input_data)
        self.model.process_data_model()

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        # self.route_map_view.create_dropdown_options(self.route_map_model.input_data)
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        feasible_heatmap_callbacks.register_feasible_heatmap_callbacks(self, app)
