import plotly.graph_objects as go


def create_pseudo_bar_trace(pseudo_bar_trace):
    return go.Bar(
        x=[None],
        y=[None],
        marker_color=pseudo_bar_trace["trace_color"],
        name=pseudo_bar_trace["trace_name"],
        showlegend=pseudo_bar_trace["show_legend"]
    )

def create_bar_trace(bar_trace_info):
    return go.Bar(
        x=bar_trace_info["x_axis_data"],
        y=bar_trace_info["y_axis_data"],
        base=bar_trace_info["base"],
        showlegend=bar_trace_info["show_legend"],
        name=bar_trace_info["trace_name"],
        marker_color=bar_trace_info["trace_color"],
        hovertemplate=bar_trace_info["tooltips"],
        width=bar_trace_info["bar_width"]
    )
