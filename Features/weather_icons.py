#weather_icons.py
"""
Feature: Weather Icons
-Canvas-Based weather representations with color-coded conditions and simple animations
"""


import tkinter as tk
import math

def draw_weather_icons(canvas, condition):
    stop_all_animations(canvas)
    canvas.delete("all")
    condition = condition.lower()

    if "sun" in condition or "clear" in condition:
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

def stop_all_animations(canvas):
    for attr in ("sun_after_id", "rain_after_id", "snow_after_id", "storm_after_id"):
        after_id = getattr(canvas, attr, None)
        if after_id:
            try:
                canvas.after_cancel(after_id)
            except tk.TclError:
                pass
            setattr(canvas, attr, None)

# SUN
def animate_sun(canvas, bright=True):
    root = canvas.winfo_toplevel()
    if not canvas.winfo_exists() or not root.winfo_exists() or getattr(root, "is_closing", False):
        return
    
    canvas.delete("all")
    x, y = 100, 100
    radius = 30
    color = "#FFD700" if bright else "#FFA500"

    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="")

    for i in range(16):
        angle = math.radians(i * 22.5)
        x_end = x + 50 * math.cos(angle)
        y_end = y + 50 * math.sin(angle)
        canvas.create_line(x, y, x_end, y_end, fill=color, width=2)

    if canvas.winfo_exists() and not getattr(root, "is_closing", False):
        canvas.sun_after_id = canvas.after(500, lambda: animate_sun(canvas, not bright))

# CLOUDS
def animate_clouds(canvas):
    canvas.delete("all")
    draw_cloud(canvas)

# RAIN
def animate_rain(canvas):
    root = canvas.winfo_toplevel()
    if not canvas.winfo_exists() or not root.winfo_exists() or getattr(root, "is_closing", False):
        return

    canvas.delete("all")
    draw_cloud(canvas)

    if not hasattr(canvas, "rain_offset"):
        canvas.rain_offset = 0

    for i in range(10):
        x = 80 + i * 8
        y = (i * 15 + canvas.rain_offset) % 100 + 130
        canvas.create_line(x, y, x, y + 10, fill="blue")

    canvas.rain_offset = (canvas.rain_offset + 5) % 100
    if canvas.winfo_exists() and not getattr(root, "is_closing", False):
        canvas.rain_after_id = canvas.after(100, lambda: animate_rain(canvas))
# SNOW
def animate_snow(canvas):
    root = canvas.winfo_toplevel()
    if not canvas.winfo_exists() or not root.winfo_exists() or getattr(root, "is_closing", False):
        return

    canvas.delete("all")
    draw_cloud(canvas)

    if not hasattr(canvas, "snow_offset"):
        canvas.snow_offset = 0

    for i in range(10):
        x = 80 + i * 10
        y = (i * 12 + canvas.snow_offset) % 100 + 130
        canvas.create_text(x, y, text="❄️", font=("Arial", 12))

    canvas.snow_offset = (canvas.snow_offset + 3) % 100
    if canvas.winfo_exists() and not getattr(root, "is_closing", False):
        canvas.snow_after_id = canvas.after(150, lambda: animate_snow(canvas))

# STORM
def animate_storm(canvas):
    root = canvas.winfo_toplevel()
    if not canvas.winfo_exists() or not root.winfo_exists() or getattr(root, "is_closing", False):
        return

    canvas.delete("all")
    draw_cloud(canvas)

    if not hasattr(canvas, "storm_flash"):
        canvas.storm_flash = True

    if canvas.storm_flash:
        canvas.create_polygon(
            110, 130, 130, 170, 120, 170, 140, 210, 115, 175, 125, 175,
            fill="yellow", outline="black"
        )

    canvas.storm_flash = not canvas.storm_flash
    if canvas.winfo_exists() and not getattr(root, "is_closing", False):
        canvas.storm_after_id = canvas.after(400, lambda: animate_storm(canvas))

# CLOUD SHAPE
def draw_cloud(canvas):
    canvas.create_oval(60, 80, 120, 130, fill="gray", outline="")
    canvas.create_oval(90, 70, 150, 130, fill="lightgray", outline="")
    canvas.create_oval(120, 80, 180, 130, fill="gray", outline="")