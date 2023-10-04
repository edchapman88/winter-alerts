from typing import TypedDict

class MetaData(TypedDict):
    name: str
    latitude: float
    longitude: float
    height: int
    timezone_abbrevation: str
    utc_timeoffset: float
    modelrun_utc: int
    modelrun_updatetime_utc: int

class Units(TypedDict):
    time: str
    predictability: str
    precipitation_probability: str
    cloudcover: str
    pressure: str
    relativehumidity: str
    radiation: str
    ghi_total: str
    extraterrestrialradiation_total: str
    temperature: str
    precipitation: str
    windspeed: str
    winddirection: str

class TrendDay(TypedDict):
    time: list[int]
    pictocode: list[int]
    temperature_max: list[float]
    temperature_min: list[float]
    temperature_mean: list[float]
    temperature_spread: list[float]
    precipitation: list[float]
    precipitation_probability: list[int]
    precipitation_spread: list[float]
    windspeed_max: list[float]
    windspeed_min: list[float]
    windspeed_mean: list[float]
    windspeed_spread: list[float]
    winddirection: list[str]
    sealevelpressure_max: list[int]
    sealevelpressure_min: list[int]
    sealevelpressure_mean: list[int]
    relativehumidity_max: list[int]
    relativehumidity_min: list[int]
    relativehumidity_mean: list[int]
    snowfraction: list[float]
    predictability: list[int]
    predictability_class: list[int]
    totalcloudcover_max: list[int]
    totalcloudcover_min: list[int]
    totalcloudcover_mean: list[int]
    totalcloudcover_spread: list[int]
    ghi_total: list[int]
    extraterrestrialradiation_total: list[int]

class MBResponse(TypedDict):
    metadata: MetaData
    units: Units
    trend_day: TrendDay

    
    
