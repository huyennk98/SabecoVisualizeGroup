import plotly.graph_objects as go

def create_scatter_map(map_settings, markers):
    smap = go.Scattermapbox(
        lat=[markers["location"][0]],
        lon=[markers["location"][1]],
        text=markers["text"],
        hoverinfo='text',
        mode='markers',
        marker=dict(size=10, color=markers["color"]),
        # name=location_type.capitalize()  # Capitalize the location type for legend
        title='Interactive Point and Line Visibility',
        clickmode='event+select',
        hovermode='closest',
        mapbox=map_settings
    )
    return smap