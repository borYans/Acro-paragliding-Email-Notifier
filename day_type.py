import converter
import datetime as dt

NOT_FLYABLE_DAY_TYPE = ""

# Pressure constants
FIZZY_DAY = range(1013, 1022)

# Humidity constants
MEDIUM_AIR_HUMIDITY = range(31, 60)

# Cloud cover constants
CLOUD_COVER = range(0, 80)

# Wind speed constants
WIND_SPEED_RANGE = (3, 7)
WIND_GUSTS_RANGE = (0, 8)

# Time of the day constant
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DAY_TIME = range(8, 16)

# Temperature constants
TEMP_CONSTANT = 8

# Rain constants
RAIN_PROBABILITY = 30

list_of_forecasts = []


# Takes five-day forecast with every 3h data object and calculates which days are potentially flyable.
# Validate only forecast which are between 12'o clock and 18'o clock.
# returns dictionary with [key] = day of the week, and [value] = list of 3 hours forecasts [max 3 forecast]
def extract_day_forecast_object(five_days_forecast, city):
    potential_flyable_days = dict()
    for three_hour_forecast in five_days_forecast:
        timestamp = three_hour_forecast['dt']
        current_timestamp = city['timezone']
        date = dt.datetime.fromtimestamp(timestamp - current_timestamp)
        previous_day_name = (date - dt.timedelta(days=1)).strftime("%A")
        is_next_day = date.hour == 0
        if is_next_day:
            potential_flyable_days[previous_day_name] = list_of_forecasts
        else:
            if date.hour in DAY_TIME:
                is_accepted_forecast = is_flyable_day(forecast=three_hour_forecast)
                if is_accepted_forecast:
                    list_of_forecasts.append(three_hour_forecast)

    return potential_flyable_days


# Takes dictionary with [key] = day of the week and [value] = list of 3 hours forecasts [max 3 forecasts]
# Filter flyable days = minimum 2 validated flyable forecasts.
# create a mail and return it.
def calculate_conditions_and_prepare_mail(forecast_days):
    days_to_fly = dict()
    for day, flyable_days in forecast_days.items():
        full_day = {day: list(filter(lambda fly_day: len(fly_day) >= 3, flyable_days))}
        days_to_fly = full_day

    return days_to_fly


# Validate if day is flyable based on several conditions.
def is_flyable_day(forecast):
    temp = converter.kelvin_to_celsius(forecast['main']['temp'])
    wind_speed = round(forecast['wind']['speed'])
    wind_gust = round(forecast['wind']['gust'])
    wind_direction = converter.get_wind_direction(forecast['wind']['deg'])
    clouds_percentage = forecast['clouds']['all']
    humidity_percentage = forecast['main']['humidity']
    pressure = forecast['main']['pressure']
    rain_probability = forecast['pop']
    date = dt.datetime.strptime(forecast['dt_txt'], DATE_TIME_FORMAT)

    is_wind_valid = (wind_speed in WIND_SPEED_RANGE) and (wind_gust in WIND_GUSTS_RANGE)
    is_temperature_valid = temp < TEMP_CONSTANT
    is_wind_direction_valid = wind_direction in converter.N_1 or wind_direction in converter.N_2
    is_cloud_valid = clouds_percentage in CLOUD_COVER
    is_humidity_valid = humidity_percentage in MEDIUM_AIR_HUMIDITY
    is_pressure_valid = pressure in FIZZY_DAY
    is_rain_valid = rain_probability < RAIN_PROBABILITY

    is_flyable_condition = is_temperature_valid \
                           # and is_rain_valid and is_pressure_valid and is_humidity_valid \
                           # and is_cloud_valid \
                           # and is_wind_direction_valid \
                           # and is_wind_valid
    return is_flyable_condition


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
           f"{short_description(pressure, wind_speed, date.hour, cloud_percentage)}\n\n" \
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


def short_description(pressure, wind, hour, cloud_percentage):
    description = ""
    if pressure < 1015:
        description += f" Vo {hour}h pritisokot ke bide dosta nizok i termikite ke se otkacuvaat" \
                       f" na mnogu mala promena na reljefot. Intervalite dosta kratki," \
                       f" vnimatelno biraj moment za poletuvanje."
    else:
        description += f" Vo {hour}h pritisokot ke bide odlicen. Dovolno nizok kade ke treba mala energija na sonceto" \
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
