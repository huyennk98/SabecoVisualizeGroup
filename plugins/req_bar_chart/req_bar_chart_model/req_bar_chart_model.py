import pandas as pd
from plugins.base_plugin.base_model import common_model


class ReqBarChartModel:
    def __init__(self, data):
        self.input_data = data
        self.lat_lng_dict = {}
        self.map_center = None
        self.tco_to_pd_mapping = {}
        self.request_dataframe = None
        self.unique_provinces = []

    def process_request_dataframe(self, requests):

        # Convert the requests data into a DataFrame
        requests_df = pd.DataFrame(requests)

        # Ensure that 'province' is a categorical type for consistent color mapping and sorting
        requests_df['province'] = pd.Categorical(requests_df['province'],
                                                 categories=requests_df['province'].unique(),
                                                 ordered=True)

        self.request_dataframe = requests_df

    def get_unique_provinces(self):
        self.unique_provinces = sorted(self.request_dataframe['province'].unique())

    @staticmethod
    def sort_request_dataframe(dataframe, settings):
        # Extract sort criteria
        sort_criteria = settings["chart_category"] if settings["sort_by"] == "load" else settings["sort_by"]

        # Sort the DataFrame based on the province code in ascending order
        dataframe.sort_values(sort_criteria, ascending=settings["sort_order"], inplace=True)

    def process_data_model(self):
        common_model.calculate_total_loads(self.input_data["requests"])
        common_model.add_province_to_requests(self.input_data["requests"], self.input_data["customers"])
        self.process_request_dataframe(self.input_data["requests"])
        self.get_unique_provinces()
