"""  
This is testing sheet for Python API to Carbon calculator

"""

from tkinter import *
from dotenv import load_dotenv
import requests,os

#load dot env
load_dotenv()

# start building UI
window = Tk()
window.title("Electric to Carbon Equivalent")
window.geometry("900x500+300+200")
window.resizable(False, False)

def elec2Carb():
	country = country_var.get()
	if country == 'Select Country': country = "Indonesia"
	print(f'country: {country}')
	unit = unit_var.get() 
	if unit == 'Select Unit': unit = 'KWh'
	print(f'unt: {unit}')
	if valueField.get().isnumeric():
		val = float(valueField.get())
	else:
		val = 1
	print(f'val: {val}')

	url = "https://carbonsutra1.p.rapidapi.com/electricity_estimate"
	RAPID_KEY = os.environ['CARBON_SUTRA_API_KEY']
	RAPID_AUTH = os.environ['CARBON_SUTRA_AUTH']

	payload = f"country_name={country}&electricity_value={val}&electricity_unit={unit}"
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"Authorization": RAPID_AUTH,
		"X-RapidAPI-Key": RAPID_KEY,
		"X-RapidAPI-Host": "carbonsutra1.p.rapidapi.com"
	}

	response = requests.request("POST", url, data=payload, headers=headers).json()
	co2_kg = response["data"]["co2e_kg"]
	Label(window, text=f"CO2 equivalent: {co2_kg} kg", font=("Arial", 18, "bold")).place(x=200, y=250)

	print(f'response: {response}')
	print(f'CO2 equivalent: {co2_kg} kg')

# let's just make the damn UI 
# mock up only
# title text
title_text = Label(text="Electric to Carbon")
title_text.config(font=("Arial", 18, "bold"), justify="left", fg="blue")
title_text.place(x=20, y=50)

# input kwh
Label(window, text="insert value: ").place(x=20, y=100)
valueField = Entry(window, justify="left", width=10, font=("arial", 12), border=2, bg="blue", fg="white")
valueField.place(x=100, y=100)
# Label(window, text="Unit: ").place(y=100, x=200)

# unit selection
unit_option = ("KWh", "MWh")
unit_var = StringVar(window, "Select Unit")
unit_menu = OptionMenu(window, unit_var, *unit_option)
unit_menu.place(x=200, y=100)

# country selection
country_option = ["Indonesia", "India", "China"]
country_var = StringVar(window, "Select Country")
country_menu = OptionMenu(window, country_var, *country_option).place(x=100, y=150)

# button calc
calc_button = Button(window, text="Calculate", command=elec2Carb).place(x=200, y=200)

# loop
window.mainloop()