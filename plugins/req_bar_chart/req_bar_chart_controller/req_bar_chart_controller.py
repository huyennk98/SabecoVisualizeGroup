from plugins.base_plugin.base_controller.abstract_controller import AbstractController
from plugins.req_bar_chart.req_bar_chart_controller import req_bar_chart_callbacks
from plugins.req_bar_chart.req_bar_chart_model.req_bar_chart_model import ReqBarChartModel
from plugins.req_bar_chart.req_bar_chart_view.req_bar_chart_view import ReqBarChartView


class ReqBarChartController(AbstractController):
    def __init__(self):
        self.view = ReqBarChartView()
        self.model = None

    def initialize_data(self, input_data, output_data):
        self.model = ReqBarChartModel(input_data)
        self.model.process_data_model()

    def get_plugin_layout_settings(self):
        self.view.get_plugin_layout_settings()
        return self.view.layout_settings

    def get_plugin_switch(self):
        return self.view.create_plugin_switch()

    def get_plugin_layout(self):
        return self.view.create_plugin_layout()

    def register_plugin_callbacks(self, app):
        req_bar_chart_callbacks.register_req_bar_chart_callbacks(self, app)
