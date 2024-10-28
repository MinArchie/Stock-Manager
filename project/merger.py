import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Database credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Swathi1015"  # Replace with your MySQL root password
DB_NAME = "StockManagementDB"

ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "pass"

class StockManagementApp:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("856x645")
        self.app.resizable(0, 0)

        set_appearance_mode("dark")
        
        self.table_data = []
        self.db_connection = None  # Holds the database connection

        # Connect to the database
        self.connect_database()

        # Create main content frame
        self.main_content_frame = CTkFrame(self.app)
        self.main_content_frame.pack(fill="both", expand=True)
        
        # Initialize sidebar as None
        self.sidebar = None
        self.content_frame = None
        
        self.login_view()
        self.app.mainloop()

    def connect_database(self):
        """Connect to the SQL database."""
        try:
            self.db_connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.db_connection.is_connected():
                print("Connected to the database")
        except Error as e:
            messagebox.showerror("Database Connection Error", f"Error connecting to database: {e}")
            self.app.quit()

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
        logo_label = CTkLabel(self.sidebar, text="Stock Management System", font=CTkFont(size=20, weight="bold"), wraplength=180)
        logo_label.pack(pady=(20, 30))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Orders", self.show_orders),
            ("Returns", self.show_returns),
            ("Settings", self.show_settings),
            ("Account", self.show_account)
        ]
        
        for btn_text, command in buttons:
            CTkButton(self.sidebar, text=btn_text, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), height=40, anchor="w", command=command).pack(fill="x", padx=10, pady=5)

    def clear_content_frame(self):
        """Clear the content frame while preserving the sidebar"""
        if self.content_frame:
            for widget in self.content_frame.winfo_children():
                widget.destroy()

    def show_dashboard(self):
        self.clear_content_frame()
        CTkLabel(self.content_frame, text="Dashboard", font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkLabel(self.content_frame, text="Welcome to the Stock Management Dashboard.").pack(pady=10)

        # Fetch and display asset stats
        self.display_assets_overview()

    def display_assets_overview(self):
        """Retrieve and display asset information on the dashboard."""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT a_id, a_name, SUM(i_qty) AS total_qty
                FROM ASSETS LEFT JOIN INVENTORY ON ASSETS.a_id = INVENTORY.a_id
                GROUP BY a_id ORDER BY total_qty DESC
            """)
            results = cursor.fetchall()

            for asset_id, asset_name, total_qty in results:
                CTkLabel(self.content_frame, text=f"{asset_name} - {total_qty} units").pack(pady=5)
            cursor.close()
        except Error as e:
            messagebox.showerror("Error Fetching Data", f"Error retrieving asset information: {e}")

    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.homepage()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

    def logout(self):
        """Properly handle logout by clearing everything and showing login view"""
        self.clear_main_content()
        self.login_view()

if __name__ == "__main__":
    StockManagementApp()
