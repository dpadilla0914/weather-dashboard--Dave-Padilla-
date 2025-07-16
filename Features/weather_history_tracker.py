#weather_history_tracker.py
"""
Feature: Weather History Tracker
-Saves daily weather to CSV. Displays the last seven days and calculates weekly average.
"""

import csv
import os
from datetime import datetime

HISTORY_FILE = "weather_history.csv"

def save_daily_weather(city, date, temp, condition):
    
    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists:
            writer.writerow(["city", "date", "temp", "condition"])
        
        writer.writerow([city, date, temp, condition])

def read_last_seven_days():
    
    if not os.path.exists(HISTORY_FILE):
        return []

    last_seven_days = []
    today = datetime.now().date()

    with open(HISTORY_FILE, "r") as csvfile:
        reader = csv.DictReader(csvfile)
       
        for row in reader:
            try:
                row_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                if (today - row_date).days < 7:
                    last_seven_days.append({
                        "city": row["city"],
                        "date": row["date"],
                        "temp": float(row["temp"]),
                        "condition": row["condition"]
                    })
            except (ValueError, KeyError):
                continue

    return last_seven_days

def calculate_weekly_avg(data):
    if not data:
        return None

    temps = [entry["temp"] for entry in data]
    return round(sum(temps) / len(temps), 2)