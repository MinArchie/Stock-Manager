import customtkinter
from customtkinter import *
from PIL import Image
from tkinter import messagebox

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "12345"

class StockManagementApp:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("856x645")
        self.app.resizable(0, 0)

        set_appearance_mode("dark")

        
        self.frame = CTkFrame(master=self.app, width=506, height=645, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", fill="both", expand=True)

        self.login_view()
        self.app.mainloop()

    def login_view(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        side_img_data = Image.open(r"project\shopping-cart-with-bag.jpg")
        self.side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 645))

        self.image_label = CTkLabel(master=self.app, text="", image=self.side_img)
        self.image_label.pack(expand=True, side="left")

        #fonts
        h1_font = customtkinter.CTkFont(family="Helvetica", size=34, weight="bold")
        h1_font_italics = customtkinter.CTkFont(family="Helvetica", size=23, weight="bold", slant="italic")
        h2_font = customtkinter.CTkFont(family="Arial Bold", size=17, weight="bold")

        #title
        CTkLabel(master=self.frame, text="Sign In", text_color="#D75B36", anchor="w", font=h1_font).pack(anchor="w", pady=(120, 0), padx=(25, 0))
        CTkLabel(master=self.frame, text="Stock Management Application", text_color="#636E79", anchor="w", font=h1_font_italics).pack(anchor="w", pady=(15, 0), padx=(25, 0))

        #email 
        CTkLabel(master=self.frame, text="    Email:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(60, 0), padx=(25, 0))
        self.email_entry = CTkEntry(master=self.frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", padx=(47, 0))

        #password
        CTkLabel(master=self.frame, text="    Password:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(30, 0), padx=(25, 0))
        self.password_entry = CTkEntry(master=self.frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.password_entry.pack(anchor="w", padx=(47, 0))

        #login button
        CTkButton(master=self.frame, text="Login", fg_color="#D2502E", hover_color="#B0C3CD", font=("Helvetica", 18, "bold"), text_color="#ffffff", width=400, command=self.authenticate).pack(anchor="w", pady=(40, 0), padx=(47, 0))

    def homepage(self):
        if self.image_label:
            self.image_label.destroy()  
        for widget in self.frame.winfo_children():
            widget.destroy() 

        

        CTkLabel(self.frame, text="Welcome to the Stock Management Application", font=("Helvetica", 28, "bold"), text_color="#D75B36").pack(expand=True, pady=50)

        CTkButton(
            self.frame, text="Logout", 
            font=("Helvetica", 18, "bold"), 
            width=200, fg_color="#D2502E", 
            hover_color="#B0C3CD", 
            text_color="#ffffff", 
            command=self.login_view  # Call login_view instead of creating a new instance
        ).pack(pady=20)

    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.homepage()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid email or password. Please try again."
            )

if __name__ == "__main__":
    StockManagementApp()
