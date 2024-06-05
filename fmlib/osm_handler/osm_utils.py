import math
from typing import Tuple
from pyproj import Transformer


class OSMUtils(object):
    """
    This class contains methods to convert between spherical and cartesian coordinates.
    """
    spherical_2_cartesian_transformer = Transformer.from_crs(4326, 3857)
    cartesian_2_spherical_transformer = Transformer.from_crs(3857, 4326)

    @staticmethod
    def get_cartesian_point(latitude:float, longitude:float) -> Tuple[float, float]:
        x, y = OSMUtils.spherical_2_cartesian_transformer.transform(latitude, longitude)
        return x, y

    @staticmethod
    def get_spherical_point(point: Tuple[float, float]) -> Tuple[float, float]:
        x, y = point
        latitude, longitude = OSMUtils.cartesian_2_spherical_transformer.transform(x, y)
        return latitude, longitude

    @staticmethod
    def num2deg(x_tile, y_tile, zoom):
        n = 2.0 ** zoom
        lon_deg = x_tile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
        lat_deg = math.degrees(lat_rad)
        return lat_deg, lon_deg

    @staticmethod
    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        x_tile = int((lon_deg + 180.0) / 360.0 * n)
        y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return x_tile, y_tile
