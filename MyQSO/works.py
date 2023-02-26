import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x400")
app.title("MyQSO")

def contacts_btn():
    print("Contacts button pressed")
    
def map_btn():
    print("Map button pressed")
    

# Use CTkButton instead of tkinter Button

button = customtkinter.CTkButton(master=app, text="MyContacts", command=contacts_btn)
button.place(relx=0.35, rely=0.5, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="MyMap", command=map_btn)
button.place(relx=0.65, rely=0.5, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Exit", command=exit)
button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)





app.mainloop()