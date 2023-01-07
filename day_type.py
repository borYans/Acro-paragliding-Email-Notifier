import datetime
import day_conditions_data_model
import converter
import constants
import datetime as dt

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

    print(f"Currently is flyable at the site [True, False]: {is_flyable_condition}")

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
def compose_mail(list_of_three_hour_forecasts, city):
    flyable_days_mail = ""
    index = 0
    for flyable in list_of_three_hour_forecasts:
        timestamp = flyable['dt']
        current_timestamp = city['timezone']
        date = dt.datetime.fromtimestamp(timestamp - current_timestamp)
        temp = converter.kelvin_to_celsius(flyable['main']['temp'])
        wind_speed = flyable['wind']['speed']
        humidity_percentage = flyable['main']['humidity']
        pressure = flyable['main']['pressure']
        cloud_percentage = flyable['clouds']['all']
        wind_direction = converter.get_wind_direction(flyable['wind']['deg'])
        wind_gust = flyable['wind']['gust']

        if index == 0:
            flyable_days_mail += get_mail_content_with_short_desc(
                date, temp, wind_direction, wind_speed, wind_gust, humidity_percentage, pressure, cloud_percentage
            )
        else:
            flyable_days_mail += get_mail_content(
                date, temp, wind_direction, wind_speed, wind_gust, humidity_percentage, pressure, cloud_percentage
            )
        index += 1

    print(flyable_days_mail)
    return flyable_days_mail


def get_mail_content_with_short_desc(
        date, temp, wind_direction, wind_speed, wind_gust, humidity_percentage, pressure, cloud_percentage):
    return f"Kratok opis na denot: " \
           f"{short_description(pressure, wind_speed, cloud_percentage)}\n\n" \
           f"\nPROGNOZA vo {date.hour}h na den {date} ({date.strftime('%A')})\nTemperatura: {round(temp)}C\n" \
           f"Veter: {wind_direction} {round(wind_speed)} m/s\n" \
           f"Veter na udari: {round(wind_gust)} m/s\n" \
           f"Pritisok: {pressure} hPa\nRelativna vlaznost: {humidity_percentage}%.\n" \
           f"Oblacnost: {cloud_percentage} %\n\n"


def get_mail_content(
        date, temp, wind_direction, wind_speed, wind_gust, humidity_percentage, pressure, cloud_percentage):
    return f"\nPROGNOZA vo {date.hour}h na den {date} ({date.strftime('%A')})\nTemperatura: {round(temp)}C\n" \
           f"Veter: {wind_direction} {round(wind_speed)} m/s\n" \
           f"Veter na udari: {round(wind_gust)} m/s\n" \
           f"Pritisok: {pressure} hPa\nRelativna vlaznost: {humidity_percentage}%.\n" \
           f"Oblacnost: {cloud_percentage} %\n\n"


def short_description(pressure, wind, cloud_percentage):
    description = ""
    if pressure < 1015:
        description += f" Pritisokot ke bide dosta nizok i termikite ke se otkacuvaat" \
                       f" na mnogu mala promena na reljefot. Intervalite dosta kratki," \
                       f" vnimatelno biraj moment za poletuvanje."
    else:
        description += f" Pritisokot ke bide odlicen. Dovolno nizok kade ke treba mala energija na sonceto" \
                       f" da generira termika.\n"

    if cloud_percentage < 40:
        description += f"Na momenti ke ima intervali kade sto oblaci ke go pokrivaat trigerot na nivite podolu.\n" \
                       f"Najavena oblacnost e {cloud_percentage}% vo tekot na denot sto znacitelno ke " \
                       f"drzat ciklusite za poletuvanje. " \
                       f" Celo vreme treba da ima termika i da se leta podolgo vreme.\n"
    else:
        description += f"Pogolemi intervali na senka koj sto ke ja gasat termikata na odredeno vreme." \
                       f" Trpelivo da se ceka na start za dobar i jak interval.\n"

    if wind > 4:
        description += f"Veterot jak i stabilen. Malku ke gi kosi stubovite i" \
                       f" najdobro e da gi baras ponapred od padinata.\n"
    else:
        description += f"Nesto poslabo veterce ama dovolno da gi aktivira termikite od platoto dole." \
                       f" Trpelivo da se priceka za poletuvanje.\n"
    return description
