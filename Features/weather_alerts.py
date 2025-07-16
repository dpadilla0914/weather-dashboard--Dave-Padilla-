#weather_alerts.py
"""
Feature: Weather Alerts
-Shows weather advisory for extreme temperatures based on user setting
"""

import json
import os


PREF_FILENAME = "preferences.json"

def load_preferences():
    if not os.path.exists(PREF_FILENAME):
        return {
            "theme": "light",
            "units": "metric",
            "alert_high": 35.0,   # Default alert if temp exceeds 35°C
            "alert_low": -5.0     # Default alert if temp drops below -5°C
        }

    with open(PREF_FILENAME, "r") as f:
        try:
            prefs = json.load(f)
        except json.JSONDecodeError:
            prefs = {}

    # Apply defaults if keys are missing
    prefs.setdefault("theme", "light")
    prefs.setdefault("units", "metric")
    prefs.setdefault("alert_high", 35.0)
    prefs.setdefault("alert_low", -5.0)

    return prefs

def save_preferences(prefs):
    with open(PREF_FILENAME, "w") as f:
        json.dump(prefs, f, indent=4)

def check_alerts(temp_f, prefs = None):
    if prefs is None:
        prefs = load_preferences()

    high = prefs.get("alert_high", 35.0)
    low = prefs.get("alert_low", -5.0)

    if temp_f >= high:
        return f"🚨 Heat alert! Temperature is {temp_f}°C (threshold: {high}°C)"
    elif temp_f <= low:
        return f"❄️ Cold alert! Temperature is {temp_f}°C (threshold: {low}°C)"
    else:
        return None