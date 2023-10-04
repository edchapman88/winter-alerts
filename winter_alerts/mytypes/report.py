from typing import TypedDict
from winter_alerts.mytypes.history import Yesterday

class Outlook(TypedDict):
    good: bool
    temperature_max: list[float]
    temperature_min: list[float]
    predictability: list[int]
    precipitation: list[float]
    precipitation_probability: list[int]
    windspeed_mean: list[float]
    windspeed_max: list[float]
    winddirection: list[str]


class RecentAscent(TypedDict):
    route: str
    grade: str
    date: str

class Report(TypedDict):
    name: str
    outlook: Outlook
    history: list[Yesterday]
    # winter_forecast_rating: str
    recent_acents: list[RecentAscent]


class Reports(TypedDict):
    locations: list[Report]