import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import messagebox
from tkinter import Toplevel, StringVar

ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "pass"

class StockManagementApp:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("856x645")
        self.app.resizable(0, 0)

        set_appearance_mode("dark")
        
        self.table_data = []
        
        # Create main content frame that will hold everything
        self.main_content_frame = CTkFrame(self.app)
        self.main_content_frame.pack(fill="both", expand=True)
        
        # Initialize sidebar as None
        self.sidebar = None
        self.content_frame = None
        
        self.login_view()
        self.app.mainloop()

    def clear_main_content(self):
        """Clear all widgets from the main content frame"""
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    def login_view(self):
        self.clear_main_content()
        
        # Create frame for login content
        self.frame = CTkFrame(master=self.main_content_frame, width=506, height=645, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", fill="both", expand=True)

        # Load and display side image
        side_img_data = Image.open(r"project\shopping-cart-with-bag.jpg")
        self.side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 645))
        self.image_label = CTkLabel(master=self.main_content_frame, text="", image=self.side_img)
        self.image_label.pack(expand=True, side="left")

        # Fonts
        h1_font = CTkFont(family="Helvetica", size=34, weight="bold")
        h1_font_italics = CTkFont(family="Helvetica", size=23, weight="bold", slant="italic")
        h2_font = CTkFont(family="Arial Bold", size=17, weight="bold")

        # Login form content
        CTkLabel(master=self.frame, text="Sign In", text_color="#D75B36", anchor="w", font=h1_font).pack(anchor="w", pady=(120, 0), padx=(25, 0))
        CTkLabel(master=self.frame, text="Stock Management Application", text_color="#636E79", anchor="w", font=h1_font_italics).pack(anchor="w", pady=(15, 0), padx=(25, 0))

        CTkLabel(master=self.frame, text="    Email:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(60, 0), padx=(25, 0))
        self.email_entry = CTkEntry(master=self.frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", padx=(47, 0))

        CTkLabel(master=self.frame, text="    Password:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(30, 0), padx=(25, 0))
        self.password_entry = CTkEntry(master=self.frame, width=400, show="*", fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.password_entry.pack(anchor="w", padx=(47, 0))

        CTkButton(master=self.frame, text="Login", fg_color="#D2502E", hover_color="#B0C3CD", font=("Helvetica", 18, "bold"), text_color="#ffffff", width=400, command=self.authenticate).pack(anchor="w", pady=(40, 0), padx=(47, 0))

    def homepage(self):
        self.clear_main_content()
        
        # Create a container frame for sidebar and content
        self.container_frame = CTkFrame(self.main_content_frame)
        self.container_frame.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content frame
        self.content_frame = CTkFrame(self.container_frame)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Show initial dashboard content
        self.show_dashboard()

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        self.sidebar = CTkFrame(self.container_frame, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar logo and buttons
        logo_label = CTkLabel(self.sidebar, text="Stock Management System", 
                            font=CTkFont(size=20, weight="bold"),
                            wraplength=180)
        logo_label.pack(pady=(20, 30))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Orders", self.show_orders),
            ("Returns", self.show_returns),
            ("Settings", self.show_settings),
            ("Account", self.show_account)
        ]
        
        for btn_text, command in buttons:
            CTkButton(self.sidebar, 
                     text=btn_text,
                     fg_color="transparent",
                     text_color=("gray10", "gray90"),
                     hover_color=("gray70", "gray30"),
                     height=40,
                     anchor="w",
                     command=command).pack(fill="x", padx=10, pady=5)

    def clear_content_frame(self):
        """Clear the content frame while preserving the sidebar"""
        if self.content_frame:
            for widget in self.content_frame.winfo_children():
                widget.destroy()

    def show_dashboard(self):
        self.clear_content_frame()
        CTkLabel(self.content_frame, text="Dashboard", 
                font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkLabel(self.content_frame, text="Welcome to the Stock Management Dashboard."
                ).pack(pady=10)

    def show_orders(self):
        self.clear_content_frame()
        self.create_orders_header()
        self.create_orders_table()

    def show_returns(self):
        self.clear_content_frame()
        CTkLabel(self.content_frame, text="Returns", 
                font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkLabel(self.content_frame, text="Manage returns for your stock."
                ).pack(pady=10)

    def show_settings(self):
        self.clear_content_frame()
        CTkLabel(self.content_frame, text="Settings", 
                font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkLabel(self.content_frame, text="Configure your stock management settings."
                ).pack(pady=10)

    def show_account(self):
        self.clear_content_frame()
        CTkLabel(self.content_frame, text="Account", 
                font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkButton(
            self.content_frame,
            text="Logout",
            font=("Helvetica", 18, "bold"),
            width=200,
            fg_color="#D2502E",
            hover_color="#B0C3CD",
            text_color="#ffffff",
            command=self.logout
        ).pack(pady=20)

    def logout(self):
        """Properly handle logout by clearing everything and showing login view"""
        self.clear_main_content()
        self.login_view()

    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.homepage()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

    def create_orders_header(self):
        """Create the orders header and stats section."""
        orders_label = CTkLabel(self.content_frame, text="Orders", 
                              font=CTkFont(size=24, weight="bold"))
        orders_label.pack(pady=(0, 20))

        # Create a frame for stats
        stats_frame = CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats = {"Orders\n123": 0, "Shipping\n91": 1, "Delivered\n23": 2}
        for text in stats.keys():
            stat_label = CTkLabel(stats_frame, text=text, 
                                font=CTkFont(size=16))
            stat_label.pack(side="left", expand=True, pady=5)

        CTkButton(self.content_frame, text="+ New Order", 
                 width=100, command=self.add_new_order).pack(pady=(0, 20))

    def create_orders_table(self):
        """Create the orders table with headers and data."""
        self.table_frame = CTkFrame(self.content_frame)
        self.table_frame.pack(fill="both", expand=True)

        # Create header frame
        header_frame = CTkFrame(self.table_frame)
        header_frame.pack(fill="x", padx=10, pady=5)

        columns = ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"]
        for col in columns:
            CTkLabel(header_frame, text=col, 
                    font=CTkFont(weight="bold")).pack(side="left", expand=True)

        # Create scrollable frame for data
        self.table_data_frame = CTkFrame(self.table_frame)
        self.table_data_frame.pack(fill="both", expand=True, padx=10)

        self.display_table_data()

    def display_table_data(self):
        """Display data in the orders table."""
        for widget in self.table_data_frame.winfo_children():
            widget.destroy()

        for row_data in self.table_data:
            row_frame = CTkFrame(self.table_data_frame)
            row_frame.pack(fill="x", pady=2)
            for item in row_data:
                CTkLabel(row_frame, text=str(item)).pack(side="left", expand=True)

if __name__ == "__main__":
    StockManagementApp()