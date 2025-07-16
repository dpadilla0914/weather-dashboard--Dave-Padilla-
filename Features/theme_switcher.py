#theme_switcher.py
"""
Feature: Theme Switcher
-Day/night mode and weather based colors. Also adds user preferences
"""

import json
import os

PREF_FILENAME = "preferences.json"

def load_preferences():
    if not os.path.exists(PREF_FILENAME):
        return {"theme": "light", "untis": "metric"} #Default preferences

    with open(PREF_FILENAME, "r") as f:
        try:
            prefs = json.load(f)
            prefs.setdefault("theme", "light")
            prefs.setdefault("units", "metric")
            return prefs

        except JSONDecodeError:
            return {"theme": "light", "units": "metric"}

def save_preferences(preferences):
    with open(PREF_FILENAME, "w") as f:
        json.dump(preferences, f, indent = 4)

def get_theme_colors(theme, weather_condition = None):
    themes = {
    "light": {
            "background": "#FFFFFF",
            "text": "#000000",
            "primary": "#007ACC",
            "secondary": "#005A9E"
        },
        "dark": {
            "background": "#1E1E1E",
            "text": "#FFFFFF",
            "primary": "#0A84FF",
            "secondary": "#005A9E"
        }
    }

    weather_accents = {
        "sunny": "#FFD700",      # gold
        "rainy": "#00ADEF",      # blue
        "cloudy": "#A0A0A0",     # gray
        "snow": "#FFFFFF",       # white
        "storm": "#800000"       # dark red
    }

    colors = themes.get(theme.lower(), themes["light"]).copy()

    #Overirde primary color with weather accent
    if weather_condition:
        accent = weather_accents.get(weather_condition.lower())
        if accent:
            colors["primary"] = accent

    return colors