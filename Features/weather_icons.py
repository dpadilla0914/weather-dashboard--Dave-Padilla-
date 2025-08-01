#weather_icons.py
"""
Feature: Weather Icons
-Canvas-Based weather representations with color-coded conditions and simple animations
"""

import tkinter as tk

def draw_weather_icons(canvas, condition):
    canvas.delete("all")
    condition = condition.lower()

    if "sun" in condition:
        animate_sun(canvas)
    elif "cloud" in condition:
        animate_clouds(canvas)
    elif "rain" in condition:
        animate_rain(canvas)
    elif "snow" in condition:
        animate_snow(canvas)
    elif "storm" in condition or "thunder" in condition:
        animate_storm(canvas)
    else:
        canvas.create_text(100, 100, text="☁️", font=("Arial", 40))

def animate_sun(canvas, bright = True):
    canvas.delete("all")
    x, y = 100, 100
    radius = 30
    color = "#FFD700" if bright else "#FFA500"

    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="")

    # Rays
    for i in range(8):
        angle = i * 45
        dx = 50 * (i % 2)
        canvas.create_line(
            x, y,
            x + dx * 0.6 * (1 if i % 2 == 0 else -1),
            y + dx * 0.6 * (1 if i < 4 else -1),
            fill=color, width=2
        )

    # Loop animation
    canvas.after(500, lambda: animate_sun(canvas, not bright))

def animate_clouds(canvas):
    canvas.delete("all")
    canvas.create_oval(60, 80, 120, 130, fill="gray", outline="")
    canvas.create_oval(90, 70, 150, 130, fill="lightgray", outline="")
    canvas.create_oval(120, 80, 180, 130, fill="gray", outline="")

def animate_rain(canvas):
    canvas.delete("all")
    draw_cloud(canvas)

    if not hasattr(animate_rain, 'drop'):
        animate_rain.drop = []

    for i in range(10):
        x = 80 + i * 8
        y = (i * 15 + animate_rain.offset) % 100 + 130
        drop = canvas.create_line(x, y, x, y + 10, fill="blue")
        animate_rain.drop.append(drop)

    animate_rain.offset = (animate_rain.offset + 5) % 100
    canvas.after(100, lambda: animate_rain(canvas))
animate_rain.offset = 0

def animate_snow(canvas):
    canvas.delete("all")
    draw_cloud(canvas)

    if not hasattr(animate_snow, "flakes"):
        animate_snow.flakes = []

    for i in range(10):
        x = 80 + i * 10
        y = (i * 12 + animate_snow.offset) % 100 + 130
        flake = canvas.create_text(x, y, text="❄️", font=("Arial", 12))
        animate_snow.flakes.append(flake)

    animate_snow.offset = (animate_snow.offset + 3) % 100
    canvas.after(150, lambda: animate_snow(canvas))
animate_snow.offset = 0

def animate_storm(canvas):
    canvas.delete("all")
    draw_cloud(canvas)

    if not hasattr(animate_storm, "flash"):
        animate_storm.flash = True

    if animate_storm.flash:
        canvas.create_polygon(
            110, 130, 130, 170, 120, 170, 140, 210, 115, 175, 125, 175,
            fill="yellow", outline="black"
        )

    animate_storm.flash = not animate_storm.flash
    canvas.after(400, lambda: animate_storm(canvas))

def draw_cloud(canvas):
    canvas.create_oval(60, 80, 120, 130, fill="gray", outline="")
    canvas.create_oval(90, 70, 150, 130, fill="lightgray", outline="")
    canvas.create_oval(120, 80, 180, 130, fill="gray", outline="")