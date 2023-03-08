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


# Setup variables and Date

unix = int(time.time())
global date
date = str(datetime.datetime.fromtimestamp(unix).strftime('%m-%d-%Y'))

on_home = True



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

c.execute("""CREATE TABLE IF NOT EXISTS contacts (
    
    contact_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    callsign TEXT,
    RQ TXEXT,
    SQ TEXT,
    con_date TEXT,
    con_count INTEGER

        )
    
    """)

#commit table creation

conn.commit()

# Contact Frames and logging functions - need to optimize calls

def log_setup(callsign, first, last, city, state, grid, date):

    callsign_query = c.execute("SELECT * FROM callsigns WHERE callsign = (?)", (callsign,))
    
    results = c.fetchall()
    table_id = results[0][0]
    state = results[0][7]
    name = results[0][2]

   
    contact_query = c.execute("SELECT MAX(con_count) FROM contacts WHERE callsign = (?)", (callsign,))

    start_count = c.fetchall()[0][0]

    if start_count == None:
        start_count = 0
        end_count = 1
        
    else: 
        end_count = start_count + 1
    
    conn.commit()


    home_right_frame = ct.CTkFrame(master=app, corner_radius=10)
    home_right_frame.grid(row=1, column=1, rowspan=4, columnspan=2, padx=40, pady=40, sticky="eW")
    home_right_frame.grid_columnconfigure((1), weight=1) 


    contact_label = ct.CTkLabel(master=home_right_frame, text="Log a QSO:", width=200, height=50, corner_radius=5, text_color="white", bg_color='transparent', font=("Arial", 14))
    contact_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  


    contact_call = ct.CTkEntry(master=home_right_frame, height=50, width=60, placeholder_text="Callsign", fg_color="white", text_color="black")
    contact_call.grid(row=2, column=0, columnspan=1, padx=20, pady=20, sticky="n")
    contact_call.insert(0, callsign)

    contact_name = ct.CTkEntry(master=home_right_frame, height=50, width=60, placeholder_text="Name", fg_color="white", text_color="black")
    contact_name.grid(row=2, column=1, columnspan=1, padx=20, pady=20, sticky="n")
    contact_name.insert(0, name)

    contact_state = ct.CTkEntry(master=home_right_frame, height=50, width=40, placeholder_text="State", fg_color="white", text_color="black")
    contact_state.grid(row=2, column=2, columnspan=1, padx=20, pady=20, sticky="n")
    contact_state.insert(0, state)

    contact_rq = ct.CTkEntry(master=home_right_frame, height=50, width=40, placeholder_text="59", fg_color="white", text_color="black")
    contact_rq.grid(row=3, column=0, columnspan=1, padx=20, pady=20, sticky="s")
    contact_rq.insert(0, "59")
        
    contact_sq = ct.CTkEntry(master=home_right_frame, height=50, width=40, placeholder_text="59", fg_color="white", text_color="black")
    contact_sq.grid(row=3, column=1, columnspan=1, padx=20, pady=20, sticky="s")
    contact_sq.insert(0, "59")

    contact_count = ct.CTkEntry(master=home_right_frame, height=50, width=40, placeholder_text="59", fg_color="white", text_color="black")
    contact_count.grid(row=3, column=2, columnspan=1, padx=20, pady=20, sticky="s")
    contact_count.insert(0, start_count)
    


    contact_button = ct.CTkButton(master=home_right_frame, text="Log QSO", width=40, height=30, command= lambda: store_contact(table_id, callsign, end_count))
    contact_button.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    
    

    def store_contact(table_id, callsign, end_count):

        rq = contact_rq.get()
        sq = contact_sq.get()
        
        c.execute("INSERT INTO contacts(user_id, callsign, RQ, SQ, con_date, con_count) VALUES(?,?,?,?,?,?)",
               (table_id, callsign.upper(), rq, sq, date, end_count)
               )
            
        conn.commit()
        

def match_found(callsign, first, last, city, state, grid, date):
    answer = tkinter.messagebox.askyesno(title=callsign + ", " + state + " Found", message="Log new contact with " + first + "?")

    if answer:
        
        global on_home
        on_home = False
        
        home_search_frame.destroy()
        log_setup(callsign, first, last, city, state, grid, date)        


def logging_function():

    if on_home == True:
        print("On home screen")
        return
    else:
        print("Not on home screen")
        

def contacts_function():
    return

def mapping_function():
    return

con_count = 1

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

        tkinter.messagebox.showerror(title="ERROR!", message="Missing or Bad Callsign!")
    else:
        
        db_search(callsign)
        

# Check DB for callsign locally

def db_search(callsign):
    
    c.execute("SELECT first_name, last_name, city, state, last_contact, map_grid FROM callsigns WHERE callsign = (?)", [callsign])
    matches = c.fetchall()

    if matches:
        found = True       
        first = matches[0][0]
        last = matches[0][1]
        city = matches[0][2]
        state = matches[0][3]
        grid = matches[0][5]

        conn.commit()

        match_found(callsign, first, last, city, state, grid, date)


    else:
        found = False
        result_label = ct.CTkLabel(master=home_search_frame, text="No prior contacts, searching online...", text_color="white", font=("Arial", 14))
        result_label.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        result_label.after(1000, result_label.destroy)
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
                (callsign.upper(), first.title(), last.title(), level, street_addr.title(), city.title(), state.upper(), int(zip), country.title(), float(lat), float(lon), grid.upper(), date)
                )
                        
        conn.commit()


        match_found(callsign, first, last, city, state, grid, date)


    else:
        tkinter.messagebox.showwarning(title="Not Found!", message="Sorry, Callsign Not found")
               

# Begin GUI

ct.set_appearance_mode("dark")  # Modes: system (default), light, dark
ct.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ct.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x400")
app.title("MyQSO")


# Configure App Grids

app.grid_rowconfigure((0, 1), weight=1)
app.grid_columnconfigure((1), weight=2)


left_frame = ct.CTkFrame(master=app, width=150)
left_frame.grid(row=0, column=0, rowspan=6, padx=0, pady=0, sticky="nsw")

left_frame = ct.CTkFrame(master=app, width=150)
left_frame.grid(row=0, column=0, rowspan=6, padx=0, pady=0, sticky="nsw")

home_search_frame = ct.CTkFrame(master=app, corner_radius=10)
home_search_frame.grid(row=1, column=1, rowspan=4, columnspan=2, padx=40, pady=40, sticky="eW")
home_search_frame.grid_columnconfigure((1), weight=1)

# Setup Text buttons

call_label = ct.CTkLabel(master=home_search_frame, text="Please Enter your callsign:", width=200, height=50, corner_radius=5, text_color="white", bg_color='transparent', font=("Arial", 14))
call_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


call_entry = ct.CTkEntry(master=home_search_frame, height=50, width=100, placeholder_text="CALLSIGN", fg_color="white", text_color="black")
call_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")


call_button = ct.CTkButton(master=home_search_frame, text="Search", command=callsign_valid, width=40, height=30)
call_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")


# Exit and Nav Buttons




log_button = ct.CTkButton(master=left_frame, text="Log Contact", command=logging_function)
log_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ns")

contact_button = ct.CTkButton(master=left_frame, text="Browse Contacts", command=contacts_function)
contact_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ns")

map_button = ct.CTkButton(master=left_frame, text="Map Contacts", command=mapping_function)
map_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ns")

exit_button = ct.CTkButton(master=left_frame, text="Exit", command=exit)
exit_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="sew")



# Bind callsign box to enter key
call_entry.bind('<Return>', callsign_valid)


# End tkinter app
app.mainloop()


# ***  OLD CODE FROM BEFORE DIALOGS  ***


    # NOT FOUND SEARCH SECTION

        #result_label = ct.CTkLabel(master=right_frame, text="Match Found! " + matches[0][0] + " from: " + matches[0][1], text_color="white", font=("Arial", 14))
        #result_label.grid(row=5, column=0, columnspan=2, sticky="sew", padx=5)
        # result_label.after(3000, result_label.destroy)

    # NOT FOUND SEARCH SECTION

        #result_label = ct.CTkLabel(master=right_frame, text=" Sorry, " + callsign + " not found online", text_color="white", font=("Arial", 14))
        #result_label.grid(row=4, column=0, columnspan=2, sticky="sew", padx=5)
        #result_label.after(2000, result_label.destroy)

    # ONLINE SEARCH SECTION

        #result_label = ct.CTkLabel(master=right_frame, text=str(callsign) + "'s Name is: " + name + "\n", text_color="white", font=("Arial", 14))
        #result_label.grid(row=4, column=0, columnspan=2, sticky="sew", padx=5)
        #result_label.after(3000, result_label.destroy)
        # state_msg = "Located in: "
        #result_label = ct.CTkLabel(master=app, text=state_msg + state, text_color="white", font=("Arial", 14))
        #result_label.place(relx=.5, rely=.8, anchor=tkinter.CENTER)
        #result_label.after(3000, result_label.destroy)

        #name = str(first) + " " + str(last)


    # BAD CALLSIGN ERROR SECTION

       # callsign = "ERROR: MISSING OR BAD CALLSIGN"
       # result_label = ct.CTkLabel(master=right_frame, text=callsign, text_color="RED", font=("Arial", 16))
       # result_label.grid(row=5, column=0, columnspan=2, sticky="sew", padx=5, pady=5)
       # result_label.after(1500, result_label.destroy)


    # Add app background/logo

      #base_folder = os.path.dirname(__file__)
      # bg_path = os.path.join(base_folder, 'myqso_bg.png')
      #logo_path = os.path.join(base_folder, 'myqso_logo.png')
      # bg = tkinter.PhotoImage(file = bg_path)

      #label1 = tkinter.Label(app, image = bg, text="")
      #label1.place(x = 0, y = 0)