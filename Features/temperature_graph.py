# #temperature_graph.py
# """
# Feature: Temperature Graph
# -Shows line graph of temperature history for a number of days using matplotlib and tkinter
# """
# from urllib import response
# import requests
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
# from datetime import datetime
# from collections import defaultdict

# API_KEY = "e5eb15476fed360e2c3a04f0328e4a4f"
# if not API_KEY:
#     raise ValueError("API key not found. Set API_KEY environment variable.")

# def get_forecast(city, days = 5):
#     geocode_url = (f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")
#     response = requests.get(geocode_url)
#      data = response.json()
    
#     if not data:
#         print("City not found.")
#         return []

#     lat = data[0]["lat"]
#     lon = data[0]["lon"]

#     forecast_url = (
#     f"https://api.openweathermap.org/data/2.5/forecast"
#     f"?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
# )
#     response = requests.get(forecast_url)
#     forecast_data = response.json()
    
    
#     dates = []
#     temps = []
#     temps_by_date = defaultdict(list)

#     for entry in forecast_data["list"]:
#         date = entry["dt_txt"].split(" ")[0]
#         temp = entry["main"]["temp"]
#         temps_by_date[date].append(temp)

#     for date in sorted(temps_by_date.keys())[:days]:
#         avg_temp = sum(temps_by_date[date]) / len(temps_by_date[date])
#         dates.append(date)
#         temps.append(avg_temp)
        
#     fig, ax = plt.subplots()
#     ax.plot(dates, temps, marker='o', linestyle='-')
#     ax.set_title(f"{days}-Day Forecast for {city}")
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Temperature (°C)")
#     ax.grid(True)
#     plt.xticks(rotation=45)


#     return fig
import requests
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

API_KEY = "e5eb15476fed360e2c3a04f0328e4a4f"

def get_forecast(city, days=5):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(geocode_url)
    data = response.json()

    if not data:
        print("City not found.")
        return [], None

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    )
    response = requests.get(forecast_url)
    forecast_data = response.json()

    temps_by_date = defaultdict(list)
    conditions_by_date = defaultdict(list)

    for entry in forecast_data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]
        condition = entry["weather"][0]["main"]  # e.g., "Rain", "Clouds", etc.
        temps_by_date[date].append(temp)
        conditions_by_date[date].append(condition)

    forecast_summary = []
    dates = []
    avg_temps = []

    for date in sorted(temps_by_date.keys())[:days]:
        avg_temp = sum(temps_by_date[date]) / len(temps_by_date[date])
        most_common_condition = Counter(conditions_by_date[date]).most_common(1)[0][0]

        forecast_summary.append({
            "date": date,
            "temp": round(avg_temp, 1),
            "condition": most_common_condition
        })

        dates.append(date)
        avg_temps.append(avg_temp)

    # Create graph
    fig, ax = plt.subplots()
    ax.plot(dates, avg_temps, marker='o', linestyle='-', color='tab:blue')
    ax.set_title(f"{days}-Day Forecast for {city.title()}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True)
    plt.xticks(rotation=45)

    return forecast_summary, fig