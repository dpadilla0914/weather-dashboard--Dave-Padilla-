import tkinter as tk
from tkinter import messagebox

from Features import activity_suggester, city_comparison, favorite_cities, temperature_graph, theme_switcher
from Features import tomorrows_guess, trend_detection, weather_alerts, weather_history_tracker, weather_icons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WeatherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Weather Dashboard")
        self.geometry("900x700")

        self.preferences = theme_switcher.load_preferences()
        # Theme colors setup (example)
        self.theme_colors = {
            "background": "#FFFFFF",
            "text": "#000000",
            "primary": "#007ACC",
            "secondary": "#005A9E"
        }
        self.configure(bg=self.theme_colors["background"])

        self.sidebar = tk.Frame(self, width=200, bg=self.theme_colors["secondary"])
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self, bg=self.theme_colors["background"])
        self.main_area.pack(side="right", expand=True, fill="both")

        features = [
            ("Activity Suggester", self.show_activity_suggester),
            ("City Comparison", self.show_city_comparison),
            ("Favorite Cities", self.show_favorite_cities_ui),
            ("Temperature Graph", self.show_temp_graph),
            ("Theme Switcher", self.show_theme_switcher),
            ("Tomorrow's Guess", self.show_tomorrows_guess),
            ("Trend Detection", self.show_trend_detection),
            ("Weather Alerts", self.show_weather_alerts),
            ("Weather History Tracker", self.show_weather_history),
            ("Weather Icons", self.show_weather_icons_ui)
        ]

        for (text, command) in features:
            btn = tk.Button(self.sidebar, text=text, bg=self.theme_colors["primary"], fg=self.theme_colors["text"],
                            relief="flat", command=command)
            btn.pack(fill="x", pady=2, padx=5)

        self.show_activity_suggester()
        
    def show_favorite_cities_ui(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="Favorite Cities", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        favorites_list = favorite_cities.load_favorites()

        def add_city(event=None):  # Accept event for key binding
            new_city = entry.get().strip()
            if new_city:
                favorite_cities.add_favorite(new_city)
                self.show_favorite_cities_ui()  # Refresh

        entry = tk.Entry(self.main_area)
        entry.pack(pady=5)
        entry.bind("<Return>", add_city)  # Pressing Enter triggers add_city

        tk.Button(self.main_area, text="Add City", command=add_city,
            bg=self.theme_colors["primary"], fg="white").pack(pady=5)
        
        def remove_city(city):
            favorite_cities.remove_favorite(city)
            self.show_favorite_cities_ui()  # Refresh UI after removal

        for city in favorites_list:
            frame = tk.Frame(self.main_area, bg=self.theme_colors["background"])
            frame.pack(fill="x", pady=2)

            tk.Label(frame, text=city, bg=self.theme_colors["background"],
                    fg=self.theme_colors["text"]).pack(side="left", padx=(0, 10))

            tk.Button(frame, text="Remove", command=lambda c=city: remove_city(c),
                                bg="#e74c3c", fg="white").pack(side="left")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
            
    def show_temp_graph(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="Temperature Graph", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        input_frame = tk.Frame(self.main_area, bg=self.theme_colors["background"])
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter city name:", bg=self.theme_colors["background"],
                fg=self.theme_colors["text"]).pack(side="left")

        city_entry = tk.Entry(input_frame)
        city_entry.pack(side="left", padx=5)

        def plot_graph():
            city = city_entry.get().strip()
            print(f"City entered: '{city}'")
            if city:
                try:
                    fig = temperature_graph.get_forecast(city)
                    canvas = FigureCanvasTkAgg(fig, master=self.main_area)
                    canvas.draw()
                    canvas.get_tk_widget().pack()
                except Exception as e:
                    messagebox.showerror("Graph Error", f"Could not plot graph:\n{e}")
            else:
                messagebox.showwarning("Input Error", "Please enter a city name.")

        tk.Button(self.main_area, text="Show Graph", command=plot_graph,
                    bg=self.theme_colors["primary"], fg="white").pack(pady=5)

    def show_theme_switcher(self):
        self.clear_main_area()
        
        tk.Label(self.main_area, text="Theme Switcher", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)
    
        def switch_to_light():
            self.theme_colors = theme_switcher.get_theme_colors("light")
            self.apply_theme()
        
        def switch_to_dark():
            self.theme_colors = theme_switcher.get_theme_colors("dark")
            self.apply_theme()
        
            btn_light = tk.Button(self.main_area, text="Light Theme", command=switch_to_light,
                                bg=self.theme_colors["primary"], fg="white")
            btn_light.pack(pady=5)
        
            btn_dark = tk.Button(self.main_area, text="Dark Theme", command=switch_to_dark,
                                bg=self.theme_colors["primary"], fg="white")
            btn_dark.pack(pady=5)

    def show_tomorrows_guess(self):
        self.clear_main_area()
        tk.Label(self.main_area, text="Tomorrow's Guess", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

    def show_trend_detection(self):
        self.clear_main_area()
        tk.Label(self.main_area, text="Trend Detection (Not implemented yet)", 
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)
    
    def show_weather_alerts(self):
        self.clear_main_area()
        tk.Label(self.main_area, text="Weather Alerts (Coming Soon)", 
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)
    
    def show_weather_history(self):
        self.clear_main_area()
        tk.Label(self.main_area, text="Weather History Tracker (Coming Soon)", 
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)
    
    def apply_theme(self):
        # Update UI colors everywhere
        self.configure(bg=self.theme_colors["background"])
        self.sidebar.config(bg=self.theme_colors["secondary"])
        self.main_area.config(bg=self.theme_colors["background"])
    
    def show_activity_suggester(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="Activity Suggester", font=("Arial", 16),
                 bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        input_frame = tk.Frame(self.main_area, bg=self.theme_colors["background"])
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter weather condition:", bg=self.theme_colors["background"],
                 fg=self.theme_colors["text"]).pack(side="left")

        entry = tk.Entry(input_frame)
        entry.pack(side="left", padx=5)

        result_label = tk.Label(self.main_area, text="", bg=self.theme_colors["background"],
                                fg=self.theme_colors["text"], wraplength=400)
        result_label.pack(pady=10)

        def on_suggest():
            weather = entry.get()
            suggestion = activity.suggest_activity(weather)
            result_label.config(text=suggestion)

        tk.Button(self.main_area, text="Suggest Activity", command=on_suggest,
                  bg=self.theme_colors["primary"], fg="white").pack()

    def show_city_comparison(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="City Comparison", font=("Arial", 16),
                 bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        comparison = city_comparison.city_comparison()

        text_widget = tk.Text(self.main_area, height=10, width=60)
        text_widget.pack(pady=10)
        text_widget.insert("1.0", comparison)
        text_widget.config(state="disabled")

    def show_weather_icons_ui(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="Weather Icons Animation", font=("Arial", 16),
                 bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        condition_entry = tk.Entry(self.main_area)
        condition_entry.pack(pady=5)

        canvas = tk.Canvas(self.main_area, width=200, height=250, bg="white")
        canvas.pack(pady=10)

        def show_icon():
            cond = condition_entry.get().strip()
            if cond:
                weather_icons.draw_weather_icons(canvas, cond)
            else:
                messagebox.showwarning("Input error", "Enter a weather condition")

        tk.Button(self.main_area, text="Show Icon", command=show_icon,
                  bg=self.theme_colors["primary"], fg="white").pack(pady=5)


if __name__ == "__main__":
    app = WeatherDashboard()
    app.mainloop()