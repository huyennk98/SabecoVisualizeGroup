import folium
from pyproj import Geod
from components.common import constants


def calculate_azimuth(geod, line_info):
    azimuth, _, _ = geod.inv(line_info["start"][1], line_info["start"][0],
                             line_info["end"][1], line_info["end"][0])
    return azimuth


def calculate_new_coord(geod, line_info, azimuth):
    new_lng, new_lat, _ = geod.fwd(line_info["end"][1], line_info["end"][0],
                                   azimuth + 180, constants.BACKWARD_DISTANCE)
    return new_lng, new_lat


def create_line_element(line_info):
    line_display = {}

    popup_bubble = folium.Popup(line_info["popup"]["content"],
                                max_width=line_info["popup"]["width"])

    line_display["line"] = folium.PolyLine([line_info["start"], line_info["end"]],
                                           color=line_info["line_color"],
                                           weight=line_info["weight"],
                                           popup=popup_bubble)

    return line_display


def create_route_element(line_info):
    grouped_line_display = {}

    popup_bubble = folium.Popup(line_info["popup"]["content"],
                                max_width=line_info["popup"]["width"])

    grouped_line_display["line"] = folium.PolyLine([line_info["coordinates"]],
                                                   color=line_info["line_color"],
                                                   weight=line_info["weight"],
                                                   popup=popup_bubble)

    return grouped_line_display

# def test_create_route_element():
#     m_test = folium.Map(location = (21, 106), zoom_start = 13,
#                         control_scale = True)
#
#     testing_marker_info = {
#         "popup": {
#             "content": "This is a sample polyline!",
#             "width": 200
#         },
#         "coordinates": [(21, 106), (21.003, 106.002), (21.01, 106.05), (21.012, 106.09)],
#         "line_color": "blue",
#         "weight": 5,
#     }
#     polyline = create_route_element(testing_marker_info)
#     add_routes_to_map(m_test, [polyline])
#
#     return m_test
#
# test_create_route_element()


def create_arrowed_route_element(line_info):
    line_display = {}

    popup_bubble = folium.Popup(line_info["popup"]["content"],
                                max_width=line_info["popup"]["width"])

    line_display["line"] = folium.PolyLine([line_info["start"], line_info["end"]],
                                           color=line_info["line_color"],
                                           weight=line_info["weight"],
                                           popup=popup_bubble)

    geod = Geod(ellps='clrk66')

    azimuth = calculate_azimuth(geod, line_info)

    new_lng, new_lat = calculate_new_coord(geod, line_info, azimuth)

    line_display["arrow"] = folium.RegularPolygonMarker(
        (new_lat, new_lng),
        fill_color=line_info["line_color"],
        number_of_sides=line_info["arrow_sides"],
        radius=line_info["arrow_radius"],
        rotation=azimuth-90
    )

    return line_display
