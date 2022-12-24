import requests
import day_type
import mail as email

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
API_KEY = "f066a787ecdffdc525046a86aaa638d2"
LATITUDE = "41.94"
LONGITUDE = "21.25"

url = BASE_URL + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&appid=" + API_KEY

response = requests.get(url).json()
five_weather_data = response['list']
city = response['city']
potential_flyable_days = day_type.extract_day_forecast_object(five_weather_data, city)
valid_flyable_days = day_type.calculate_conditions_and_prepare_mail(potential_flyable_days)
valid_flyable_forecasts = day_type.get_flyable_forecasts(valid_flyable_days)
mail = day_type.compose_mail(valid_flyable_forecasts, city)
if mail != day_type.NOT_FLYABLE_DAY_TYPE:
    email.send_mail(mail_subject="Acro na Osoj - DETALNA PROGNOZA", mail_content=mail)
