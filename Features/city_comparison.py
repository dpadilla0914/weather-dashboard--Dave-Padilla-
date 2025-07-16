#city_comparison.py
"""Feature: City Comparison
-Compare 2 or more cities and show temperature differences
"""

def city_comparison(weather_data = None):
    
    #If no data provided, uses default set of citites
    if weather_data is None:
        weather_data = {
            "New York": 28,
            "London": 22,
            "Tokyo": 31
        }

    output_lines = [] #Stores comparison of output lines
    cities = list(weather_data.keys()) #Get a list of city names from dictionary

    #Compare each pair of cities
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            city1 = cities[i]
            city2 = cities[j]
            diff = abs(weather_data[city1] - weather_data[city2]) #Calculates absolute temp
            output_lines.append(f"The temperature difference between {city1} and {city2} is {diff}°C.")

    #Join all lines with newline characters and return the final result
    return "\n".join(output_lines)

