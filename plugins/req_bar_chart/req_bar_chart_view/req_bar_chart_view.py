import dash_bootstrap_components as dbc
import dash_daq as daq
import json
from common.styles import colors
from components.bar_chart import bar_chart, bar_traces
from dash import dcc, html
from plugins.base_plugin.constants import base_data_const, base_display_const
from plugins.base_plugin.base_view import common_view
from plugins.req_bar_chart.constants import display_const


class ReqBarChartView:
    def __init__(self):
        self.color_array = colors.PLOTLY_GO_COLOR
        self.province_colors = {}
        self.tooltip_texts = []
        self.display_settings = {}
        self.layout_settings = {}

    def get_plugin_layout_settings(self):
        # print("Current dir: " + os.getcwd())
        with open('plugins/req_bar_chart/config/plugin_config.json') as json_plugin_config:
            self.layout_settings = json.load(json_plugin_config)

    def create_bar_chart_settings(self, chart_category, y_axis_type,
                                  group_by_province, sort_by, sort_order):
        return {
            "chart_category": chart_category,
            "y_axis_type": y_axis_type,
            "group_by_province": group_by_province,
            "sort_by": sort_by,
            "sort_order": sort_order
        }

    def assign_color_to_requests(self, requests_df):
        requests_df['color'] = requests_df['province'].map(self.province_colors)

    def create_tooltips(self, dataframe):
        self.tooltip_texts = [
            (f"Province: {row['province']} <br>"
             f"Order Code: {row['orderCode']}<br>"
             f"Weight: {row['totalWeight'] / base_data_const.TONS_TO_GRAMS} tons<br>"
             f"Volume: {row['totalVolume'] / base_data_const.CBM_TO_ML} cbm")
            for index, row in dataframe.iterrows()]

    def create_bar_traces(self, requests_df, settings, tooltip_texts,
                          unique_provinces):

        bar_traces_array = []

        if settings["group_by_province"]:
            for province in unique_provinces:
                province_df = requests_df[requests_df['province'] == province]
                display_unit = settings["chart_category"]
                y_axis_data = province_df[display_unit] / base_data_const.UNIT_CONVERSION_2

                bar_trace_info = {}
                bar_trace_info["x_axis_data"] = province_df["orderCode"]
                bar_trace_info["y_axis_data"] = y_axis_data
                bar_trace_info["base"] = None
                bar_trace_info["show_legend"] = True
                bar_trace_info["trace_name"] = province
                bar_trace_info["trace_color"] = province_df["color"]
                bar_trace_info["tooltips"] = tooltip_texts
                bar_trace_info["bar_width"] = display_const.BAR_WIDTH

                new_bar_trace = bar_traces.create_bar_trace(bar_trace_info)
                bar_traces_array.append(new_bar_trace)

        else:
            display_unit = settings["chart_category"]
            y_axis_data = requests_df[display_unit] / base_data_const.UNIT_CONVERSION_2

            bar_trace_info = {}
            bar_trace_info["x_axis_data"] = requests_df["orderCode"]
            bar_trace_info["y_axis_data"] = y_axis_data
            bar_trace_info["base"] = None
            bar_trace_info["show_legend"] = False
            bar_trace_info["trace_name"] = None
            bar_trace_info["trace_color"] = requests_df["color"]
            bar_trace_info["tooltips"] = tooltip_texts
            bar_trace_info["bar_width"] = display_const.BAR_WIDTH

            new_bar_trace = bar_traces.create_bar_trace(bar_trace_info)
            bar_traces_array.append(new_bar_trace)

            for province in unique_provinces:
                pseudo_bar_trace_info = {}
                pseudo_bar_trace_info["trace_color"] = self.province_colors[province]
                pseudo_bar_trace_info["trace_name"] = province
                pseudo_bar_trace_info["show_legend"] = True

                pseudo_bar_trace = bar_traces.create_pseudo_bar_trace(pseudo_bar_trace_info)
                bar_traces_array.append(pseudo_bar_trace)

        return bar_traces_array

    def get_bar_chart_titles(self, settings):
        """
        Get the chart title and y-axis title based on the chart category.
        Args:
            settings (dict): A dictionary containing the chart category.
        Returns:
            tuple: The chart title and y-axis title.
        """
        # Mapping of chart categories to their respective titles
        title_mapping = {
            "totalWeight": ("Total Weight of Each Request", "Total Weight (Tons)"),
            "totalVolume": ("Total Volume of Each Request", "Total Volume (cbm)")
        }

        # Get the titles from the mapping, defaulting to empty strings if the category is not found
        return title_mapping.get(settings.get("chart_category"), ("", ""))

    def get_bar_chart_display_settings(self, chart_title, y_axis_title, settings):
        self.display_settings["legend_title"] = "Provinces"
        self.display_settings["chart_title"] = chart_title
        self.display_settings["x_axis_title"] = "Request Order Codes"
        self.display_settings["y_axis_title"] = y_axis_title
        self.display_settings["bar_mode"] = "group"
        self.display_settings["chart_height"] = base_display_const.FIGURE_HEIGHT
        self.display_settings["tickangle"] = display_const.BAR_CHART_TICKANGLE
        self.display_settings["y_axis_type"] = dict(type=settings["y_axis_type"])

    def create_visualization(self, requests_df, unique_provinces, settings):
        self.province_colors = common_view.assign_colors_to_provinces(unique_provinces, self.color_array)
        self.assign_color_to_requests(requests_df)
        self.create_tooltips(requests_df)
        bar_traces_array = self.create_bar_traces(requests_df, settings, self.tooltip_texts, unique_provinces)
        chart_title, y_axis_title = self.get_bar_chart_titles(settings)
        self.get_bar_chart_display_settings(chart_title, y_axis_title, settings)

        req_bar_chart = bar_chart.generate_bar_chart(bar_traces_array, self.display_settings)

        return req_bar_chart

    def create_plugin_switch(self):
        return daq.BooleanSwitch(
            id='req-bar-chart-switch',
            label={"label": "Request Bar Chart",
                   "style": {"font-size": "24px"}},
            # label="Request Bar Chart",
            labelPosition="top",
            on=False
        )

    def create_radio_buttons_options(self):
        return {
            "chart_category_options": [{'label': '  Weight Chart', 'value': 'totalWeight'},
                                       {'label': '  Volume Chart', 'value': 'totalVolume'}],
            "y_axis_options": [{'label': '  Linear', 'value': 'linear'}, {'label': '  Logarithmic', 'value': 'log'}],
            "group_province_options": [{'label': '  Yes', 'value': True}, {'label': '  No', 'value': False}],
            "sorting_options": [{'label': '  Request Code', 'value': 'orderCode'},
                                {'label': '  Request Load (Ton OR Cbm)', 'value': 'load'}],
            "sorting_order_options": [{'label': '  Increasing', 'value': True}, {'label': '  Decreasing', 'value': False}]
        }

    def create_radio_buttons(self):
        radio_buttons_options = self.create_radio_buttons_options()
        return {
            "chart_category": dcc.RadioItems(id='radio-chart-category', value='totalWeight',
                                             options=radio_buttons_options["chart_category_options"],
                                             style={'paddingLeft': '50px'}),
            "y_axis": dcc.RadioItems(id='radio-y-axis-type', value='linear',
                                     options=radio_buttons_options["y_axis_options"],
                                     style={'paddingLeft': '50px'}),
            "group_province": dcc.RadioItems(id='radio-group-province', value=True,
                                             options=radio_buttons_options["group_province_options"],
                                             style={'paddingLeft': '50px'}),
            "sorting": dcc.RadioItems(id='radio-sort-by', value='orderCode',
                                      options=radio_buttons_options["sorting_options"],
                                      style={'paddingLeft': '50px'}),
            "sorting_order": dcc.RadioItems(id='radio-sort-order', value=True,
                                            options=radio_buttons_options["sorting_order_options"],
                                            style={'paddingLeft': '50px'})
        }

    def create_control_board(self):
        radio_buttons = self.create_radio_buttons()

        control_board = [
            dbc.Row(html.Div([html.Label(html.B("Select Chart Category:"))])),
            dbc.Row(radio_buttons["chart_category"]),
            dbc.Row(html.Div([html.Br(), html.Label(html.B("Select Y-Axis Type:"))])),
            dbc.Row(radio_buttons["y_axis"]),
            dbc.Row(html.Div([html.Br(), html.Label(html.B("Group Requests by Province?"))])),
            dbc.Row(radio_buttons["group_province"]),
            dbc.Row(html.Div([html.Br(), html.Label(html.B("Sort By:"))])),
            dbc.Row(radio_buttons["sorting"]),
            dbc.Row(html.Div([html.Br(), html.Label(html.B("Sort Order:"))])),
            dbc.Row(radio_buttons["sorting_order"])
        ]

        return control_board

    def create_display_area(self):
        return dbc.Card(id='display-req-bar-chart')

    def create_plugin_layout(self):
        control_board = self.create_control_board()
        display_area = self.create_display_area()
        return dbc.Card(
            dbc.Row([
                dbc.Col(control_board, width=base_display_const.CONTROL_BOARD_WIDTH),
                dbc.Col(display_area, width=base_display_const.VISUALIZATION_WIDTH)
            ]),
            id='req-bar-chart-cover'
        )
