import dash_bootstrap_components as dbc


def create_progress_bar(display_value, max_value, display_settings, color):
    return dbc.Progress(value=display_value, max=max_value, color=color,
                        style=display_settings["style"],
                        className=display_settings["classname"])
