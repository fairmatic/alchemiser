from .haversine_distance import haversine_dist_wsgi_points
from .osm_utils import OSMUtils
from typing import Tuple, Dict, Any, Text, List
from copy import deepcopy


class BaseSegment:
    """
    This class represents a segment of a trip. A segment is defined as a part of a trip
    determined via the beacons discoveries and the parent datapoint
    """
    def __init__(
            self,
            parent_datapoint: dict,
            segment_timestamp: int,
            segment_timestamp_end: int,
            is_first_segment: bool,
            is_last_segment: bool,
            minimum_distance_km_to_interpolate: float,
            minimum_seconds_to_interpolate: float
    ):
        """
        This method initializes the segment.
        param parent_datapoint: Parent datapoint of the segment
        param segment_timestamp: Start timestamp of the segment
        param segment_timestamp_end: End timestamp of the segment
        param is_first_segment: True if the segment is the first segment of the trip
        param is_last_segment: True if the segment is the last segment of the trip
        param minimum_distance_km_to_interpolate: Minimum distance in kms between two trail points to interpolate
        param minimum_seconds_to_interpolate: Minimum duration in seconds between two trail points to interpolate
        """
        self.parent_datapoint = parent_datapoint
        self.segment_timestamp = segment_timestamp
        self.segment_timestamp_end = segment_timestamp_end
        self.count_events = len(self.parent_datapoint["events"])
        self.count_trail_points = len(self.parent_datapoint["trail"])
        self.is_first_segment = is_first_segment
        self.is_last_segment = is_last_segment
        self.minimum_distance_km_to_interpolate = minimum_distance_km_to_interpolate
        self.minimum_seconds_to_interpolate = minimum_seconds_to_interpolate

        self.is_start_interpolated = False
        self.is_end_interpolated = False

        # Readjust the start timestamp
        self.segment_timestamp = segment_timestamp - 1 if is_first_segment else self.segment_timestamp

    @staticmethod
    def interpolate_lat_long(timestamp: int, previous_point_ts: int, next_point_ts: int, prev_lat: float,
                             prev_lon: float, next_lat: float, next_lon: float) -> Tuple[float, float, float]:
        """
        This method interpolates the latitude and longitude of a point between two points, given the timestamp the point
        could have occurred.
        """
        total_distance = haversine_dist_wsgi_points([(prev_lat, prev_lon), (next_lat, next_lon)])
        total_duration_s = (next_point_ts - previous_point_ts) / 1000
        intermediate_duration_s = (timestamp - previous_point_ts) / 1000
        x0, y0 = OSMUtils.get_cartesian_point(latitude=prev_lat, longitude=prev_lon)
        x1, y1 = OSMUtils.get_cartesian_point(latitude=next_lat, longitude=next_lon)
        speed = total_distance / total_duration_s
        straight_line_dist = speed * intermediate_duration_s
        intermediate_x = ((straight_line_dist / total_distance) * (x1 - x0)) + x0
        intermediate_y = ((straight_line_dist / total_distance) * (y1 - y0)) + y0
        intermediate_lat, intermediate_lon = OSMUtils.get_spherical_point((intermediate_x, intermediate_y))
        return intermediate_lat, intermediate_lon, straight_line_dist

    @staticmethod
    def get_interpolated_trail_point(previous_trail_point: Dict[Text, Any], next_trail_point: Dict[Text, Any],
                                     intermediate_timestamp: int) -> Dict[Text, Any]:
        """
        This method returns the interpolated trail point between two trail points,
        given the timestamp the intermediate point
        """
        prev_lat = previous_trail_point["location"]["latitude"]
        prev_lon = previous_trail_point["location"]["longitude"]
        next_lat = next_trail_point["location"]["latitude"]
        next_lon = next_trail_point["location"]["longitude"]
        interpolated_lat, interpolated_lon, distance = BaseSegment.interpolate_lat_long(
            timestamp=intermediate_timestamp,
            previous_point_ts=previous_trail_point["timestamp"],
            next_point_ts=next_trail_point["timestamp"],
            prev_lat=prev_lat,
            prev_lon=prev_lon,
            next_lat=next_lat,
            next_lon=next_lon
        )

        return dict(
            previous_trail_point,
            location={"latitude": interpolated_lat, "longitude": interpolated_lon},
            timestamp=float(intermediate_timestamp)
        )

    def get_segment_events(self) -> List[Dict[Text, Any]]:
        """
        This method returns the events in the segment, from the parent events
        """
        events = []
        event_idx = [
            i for i, t in enumerate(self.parent_datapoint["events"])
            if (self.segment_timestamp <= t["timestamp"] <= self.segment_timestamp_end)
        ]
        if len(event_idx) > 0:
            event_start_idx = 0 if self.is_first_segment else event_idx[0]
            event_end_idx = self.count_events - 1 if self.is_last_segment else event_idx[-1]
            events = self.parent_datapoint["events"][event_start_idx:event_end_idx + 1]
        for event in self.parent_datapoint["events"]:
            if event["timestamp"] < self.segment_timestamp < event["timestampEnd"]:
                copied_event = deepcopy(event)
                copied_event["timestamp"] = self.segment_timestamp
                events.insert(0, copied_event)
            elif event["timestamp"] < self.segment_timestamp_end < event["timestampEnd"]:
                copied_event = deepcopy(event)
                copied_event["timestamp"] = self.segment_timestamp_end
                events.append(copied_event)
        return events

    def requires_interpolation_with_next_trail(self, trail_start_idx: int, duration_s: int) -> bool:
        """
        This method returns True if the trail point needs to be interpolated with the next trail point.
        """
        previous_trail_point = self.parent_datapoint["trail"][trail_start_idx]
        next_trail_point = self.parent_datapoint["trail"][trail_start_idx + 1]
        prev_lat = previous_trail_point["location"]["latitude"]
        prev_lon = previous_trail_point["location"]["longitude"]
        next_lat = next_trail_point["location"]["latitude"]
        next_lon = next_trail_point["location"]["longitude"]
        distance = haversine_dist_wsgi_points([(prev_lat, prev_lon), (next_lat, next_lon)])
        return(
            True if (
                    (distance > self.minimum_distance_km_to_interpolate) and
                    (duration_s > self.minimum_seconds_to_interpolate)
            ) else False
        )

    def augment_trail_with_interpolation(self, trail_start_idx: int, trail_end_idx: int, trail: List[Dict[Text, Any]]
                                         ) -> List[Dict[Text, Any]]:
        """
        This method augments the trail with interpolated points.
        param trail_start_idx: Index of the first trail point in the segment, wrt parent trail
        param trail_end_idx: Index of the last trail point in the segment, wrt parent trail
        param trail: Trail points in the segment
        """
        duration_from_start_ts_to_first_tp = (
                (self.parent_datapoint["trail"][trail_start_idx]["timestamp"] - self.segment_timestamp) / 1000
        )
        if (
                trail_start_idx > 0 and
                self.requires_interpolation_with_next_trail(trail_start_idx - 1, duration_from_start_ts_to_first_tp)
        ):
            interpolated_point = self.get_interpolated_trail_point(
                previous_trail_point=self.parent_datapoint["trail"][trail_start_idx - 1],
                next_trail_point=self.parent_datapoint["trail"][trail_start_idx],
                intermediate_timestamp=self.segment_timestamp,
            )
            trail = [interpolated_point] + trail
            self.is_start_interpolated = True
        duration_from_end_ts_to_last_tp = (
                (self.segment_timestamp_end - self.parent_datapoint["trail"][trail_end_idx]["timestamp"]) / 1000
        )
        if (
                trail_end_idx < self.count_trail_points - 1 and
                self.requires_interpolation_with_next_trail(trail_end_idx, duration_from_end_ts_to_last_tp)
        ):
            interpolated_point = self.get_interpolated_trail_point(
                previous_trail_point=self.parent_datapoint["trail"][trail_end_idx],
                next_trail_point=self.parent_datapoint["trail"][trail_end_idx + 1],
                intermediate_timestamp=self.segment_timestamp_end
            )
            trail = trail + [interpolated_point]
            self.is_end_interpolated = True
        return trail

    def get_segment_trail(self) -> List[Dict[Text, Any]]:
        """
        This method returns the trail points in the segment. It also augments the trail with interpolated points.
        If the segment lies between two trail points, then it returns the interpolated trail points.
        """
        trail = []
        self.parent_datapoint["trail"].sort(key=lambda x: x["timestamp"])
        trail_idx = [
            i for i, t in enumerate(self.parent_datapoint["trail"])
            if (self.segment_timestamp <= t["timestamp"] <= self.segment_timestamp_end)
        ]
        if len(trail_idx) > 0:
            trail_start_idx = 0 if self.is_first_segment else trail_idx[0]
            trail_end_idx = self.count_trail_points - 1 if self.is_last_segment else trail_idx[-1]
            trail = self.parent_datapoint["trail"][trail_start_idx:trail_end_idx + 1]
            trail = self.augment_trail_with_interpolation(trail_start_idx, trail_end_idx, trail)
        else:
            # This means that trail points lie between two trail points.
            start_trail_point_idx = max(
                i for i, t in enumerate(self.parent_datapoint["trail"])
                if self.segment_timestamp >= t["timestamp"]
            )
            if start_trail_point_idx < self.count_trail_points - 1:
                trail = self.augment_trail_with_interpolation(start_trail_point_idx + 1, start_trail_point_idx, trail)
        if len(trail) < 2:
            # We would need atleast two trail points in the segmented trail
            raise Exception(f"Unable to segment trail for {self.segment_timestamp}")
        return trail

    def get_updated_trip_datapoint(self) -> Dict[Text, Any]:
        """
        This method returns the updated trip datapoint for the segment, given the parent datapoint.
        """
        datapoint = deepcopy(self.parent_datapoint)
        events = self.get_segment_events()
        trail = self.get_segment_trail()
        distance_km = haversine_dist_wsgi_points(
            [(t["location"]["latitude"], t["location"]["longitude"]) for t in trail]
        )
        distance_km_parent = float(haversine_dist_wsgi_points(
            [(t["location"]["latitude"], t["location"]["longitude"]) for t in self.parent_datapoint['trail']]
        ))
        adjustment_factor = (
            (float(self.parent_datapoint["trip"]["distance"]) / 1000) /
            (1 if distance_km_parent == 0 else distance_km_parent)
        )
        drive_time = (self.segment_timestamp_end - self.segment_timestamp) / 1000
        datapoint["trip"]["distance"] = adjustment_factor * distance_km * 1000
        datapoint["trip"]["driveTime"] = drive_time
        datapoint['trip']['averageSpeed'] = (
                0 if drive_time == 0 else datapoint['trip']['distance'] / drive_time
        )
        if not self.is_first_segment:
            datapoint["trip"]["startLocation"] = trail[0]["location"]
        if not self.is_last_segment:
            datapoint["trip"]["endLocation"] = trail[-1]["location"]
        datapoint["trail"] = trail
        datapoint["events"] = events
        return datapoint
