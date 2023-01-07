import datetime
import day_conditions_data_model
import converter
import constants
import datetime as dt

from mail_factory import MailFactory

list_of_forecasts = []
VODNO_SITE = 'Vodno'
OSOJ_SITE = 'Osoj'


# Takes five-day forecast with every 3h data object and calculates which days are potentially flyable.
# Validate only forecast which are between 8'o clock and 16'o clock.
# returns dictionary with [key] = day of the week, and [value] = list of 3 hours forecasts [max 3 forecast]
def extract_day_forecast_object(five_days_forecast, city, take_off_site):
    potential_flyable_days = dict()
    current_day = datetime.datetime.today().now()
    for three_hour_forecast in five_days_forecast:
        timestamp = three_hour_forecast['dt']
        current_timestamp = city['timezone']
        date = dt.datetime.fromtimestamp(timestamp - current_timestamp)
        previous_day_name = (date - dt.timedelta(days=1)).strftime("%A")
        is_next_day = current_day.day != date.day
        current_day = date
        if is_next_day:
            potential_flyable_days[previous_day_name] = list_of_forecasts
        else:
            if date.hour in constants.DAY_TIME:
                is_accepted_forecast = is_flyable_day(forecast=three_hour_forecast, site=take_off_site)
                if is_accepted_forecast:
                    list_of_forecasts.append(three_hour_forecast)

    return potential_flyable_days


# Takes dictionary with [key] = day of the week and [value] = list of 3 hours forecasts [max 3 forecasts]
# Filter flyable days = minimum 2 validated flyable forecasts.
# create a mail and return it.
def calculate_conditions_and_prepare_mail(forecast_days):
    days_to_fly = dict()
    for day, flyable_days in forecast_days.items():
        full_day = {day: list(filter(lambda fly_day: len(fly_day) >= 2, flyable_days))}
        days_to_fly = full_day

    return days_to_fly


def is_flyable_at_the_site(day_conditions, site_ranges):
    is_wind_valid = (day_conditions.wind_speed in site_ranges.wind_speed_range) \
                    and (day_conditions.wind_gusts in site_ranges.wind_gust_range)

    is_temperature_valid = day_conditions.temp > site_ranges.minimum_temperature

    is_wind_direction_valid = day_conditions.wind_direction in [converter.N_1, converter.N_2, converter.NNW,
                                                                converter.NW, converter.NE, converter.NNE]
    is_cloud_valid = day_conditions.cloud_percentage in site_ranges.cloud_cover_range

    is_humidity_valid = day_conditions.humidity_percentage in site_ranges.humidity_range

    is_pressure_valid = day_conditions.pressure in site_ranges.pressure_range

    is_rain_valid = day_conditions.rain_probability < site_ranges.minimum_rain

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
        minimum_rain=constants.RAIN_PROBABILITY_OSOJ
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
        minimum_rain=constants.RAIN_PROBABILITY_VODNO
    )
    return site_ranges


# Extract only values from days_to_fly dictionary and compose mail out of the values.
def get_flyable_forecasts(days_to_fly):
    days = []
    for day in days_to_fly:
        days = days_to_fly[day]

    return days


# Create a mail for every flyable forecast in detail.
def create_and_send_mails(list_of_three_hour_forecasts, city, take_off_site):
    for flyable in list_of_three_hour_forecasts:
        timestamp = flyable['dt']
        current_timestamp = city['timezone']
        date = dt.datetime.fromtimestamp(timestamp - current_timestamp)

        three_hour_forecast = day_conditions_data_model.DayConditions(
            temp=converter.kelvin_to_celsius(flyable['main']['temp']),
            wind_speed=flyable['wind']['speed'],
            humidity_percentage=flyable['main']['humidity'],
            pressure=flyable['main']['pressure'],
            cloud_percentage=flyable['clouds']['all'],
            wind_direction=converter.get_wind_direction(flyable['wind']['deg']),
            wind_gusts=flyable['wind']['gust'],
            rain_probability=0
        )

        if take_off_site == OSOJ_SITE:
            MailFactory.send_mail(mail_type=OSOJ_SITE, wind=three_hour_forecast.wind_speed,
                                  wind_gust=three_hour_forecast.wind_gusts, date=date)
        elif take_off_site == VODNO_SITE:
            MailFactory.send_mail(mail_type=VODNO_SITE, wind=three_hour_forecast.wind_speed,
                                  wind_gust=three_hour_forecast.wind_gusts, date=date)

        break
