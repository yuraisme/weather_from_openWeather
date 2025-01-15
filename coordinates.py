from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    return Coordinates(latitude=54.892556, longitude=38.072565)
