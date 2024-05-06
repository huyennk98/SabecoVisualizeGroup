import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output


def register_req_bar_chart_callbacks(self, app):
    @app.callback(
        Output('display-req-bar-chart', 'children'),
        [Input('radio-chart-category', 'value'),
        Input('radio-y-axis-type', 'value'),
        Input('radio-group-province', 'value'),
        Input('radio-sort-by', 'value'),
        Input('radio-sort-order', 'value'),
        Input('req-bar-chart-switch', 'on')]
    )
    def update_req_bar_chart(chart_category, y_axis_type, group_by_province, sort_by, sort_order, switch):
        # Define a utilities
        if self.model and switch:
            bar_chart_settings = self.view.create_bar_chart_settings(chart_category, y_axis_type, group_by_province,
                                                                     sort_by, sort_order)

            self.model.sort_request_dataframe(self.model.request_dataframe, bar_chart_settings)

            req_bar_chart = self.view.create_visualization(self.model.request_dataframe, self.model.unique_provinces,
                                                           bar_chart_settings)

            return dbc.Row(dcc.Graph(figure=req_bar_chart))
        else:
            return None

    @app.callback(
        Output('req-bar-chart-cover', 'style'),
        Input('req-bar-chart-switch', 'on')
    )
    def display_req_bar_chart(switch):
        if switch:
            return {}
        else:
            return {'display': 'none'}
