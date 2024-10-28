import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import messagebox, simpledialog
import mysql.connector
from mysql.connector import Error

ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "pass"

class StockManagementApp:
    def __init__(self):
        # Connect to MySQL database
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',
                database='StockManagementDB',
                user='root',
                password='rkp@2005'  # Replace with your actual password
            )

            if self.db_connection.is_connected():
                print("Successfully connected to the database")
                
        except Error as e:
            print(f"Error: {e}")
            return  # Exit if the database connection fails

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
            ("Orders", self.show_assets),
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

    def show_assets(self):
        self.clear_content_frame()
        self.create_assets_header()
        self.create_assets_table()

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

    def create_assets_header(self):
        """Create the assets header and stats section."""
        assets_label = CTkLabel(self.content_frame, text="Orders", 
                              font=CTkFont(size=24, weight="bold"))
        assets_label.pack(pady=(0, 20))

        # Create a frame for stats
        stats_frame = CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats = {"Orders\n123": 0, "Shipping\n91": 1, "Delivered\n23": 2}
        for text in stats.keys():
            stat_label = CTkLabel(stats_frame, text=text, 
                                font=CTkFont(size=16))
            stat_label.pack(side="left", expand=True, pady=5)

        CTkButton(self.content_frame, text="+ New Order", 
                 width=100, command=self.add_new_asset).pack(pady=(0, 20))

    def create_assets_table(self):
        """Create the assets table."""
        self.table_frame = CTkFrame(self.content_frame)
        self.table_frame.pack(fill="both", expand=True)

        # Create header
        headers = ["Asset ID", "Product Name", "Quantity", "Status"]
        for header in headers:
            label = CTkLabel(self.table_frame, text=header, 
                             font=CTkFont(size=14, weight="bold"))
            label.grid(row=0, column=headers.index(header), padx=10, pady=5)

        # Fetch assets from database and populate table
        self.refresh_assets()

    def refresh_assets(self):
        """Fetch assets from database and display in the assets table."""
        self.clear_assets_table()
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM Assets")
            self.table_data = cursor.fetchall()
            
            for row_index, row in enumerate(self.table_data, start=1):
                for col_index, value in enumerate(row):
                    label = CTkLabel(self.table_frame, text=value)
                    label.grid(row=row_index, column=col_index, padx=10, pady=5)
                    
        except Error as e:
            print(f"Error: {e}")

    def clear_assets_table(self):
        """Clear the assets table before refreshing."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def add_new_asset(self):
        """Open a dialog to add a new asset to the database."""
        # Create a new top-level window
        self.asset_dialog = CTkToplevel(self.app)
        self.asset_dialog.title("Add New Asset")
        self.asset_dialog.geometry("400x400")

        # Create labels and entry fields for each asset attribute
        CTkLabel(self.asset_dialog, text="Asset Name:").pack(pady=5)
        self.asset_name_entry = CTkEntry(self.asset_dialog)
        self.asset_name_entry.pack(pady=5)

        CTkLabel(self.asset_dialog, text="Quantity:").pack(pady=5)
        self.quantity_entry = CTkEntry(self.asset_dialog)
        self.quantity_entry.pack(pady=5)

        CTkLabel(self.asset_dialog, text="Status:").pack(pady=5)
        self.status_entry = CTkEntry(self.asset_dialog)
        self.status_entry.pack(pady=5)

        # Add more fields as required
        CTkLabel(self.asset_dialog, text="Description:").pack(pady=5)
        self.description_entry = CTkEntry(self.asset_dialog)
        self.description_entry.pack(pady=5)

        # Add button to submit the form
        CTkButton(self.asset_dialog, text="Add Asset", command=self.submit_asset).pack(pady=20)

    def submit_asset(self):
        """Submit the asset information to the database."""
        product_name = self.asset_name_entry.get()
        quantity = self.quantity_entry.get()
        status = self.status_entry.get()
        description = self.description_entry.get()  # Example additional field

        # Validate inputs
        if product_name and quantity.isdigit() and status:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    "INSERT INTO Assets (product_name, quantity, status, description) VALUES (%s, %s, %s, %s)",
                    (product_name, int(quantity), status, description)  # Assuming quantity is an integer
                )
                self.db_connection.commit()
                messagebox.showinfo("Success", "New asset added successfully!")
                self.asset_dialog.destroy()  # Close the dialog
                self.refresh_assets()  # Refresh the asset table to show new asset
            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Failed to add new asset.")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out correctly.")


if __name__ == "__main__":
    StockManagementApp()
