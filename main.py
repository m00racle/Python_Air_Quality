from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
root = Tk()
root.title("Air Quality App")
root.geometry("900x500+300+200")
root.resizable(False, False)


def getAirQuality():
    try:
        city = textfield.get()
        API = os.environ["OPEN_WEATHER_API_KEY"]

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        print(result)
        print(location.longitude, location.latitude)
        lat = location.latitude
        lon = location.longitude

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT AIR QUALITY")

        # weather
        api = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API}"

        json_data = requests.get(api).json()
        print(json_data["list"])
        condition = json_data["list"][0]["main"]["aqi"]
        no2 = json_data["list"][0]["components"]["no2"]
        pm10 = json_data["list"][0]["components"]["pm10"]
        o3 = json_data["list"][0]["components"]["o3"]
        pm25 = json_data["list"][0]["components"]["pm2_5"]

        if condition == 1:
            condition = "Good"
        elif condition == 2:
            condition = "Fair"
        elif condition == 3:
            condition = "Moderate"
        elif condition == 4:
            condition = "Poor"
        else:
            condition = "Very Poor"

        t.config(text=condition)
        c.config(text=("Air Quality: ", condition))

        w.config(text=round(no2, 2))
        h.config(text=round(pm10, 2))
        d.config(text=round(o3, 2))
        p.config(text=round(pm25, 2))

    except Exception as e:
        messagebox.showerror("Air Quality App", "Invalid Input")


def legends():
    window = Toplevel(root)
    window.title("Legend")
    window.geometry("300x100")
    window.resizable(False, False)
    window.iconphoto(False, Logo_image)

    Label(window, text="NO2 = Nitrogen dioxide (μg/m3)").place(x=0, y=0)
    Label(window, text="PM10 = Coarse particulate matter (μg/m3)").place(x=0, y=20)
    Label(window, text="O3 = Ozone (μg/m3)").place(x=0, y=40)
    Label(window, text="PM2.5 = Fine particles matter (μg/m3)").place(x=0, y=60)
    Label(window, text="F.Ramadhan, Pre-Selection Code Olympiad 2023", font=("arial", 5, "bold")).place(x=0, y=90)


# search box
Search_image = PhotoImage(file="search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getAirQuality)
myimage_icon.place(x=400, y=34)

Logo_image = PhotoImage(file="logo.png")
logo = Label(image=Logo_image)
logo.place(x=150, y=110)
root.iconphoto(False, Logo_image)

Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# label
label1 = Label(root, text="NO2 (μg/m3)", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=150, y=400)

label2 = Label(root, text="PM10 (μg/m3)", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=300, y=400)

label3 = Label(root, text="O3 (μg/m3)", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=450, y=400)

label4 = Label(root, text="PM25 (μg/m3)", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=600, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=260)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=150, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=300, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=600, y=430)

# legends
img = PhotoImage(file="legends.png")
Button(root, image=Search_icon, borderwidth=0, cursor="hand2", bg="#1CB7F1", width=40, height=40, command=legends, activebackground="#1CB7F1").place(x=765, y=420)

# watermark
Label(root, text="F.Ramadhan, Pre-Selection Code Olympiad 2023", font=("arial", 5, "bold")).place(x=0, y=0)

root.mainloop()
