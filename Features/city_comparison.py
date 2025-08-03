#city_comparison.py
"""Feature: City Comparison
-Compare 2 or more cities and show temperature differences
"""

import requests

def get_current_temperature(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise Exception(data.get("message", "API error"))

    return data["main"]["temp"]

def compare_cities(city1, city2, api_key):
    temp1 = get_current_temperature(city1, api_key)
    temp2 = get_current_temperature(city2, api_key)
    diff = abs(temp1 - temp2)

    return {
        "city1": city1,
        "temp1": temp1,
        "city2": city2,
        "temp2": temp2,
        "difference": diff
    }