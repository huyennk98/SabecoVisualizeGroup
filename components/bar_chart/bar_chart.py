import plotly.graph_objects as go


def update_bar_chart_layout(bar_chart, display_settings):

    # Update layout for better readability
    bar_chart.update_layout(
        legend_title=display_settings["legend_title"],
        title=display_settings["chart_title"],
        xaxis_title=display_settings["x_axis_title"],
        yaxis_title=display_settings["y_axis_title"],
        barmode=display_settings["bar_mode"],  # This ensures that the bars are not stacked
        height=display_settings["chart_height"],
        xaxis_tickangle=display_settings["tickangle"],  # Rotate the x-axis labels for better visibility
        yaxis=display_settings["y_axis_type"]
    )

def generate_bar_chart(bar_chart_traces, display_settings):
    bar_chart = go.Figure()

    for trace in bar_chart_traces:
        bar_chart.add_trace(trace)

    update_bar_chart_layout(bar_chart, display_settings)

    return bar_chart
