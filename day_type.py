import datetime
import day_conditions_data_model
import converter
import constants
import datetime as dt

import mail_factory
from mail_factory import MailFactory

list_of_forecasts = []
VODNO_SITE = 'Vodno'
OSOJ_SITE = 'Osoj'
AJVATOVCI_SITE = 'Ajvatovci'
SKOPSKA_CRNA_GORA = 'Skopska Crna Gora'


# Takes five-day forecast with every 3h data object and calculates which days are potentially flyable.
# Validate only forecast which are between 8'o clock and 16'o clock.
def extract_day_forecast_object(five_days_forecast, city, take_off_site):
    current_day = datetime.datetime.today().now()
    for three_hour_forecast in five_days_forecast:
        date = get_date(city, three_hour_forecast)
        is_next_day = current_day.day != date.day
        current_day = date
        if is_next_day:
            if len(list_of_forecasts) >= 2:
                print(f"Flyable forecasts: {len(list_of_forecasts)}")
                print("\n")
                first_flyable_forecast = list_of_forecasts[0]
                mail_model = mail_factory.MailDataModel(
                    site=take_off_site,
                    wind_direction=get_wind_direction(first_flyable_forecast),
                    wind_speed=get_wind_speed(first_flyable_forecast),
                    wind_gust=get_wind_gusts(first_flyable_forecast),
                    date=get_date(city, first_flyable_forecast)
                )
                MailFactory.send_mail(mail_model)
                list_of_forecasts.clear()
                break

        else:
            if date.hour in constants.DAY_TIME:
                is_accepted_forecast = is_flyable_day(forecast=three_hour_forecast, site=take_off_site)
                if is_accepted_forecast:
                    list_of_forecasts.append(three_hour_forecast)


def get_date(city, three_hour_forecast):
    timestamp = three_hour_forecast['dt']
    current_timestamp = city['timezone']
    date = dt.datetime.fromtimestamp(timestamp - current_timestamp)
    return date


def get_wind_gusts(three_hour_forecast):
    return round(three_hour_forecast['wind']['gust'])


def get_wind_speed(three_hour_forecast):
    return round(three_hour_forecast['wind']['speed'])


def get_wind_direction(three_hour_forecast):
    return round(three_hour_forecast['wind']['deg'])


def is_flyable_at_the_site(day_conditions, site_ranges):
    is_wind_valid = (day_conditions.wind_speed in site_ranges.wind_speed_range) \
                    and (day_conditions.wind_gusts in site_ranges.wind_gust_range)

    is_temperature_valid = day_conditions.temp > site_ranges.minimum_temperature

    is_wind_direction_valid = day_conditions.wind_direction in site_ranges.wind_direction_ranges

    is_cloud_valid = day_conditions.cloud_percentage in site_ranges.cloud_cover_range

    is_humidity_valid = day_conditions.humidity_percentage in site_ranges.humidity_range

    is_pressure_valid = day_conditions.pressure in site_ranges.pressure_range

    is_rain_valid = round((day_conditions.rain_probability * 100)) < site_ranges.minimum_rain

    is_flyable_condition = is_temperature_valid \
                           and is_rain_valid and is_pressure_valid and is_humidity_valid \
                           and is_cloud_valid and is_wind_direction_valid and is_wind_valid

    return is_flyable_condition


# Validate if day is flyable based on several conditions.
def is_flyable_day(forecast, site):
    day_conditions = get_day_conditions_from_response(forecast)

    if site == VODNO_SITE:
        site_ranges = get_ranges_for_vodno()
        return is_flyable_at_the_site(day_conditions, site_ranges)

    elif site == OSOJ_SITE:
        site_ranges = get_ranges_for_osoj()
        return is_flyable_at_the_site(day_conditions, site_ranges)

    elif site == AJVATOVCI_SITE:
        site_ranges = get_ranges_for_ajvatovci()
        return is_flyable_at_the_site(day_conditions, site_ranges)

    elif site == SKOPSKA_CRNA_GORA:
        site_ranges = get_ranges_for_skopska_crna_gora()
        return is_flyable_at_the_site(day_conditions, site_ranges)


def get_day_conditions_from_response(forecast):
    day_conditions = day_conditions_data_model.DayConditions(
        temp=converter.kelvin_to_celsius(forecast['main']['temp']),
        wind_speed=round(forecast['wind']['speed']),
        wind_gusts=round(forecast['wind']['gust']),
        wind_direction=round(forecast['wind']['deg']),
        cloud_percentage=forecast['clouds']['all'],
        humidity_percentage=forecast['main']['humidity'],
        pressure=forecast['main']['pressure'],
        rain_probability=forecast['pop']
    )
    return day_conditions


def get_ranges_for_osoj():
    site_ranges = day_conditions_data_model.SiteRanges(
        pressure_range=constants.FIZZY_DAY_OSOJ,
        humidity_range=constants.MEDIUM_AIR_HUMIDITY_OSOJ,
        cloud_cover_range=constants.CLOUD_COVER_OSOJ,
        wind_speed_range=constants.WIND_SPEED_RANGE_OSOJ,
        wind_gust_range=constants.WIND_GUSTS_RANGE_OSOJ,
        minimum_temperature=constants.TEMP_CONSTANT_OSOJ,
        minimum_rain=constants.RAIN_PROBABILITY_OSOJ,
        wind_direction_ranges=[converter.N_1, converter.N_2, converter.NE, converter.NW, converter.NNE, converter.NNW]
    )
    return site_ranges


def get_ranges_for_vodno():
    site_ranges = day_conditions_data_model.SiteRanges(
        pressure_range=constants.FIZZY_DAY_VODNO,
        humidity_range=constants.MEDIUM_AIR_HUMIDITY_VODNO,
        cloud_cover_range=constants.CLOUD_COVER_VODNO,
        wind_speed_range=constants.WIND_SPEED_RANGE_VODNO,
        wind_gust_range=constants.WIND_GUSTS_RANGE_VODNO,
        minimum_temperature=constants.TEMP_CONSTANT_VODNO,
        minimum_rain=constants.RAIN_PROBABILITY_VODNO,
        wind_direction_ranges=[converter.N_1, converter.N_2, converter.NE, converter.NW, converter.NNE, converter.NNW]
    )
    return site_ranges


def get_ranges_for_ajvatovci():
    site_ranges = day_conditions_data_model.SiteRanges(
        pressure_range=constants.PRESSURE_AJVATOVCI,
        humidity_range=constants.MEDIUM_AIR_HUMIDITY_AJVATOVCI,
        cloud_cover_range=constants.CLOUD_COVER_AJVATOVCI,
        wind_speed_range=constants.WIND_SPEED_RANGE_AJVATOVCI,
        wind_gust_range=constants.WIND_GUSTS_RANGE_AJVATOVCI,
        minimum_temperature=constants.TEMP_CONSTANT_AJVATOVCI,
        minimum_rain=constants.RAIN_PROBABILITY_AJVATOVCI,
        wind_direction_ranges=[converter.S, converter.SW, converter.SE, converter.SSE, converter.SSW, converter.ESE]
    )
    return site_ranges


def get_ranges_for_skopska_crna_gora():
    site_ranges = day_conditions_data_model.SiteRanges(
        pressure_range=constants.PRESSURE_SKOPSKA_CRNA_GORA,
        humidity_range=constants.MEDIUM_AIR_HUMIDITY_SKOPSKA_CRNA_GORA,
        cloud_cover_range=constants.CLOUD_COVER_SKOPSKA_CRNA_GORA,
        wind_speed_range=constants.WIND_SPEED_RANGE_SKOPSKA_CRNA_GORA,
        wind_gust_range=constants.WIND_GUSTS_RANGE_SKOPSKA_CRNA_GORA,
        minimum_temperature=constants.TEMP_CONSTANT_SKOPSKA_CRNA_GORA,
        minimum_rain=constants.RAIN_PROBABILITY_SKOPSKA_CRNA_GORA,
        wind_direction_ranges=[converter.S, converter.SW, converter.SE, converter.SSE, converter.SSW, converter.ESE]
    )
    return site_ranges
