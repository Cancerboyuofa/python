
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


