from abc import ABC, abstractmethod


class AbstractModel(ABC):
    @abstractmethod
    def process_data_model(self):
        pass
