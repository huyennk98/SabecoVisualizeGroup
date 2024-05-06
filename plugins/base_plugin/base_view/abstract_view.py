from abc import ABC, abstractmethod


class AbstractView(ABC):

    @abstractmethod
    def create_boolean_switch(self):
        pass

    @abstractmethod
    def create_plugin_layout(self):
        pass
