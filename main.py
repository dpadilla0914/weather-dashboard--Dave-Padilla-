import tkinter as tk
from tkinter import messagebox, colorchooser
from Features import activity_suggester, city_comparison, favorite_cities, temperature_graph, theme_switcher
from Features import weather_icons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import API_KEY
from PIL import Image, ImageTk
import os

class WeatherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.is_closing = False
        self.canvas = None
        self.api_key = API_KEY
        self.animated_canvases = []

        # Set window title and size
        self.title("Weather Dashboard")
        self.geometry("1500x1000")

        # Load user preferences (theme, units)
        self.preferences = theme_switcher.load_preferences()
        # Initialize theme colors based on saved preferences or default light theme
        self.theme_colors = theme_switcher.get_theme_colors(self.preferences.get("theme", "light"))
        
        if "card_bg" not in self.theme_colors:
            self.theme_colors["card_bg"] = self.theme_colors["background"]
        
        self.configure(bg=self.theme_colors["background"])

        # Sidebar on the left for navigation buttons
        self.sidebar = tk.Frame(self, width=200, bg=self.theme_colors["secondary"])
        self.sidebar.pack(side="left", fill="y")

        # Main content area on the right
        self.main_area = tk.Frame(self, bg=self.theme_colors["background"])
        self.main_area.pack(side="right", expand=True, fill="both")

        # List of features/buttons to show in the sidebar
        features = [
            ("Activity Suggester", self.show_activity_suggester),
            ("City Comparison", self.show_city_comparison),
            ("Favorite Cities", self.show_favorite_cities_ui),
            ("Temperature Graph", self.show_temp_graph),
            ("Theme Switcher", self.show_theme_switcher),
        ]

        # Create buttons in sidebar using theme colors
        for (text, command) in features:
            btn = tk.Button(self.sidebar, text=text, bg=self.theme_colors["primary"], fg=self.theme_colors["text"],
                            relief="flat", command=command)
            btn.pack(fill="x", pady=2, padx=5)

        # Show temperature graph by default on launch
        self.show_temp_graph()

        # Handle window closing event for cleanup
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Clean up animations and close the app."""
        self.is_closing = True

        # Stop all animated weather icons
        for canvas in self.animated_canvases:
            weather_icons.stop_all_animations(canvas)
        if self.canvas:
            weather_icons.stop_all_animations(self.canvas)

        self.animated_canvases.clear()
        self.destroy()

    def register_animated_canvas(self, canvas):
        """Add canvas to animated list for cleanup."""
        if canvas not in self.animated_canvases:
            self.animated_canvases.append(canvas)

    def unregister_animated_canvas(self, canvas):
        """Remove canvas from animated list."""
        if canvas in self.animated_canvases:
            self.animated_canvases.remove(canvas)

    def clear_main_area(self):
        """Clear the main content area and stop animations."""
        for widget in self.main_area.winfo_children():
            if isinstance(widget, tk.Canvas):
                weather_icons.stop_all_animations(widget)
                self.unregister_animated_canvas(widget)
            widget.destroy()

    def show_favorite_cities_ui(self):
        
        self.clear_main_area()

        tk.Label(self.main_area, text="Favorite Cities", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        favorites_list = favorite_cities.load_favorites()

        def add_city(event=None):
            new_city = entry.get().strip()
            if new_city:
                favorite_cities.add_favorite(new_city)
                self.show_favorite_cities_ui()  # Refresh UI

        entry = tk.Entry(self.main_area)
        entry.pack(pady=5)
        entry.bind("<Return>", add_city)  # Add city on Enter key

        tk.Button(self.main_area, text="Add City", command=add_city,
                  bg=self.theme_colors["primary"], fg="white").pack(pady=5)

        def remove_city(city):
            favorite_cities.remove_favorite(city)
            self.show_favorite_cities_ui()  # Refresh UI

        # Display favorite cities with remove buttons
        for city in favorites_list:
            frame = tk.Frame(self.main_area, bg=self.theme_colors["background"])
            frame.pack(fill="x", pady=2)

            tk.Label(frame, text=city, bg=self.theme_colors["background"],
                     fg=self.theme_colors["text"]).pack(side="left", padx=(0, 10))

            tk.Button(frame, text="Remove", command=lambda c=city: remove_city(c),
                      bg="#e74c3c", fg="white").pack(side="left")

    def show_temp_graph(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="Weather Forecast", font=("Arial", 16),
                 bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        input_frame = tk.Frame(self.main_area, bg=self.theme_colors["background"])
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter city name:", bg=self.theme_colors["background"],
                 fg=self.theme_colors["text"]).pack(anchor="w")

        city_entry = tk.Entry(input_frame)
        city_entry.pack(fill="x", pady=2)
        city_entry.focus_set()  #  Ensure typing works

        tk.Label(input_frame, text="Or select a favorite city:",
                 bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(anchor="w", pady=(10, 0))

        favorites_list = favorite_cities.load_favorites()
        selected_city = tk.StringVar()
        placeholder = "Select a city"
        selected_city.set(placeholder)

        def on_dropdown_select(value):
            city_entry.delete(0, tk.END)
            city_entry.insert(0, value)

        city_dropdown = tk.OptionMenu(input_frame, selected_city, placeholder, *favorites_list, command=on_dropdown_select)
        city_dropdown.config(bg=self.theme_colors["primary"], fg="white")
        city_dropdown.pack(fill="x", pady=2)

        forecast_container = tk.Frame(self.main_area, bg=self.theme_colors["background"])
        forecast_container.pack(pady=10)

        def plot_forecast():
            city = city_entry.get().strip()
            if not city or city == placeholder:
                messagebox.showwarning("Input Error", "Please enter or select a city name.")
                return

            try:
                forecast_data, fig = temperature_graph.get_forecast(city)

                for widget in forecast_container.winfo_children():
                    widget.destroy()

                forecast_frame = tk.Frame(forecast_container, bg=self.theme_colors["background"])
                forecast_frame.pack()

                for day in forecast_data:
                    temp = day["temp"]
                    condition = day["condition"]
                    date = day["date"]

                    card = tk.Frame(forecast_frame, bg=self.theme_colors["card_bg"], bd=1,
                                    relief="raised", padx=10, pady=5)
                    card.pack(side="left", padx=5)

                    tk.Label(card, text=date, font=("Arial", 10, "bold"),
                             bg=self.theme_colors["card_bg"], fg=self.theme_colors["text"]).pack()

                    icon_canvas = tk.Canvas(card, width=200, height=200,
                                            bg=self.theme_colors["card_bg"], highlightthickness=0)
                    icon_canvas.pack()
                    self.register_animated_canvas(icon_canvas)
                    weather_icons.draw_weather_icons(icon_canvas, condition)

                    tk.Label(card, text=f"{temp}°C", font=("Arial", 12),
                             bg=self.theme_colors["card_bg"], fg=self.theme_colors["text"]).pack()

                    tk.Label(card, text=condition.title(), font=("Arial", 10),
                             bg=self.theme_colors["card_bg"], fg=self.theme_colors["text"]).pack()

                graph_canvas = None

                def toggle_graph():
                    nonlocal graph_canvas
                    if graph_canvas is None:
                        graph_canvas = FigureCanvasTkAgg(fig, master=forecast_container)
                        graph_canvas.draw()
                        graph_canvas.get_tk_widget().pack(pady=10)
                        graph_button.config(text="Hide Temperature Graph")
                    else:
                        graph_canvas.get_tk_widget().pack_forget()
                        graph_canvas = None
                        graph_button.config(text="Show Temperature Graph")

                graph_button = tk.Button(forecast_container, text="Show Temperature Graph",
                                         command=toggle_graph,
                                         bg=self.theme_colors["primary"], fg="white")
                graph_button.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Forecast Error", f"Could not load forecast:\n{e}")

        city_entry.bind("<Return>", lambda e: plot_forecast())

        tk.Button(self.main_area, text="Get Forecast", command=plot_forecast,
                  bg=self.theme_colors["primary"], fg="white").pack(pady=5)

        city_entry.bind("<Return>", lambda e: plot_forecast())


    def show_city_comparison(self):
        
        self.clear_main_area()

        tk.Label(self.main_area, text="Compare Two Cities", font=("Arial", 16),
                 bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        tk.Label(self.main_area, text="City 1:", bg=self.theme_colors["background"],
                 fg=self.theme_colors["text"]).pack()
        city1_entry = tk.Entry(self.main_area)
        city1_entry.pack()

        tk.Label(self.main_area, text="City 2:", bg=self.theme_colors["background"],
                 fg=self.theme_colors["text"]).pack()
        city2_entry = tk.Entry(self.main_area)
        city2_entry.pack()

        compare_btn = tk.Button(self.main_area, text="Compare",
                                command=lambda: self.handle_compare(city1_entry.get(), city2_entry.get()),
                                bg=self.theme_colors["primary"], fg="white")
        compare_btn.pack(pady=10)

        self.compare_result = tk.Text(self.main_area, height=8, width=60,
                                      bg=self.theme_colors["background"], fg=self.theme_colors["text"])
        self.compare_result.pack()

    def handle_compare(self, city1, city2):
        # Fetch and display temperature comparison between two cities
        self.compare_result.delete(1.0, tk.END)

        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names.")
            return

        try:
            comparison = city_comparison.compare_cities(city1, city2)
            self.compare_result.insert(tk.END, comparison)
        except Exception as e:
            messagebox.showerror("Comparison Error", f"Could not compare cities:\n{e}")

    def show_activity_suggester(self):
        self.clear_main_area()

        tk.Label(self.main_area, text="Activity Suggester", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        tk.Label(self.main_area, text="Select weather condition:", bg=self.theme_colors["background"],
                fg=self.theme_colors["text"]).pack()

        weather_options = ["Sun", "Cloud", "Rain", "Snow", "Storm", "Thunder"]
        weather_var = tk.StringVar(value=weather_options[0])

        weather_dropdown = tk.OptionMenu(self.main_area, weather_var, *weather_options)
        weather_dropdown.config(bg=self.theme_colors["primary"], fg="white")
        weather_dropdown.pack()

        suggestion_label = tk.Label(self.main_area, text="", font=("Arial", 14, "italic"),
                                    bg=self.theme_colors["background"], fg=self.theme_colors["text"], wraplength=400)
        suggestion_label.pack(pady=10)

        def get_suggestion():
            weather = weather_var.get()
            try:
                suggestion = activity_suggester.suggest_activity(weather)
                suggestion_label.config(text=suggestion)
            except Exception as e:
                messagebox.showerror("Suggestion Error", f"Could not get suggestion:\n{e}")

        tk.Button(self.main_area, text="Suggest Activity", command=get_suggestion,
                bg=self.theme_colors["primary"], fg="white").pack(pady=5)

    def show_theme_switcher(self):
        # Refresh theme colors from saved preferences
        self.theme_colors = theme_switcher.get_theme_colors(self.preferences.get("theme", "light"))
        if self.preferences.get("use_custom_colors"):
            self.theme_colors["background"] = self.preferences.get("custom_background", "#FFFFFF")
            self.theme_colors["secondary"] = self.preferences.get("custom_sidebar", "#444444")
            self.theme_colors["primary"] = self.preferences.get("custom_primary", "#007BFF")
            self.theme_colors["text"] = self.preferences.get("custom_text", "#000000")
            self.theme_colors["card_bg"] = self.theme_colors["background"]
        if "card_bg" not in self.theme_colors:
            self.theme_colors["card_bg"] = self.theme_colors["background"]

        self.clear_main_area()

        tk.Label(self.main_area, text="Theme Switcher", font=("Arial", 16),
                bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(pady=10)

        # Theme-related variables
        self.theme_var = tk.StringVar(value=self.preferences.get("theme", "light"))
        self.use_custom = tk.BooleanVar(value=self.preferences.get("use_custom_colors", False))
        self.custom_background = tk.StringVar(value=self.preferences.get("custom_background", "#FFFFFF"))
        self.custom_button = tk.StringVar(value=self.preferences.get("custom_primary", "#007BFF"))
        self.custom_sidebar = tk.StringVar(value=self.preferences.get("custom_sidebar", "#444444"))

        # Theme selection radio buttons
        tk.Radiobutton(self.main_area, text="Light Theme", variable=self.theme_var, value="light",
                    bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(anchor="w")
        tk.Radiobutton(self.main_area, text="Dark Theme", variable=self.theme_var, value="dark",
                    bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(anchor="w")

        # Custom color toggle
        tk.Checkbutton(self.main_area, text="Use Custom Colors", variable=self.use_custom,
                    bg=self.theme_colors["background"], fg=self.theme_colors["text"]).pack(anchor="w", pady=5)

        # Frame for color pickers
        color_frame = tk.Frame(self.main_area, bg=self.theme_colors["background"])
        color_frame.pack(pady=10)

        # Helper function to make each color picker row
        def make_color_picker(row, label, var):
            tk.Label(color_frame, text=label, bg=self.theme_colors["background"],
                    fg=self.theme_colors["text"]).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            tk.Entry(color_frame, textvariable=var, width=20).grid(row=row, column=1, padx=5)

            def pick_color():
                color = colorchooser.askcolor(title=f"Choose {label}", initialcolor=var.get())
                if color[1]:
                    var.set(color[1])  # This triggers the trace_add callback
                    self.preferences[label.lower().replace(" ", "_").replace(":", "")] = color[1]

            tk.Button(color_frame, text="Pick", command=pick_color,
                bg=self.theme_colors["primary"], fg=self._get_contrast_color(self.theme_colors["primary"])).grid(row=row, column=2, padx=5)


        # Create each color picker
        make_color_picker(0, "Custom Background Color:", self.custom_background)
        make_color_picker(1, "Custom Sidebar Color:", self.custom_sidebar)
        make_color_picker(2, "Custom Button Color:", self.custom_button)

        # Save preferences and apply theme
        def on_theme_change(*args):
            new_prefs = {
                "theme": self.theme_var.get(),
                "use_custom_colors": self.use_custom.get(),
                "custom_background": self.custom_background.get(),
                "custom_primary": self.custom_button.get(),
                "custom_sidebar": self.custom_sidebar.get(),
            }
            theme_switcher.save_preferences(new_prefs)
            self.preferences = new_prefs
            self.apply_theme()
            self.configure(bg=self.theme_colors["background"])
            self.main_area.configure(bg=self.theme_colors["background"])
            self.winfo_toplevel().configure(bg=self.theme_colors["background"])
            self.sidebar.configure(bg=self.theme_colors["secondary"])
            self.show_theme_switcher()

        # Trace variables for real-time theme updates
        self.theme_var.trace_add('write', on_theme_change)
        self.use_custom.trace_add('write', on_theme_change)
        self.custom_background.trace_add('write', on_theme_change)
        self.custom_button.trace_add('write', on_theme_change)
        self.custom_sidebar.trace_add('write', on_theme_change)

        # Save button
        tk.Button(self.main_area, text="Save Preferences",
                command=lambda: (theme_switcher.save_preferences(self.preferences),
                                messagebox.showinfo("Preferences Saved", "Preferences saved successfully.")),
                bg=self.theme_colors["primary"], fg="white").pack(pady=10)



    def apply_theme(self):
        # Load updated preferences and theme colors
        if self.preferences.get("use_custom_colors"):
            bg_color = self.preferences.get("custom_background", "#FFFFFF")
            self.theme_colors["background"] = bg_color
            self.theme_colors["background"] = self.preferences.get("custom_background", "#FFFFFF")
            self.theme_colors["secondary"] = self.preferences.get("custom_sidebar", "#444444")
            self.theme_colors["primary"] = self.preferences.get("custom_primary", "#007BFF")
            self.theme_colors["text"] = self.preferences.get("custom_text", "#000000")
            self.theme_colors["card_bg"] = self.theme_colors["background"]
        else:
            self.theme_colors = theme_switcher.get_theme_colors(self.preferences.get("theme", "light"))
            if "card_bg" not in self.theme_colors:
                self.theme_colors["card_bg"] = self.theme_colors["background"]

        # Apply colors to top-level window and containers
        self.configure(bg=self.theme_colors["background"])
        self.sidebar.configure(bg=self.theme_colors["secondary"])
        self.main_area.configure(bg=self.theme_colors["background"])

        # Also force update sidebar buttons (these may not re-render correctly otherwise)
        for child in self.sidebar.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(bg=self.theme_colors["primary"], fg=self.theme_colors["text"])

        # Recursive update for all widgets in main_area
        def recursive_update(widget):
            for w in widget.winfo_children():
                recursive_update(w)

            try:
                if isinstance(widget, tk.Button):
                    widget.configure(bg=self.theme_colors["primary"], fg=self.theme_colors["text"])
                elif isinstance(widget, tk.OptionMenu):
                    widget.configure(bg=self.theme_colors["background"], fg=self.theme_colors["text"])
                    widget['menu'].config(bg=self.theme_colors["background"], fg=self.theme_colors["text"])
                elif isinstance(widget, (tk.Frame, tk.Label, tk.Entry, tk.Radiobutton, tk.Checkbutton, tk.Text)):
                    widget.configure(bg=self.theme_colors["background"], fg=self.theme_colors["text"])
            except tk.TclError:
                pass

        recursive_update(self.main_area)
        
    def _get_contrast_color(self, hex_color):
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return "black" if brightness > 128 else "white"
        except Exception:
            return "black"


if __name__ == "__main__":
    app = WeatherDashboard()
    app.mainloop()
