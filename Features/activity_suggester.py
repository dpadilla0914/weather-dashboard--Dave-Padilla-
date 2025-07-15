#activity_suggester.py
"""Feature: Activity Suggester
-Suggest activity based on weather
"""

def suggest_activity(weather)

    weather = weather.lower()

    if "sun" in weather:
        return "It's sunny! How about going for a hike or a picnic?"

    elif "rain" in weather:
        return "Rainy weather calls for indoor activities. Maybe visit a museum or watch a movie at home."

    elif "snow"in weather:
        return "It's snowing. Great day for building a snow man or skiing!"

    elif "cloud" in weather:
        return "Cloudy skies are perfect for a walk in the park or reading a book outside."

    elif "storm" in weather or "thunder" in weather:
        return "Better to stay indoors during a storm. Try a new recipe or playing some games."

    else:
        return "Weather is a bit unclear. Go with what feels good."