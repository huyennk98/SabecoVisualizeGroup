import dash_bootstrap_components as dbc
import dash_daq as daq
from dash_bootstrap_templates import ThemeChangerAIO
from dash import dcc, html
from common.constants import common_display_const
from common.styles import card_styles
from core.view import drag_and_drop_zone


class CoreView:
    def __init__(self):
        self.drag_and_drop_zone = None
        self.render_visualization_button = dbc.Button("Render Visualization", id="render-vis-button",
                                                       className="button-render-vis",
                                                       style=card_styles.RENDER_VIS_BUTTON_STYLE)
        self.visualize_init_routes_button = dbc.Button("Visualize Initial Routes", id="vis-init-routes-button",
                                                       className="button-init-routes",
                                                       style=card_styles.VIS_INIT_ROUTES_BUTTON_STYLE)
        self.get_updated_routes_button = dbc.Button("Get Updated Routes", id="get-updated-routes-button",
                                                    className="button-get-update-routes",
                                                    style=card_styles.GET_UPDATED_ROUTES_BUTTON_STYLE)
        self.drag_and_drop_zone = dbc.Card(id='drag-and-drop-zone', className='drag-and-drop-zone',
                                           style=card_styles.DRAG_AND_DROP_ZONE_STYLE)

    def create_header(self):
        return dbc.Row(
            children=[
                html.Div(
                    [
                        html.H1("VRP DASHBOARD PROTOTYPE")
                    ],
                    className='header',
                )
            ],
        )

    def create_input_upload_button(self):
        return dcc.Upload(
            id='upload-input-data',
            children=dbc.Button([html.Div(style={'height':'25%', 'width':'25%'}), "Upload JSON Input Data"],
                                id="button-upload-input-data", color="dark"),
            multiple=False  # Allow one file at a time
        )

    def create_ouput_upload_button(self):
        return dcc.Upload(
            id='upload-output-data',
            children=dbc.Button([html.Div(style={'height':'25%', 'width':'25%'}), "Upload JSON Output Data"],
                                id="button-upload-output-data", color="dark"),
            multiple=False  # Allow one file at a time
        )

    def create_input_upload_message_box(self):
        return dbc.Row(
            dbc.Col(html.Div(id='input-upload-message-box'), width={'size': 6}),
            className="mb-4"
        )

    def create_output_upload_message_box(self):
        return dbc.Row(
            dbc.Col(html.Div(id='output-upload-message-box'), width={'size': 6}),
            className="mb-4"
        )

    def create_validate_io_message_box(self):
        return dbc.Row(
            dbc.Col(html.Div(id='validate-io-message-box'), width={'size': 6}),
            className="mb-4"
        )

    def create_render_visualization_message_box(self):
        return dbc.Row(
            dbc.Col(html.Div(id='render-visualization-message-box'), width={'size': 6}),
            className="mb-4"
        )

    def create_drag_and_drop_zone(self, input_data, routes_data, unscheduled_req_data):
        self.drag_and_drop_zone = dbc.Card(id='drag-and-drop-zone',
                                           children=drag_and_drop_zone.create_drag_and_drop_section(input_data,
                                                                                                    routes_data,
                                                                                                    unscheduled_req_data),
                                           className='drag-and-drop-zone',
                                           style=card_styles.DRAG_AND_DROP_ZONE_STYLE)

    def create_tab_content_input_visualization(self, switches, plugins):
        tab_row = [
            dbc.Col(switches, width=common_display_const.TAB_SIDEBAR_WIDTH),
            dbc.Col(plugins, width=common_display_const.TAB_MAIN_CONTENT_WIDTH)
        ]

        # return dbc.Row(tab_row)
        return dbc.Tab(label="Input Visualization", children=dbc.Row(tab_row))

    def create_tab_content_output_visualization(self, switches, plugins):
        main_tab_row = dbc.Row([
            dbc.Col(switches, width=common_display_const.TAB_SIDEBAR_WIDTH),
            dbc.Col(plugins, width=common_display_const.TAB_MAIN_CONTENT_WIDTH)
        ])

        additional_buttons_row = dbc.Row([
            dbc.Col(self.visualize_init_routes_button, width=common_display_const.BUTTON_WIDTH),
            # dbc.Col(self.visualize_updated_routes_button, width=common_display_const.BUTTON_WIDTH),
            dbc.Col(self.get_updated_routes_button, width=common_display_const.BUTTON_WIDTH)
        ])

        drag_and_drop_tab_row = dbc.Row([self.drag_and_drop_zone])

        # return [main_tab_row, additional_buttons_row]
        return dbc.Tab(label="Output Visualization", children=[main_tab_row, additional_buttons_row,
                                                               drag_and_drop_tab_row])

    def create_layout(self, tab_switches, tab_plugins):
        header = self.create_header()
        input_upload_message_box = self.create_input_upload_message_box()
        output_upload_message_box = self.create_output_upload_message_box()
        validate_io_message_box = self.create_validate_io_message_box()
        render_visualization_message_box = self.create_render_visualization_message_box()

        first_row = dbc.Row([
            dbc.Col(header, width=8),
            dbc.Col(
                [dbc.Row(input_upload_message_box, class_name="mt-0 mb-0"),
                 dbc.Row(output_upload_message_box, class_name="mt-0 mb-0"),
                 dbc.Row(validate_io_message_box, class_name="mt-0 mb-0"),
                 dbc.Row(render_visualization_message_box, class_name="mt-0 mb-0")],
                width=4
            )
        ])

        # Define Theme Changer
        theme_changer = ThemeChangerAIO(aio_id='theme-changer', button_props={"size": "l", "color": "light",
                                                                              "style": {"background-color": "black"}})

        # Define JSON / zip Input & Output Files Upload Button
        input_upload_button = self.create_input_upload_button()
        output_upload_button = self.create_ouput_upload_button()

        # Define Input Visualization Tab
        input_vis_tab = self.create_tab_content_input_visualization(tab_switches["Input Visualization"],
                                                                    tab_plugins["Input Visualization"])

        # Define Output Visualization Tab
        output_vis_tab = self.create_tab_content_output_visualization(tab_switches["Output Visualization"],
                                                                      tab_plugins["Output Visualization"])

        # Create a combined button row with reduced spacing
        combined_button_row = dbc.Row([
            dbc.Col(input_upload_button, width=2),
            dbc.Col(output_upload_button, width=2, className="ml-1"),  # Reduce spacing using ml-1 class
            dbc.Col(theme_changer, width=2, className="ml-auto"),  # Align to right using ml-auto class
            dbc.Col(html.Link(rel='stylesheet', href=dbc.themes.BOOTSTRAP, id='theme'), width=2)
        ])

        layout_structure = dbc.Container(fluid=True, children = [
            # Header
            first_row,

            # Theme Changer and Upload Buttons in a single row
            combined_button_row,

            # Placeholder for render visualization button
            dbc.Row([dbc.Col("", width=2),
                     dbc.Col(dbc.Button("Render Visualization", id="render-vis-button",
                                        className="button-render-vis",
                                        style=card_styles.RENDER_VIS_BUTTON_STYLE), width=2)]),

            # Main Tabs
            dbc.Row(dbc.Tabs(id="main-tabs", children=[
                dbc.Tab(id='input-vis-tab', label="Input Visualization", tab_id="tab_input", children=input_vis_tab, ),
                dbc.Tab(id='output-vis-tab', label="Output Visualization", tab_id="tab_output",children=output_vis_tab)
            ])),

            # Hidden Data Storages
            dbc.Row(html.Div(id='last-clicked-vis-button'),style={'display': 'none'}),
            dbc.Row(html.Div(id='input-data-storage', style={'display': 'none'})),
            dbc.Row(html.Div(id='output-data-storage', style={'display': 'none'})),
            dbc.Row(html.Div(id='dummy-div', style={'display': 'none'})),
            dbc.Row(dcc.Store(id='json-output-store')),
            dbc.Row(dcc.Store(id='drag-and-drop-data-store')),
        ])

        return layout_structure
