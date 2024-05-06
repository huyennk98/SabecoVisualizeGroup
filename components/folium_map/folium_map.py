import folium


def add_markers_to_map(folium_map, markers_array):
    for marker in markers_array:
        marker.add_to(folium_map)


# Viết code tổng quát nhất có thể, add line & các decorators của line đi kèm
def add_routes_to_map(folium_map, routes):
    for route in routes:
        for segment in route:
            route[segment].add_to(folium_map)


def add_feature_groups_to_map(folium_map, feature_groups):
    for fg in feature_groups:
        folium_map.add_child(fg)


def create_folium_map(map_settings, markers, routes, feature_groups):

    fmap = folium.Map(location=map_settings["center"], zoom_start=map_settings["zoom"],
                      control_scale=map_settings["display_scalebar"])
    add_markers_to_map(fmap, markers)
    add_routes_to_map(fmap, routes)
    add_feature_groups_to_map(fmap, feature_groups)

    return fmap
