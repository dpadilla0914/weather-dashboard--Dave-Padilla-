#trend_detection.py
"""
Feature: Trend Detection
-Shows temperature trend arrows, pattern identification and simple analysis
"""

def detect_trend(temps):
    trends = []
    for i in range(1, len(temps)):
        
        if temps[i] > temps[i - 1]:
            trends.append("↑")
        elif temps[i] < temps[i - 1]:
            trends.append("↓")
        else:
            trends.append("-")
    return trends

def analyze_pattern(temps):
    
    if len(temps) < 2:
        return "Not enough data to analyze."

    trend = detect_trend(temps)
    up = trend.count("↑")
    down = trend.count("↓")
    flat = trend.count("-")

    if up > down and up > flat:
        return "Overall warming trend."
    elif down > up and down > flat:
        return "Overall cooling trend."
    elif flat > up and flat > down:
        return "Stable pattern."
    else:
        return "Fluctuating temperatures."

def display_trend_summary(temps):
    trends = detect_trend(temps)
    pattern = analyze_pattern(temps)
    trend_line = " ".join(trends)
    return f"Trend: {trend_line}\nPattern: {pattern}"