"""Geography utilities."""
from typing import List, Tuple
import math


def old_div(x, y):
    return 0 if y == 0 else x / y


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Haversine distance between 2 points on the map.
    :param float lat1: Latitude in degress of first point.
    :param float lon1: Longitude in degress of first point.
    :param float lat2: Latitude in degress of second point.
    :param float lon2: Longitude in degress of second point.
    :return: Distance in kms.
    :rtype: float
    """
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(old_div(dlat, 2)) * math.sin(old_div(dlat, 2)) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(old_div(dlon, 2)) * math.sin(old_div(dlon, 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def haversine_dist_wsgi_points(wsgi_points: List[Tuple[float, float]]) -> float:
    dist = 0
    for i in range(len(wsgi_points) - 1):
        p1 = wsgi_points[i]
        p2 = wsgi_points[i + 1]
        dist += haversine_distance(lat1=p1[0], lon1=p1[1], lat2=p2[0], lon2=p2[1])
    return dist
