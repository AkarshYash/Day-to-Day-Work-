import tkinter as tk
from tkinter import messagebox
import requests
import pyttsx3
import geocoder
from PIL import Image, ImageTk

# Get your API key from: https://openweathermap.org/api
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_location():
    g = geocoder.ip('me')
    return g.city

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return None

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "wind": data["wind"]["speed"]
        }
        return weather_info
    except Exception as e:
        return None

def update_weather():
    city = city_entry.get()
    if city.strip() == "":
        city = get_location()
        if not city:
            messagebox.showerror("Error", "Could not detect location.")
            return
        
    weather = get_weather(city)
    if not weather:
        messagebox.showerror("Error", f"Cannot find weather for '{city}'.")
        return
    
    info = f"""
    ☁ City: {weather['city']}
    🌡 Temperature: {weather['temperature']} °C
    💧 Humidity: {weather['humidity']}%
    🌬 Wind: {weather['wind']} m/s
    🔎 Description: {weather['description']}
    """
    weather_text.config(text=info)
    speak(f"The weather in {weather['city']} is {weather['description']} with a temperature of {weather['temperature']} degrees Celsius.")

# GUI
root = tk.Tk()
root.title("☀️ Smart Weather App")
root.geometry("500x450")
root.resizable(False, False)

bg_img = Image.open("weather_bg.jpg")  # Make sure the image exists
bg_img = bg_img.resize((500, 450), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0)

frame = tk.Frame(root, bg='white', padx=10, pady=10)
frame.place(x=75, y=40, width=350, height=330)

title = tk.Label(frame, text="🌦 Weather Assistant", font=("Helvetica", 18, "bold"), fg="#333", bg="white")
title.pack(pady=10)

city_entry = tk.Entry(frame, width=25, font=("Helvetica", 14))
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name...")

get_btn = tk.Button(frame, text="Get Weather", command=update_weather, font=("Helvetica", 12), bg="#4CAF50", fg="white")
get_btn.pack(pady=5)

weather_text = tk.Label(frame, text="", bg="white", fg="#000", font=("Courier", 12), justify='left')
weather_text.pack(pady=15)

root.mainloop()
