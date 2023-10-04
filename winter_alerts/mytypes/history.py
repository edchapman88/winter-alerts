from typing import TypedDict

class Yesterday(TypedDict):
    temperature_max: float
    temperature_min: float
    precipitation: float
    windspeed_max: float
    windspeed_mean: float
    winddirection: str
    snowfraction: float

class History(TypedDict):
    # partition key
    pk: str
    timestamp: int
    locations: dict[str, Yesterday]
    

    