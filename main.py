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


def is_valid_response(response_code):
    return response_code == 200


for site, coordinates in sorted_locations:
    print(f"\nGetting values for {site}")
    url = BASE_URL + "lat=" + coordinates[0] + "&lon=" + coordinates[1] + "&appid=" + API_KEY
    response_body = requests.get(url)

    if is_valid_response(response_body.status_code):
        response = response_body.json()
        five_weather_data = response['list']
        city = response['city']
        potential_flyable_days = day_type.extract_day_forecast_object(five_weather_data, city, site)
        valid_flyable_days = day_type.calculate_conditions_and_prepare_mail(potential_flyable_days)
        valid_flyable_forecasts = day_type.get_flyable_forecasts(valid_flyable_days)
        day_type.create_and_send_mails(valid_flyable_forecasts, city, site)
    else:
        print(f"Exception occured with response code: {response_body.status_code}")
