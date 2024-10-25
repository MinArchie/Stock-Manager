import customtkinter
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from tkinter import messagebox


ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "12345"

def homepage():
    home = CTk()  # Create a new window for the homepage
    home.geometry("856x645")
    home.title("Homepage - Stock Management Application")

    set_appearance_mode("dark")

    CTkLabel(
        home, text="Welcome to the Stock Management Application", 
        font=("Helvetica", 28, "bold"), 
        text_color="#D75B36"
    ).pack(expand=True, pady=50)

    CTkButton(
        home, text="Logout", 
        font=("Helvetica", 18, "bold"), 
        width=200, fg_color="#D2502E", 
        hover_color="#B0C3CD", 
        text_color="#ffffff", 
        command=home.destroy  # Close the homepage window on logout
    ).pack(pady=20)

    home.mainloop()

def authenticate():
    email = email_entry.get()
    password = password_entry.get()
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        app.destroy()
        homepage()
    else:
        messagebox.showerror(
            "Login Failed", "Invalid email or password. Please try again."
        )

app = CTk()
app.geometry("856x645")
app.resizable(0,0)

set_appearance_mode("dark")

side_img_data = Image.open(r"project\shopping-cart-with-bag.jpg")
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350,645))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=506, height=645, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

h1_font = customtkinter.CTkFont(family="Helvetica", size=34, weight="bold")
h1_font_italics = customtkinter.CTkFont(family="Helvetica", size=23, weight="bold", slant="italic")
button_font = customtkinter.CTkFont(family="Helvetica", size=18, weight="bold")


CTkLabel(master=frame, text="Sign In", text_color="#D75B36", anchor="w", justify="left", font=h1_font).pack(anchor="w", pady=(120,0), padx=(25,0))
CTkLabel(master=frame, text="Stock Management Application", text_color="#636E79", anchor="w", justify="left", font=h1_font_italics).pack(anchor="w",pady=(15,0), padx=(25, 0))

CTkLabel(master=frame, text="    Email:", text_color="#9A4220", anchor="w", justify="left", font=("Arial Bold", 17), compound="left").pack(anchor="w", pady=(60, 0), padx=(25, 0))
email_entry =  CTkEntry(master=frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
email_entry.pack(anchor="w", padx=(47, 0))

CTkLabel(master=frame, text="    Password:", text_color="#9A4220", anchor="w", justify="left", font=("Arial Bold", 17), compound="left").pack(anchor="w", pady=(30, 0), padx=(25, 0))
password_entry = CTkEntry(master=frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
password_entry.pack(anchor="w", padx=(47, 0))

CTkButton(master=frame, text="Login", fg_color="#D2502E", hover_color="#B0C3CD", font=button_font, text_color="#ffffff", width=400, command=authenticate).pack(anchor="w", pady=(40,0), padx=(47,0))

app.mainloop()