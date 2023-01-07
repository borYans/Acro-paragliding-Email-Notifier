import requests
import day_type
import constants
import mail as email

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
API_KEY = "f066a787ecdffdc525046a86aaa638d2"

locations = {
    'Osoj': ['41.94', '21.25'],
    'Vodno': ['41.9650', '21.3944']
}
sorted_locations = sorted(locations.items())

for site, coordinates in sorted_locations:
    print(f"Getting values for {site}")
    url = BASE_URL + "lat=" + coordinates[0] + "&lon=" + coordinates[1] + "&appid=" + API_KEY
    response_body = requests.get(url)

    if response_body.status_code == 200:
        response = response_body.json()
        five_weather_data = response['list']
        city = response['city']
        potential_flyable_days = day_type.extract_day_forecast_object(five_weather_data, city, site)
        valid_flyable_days = day_type.calculate_conditions_and_prepare_mail(potential_flyable_days)
        valid_flyable_forecasts = day_type.get_flyable_forecasts(valid_flyable_days)
        mail = day_type.compose_mail(valid_flyable_forecasts, city)
        if mail != constants.NOT_FLYABLE_DAY_TYPE:
            email.send_mail(mail_subject=f"Acro na {site} - DETALNA PROGNOZA", mail_content=mail)
    else:
        email.send_mail(mail_subject=f"Acro na {site} - DETALNA ANALIZA",
                        mail_content="Ne sme vo moznost da dobieme podatoci od vremenska prognoza.")
