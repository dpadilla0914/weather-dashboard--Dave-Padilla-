#theme_switcher.py
"""
Feature: Theme Switcher
-Day/night mode and weather based colors. Also adds user preferences
"""

import json
import os
from json.decoder import JSONDecodeError

PREF_FILENAME = "preferences.json"

def load_preferences():
    if not os.path.exists(PREF_FILENAME):
        return {"theme": "light", "units": "metric", "custom_colors": {}}  # Default prefs

    with open(PREF_FILENAME, "r") as f:
        try:
            prefs = json.load(f)
            prefs.setdefault("theme", "light")
            prefs.setdefault("units", "metric")
            prefs.setdefault("custom_colors", {})
            return prefs

        except JSONDecodeError:
            return {"theme": "light", "units": "metric", "custom_colors": {}}

def save_preferences(preferences):
    with open(PREF_FILENAME, "w") as f:
        json.dump(preferences, f, indent=4)

def get_theme_colors(theme_name: str, custom_colors: dict = None) -> dict:
    default_themes = {
        "light": {
            "background": "#F9F9F9",
            "primary": "#229954",
            "secondary": "#C8E6C9",  # Light green shade for sidebar
            "text": "#333333",
        },
        "dark": {
            "background": "#2C3E50",
            "primary": "#1ABC9C",
            "secondary": "#34495E",  # Darker blue shade for sidebar
            "text": "#ECF0F1",
        }
    }

    theme_colors = default_themes.get(theme_name, default_themes["light"]).copy()

    if custom_colors:
        # Allow override for secondary as well
        for key in ["background", "primary", "secondary"]:
            if key in custom_colors:
                theme_colors[key] = custom_colors[key]

    return theme_colors