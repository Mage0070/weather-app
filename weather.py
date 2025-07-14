import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ---------- CONFIG ----------
API_KEY = "d72ce2bf4ed0bc2652a0012c233467b9"            # <-- Put your OpenWeatherMap key here
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# -----------------------------

def fetch_weather():
    city = city_var.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        res = requests.get(BASE_URL, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Unable to connect:\n{e}")
        return

    if res.status_code != 200:
        messagebox.showerror("API Error", "City not found or API limit reached.")
        return

    data = res.json()
    # Extract & display data
    temperature = f"{data['main']['temp']} °C"
    condition   = data['weather'][0]['description'].title()
    humidity    = f"{data['main']['humidity']} %"
    wind_speed  = f"{data['wind']['speed']} m/s"

    temp_val.config(text=temperature)
    cond_val.config(text=condition)
    hum_val.config(text=humidity)
    wind_val.config(text=wind_speed)

# ------------- UI SETUP -------------
root = tk.Tk()
root.title("Weather Forecast")
root.geometry("350x250")
root.resizable(False, False)

# Form frame
frm_top = ttk.Frame(root, padding=10)
frm_top.pack(fill="x")

ttk.Label(frm_top, text="Enter city name:").pack(side="left")
city_var = tk.StringVar()
city_entry = ttk.Entry(frm_top, textvariable=city_var, width=20)
city_entry.pack(side="left", padx=5)
ttk.Button(frm_top, text="Get Weather", command=fetch_weather).pack(side="left")

# Results frame
frm_results = ttk.LabelFrame(root, text="Current Weather", padding=10)
frm_results.pack(fill="both", expand=True, padx=10, pady=10)

def add_row(label_text, row):
    ttk.Label(frm_results, text=label_text, width=12).grid(row=row, column=0, sticky="w")
    val = ttk.Label(frm_results, width=20)
    val.grid(row=row, column=1, sticky="w")
    return val

temp_val = add_row("Temperature:", 0)
cond_val = add_row("Condition:",   1)
hum_val  = add_row("Humidity:",    2)
wind_val = add_row("Wind Speed:",  3)

city_entry.focus()
root.mainloop()
