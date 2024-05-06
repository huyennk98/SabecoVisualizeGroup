import folium
from scipy.spatial import ConvexHull


def create_convex_hull_polygon(route, opacity_convex=0.8):
    convex_hull = folium.FeatureGroup(name="test")

    # Get convex hull coordinates
    convex_hull_vertices = [route["coordinates"][idx] for idx in ConvexHull(route["coordinates"]).vertices]

    popup_bubble = folium.Popup(route["popup"]["content"],
                                max_width=route["popup"]["width"])

    # Create Folium convex hull
    convex_hull.add_child(
        folium.vector_layers.Polygon(
            locations=convex_hull_vertices,
            fill_color=route["line_color"],
            opacity=route["opacity"],
            weight=route["weight"],
            tooltip="This is the Convex Hull!",
            popup=popup_bubble
        )
    )

    return convex_hull

# m = folium.Map(location=[21, 106], zoom_start=11)
# def create_convexhull_polygon(route,  opacity_convex =  0.8, weight_line=1):
#     fg = folium.FeatureGroup(name="test")

#     # Create the convex hull using scipy.spatial
#     convex_hull = [route[i] for i in ConvexHull(route).vertices]
#     print(convex_hull)
#     # form =  ConvexHull(form)
#     #
#     fg.add_child(
#         folium.vector_layers.Polygon(
#             locations=convex_hull,
#             # color=line_color,
#             fill_color="blue",
#             opacity = opacity_convex,
#             weight = weight_line,
#             # popup=(folium.Popup(text)),
#         )
#     )
#     return fg

# # guide to use
# routes = [(21, 106), (21.08, 106.002),(21.18, 106.102),(21, 106.102), (21.012, 106.19)]
# fg = create_convexhull_polygon(routes)
# m.add_child(fg)
# m
