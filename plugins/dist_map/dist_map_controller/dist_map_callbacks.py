import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from plugins.dist_map.constants import display_const


def register_dist_map_callbacks(self, app):
    @app.callback(
        Output("display-dist-map", "children"),
        Input("radio-map-category", "value"),
        Input('dist-map-switch', 'on')
    )
    def update_dist_map(map_type, switch):
        """
        Updates and returns the distribution map based on the selected map type.

        Args:
            map_type (str): The type of map to display.
            switch
        Returns:
            dbc.Row: A Dash component containing the updated distribution map.
        """

        if self.model and switch:
            # Create visualization
            distribution_map = self.view.create_visualization(self.model.map_center, self.model.dist_map_data, map_type,
                                                              self.model.unique_provinces, self.model.list_of_loads)

            # Return visualization
            return dbc.Row([html.Iframe(srcDoc=distribution_map, width=display_const.MAP_FRAME_WIDTH,
                                        height=display_const.MAP_FRAME_HEIGHT)])

        else:
            return None

    @app.callback(
            Output('dist-map-cover', 'style'),
            Input('dist-map-switch', 'on')
        )
    def display_dist_map(switch):
        if switch:
            return {}
        else:
            return {'display': 'none'}
