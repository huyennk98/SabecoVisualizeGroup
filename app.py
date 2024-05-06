import dash
import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy
from core.controller.core_controller import CoreController

app = DashProxy(
    __name__,
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    prevent_initial_callbacks='initial_duplicate'
)

core_controller = CoreController()
app.layout = core_controller.init_layout(app)

core_controller.register_execution_callback(app)

core_controller.register_core_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=3080)
