# Style for vehicle information display within route containers
VEHICLE_CARD_STYLE = {
    'padding': '4px 8px',  # Smaller padding to make the card smaller
    'background': '#17a2b8',  # Bootstrap-like information color
    'color': 'white',
    'borderRadius': '1px',
    'fontWeight': 'bold',
    'textAlign': 'left',  # Align text to the left
    'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.1)',  # Soft shadow for depth
    'marginBottom': '1px',  # Reduced margin from the route_container
    'marginRight': '1px',
    'width': 'fit-content',  # Shrink the width to fit its content
    'alignSelf': 'flex-start',  # Align to the left of flex container
    'flexShrink': '0', # Prevent the vehicle info from shrinking
}

# Style for request cards (To drag-n-drop)
REQUEST_CARD_STYLE = {
    'display': 'inline-flex',  # Make request cards inline elements
    'padding': '4px 8px',  # Reduced padding
    'margin': '2px',
    'borderRadius': '1px',
    'border': '1px solid #ccc',
    'fontWeight': 'bold',
    'textAlign': 'center',
    'color': 'white',
    # 'background': f'linear-gradient(45deg, #6db1ff, #{np.random.randint(100, 999)})',
    # 'color': 'white',
    # 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
    # 'flex': '0 1 auto',  # Flex property for flexible sizing
    # 'cursor': 'grab',  # Indicate that the cards are draggable
}

ROUTE_CONTAINER_STYLE = {
    'display': 'flex',  # Display as flex to align children in a row
    'flexDirection': 'row',  # Lay out children in a horizontal row
    'overflowX': 'auto',  # Allow horizontal scrolling
    'padding': '6px',
    'border': '1px dashed #808080',
    'borderRadius': '2px',
    'marginTop': '1px',
    'marginBottom': '6px',
    'boxShadow': '0 4px 8px rgba(0,0,0,0.05)',
    'alignItems': 'left',  # Center items vertically
    # 'background': 'white',
    # 'justifyContent': 'flex-start',  # Align items to the start of the container
    # 'whiteSpace': 'nowrap',  # Prevent wrapping of items
}

DRAG_AND_DROP_ZONE_STYLE = {
    'padding': '20px',
    'border': '2px solid #28a745',  # Changed to a green shade for a more vibrant look
    'borderRadius': '12px',
    'marginTop': '20px',
    'background': '#f9f9f9',  # Light grey background for subtle contrast
    'boxShadow': '0 6px 12px rgba(0,0,0,0.1)',  # Deeper shadow for a 3D effect
    'display': 'flex',
    'flexDirection': 'column',  # Align route containers in a column
    'gap': '20px',  # Space between route containers
    'overflowY': 'auto',  # Enable vertical scrolling
    'maxHeight': '600px',  # Maximum height of the container
}

VIS_INIT_ROUTES_BUTTON_STYLE = {
    'backgroundColor': 'cyan',
    'color': 'black',
    'border': 'none',
    'padding': '10px',
    'margin': '10px',
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'fontSize': '16px',
    'cursor': 'pointer'
}

VIS_UPDATED_ROUTES_BUTTON_STYLE = {
    'backgroundColor': 'magenta',
    'color': 'white',
    'border': 'none',
    'padding': '10px',
    'margin': '10px',
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'fontSize': '16px',
    'cursor': 'pointer'
}

GET_UPDATED_ROUTES_BUTTON_STYLE = {
    'backgroundColor': 'red',
    'color': 'white',
    'border': 'none',
    'padding': '10px',
    'margin': '10px',
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'fontSize': '16px',
    'cursor': 'pointer'
}

RENDER_VIS_BUTTON_STYLE = {
    'backgroundColor': 'orange',
    'color': 'white',
    'border': 'none',
    'padding': '10px',
    'margin': '10px',
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'fontSize': '16px',
    'cursor': 'pointer'
}