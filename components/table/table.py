import plotly.graph_objects as go

def create_general_table_from_json(input_json):
    """
    Creates a Plotly table from a JSON-like structure.

    Parameters:
    - input_json: A dict with keys 'data' containing a list of dicts for each row's values,
                  and 'style_info' containing optional styling information.

    Returns:
    - Plotly figure object containing the configured table.
    """
    data = input_json.get('data', [])
    if not data:
        fig = go.Figure()
        fig.update_layout(title="No data to display",
                          xaxis={'visible': False},  # Hide x-axis
                          yaxis={'visible': False},  # Hide y-axis
                          annotations=[{
                              'xref': "paper",
                              'yref': "paper",
                              'showarrow': False,
                              'font': {'size': 16}
                          }],
                          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                          paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper
            )
        return fig

    style_info = input_json.get('style_info', {})
    cell_colors = style_info.get('cell_colors', [])

    # Extract column headers from the first row (assuming all rows have the same keys)
    headers = list(data[0].keys())

    # Extract row values
    rows = [[row.get(col, None) for col in headers] for row in data]

    # Define default styles
    default_header_style = {
        'line_color': 'darkslategray',
        'fill_color': 'grey',
        'align': 'left',
        'font': {'color': 'white', 'size': 12}
    }
    default_cell_style = {
        'line_color': 'darkslategray',
        'align': 'left',
        'font': {'color': 'darkslategray', 'size': 11}
    }

    # Merge default styles with user-provided styles
    header_style = {**default_header_style, **style_info.get('header', {})}
    cell_style = {**default_cell_style, **style_info.get('cells', {})}
    cell_style.pop('fill_color', None)  # Remove fill_color if present since it's managed separately

    # Handle cell colors configuration
    if not cell_colors:
        # Default to white if no cell_colors provided
        cell_colors = [['white' for _ in range(len(headers))] for _ in range(len(data))]

    # Create the table figure
    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b>{}</b>'.format(h) for h in headers], **header_style),
        cells=dict(values=list(map(list, zip(*rows))), fill_color=cell_colors, **cell_style)
    )])

    # Update layout with optional figure title and height if provided
    fig.update_layout(
        title=style_info.get("figure_title", "Your Table Title"),
        height=style_info.get("figure_height", 300)  # Default height if not specified
    )

    return fig

# This function now handles missing keys and data more gracefully and allows for more flexible styling.
