from typing import TypedDict

class Location(TypedDict):
    name: str
    lat: float
    lon: float
    # "above sea level"
    asl: int
    crag_id: str