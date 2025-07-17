#temperature_graph.py
"""
Feature: Temperature Graph
-Shows line graph of temperature history for a number of days using matplotlib and tkinter
"""
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime

def get_forecast(city, days = 7):
    geocode_url = (f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")
    response = requests.get(geocode_url)
    data = response.json()

    if not data:
        print("City not found.")
        return []

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    forecast_url = (f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=metric&appid={API_KEY}")
    response = requests.get(forecast_url)
    forecast_data = response.json()

    result = []
    for day_data in forecast_data["daily"][:days]:
        date = datetime.utcfromtimestamp(day_data["dt"]).strftime("%Y-%m-%d")
        temp = day_data["temp"]["day"]
        result.append((date, temp))

    return result

def plot_graph(city)
    forecast = get_forecast(city)
    dates = [day for day, temp in forecast]
    temps = [temp for day, temp in forecast]

    root = tk.Tk()
    root.title(f"Temperature History for {city}")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, temps, marker='o', linestyle='-', color='b')
    ax.set_title(f"Temperature Over Last {len(dates)} Days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True)
    plt.xticks(rotation=45)

    # Embed plot in tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()