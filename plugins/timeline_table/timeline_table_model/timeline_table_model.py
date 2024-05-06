import datetime
from plugins.base_plugin.base_model import common_model


class TimelineTableModel:
    def __init__(self, input_data, output_data, routes_data):
        self.input_data = input_data  # JSON Input File
        self.output_data = output_data  # JSON Output
        self.routes_data = routes_data  # Custom Route
        ''' Convert location (customers and depots) and vehicle to dict for easy access to Time Windows'''
        self.locations_dict = common_model.list_of_dicts_to_dict_of_dicts(input_data["customers"], "locationCode")
        self.locations_dict.update(common_model.list_of_dicts_to_dict_of_dicts(input_data["depots"], "locationCode"))
        self.vehicles_dict = common_model.list_of_dicts_to_dict_of_dicts(input_data["vehicles"], "vehicleCode")

    @staticmethod
    def parse_time(time_str):
        return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    def find_common_working_time(self, objects):
        """
        Find common working time across multiple locations.
        """
        # Initialize common working time with the first location's working time
        common_start = self.parse_time(objects[0]["workingTime"]["start"])
        common_end = self.parse_time(objects[0]["workingTime"]["end"])

        # Iterate through the rest of the locations to find common working time
        for obj in objects[1:]:
            start = self.parse_time(obj["workingTime"]["start"])
            end = self.parse_time(obj["workingTime"]["end"])
            common_start = max(common_start, start)
            common_end = min(common_end, end)

            # If there's no overlap, return None immediately
            if common_start >= common_end:
                return {"start": None, "end": None}

        return {"start": common_start.strftime("%Y-%m-%d %H:%M:%S"), "end": common_end.strftime("%Y-%m-%d %H:%M:%S")}

    def merge_break_times(self, objects):
        """
        Merge break times from multiple locations.
        """
        # Collect all break times from all locations
        all_breaks = []
        for obj in objects:
            all_breaks.extend(obj["breakTimes"])

        # Sort all breaks by start time
        all_breaks_sorted = sorted(all_breaks, key=lambda x: x["start"])

        # Merge overlapping break times
        merged_breaks = []
        for current in all_breaks_sorted:
            if not merged_breaks:
                merged_breaks.append(current)
            else:
                last = merged_breaks[-1]
                if self.parse_time(current["start"]) <= self.parse_time(last["end"]):
                    last["end"] = max(self.parse_time(last["end"]),
                                      self.parse_time(current["end"])).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    merged_breaks.append(current)
        return merged_breaks

    @staticmethod
    def is_within_time_range(timestamp, time_range, is_inclusive=True):
        """
        Check if a timestamp is within a specified time range.
        """
        start, end = time_range
        return start <= timestamp <= end if is_inclusive else start < timestamp < end

    def is_outside_break_times(self, timestamp, break_times):
        """
        Check if a timestamp is outside all break times.
        """
        for break_time in break_times:
            if self.is_within_time_range(timestamp,
                                         (self.parse_time(break_time["start"]),
                                          self.parse_time(break_time["end"])),
                                         is_inclusive=False):
                return False
        return True

    def check_timestamp_violation(self, timestamp, working_time, break_times):
        """
        Check if a timestamp violates time window constraints.
        """
        timestamp_parsed = self.parse_time(timestamp)
        working_time_range = (self.parse_time(working_time["start"]), self.parse_time(working_time["end"]))

        return (self.is_within_time_range(timestamp_parsed, working_time_range, is_inclusive=True) and
                self.is_outside_break_times(timestamp_parsed, break_times))

    def processing_data_to_view(self, routes_data):
        timeline_table_input = {
            "data": [],
            "style_info": {
                "header": {"fill_color": "navy",
                           'font': dict(color='white', size=18)},
                "cells": {'height': 32, 'font': dict(color='black', size=16),
                          "fill_color": "limegreen"},
                "figure_title": "Annotations:<br>S: Start;    E: End<br>A:Arrive;   L: Leave",
                "figure_height": 1000
            },
            "cell_colors": []
        }

        max_points_of_route = max([len(route['elements']) for route in routes_data])

        for route_idx, route in enumerate(routes_data):
            vehicle_code = route["vehicle_code"]
            row_data = {"Route": f"Route {route_idx + 1}"}
            row_colors = ["limegreen"]

            for ele_idx, element in enumerate(route["elements"]):
                loc_code = element["location_code"]
                time_window = self.locations_dict[loc_code]["workingTime"]

                date_obj = datetime.datetime.strptime(time_window['start'], '%Y-%m-%d %H:%M:%S')
                date_display = date_obj.strftime('%Y-%m-%d')
                arrival_date = datetime.datetime.strptime(element["arrival_time"], '%Y-%m-%d %H:%M:%S').date()
                leaving_date = datetime.datetime.strptime(element["leaving_time"], '%Y-%m-%d %H:%M:%S').date()
                dates_differ = date_obj.date() != arrival_date or date_obj.date() != leaving_date

                break_times = self.locations_dict[loc_code]["breakTimes"]
                common_time_window = self.find_common_working_time([self.vehicles_dict[vehicle_code],
                                                                    self.locations_dict[loc_code]])
                common_break_times = self.merge_break_times([self.vehicles_dict[vehicle_code],
                                                             self.locations_dict[loc_code]])
                check_time_window_st = self.check_timestamp_violation(element["arrival_time"],
                                                                      common_time_window,
                                                                      common_break_times) and \
                                       self.check_timestamp_violation(element["leaving_time"],
                                                                      common_time_window,
                                                                      common_break_times)

                time_window_key = f"Location {ele_idx + 1} Time Window{(' (' + date_display + ')') if dates_differ else ''}"
                row_data[time_window_key] = f"S: {time_window['start'][11:-3]}<br>E: {time_window['end'][11:-3]}"

                break_times_key = f"Location {ele_idx + 1} Break Times{(' (' + date_display + ')') if dates_differ else ''}"
                break_time_string = ""
                for break_interval in break_times:
                    break_time_string += f"S: {break_interval['start'][11:-3]}<br>E: {break_interval['end'][11:-3]}"
                row_data[break_times_key] = break_time_string

                active_times_key = f"Location {ele_idx + 1} Active Times"
                row_data[active_times_key] = f"A: " + element["arrival_time"][11:-3] + "<br>"\
                                             f"L: " + element["leaving_time"][11:-3]

                # Determine the cell color based on the condition
                cell_color = "lightgrey" if check_time_window_st else "red"
                row_colors.extend([cell_color] * 3)
                row_colors.append(cell_color)

            if len(route['elements']) < max_points_of_route:
                row_colors.extend(["lightgrey"] * 3 * (max_points_of_route - len(route['elements'])))
                for i in range(len(route['elements'])+1, max_points_of_route + 1):
                    row_data[f"Location {i} Time Window"] = ""
                    row_data[f"Location {i} Break Times"] = ""
                    row_data[f"Location {i} Active Times"] = ""

            timeline_table_input["data"].append(row_data)
            timeline_table_input["cell_colors"].append(row_colors)

        # Now fishbone_table_input is prepared with the data and cell_colors according to the requirements
        timeline_table_input["cell_colors"] = list(
            map(list, zip(*timeline_table_input["cell_colors"])))  # Transpose the cell colors

        return timeline_table_input
