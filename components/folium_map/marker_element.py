import folium

# Chấm tròn cố định về p, thay đổi kích thước khi zoom in / out
def create_circle_marker_element(marker_info):

    popup_bubble = folium.Popup(marker_info["popup"]["content"], max_width=marker_info["popup"]["width"])
    display_fixed_size =  False
    if "fixed_size" in marker_info:
        if marker_info['fixed_size']:
            display_fixed_size= True

    if display_fixed_size:
        return folium.Circle(
            location=marker_info["location"],
            color=marker_info["color"],
            fill=marker_info["fill"],
            fill_color=marker_info["color"],
            popup=popup_bubble,
            fill_opacity=marker_info["opacity"],
            radius=marker_info["radius"]
        )
    else:
        # Nếu fixed size không được khai báo, hoặc được khai báo nhưng bằng False
        # Fix Tỉ Lệ
        print("fix ratio")
        return folium.CircleMarker(
            location=marker_info["location"],
            color=marker_info["color"],
            fill=marker_info["fill"],
            fill_color=marker_info["color"],
            popup=popup_bubble,
            fill_opacity=marker_info["opacity"],
            radius=marker_info["radius"]
        )

# def test_create_circle_marker_element():
#     m_test = folium.Map(location = (21, 106), zoom_start = 13,
#                         control_scale = True)
#
#     testing_marker_info = {
#         "popup": {
#             "content": "This is a sample marker!",
#             "width": 200
#         },
#         "location": (21, 106),
#         "color": "red",
#         "fill": "True",
#         "radius": 30,
#         "opacity": 0.8,
#         "fixed_size": False
#     }
#     create_circle_marker_element(testing_marker_info).add_to(m_test)
#     return m_test
#
# test_create_circle_marker_element()


# def create_circle_marker_element(marker_info):
#
#     popup_bubble = folium.Popup(marker_info["popup"]["content"], max_width=marker_info["popup"]["width"])
#
#     return folium.CircleMarker(
#         location=marker_info["location"],
#         color=marker_info["color"],
#         fill=marker_info["fill"],
#         fill_color=marker_info["color"],
#         popup=popup_bubble,
#         radius=marker_info["radius"]
#     )
#
# def create_fixed_circle_marker_element(marker_info):
#
#     popup_bubble = folium.Popup(marker_info["popup"]["content"], max_width=marker_info["popup"]["width"])
#
#     return folium.Circle(
#         location=marker_info["location"],
#         color=marker_info["color"],
#         fill=marker_info["fill"],
#         fill_color=marker_info["color"],
#         popup=popup_bubble,
#         radius=marker_info["radius"]
#     )

def create_plain_marker_element(marker_info):

    popup_bubble = folium.Popup(marker_info["popup"]["content"], max_width=marker_info["popup"]["width"])

    return folium.Marker(
        location=marker_info["location"],
        icon=folium.Icon(color=marker_info["color"], icon=marker_info["icon"], prefix=marker_info["prefix"]),
        popup=popup_bubble
    )

# def test_create_plain_marker_element():
#     m_test = folium.Map(location = (21, 106), zoom_start = 13,
#                         control_scale = True)
#
#     testing_marker_info = {
#         "popup": {
#             "content": "This is a sample marker!",
#             "width": 200
#         },
#         "location": (21, 106),
#         "color": "red",
#         "icon": "industry",
#         "prefix": 'fa'
#     }
#     create_plain_marker_element( testing_marker_info).add_to(m_test)
#     return m_test
# test_create_plain_marker_element()
