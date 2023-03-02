import os
import time
import datetime
import sqlite3

import requests
from requests.exceptions import HTTPError
import json
import tkinter
import customtkinter as ct
import threading

# Get Current Date and Time

unix = int(time.time())
date = str(datetime.datetime.fromtimestamp(unix).strftime('%m-%d-%Y'))

# Begin GUI

ct.set_appearance_mode("dark")  # Modes: system (default), light, dark
ct.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ct.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x400")
app.resizable(False, False)
app.title("MyQSO")


# Add app background/logo

base_folder = os.path.dirname(__file__)
bg_path = os.path.join(base_folder, 'myqso_bg.png')
logo_path = os.path.join(base_folder, 'myqso_logo.png')
bg = tkinter.PhotoImage(file = bg_path)
label1 = tkinter.Label(app, image = bg, text="")
label1.place(x = 0, y = 0)


# Setup Database

conn = sqlite3.connect('MyQSO.db')

c = conn.cursor()

# Create DB Table

c.execute("""CREATE TABLE IF NOT EXISTS callsigns (
    
    id INTEGER PRIMARY KEY,
    callsign TEXT, 
    first_name TEXT,
    last_name TXEXT,
    class TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code INTEGER,
    country TEXT,
    map_lat BLOB,
    map_lon BLOB,
    map_grid TEXT,
    last_contact INTEGER
    )
    
    """)

#commit table creation

conn.commit()


# Callsign Functions

def get_data(sign):

    try:
        api_request = requests.get("http://api.hamdb.org/v1/" + sign + "/json/myqso")

    # Parse JSON Return

        api = json.loads(api_request.content)
        f_name = api['hamdb']['callsign']['fname']
        l_name = api['hamdb']['callsign']['name']
        level = api['hamdb']['callsign']['class']
        address = api['hamdb']['callsign']['addr1']
        city = api['hamdb']['callsign']['addr2']
        state = api['hamdb']['callsign']['state']
        zip = api['hamdb']['callsign']['zip']
        country = api['hamdb']['callsign']['country']
        lat = api['hamdb']['callsign']['lat']
        lon = api['hamdb']['callsign']['lon']
        grid = api['hamdb']['callsign']['grid']

        return [f_name, l_name, level, address, city, state, zip, country, lat, lon, grid]
    
    # HTTP Error Checking

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


# Check callsign for errors

def callsign_valid(*args):

    callsign = call_entry.get()

    if len(callsign) <= 1 or callsign.isalnum() == False:
        callsign = "ERROR: MISSING OR BAD CALLSIGN"
        result_label = ct.CTkLabel(master=app, text=callsign, text_color="RED", font=("Arial", 16))
        result_label.place(relx=.5, rely=.75, anchor=tkinter.CENTER)
        result_label.after(1500, result_label.destroy)
    else:
        call_entry.delete(0,8)
        db_search(callsign)
        


# Check DB for callsign locally

def db_search(callsign):
    
    c.execute("SELECT first_name, state, last_contact FROM callsigns WHERE callsign = (?)", [callsign])
    matches = c.fetchall()
    
    if matches:
        found = True
        result_label = ct.CTkLabel(master=app, text="Match Found! \n\n" + matches[0][0] + " from: " + matches[0][1] + "\n Your last QSO was on " + matches[0][2], text_color="white", font=("Arial", 14))
        result_label.place(relx=.5, rely=.65, anchor=tkinter.CENTER)
        result_label.after(3000, result_label.destroy)


    else:
        found = False
        result_label = ct.CTkLabel(master=app, text="No prior contacts, searching online...", text_color="white", font=("Arial", 14))
        result_label.place(relx=.5, rely=.7, anchor=tkinter.CENTER)
        result_label.after(2000, result_label.destroy)
        app.after(1000, lambda: threading.Thread(call_search(callsign, found)))
        


def call_search(callsign, found):
    
    data = get_data(callsign)
    first = data[0]
    last = data[1]
    level = data[2]
    street_addr = data[3]
    city = data[4]
    state = data[5]
    zip = data[6]
    country = data[7]
    lat = data[8]
    lon = data[9]
    grid = data[10]

        # Check if callsign in DB or not

    if not zip == "NOT_FOUND" and found == False:
        
        c.execute("INSERT INTO callsigns(callsign, first_name, last_name, class, address, city, state, zip_code, country, map_lat, map_lon, map_grid, last_contact) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (callsign.upper(), first.title(), last.title(), level, street_addr, city.title(), state.upper(), zip, country.title(), lat, lon, grid.upper(), date)
                )
                
        conn.commit()

        # Parse and format callsign data

        name = str(first) + " " + str(last)
        result_label = ct.CTkLabel(master=app, text=str(callsign) + "'s Name is: " + name + "\n", text_color="white", font=("Arial", 14))
        result_label.place(relx=.5, rely=.7, anchor=tkinter.CENTER)
        result_label.after(3000, result_label.destroy)
        state_msg = "Located in: "
        result_label = ct.CTkLabel(master=app, text=state_msg + state, text_color="white", font=("Arial", 14))
        result_label.place(relx=.5, rely=.8, anchor=tkinter.CENTER)
        result_label.after(3000, result_label.destroy)

    else:
        result_label = ct.CTkLabel(master=app, text=" Sorry, " + callsign + " not found online", text_color="white", font=("Arial", 14))
        result_label.place(relx=.5, rely=.7, anchor=tkinter.CENTER)
        result_label.after(2000, result_label.destroy)             

           

# Setup Text buttons
call_entry = ct.CTkEntry(master=app, height=50, width=100, placeholder_text="CALL SIGN", fg_color="white", text_color="black")
call_entry.place(relx=.45, rely=.5, anchor = tkinter.CENTER)

call_button = ct.CTkButton(master=app, text="Search", command=callsign_valid, width=50, height=50)
call_button.place(relx=0.6, rely=0.5, anchor=tkinter.CENTER)


# Exit and Nav Buttons
button = ct.CTkButton(master=app, text="Exit", command=exit)
button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)


# Bind callsign box to enter key
call_entry.bind('<Return>', callsign_valid)


# End tkinter app
app.mainloop()