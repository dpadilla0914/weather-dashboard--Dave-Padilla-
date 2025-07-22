# import tkinter as tk
# from tkinter import ttk

# def create_activity_suggester_gui(root):
#     frame = ttk.LabelFrame(root, text="Activity Suggester", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     weather_label = ttk.Label(frame, text="Enter weather description:")
#     weather_label.pack(anchor="w")

#     weather_entry = ttk.Entry(frame, width=40)
#     weather_entry.pack(pady=5)

#     result_label = ttk.Label(frame, text="", wraplength=300)
#     result_label.pack(pady=5)

#     def on_suggest():
#         weather_input = weather_entry.get()
#         suggestion = suggest_activity(weather_input)
#         result_label.config(text=suggestion)

#     suggest_button = ttk.Button(frame, text="Suggest Activity", command=on_suggest)
#     suggest_button.pack(pady=5)

# # GUI Component: City Comparison
# def create_city_comparison_gui(root):
#     frame = ttk.LabelFrame(root, text="City Comparison", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     instruction_label = ttk.Label(frame, text="Enter city data (Format: City1:Temp1, City2:Temp2, ...):")
#     instruction_label.pack(anchor="w")

#     input_entry = ttk.Entry(frame, width=60)
#     input_entry.pack(pady=5)

#     output_text = tk.Text(frame, height=6, wrap="word", state="disabled")
#     output_text.pack(pady=5)

#     def parse_input(input_str):
#         try:
#             city_entries = input_str.split(',')
#             data = {}
#             for entry in city_entries:
#                 if ':' not in entry:
#                     raise ValueError("Missing ':' in entry.")
#                 city, temp = entry.split(':')
#                 data[city.strip()] = float(temp.strip())
#             return data
#         except Exception as e:
#             messagebox.showerror("Input Error", f"Invalid format: {e}")
#             return None

#     def on_compare():
#         input_str = input_entry.get()
#         if not input_str.strip():
#             data = None  # Use default
#         else:
#             data = parse_input(input_str)
#         if data is not None:
#             result = city_comparison(data)
#             output_text.config(state="normal")
#             output_text.delete("1.0", tk.END)
#             output_text.insert(tk.END, result)
#             output_text.config(state="disabled")

#     compare_button = ttk.Button(frame, text="Compare Cities", command=on_compare)
#     compare_button.pack(pady=5)

# # GUI Component: Favorite Cities
# def create_favorite_cities_gui(root):
#     frame = ttk.LabelFrame(root, text="Favorite Cities", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     entry = ttk.Entry(frame, width=30)
#     entry.pack(pady=5)

#     listbox = tk.Listbox(frame, height=5)
#     listbox.pack(pady=5, fill="x")

#     def refresh_listbox():
#         listbox.delete(0, tk.END)
#         for city in show_favorites():
#             listbox.insert(tk.END, city)

#     def on_add():
#         city = entry.get()
#         if city:
#             add_favorite(city)
#             entry.delete(0, tk.END)
#             refresh_listbox()

#     def on_remove():
#         selection = listbox.curselection()
#         if selection:
#             city = listbox.get(selection[0])
#             remove_favorite(city)
#             refresh_listbox()

#     btn_frame = ttk.Frame(frame)
#     btn_frame.pack(pady=5)

#     add_btn = ttk.Button(btn_frame, text="Add", command=on_add)
#     add_btn.grid(row=0, column=0, padx=5)

#     remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=on_remove)
#     remove_btn.grid(row=0, column=1, padx=5)

#     refresh_listbox()

# #GUI Component: Temperature graph
# def create_temperature_graph_gui(root):
#     frame = ttk.LabelFrame(root, text="Temperature Graph", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     entry_label = ttk.Label(frame, text="Enter city name:")
#     entry_label.pack(anchor="w")

#     city_entry = ttk.Entry(frame, width=30)
#     city_entry.pack(pady=5)

#     graph_frame = ttk.Frame(frame)
#     graph_frame.pack(pady=5, fill="both", expand=True)

#     def on_plot():
#         city = city_entry.get().strip()
#         if not city:
#             messagebox.showerror("Input Error", "Please enter a city name.")
#             return

#         forecast = get_forecast(city)
#         if not forecast:
#             messagebox.showerror("API Error", "City not found or data unavailable.")
#             return

#         dates = [day for day, _ in forecast]
#         temps = [temp for _, temp in forecast]

#         # Clear old graph
#         for widget in graph_frame.winfo_children():
#             widget.destroy()

#         fig, ax = plt.subplots(figsize=(6, 3))
#         ax.plot(dates, temps, marker='o', linestyle='-', color='blue')
#         ax.set_title(f"Temperature Forecast: {city}")
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Temp (°C)")
#         ax.grid(True)
#         fig.autofmt_xdate(rotation=45)

#         canvas = FigureCanvasTkAgg(fig, master=graph_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill="both", expand=True)

#     plot_button = ttk.Button(frame, text="Show Graph", command=on_plot)
#     plot_button.pack(pady=5)

# #GUI Component: Theme Switcher
# def create_theme_switcher_gui(root, apply_theme_callback):
#     frame = ttk.LabelFrame(root, text="Theme Settings", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     prefs = load_preferences()
#     current_theme = tk.StringVar(value=prefs.get("theme", "light"))

#     def on_theme_change():
#         prefs["theme"] = current_theme.get()
#         save_preferences(prefs)
#         apply_theme_callback(current_theme.get())  # Update GUI theme

#     ttk.Label(frame, text="Choose Theme:").pack(anchor="w", pady=(0, 5))

#     light_btn = ttk.Radiobutton(frame, text="Light", variable=current_theme, value="light", command=on_theme_change)
#     dark_btn = ttk.Radiobutton(frame, text="Dark", variable=current_theme, value="dark", command=on_theme_change)
#     light_btn.pack(anchor="w")
#     dark_btn.pack(anchor="w")

# def apply_theme(theme_name):
#     colors = get_theme_colors(theme_name)
#     root.configure(bg=colors["background"])

#     style = ttk.Style()
#     style.theme_use("default")

#     style.configure("TFrame", background=colors["background"])
#     style.configure("TLabel", background=colors["background"], foreground=colors["text"])
#     style.configure("TButton", background=colors["primary"], foreground=colors["text"])
#     style.configure("TRadiobutton", background=colors["background"], foreground=colors["text"])
#     style.configure("TEntry", fieldbackground=colors["background"], foreground=colors["text"])

# #GUI Component: Tomorrow's Guess
# def create_tomorrow_guess_gui(root):
#     frame = ttk.LabelFrame(root, text="Tomorrow's Weather Guess", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     ttk.Label(frame, text="Enter city:").pack(anchor="w")

#     city_entry = ttk.Entry(frame, width=30)
#     city_entry.pack(pady=5)

#     result_label = ttk.Label(frame, text="", wraplength=300)
#     result_label.pack(pady=5)

#     accuracy_label = ttk.Label(frame, text="", wraplength=300)
#     accuracy_label.pack(pady=5)

#     # Treeview for history
#     columns = ("city", "guess", "actual", "matched")
#     tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
#     for col in columns:
#         tree.heading(col, text=col.title())
#     tree.pack(pady=5, fill="x")

#     # Combobox to select actual weather
#     ttk.Label(frame, text="Update Actual Weather:").pack(anchor="w")
#     actual_var = tk.StringVar()
#     actual_combo = ttk.Combobox(frame, textvariable=actual_var, values=["sunny", "rainy", "cloudy", "snow", "storm", "unknown"], state="readonly")
#     actual_combo.pack(pady=2)

#     def load_history():
#         for i in tree.get_children():
#             tree.delete(i)
#         if os.path.exists(GUESS_FILE):
#             with open(GUESS_FILE, "r") as f:
#                 try:
#                     data = json.load(f)
#                 except json.JSONDecodeError:
#                     messagebox.showerror("Error", "Corrupted guess file.")
#                     return
#             for idx, rec in enumerate(data):
#                 matched = rec["matched"]
#                 matched_str = "Yes" if matched else ("No" if matched == False else "N/A")
#                 tree.insert("", "end", iid=idx, values=(rec["city"], rec["guess"], rec["actual"] or "N/A", matched_str))

#     def on_guess():
#         city = city_entry.get().strip()
#         if not city:
#             messagebox.showerror("Input Error", "Please enter a city.")
#             return

#         guess, confidence = predict_tomorrow(city)
#         result_label.config(text=f"Prediction for tomorrow in {city}:\n{guess.title()} (Confidence: {confidence})")
#         save_guess(city, guess)
#         load_history()

#     def on_check_accuracy():
#         message = calculate_accuracy()
#         accuracy_label.config(text=message)

#     def on_update_actual():
#         selected = tree.selection()
#         if not selected:
#             messagebox.showwarning("Selection Error", "Select a guess from the history to update.")
#             return

#         actual = actual_var.get()
#         if not actual:
#             messagebox.showwarning("Input Error", "Select an actual weather value.")
#             return

#         idx = int(selected[0])
#         success, msg = update_actual_result(idx, actual)
#         if success:
#             messagebox.showinfo("Success", msg)
#             load_history()
#         else:
#             messagebox.showerror("Error", msg)

#     btn_frame = ttk.Frame(frame)
#     btn_frame.pack(pady=5)

#     guess_btn = ttk.Button(btn_frame, text="Make Prediction", command=on_guess)
#     guess_btn.grid(row=0, column=0, padx=5)

#     accuracy_btn = ttk.Button(btn_frame, text="Check Accuracy", command=on_check_accuracy)
#     accuracy_btn.grid(row=0, column=1, padx=5)

#     update_btn = ttk.Button(frame, text="Update Actual Weather", command=on_update_actual)
#     update_btn.pack(pady=5)

#     load_history()

# #GUI Component: Trend Detection
# def create_trend_detection_gui(root):
#     frame = ttk.LabelFrame(root, text="Temperature Trend Detection", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     ttk.Label(frame, text="Enter city:").pack(anchor="w")

#     city_entry = ttk.Entry(frame, width=30)
#     city_entry.pack(pady=5)

#     trend_label = ttk.Label(frame, text="", justify="left", font=("Courier", 12))
#     trend_label.pack(pady=10)

#     def on_show_trend():
#         city = city_entry.get().strip()
#         if not city:
#             messagebox.showerror("Input Error", "Please enter a city.")
#             return

#         forecast = get_forecast(city)
#         if not forecast:
#             messagebox.showerror("Data Error", "Could not get forecast data for this city.")
#             return

#         temps = [temp for _, temp in forecast]
#         summary = display_trend_summary(temps)
#         trend_label.config(text=summary)

#     show_btn = ttk.Button(frame, text="Show Trend", command=on_show_trend)
#     show_btn.pack(pady=5)

# #GUI Component: Weather Alerts
# def create_weather_alerts_gui(root):
#     frame = ttk.LabelFrame(root, text="Weather Alerts", padding=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     ttk.Label(frame, text="Enter city:").pack(anchor="w")
#     city_entry = ttk.Entry(frame, width=30)
#     city_entry.pack(pady=5)

#     alert_label = ttk.Label(frame, text="", foreground="red", font=("Arial", 12, "bold"))
#     alert_label.pack(pady=10)

#     def on_check_alert():
#         city = city_entry.get().strip()
#         if not city:
#             messagebox.showerror("Input Error", "Please enter a city.")
#             return

#         forecast = get_forecast(city, days=1)
#         if not forecast:
#             messagebox.showerror("Data Error", "Could not retrieve temperature data for this city.")
#             return

#         temp_today = forecast[0][1]  # temperature in °C
#         prefs = load_preferences()
#         alert_msg = check_alerts(temp_today, prefs)

#         if alert_msg:
#             alert_label.config(text=alert_msg)
#         else:
#             alert_label.config(text="No alerts. Weather is normal.")

#     check_btn = ttk.Button(frame, text="Check Alerts", command=on_check_alert)
#     check_btn.pack(pady=5)

# #GUI Component: Weather History Tracker
# def create_weather_history_gui(root):
#     frame = ttk.LabelFrame(root, text="Weather History Tracker", padding=10)
#     frame.pack(padx=10, pady=10, fill="both", expand=True)

#     history_text = tk.Text(frame, height=10, width=50)
#     history_text.pack(pady=5)

#     avg_label = ttk.Label(frame, text="Weekly Average Temperature: N/A")
#     avg_label.pack(pady=5)

#     def show_history():
#         data = read_last_seven_days()
#         history_text.delete("1.0", tk.END)

#         if not data:
#             history_text.insert(tk.END, "No weather history data available.\n")
#             avg_label.config(text="Weekly Average Temperature: N/A")
#             return

#         # Display last seven days records
#         for entry in data:
#             line = f"{entry['date']} - {entry['city']}: {entry['temp']}°C, {entry['condition']}\n"
#             history_text.insert(tk.END, line)

#         avg = calculate_weekly_avg(data)
#         avg_label.config(text=f"Weekly Average Temperature: {avg}°C")

#     # Show history on load
#     show_history()


# # Main window
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Weather Dashboard")

#     prefs = load_preferences()
#     apply_theme(prefs.get("theme", "light"))

#     create_activity_suggester_gui(root)
#     create_city_comparison_gui(root)
#     create_favorite_cities_gui(root)
#     create_temperature_graph_gui(root)
#     create_theme_switcher_gui(root, apply_theme)
#     create_tomorrow_guess_gui(root)
#     create_trend_detection_gui(root)
#     create_weather_alerts_gui(root)
#     create_weather_history_gui(root)


#     root.mainloop()

import tkinter as tk
from tkinter import messagebox

from features import activity, city_comparison, favorites, temp_graph, theme_switcher
from features import tomorrows_guess, trend_detection, weather_alerts, weather_history, weather_icons
import preferences

class WeatherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Weather Dashboard")
        self.geometry("900x600")

        self.preferences = preferences.load_preferences()
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
            ("Favorite Cities", self.show_favorites_ui),
            ("Temperature Graph", self.show_temp_graph_ui),
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

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

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

    # ... similarly for other features, importing and using functions
    # For brevity, just one more example:

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