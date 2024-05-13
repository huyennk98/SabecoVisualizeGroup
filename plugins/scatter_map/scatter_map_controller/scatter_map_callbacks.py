import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from plugins.dist_map.constants import display_const
import plotly.graph_objects as go



def register_scatter_map_callbacks(self, app):
    @app.callback(
        Output('display-scatter-map', 'figure'),
        [Input('scatter-map-switch', 'on'),
        State('display-scatter-map', 'figure')]
    )
    def update_scatter_map(switch, figure):


        if self.model and switch:
            # Create visualization
            scatter_map = self.view.create_visualization(self.model.map_center, self.model.dist_map_data)

            # Return visualization
            return dbc.Row([html.Iframe(srcDoc=scatter_map, width=display_const.MAP_FRAME_WIDTH,
                                        height=display_const.MAP_FRAME_HEIGHT)])

        else:
            return None

        # if not clickData:
        #     # Return empty figure if no click data is available
        #     return fig
        

        # # Get the clicked location
        # clicked_location = (clickData['points'][0]['lat'], clickData['points'][0]['lon'])


        # # Initialize lists to hold Scattermapbox traces
        # traces = []

        # # Initialize a list to hold lines for the big trace
        # big_trace_lines = []

        # name_line = ""

        

        # # Find all lines related to the clicked location and add them to the big trace
        # for line in assignment_map_data['mapping_lines']:
        #     if line['type'] == 'phy_depot_to_customer' or line['type'] == 'customer_to_phy_depot':
        #         line_color = 'gray'  # Màu xám cho đường nối depot-customer
        #     elif line['type'] == 'phy_depot_to_factory' or line['type'] == 'factory_to_phy_depot':
        #         line_color = 'brown'  # Màu nâu cho đường nối depot-factory  

        #     if line['start_coordinate'] == clicked_location:
        #         big_trace_lines.append(
        #             go.Scattermapbox(
        #                 lat=[line['start_coordinate'][0], line['end_coordinate'][0]],
        #                 lon=[line['start_coordinate'][1], line['end_coordinate'][1]],
        #                 mode='lines',
        #                 line=dict(width=2, color = line_color),
        #                 name=f'Lines from {clicked_location}'
        #             )
        #         )

        # '''
        # assignment_map_data["mapping_lines"]
        # 'type': 'factory_to_phy_depot',
        # 'start_location': '061',
        # 'end_location': 'PD-146',
        # '''

        # # Cập nhật big_trace_lines vào fig
        # fig.update_traces(
        #     overwrite=True,
        #     visible=True,  # Ẩn các trace hiện có trên biểu đồ
        # )
        # # fig.add_traces(traces + big_trace_lines)  # Thêm big_trace_lines vào biểu đồ
        # fig.add_traces(traces + big_trace_lines)  # Thêm big_trace_lines vào biểu đồ

        # return fig
    
    @app.callback(
            Output('scatter-map-cover', 'style'),
            Input('scatter-map-switch', 'on')
        )
    def display_scatter_map(switch):
        if switch:
            return {}
        else:
            return {'display': 'none'}