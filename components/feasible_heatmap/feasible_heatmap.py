import plotly.graph_objects as go


def update_feasible_heatmap_layout(feasible_heatmap, display_settings):
    feasible_heatmap.update_layout(
        title=display_settings["chart_title"],
        xaxis=display_settings["x_axis_settings"],
        yaxis=display_settings["y_axis_settings"],
        margin=display_settings["margins"],
        height=display_settings["chart_height"]
    )


def create_feasible_heatmap(heatmap_data, display_settings):
    feasible_heatmap = go.Figure(data=go.Heatmap(
        x=heatmap_data["x_axis_data"],
        y=heatmap_data["y_axis_data"],
        z=heatmap_data["z_axis_data"],
        colorscale=display_settings["color_scale"],
        showscale=display_settings["show_scale"],
        hoverinfo=display_settings["hover_info"]
        )
    )

    update_feasible_heatmap_layout(feasible_heatmap, display_settings)

    return feasible_heatmap
