def assign_colors_to_provinces(unique_provinces, colors_array):
    province_colors = dict()
    for index, province in enumerate(unique_provinces):
        # Use modulo operator to cycle through colors_array
        color = colors_array[index % len(colors_array)]
        province_colors[province] = color

    return province_colors
