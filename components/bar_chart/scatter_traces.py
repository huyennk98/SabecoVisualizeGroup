import plotly.graph_objects as go


def create_scatter_trace(scatter_trace_info):
    return go.Scatter(
        x=scatter_trace_info["x_axis_data"],
        y=scatter_trace_info["y_axis_data"],
        mode=scatter_trace_info["mode"],
        name=scatter_trace_info["trace_name"],
        line=scatter_trace_info["line_settings"],
        marker=scatter_trace_info["markers_settings"],
        showlegend=scatter_trace_info["show_legend"],
    )
