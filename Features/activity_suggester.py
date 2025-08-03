#activity_suggester.py
"""Feature: Activity Suggester
-Suggest activity based on weather
"""
import os
import csv
import random

def load_teas_by_weather(folder_path='csv_data'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_folder_path = os.path.normpath(os.path.join(base_dir, '..', 'Docs', folder_path))

    teas_by_weather = {}

    if not os.path.exists(full_folder_path):
        raise FileNotFoundError(f"Teas folder not found at {full_folder_path}")

    for filename in os.listdir(full_folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(full_folder_path, filename)
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                required_headers = {'tea_name', 'weather_type'}
                missing = required_headers - set(reader.fieldnames)
                if missing:
                    raise ValueError(f"Missing required CSV headers: {missing} in {filename}")

                for row in reader:
                    weather_key = row['weather_type'].lower()
                    tea_info = {
                        'name': row['tea_name'].strip(),
                        'description': row.get('description', '').strip()
                    }
                    teas_by_weather.setdefault(weather_key, []).append(tea_info)

    return teas_by_weather

def suggest_activity(weather):
    weather = weather.lower()
    teas_by_weather = load_teas_by_weather()

    matching_teas = teas_by_weather.get(weather, [])
    if matching_teas:
        tea = random.choice(matching_teas)
    else:
        all_teas = [tea for teas in teas_by_weather.values() for tea in teas]
        tea = random.choice(all_teas) if all_teas else {'name': 'your favorite', 'description': ''}

    tea_suggestion = f"{tea['name']} – {tea['description']}" if tea['description'] else tea['name']

    weather_icons = {
        "sun": "☀️",
        "rain": "🌧️",
        "snow": "❄️",
        "cloud": "☁️",
        "storm": "⛈️",
        "thunder": "⛈️"
    }
    icon = next((emoji for key, emoji in weather_icons.items() if key in weather), "🌈")

    # Activity message
    if "sun" in weather:
        activity = "It's sunny! How about going for a hike or a picnic?"
    elif "rain" in weather:
        activity = "Rainy weather calls for indoor activities. Maybe visit a museum or watch a movie at home."
    elif "snow" in weather:
        activity = "It's snowing. Great day for building a snowman or skiing!"
    elif "cloud" in weather:
        activity = "Cloudy skies are perfect for a walk in the park or reading a book outside."
    elif "storm" in weather or "thunder" in weather:
        activity = "Better to stay indoors during a storm. Try a new recipe or play some games."
    else:
        activity = "Weather is a bit unclear. Go with what feels good."

    return (
        f"{icon} {activity}\n\n"
        f"🍵 Tea pairing: {tea_suggestion}"
    )