import customtkinter
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

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


CTkLabel(master=frame, text="Sign In", text_color="#D75B36", anchor="w", justify="left", font=h1_font).pack(anchor="w", pady=(25,0), padx=(25,0))
CTkLabel(master=frame, text="Stock Management Application", text_color="#636E79", anchor="w", justify="left", font=h1_font_italics).pack(anchor="w",pady=(15,0), padx=(25, 0))

CTkLabel(master=frame, text="    Email:", text_color="#9A4220", anchor="w", justify="left", font=("Arial Bold", 17), compound="left").pack(anchor="w", pady=(90, 0), padx=(25, 0))
CTkEntry(master=frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000").pack(anchor="w", padx=(47, 0))

CTkLabel(master=frame, text="    Password:", text_color="#9A4220", anchor="w", justify="left", font=("Arial Bold", 17), compound="left").pack(anchor="w", pady=(30, 0), padx=(25, 0))
CTkEntry(master=frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000").pack(anchor="w", padx=(47, 0))

CTkButton(master=frame, text="Login", fg_color="#D2502E", hover_color="#B0C3CD", font=button_font, text_color="#ffffff", width=400).pack(anchor="w", pady=(40,0), padx=(47,0))

app.mainloop()