#favorite_cities.py
"""
Feature: Favorite Cities
-Save preferred locations for quick switching and persistent storage
"""

import json
import os

FILENAME = "favorites.json"

def load_favorites():
    if not os.path.exists(FILENAME):
        return []
    
    with open(FILENAME, "r") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, list) else []

        except json.JSONDecodeError:
            return []

def save_favorites(cities):
    with open(FILENAME, "w") as file:
        json.dump(cities, file, indent = 4)

def add_favorite(city):
    city = city.strip().title() #Clean and standardize city name
    cities = load_favorites()

    if city not in cities:
        cities.append(city)
        save_favorites(cities)
        print(f"{city} has been added to your favorites.")

    else:
        print(f"{city} is already in your favorites.")

def remove_favorite(city):
    city = city.strip().title()
    cities = load_favorites()

    if city in cities:
        cities.remove(city)
        save_favorites(cities)
        print(f"{city} has been removed from your favorites.")

    else:
        print(f"{city} is not in your favorites.")

    def show_favorites():
        cities = load_favorites()
        if not cities:
            print("No favorite cities saved.")

        else:
            print("Your favorite cities: ")
            for city in cities:
                print(f"-{city}")