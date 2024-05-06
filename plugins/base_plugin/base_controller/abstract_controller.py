from abc import ABC, abstractmethod


class AbstractController(ABC):

    @abstractmethod
    def initialize_data(self, input_data, output_data):
        pass

    @abstractmethod
    def get_plugin_layout_settings(self):
        pass

    @abstractmethod
    def get_plugin_switch(self):
        pass

    @abstractmethod
    def get_plugin_layout(self):
        pass

    @abstractmethod
    def register_plugin_callbacks(self, app):
        pass
