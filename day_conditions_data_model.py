from dataclasses import dataclass


@dataclass
class DayConditions:
    temp: int
    wind_speed: int
    wind_gusts: int
    wind_direction: int
    humidity_percentage: int
    cloud_percentage: int
    pressure: int
    rain_probability: int


@dataclass
class SiteRanges:
    pressure_range: range
    humidity_range: range
    cloud_cover_range: range
    wind_speed_range: range
    wind_gust_range: range
    wind_direction_ranges: list
    minimum_temperature: int
    minimum_rain: int
