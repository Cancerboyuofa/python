import tkinter
import customtkinter as ct

ct.set_appearance_mode("dark")  # Modes: system (default), light, dark
ct.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ct.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x400")
app.title("MyQSO")


# variables



# Functions

def contacts_btn():
    print("Contacts button pressed")
    
def map_btn():
    print("Map button pressed")

def get_data():
   call_entry.config(text= entry.get())


# Call Entry and Search

call_entry = ct.CTkEntry(master=app, height=50, width=100, placeholder_text="CALL SIGN", fg_color="white", text_color="black")
call_entry.place(relx=.4, rely=.5, anchor = tkinter.CENTER)

call_button = ct.CTkButton(master=app, text="Search", command=call_search(callsign), width=50, height=50)
call_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


#name_entry = ct.CTkEntry(master=app, height=10, width=150, placeholder_text="CALL SIGN", fg_color="white", text_color="black")
#call_entry.place(relx=.2, rely=.5, anchor = tkinter.CENTER)


# Use CTkButton instead of tkinter Button

button = ct.CTkButton(master=app, text="MyContacts", command=contacts_btn)
button.place(relx=0.35, rely=0.1, anchor=tkinter.CENTER)


button = ct.CTkButton(master=app, text="MyMap", command=map_btn)
button.place(relx=0.65, rely=0.1, anchor=tkinter.CENTER)

button = ct.CTkButton(master=app, text="Exit", command=exit)
button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)





app.mainloop()