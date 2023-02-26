import os
import requests
from requests.exceptions import HTTPError
import json
import tkinter
import customtkinter as ct

base_folder = os.path.dirname(__file__)
bg_path = os.path.join(base_folder, 'myqso_bg.png')
logo_path = os.path.join(base_folder, 'myqso_logo.png')

ct.set_appearance_mode("dark")  # Modes: system (default), light, dark
ct.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ct.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x400")
app.resizable(False, False)
app.title("MyQSO")


# Add background
bg = tkinter.PhotoImage(file = bg_path)
label1 = tkinter.Label(app, image = bg, text="")
label1.place(x = 0, y = 0)

# Add Logo
#logo = tkinter.PhotoImage(file = logo_path)
#label1 = ct.CTkLabel(app, image = logo, text="")
#label1.place(relx = .5, rely = .15, anchor=tkinter.CENTER)


# Functions

def get_data(sign):

    try:
        api_request = requests.get("http://api.hamdb.org/" + sign + "/json/myqso")

        # Parse JSON Return
        api = json.loads(api_request.content)
        f_name = api['hamdb']['callsign']['fname']
        l_name = api['hamdb']['callsign']['name']
        zip = api['hamdb']['callsign']['zip']
        return [f_name, l_name, zip]


    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')



def contacts_btn():
    print("Contacts button pressed")
    


def map_btn():
    print("Map button pressed")



def call_search(*args):
    callsign = call_entry.get()

    if len(callsign) <= 1 or callsign.isalnum() == False:
        callsign = "ERROR: MISSING OR BAD CALLSIGN"
        result_label = ct.CTkLabel(master=app, text=callsign, text_color="RED", font=("Arial", 16))
        result_label.place(relx=.5, rely=.75, anchor=tkinter.CENTER)
        result_label.after(2000, result_label.destroy)

    else:
        callsign = call_entry.get()
        data = get_data(callsign)
        first = data[0]
        last = data[1]
        name = str(first) + " " + str(last)
        zip = str(data[2])
        
        if zip == "NOT_FOUND":
            result_label = ct.CTkLabel(master=app, text=callsign + " Not Found in DB", text_color="white", font=("Arial", 14))
            result_label.place(relx=.5, rely=.7, anchor=tkinter.CENTER)
            result_label.after(3000, result_label.destroy)

        else:
            result_label = ct.CTkLabel(master=app, text=str(callsign) + "'s Name is: " + name, text_color="white", font=("Arial", 14))
            result_label.place(relx=.5, rely=.7, anchor=tkinter.CENTER)
            result_label.after(3000, result_label.destroy)

            result_label = ct.CTkLabel(master=app, text="The zip code is: " + zip, text_color="white", font=("Arial", 14))
            result_label.place(relx=.5, rely=.8, anchor=tkinter.CENTER)
            result_label.after(3000, result_label.destroy)
  
# Setup main window navigation buttons

#header = ct.CTkLabel(master=app, text="MyQSO", text_color="white", font=("Arial", 46))
#header.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

#button = ct.CTkButton(master=app, text="MyContacts", command=contacts_btn)
#button.place(relx=0.35, rely=0.8, anchor=tkinter.CENTER)

#button = ct.CTkButton(master=app, text="MyMap", command=map_btn)
#button.place(relx=0.65, rely=0.8, anchor=tkinter.CENTER)

button = ct.CTkButton(master=app, text="Exit", command=exit)
button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

# Call Entry and Search

call_entry = ct.CTkEntry(master=app, height=50, width=100, placeholder_text="CALL SIGN", fg_color="white", text_color="black")
call_entry.place(relx=.45, rely=.5, anchor = tkinter.CENTER)

call_button = ct.CTkButton(master=app, text="Search", command=call_search, width=50, height=50)
call_button.place(relx=0.6, rely=0.5, anchor=tkinter.CENTER)

call_entry.bind('<Return>', call_search)


app.mainloop()