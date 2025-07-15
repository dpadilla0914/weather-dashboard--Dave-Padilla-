#tomorrows_guess.py
"""
Feature: Tomorrow's Guess
-Predicts tomorrows weather based on basic prediction logic. Shows confidence levels and accuracy tracking
"""

def predict_tomorrow(city):
    forecast = get_forecast(city, days=2)
    if len(forecast) < 2:
        return ("unknown", "low")

    today_temp = forecast[-1][1]
    yesterday_temp = forecast[-2][1]

    if today_temp > yesterday_temp + 2:
        guess = "sunny"
        confidence = "medium"
    elif today_temp < yesterday_temp - 2:
        guess = "cloudy"
        confidence = "medium"
    else:
        guess = random.choice(["cloudy", "sunny", "rainy"])
        confidence = "low"

    return guess, confidence

def save_guess(city, guess, actual = None):
    record = {
        "city": city,
        "guess": guess,
        "actual": actual,
        "matched": guess == actual if actual else None
    }

    if os.path.exists(GUESS_FILE):
        with open(GUESS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(record)

    with open(GUESS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_accuracy():
    if not os.path.exists(GUESS_FILE):
        print("No predictions recorded yet.")
        return

    with open(GUESS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Corrupted guess file.")
            return

    total = 0
    correct = 0

    for record in data:
        if record.get("matched") is True:
            correct += 1
            total += 1
        elif record.get("matched") is False:
            total += 1

    if total == 0:
        print("No completed guesses to evaluate.")
    else:
        accuracy = round((correct / total) * 100, 2)
        print(f"Prediction accuracy: {accuracy}% ({correct} correct out of {total})")