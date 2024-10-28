import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import messagebox
from tkinter import Toplevel, StringVar
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
                password='abc@2413'  # Replace with your actual password
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
            ("Manage Assets", self.show_assets),
            ("Manage Inventory", self.show_inventory),
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
        CTkLabel(self.content_frame, text="Manage Assets", font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkButton(self.content_frame, text="Add Asset", command=self.add_asset).pack(pady=(10, 0))
        self.display_assets()

    def display_assets(self):
        """Display the assets in a table format"""
        self.assets_table = CTkFrame(self.content_frame)
        self.assets_table.pack(fill="x", expand=True)

        # Table headers
        headers = ["Asset ID", "Name", "Type", "Category", "Quantity", "Market Price", "Actions"]
        for header in headers:
            header_label = CTkLabel(self.assets_table, text=header, 
                                   font=CTkFont(size=14, weight="bold"))
            header_label.grid(row=0, column=headers.index(header), padx=10, pady=5)

        # Fetch and display assets from the database
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM ASSETS")
            assets = cursor.fetchall()

            for asset in assets:
                for item in asset[:-1]:  # Exclude last_updated column from display
                    asset_label = CTkLabel(self.assets_table, text=str(item))
                    asset_label.grid(row=assets.index(asset) + 1, column=asset.index(item), padx=10, pady=5)

                # Add action buttons for updating and deleting
                update_button = CTkButton(self.assets_table, text="Update", command=lambda a_id=asset[0]: self.update_asset(a_id))
                update_button.grid(row=assets.index(asset) + 1, column=len(asset)-1, padx=10, pady=5)

                delete_button = CTkButton(self.assets_table, text="Delete", command=lambda a_id=asset[0]: self.delete_asset(a_id))
                delete_button.grid(row=assets.index(asset) + 1, column=len(asset), padx=10, pady=5)

        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching assets: {e}")

    def add_asset(self):
        """Functionality to add a new asset"""
        self.asset_window = Toplevel(self.app)
        self.asset_window.title("Add Asset")
        self.asset_window.geometry("400x400")

        CTkLabel(self.asset_window, text="Asset Name").pack(pady=5)
        self.asset_name_entry = CTkEntry(self.asset_window)
        self.asset_name_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Asset Type").pack(pady=5)
        self.asset_type_entry = CTkEntry(self.asset_window)
        self.asset_type_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Category").pack(pady=5)
        self.category_entry = CTkEntry(self.asset_window)
        self.category_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Quantity").pack(pady=5)
        self.quantity_entry = CTkEntry(self.asset_window)
        self.quantity_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Market Price").pack(pady=5)
        self.market_price_entry = CTkEntry(self.asset_window)
        self.market_price_entry.pack(pady=5)

        CTkButton(self.asset_window, text="Add Asset", command=self.save_asset).pack(pady=20)

    def save_asset(self):
        """Save the asset to the database"""
        asset_name = self.asset_name_entry.get()
        asset_type = self.asset_type_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        market_price = float(self.market_price_entry.get())

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                INSERT INTO ASSETS (a_name, a_type, category, a_qty, market_price) 
                VALUES (%s, %s, %s, %s, %s)
            """, (asset_name, asset_type, category, quantity, market_price))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Asset added successfully!")
            self.asset_window.destroy()
            self.display_assets()
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding asset: {e}")

    def update_asset(self, a_id):
        """Update asset details"""
        self.asset_window = Toplevel(self.app)
        self.asset_window.title("Update Asset")
        self.asset_window.geometry("400x400")

        # Fetch current asset details
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM ASSETS WHERE a_id = %s", (a_id,))
        asset = cursor.fetchone()

        CTkLabel(self.asset_window, text="Asset Name").pack(pady=5)
        self.asset_name_entry = CTkEntry(self.asset_window)
        self.asset_name_entry.insert(0, asset[1])
        self.asset_name_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Asset Type").pack(pady=5)
        self.asset_type_entry = CTkEntry(self.asset_window)
        self.asset_type_entry.insert(0, asset[2])
        self.asset_type_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Category").pack(pady=5)
        self.category_entry = CTkEntry(self.asset_window)
        self.category_entry.insert(0, asset[3])
        self.category_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Quantity").pack(pady=5)
        self.quantity_entry = CTkEntry(self.asset_window)
        self.quantity_entry.insert(0, asset[4])
        self.quantity_entry.pack(pady=5)

        CTkLabel(self.asset_window, text="Market Price").pack(pady=5)
        self.market_price_entry = CTkEntry(self.asset_window)
        self.market_price_entry.insert(0, asset[5])
        self.market_price_entry.pack(pady=5)

        CTkButton(self.asset_window, text="Update Asset", command=lambda: self.save_updated_asset(a_id)).pack(pady=20)

    def save_updated_asset(self, a_id):
        """Save the updated asset to the database"""
        asset_name = self.asset_name_entry.get()
        asset_type = self.asset_type_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        market_price = float(self.market_price_entry.get())

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                UPDATE ASSETS SET a_name = %s, a_type = %s, category = %s, a_qty = %s, market_price = %s 
                WHERE a_id = %s
            """, (asset_name, asset_type, category, quantity, market_price, a_id))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Asset updated successfully!")
            self.asset_window.destroy()
            self.display_assets()
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating asset: {e}")

    def delete_asset(self, a_id):
        """Delete an asset"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this asset?"):
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM ASSETS WHERE a_id = %s", (a_id,))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Asset deleted successfully!")
                self.display_assets()
            except Error as e:
                messagebox.showerror("Database Error", f"Error deleting asset: {e}")

    def show_inventory(self):
        self.clear_content_frame()
        CTkLabel(self.content_frame, text="Manage Inventory", font=CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        CTkButton(self.content_frame, text="Add Inventory", command=self.add_inventory).pack(pady=(10, 0))
        self.display_inventory()

    def display_inventory(self):
        """Display the inventory in a table format"""
        self.inventory_table = CTkFrame(self.content_frame)
        self.inventory_table.pack(fill="x", expand=True)

        # Table headers
        headers = ["Inventory ID", "Asset ID", "Quantity", "Status", "Actions"]
        for header in headers:
            header_label = CTkLabel(self.inventory_table, text=header, 
                                   font=CTkFont(size=14, weight="bold"))
            header_label.grid(row=0, column=headers.index(header), padx=10, pady=5)

        # Fetch and display inventory from the database
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM INVENTORY")
            inventory = cursor.fetchall()

            for item in inventory:
                for value in item[:-1]:  # Exclude movement_date column from display
                    inv_label = CTkLabel(self.inventory_table, text=str(value))
                    inv_label.grid(row=inventory.index(item) + 1, column=item.index(value), padx=10, pady=5)

                # Add action buttons for updating and deleting
                update_button = CTkButton(self.inventory_table, text="Update", command=lambda i_id=item[0]: self.update_inventory(i_id))
                update_button.grid(row=inventory.index(item) + 1, column=len(item)-1, padx=10, pady=5)

                delete_button = CTkButton(self.inventory_table, text="Delete", command=lambda i_id=item[0]: self.delete_inventory(i_id))
                delete_button.grid(row=inventory.index(item) + 1, column=len(item), padx=10, pady=5)

        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching inventory: {e}")

    def add_inventory(self):
        """Functionality to add new inventory"""
        self.inventory_window = Toplevel(self.app)
        self.inventory_window.title("Add Inventory")
        self.inventory_window.geometry("400x400")

        CTkLabel(self.inventory_window, text="Asset ID").pack(pady=5)
        self.asset_id_entry = CTkEntry(self.inventory_window)
        self.asset_id_entry.pack(pady=5)

        CTkLabel(self.inventory_window, text="Quantity").pack(pady=5)
        self.quantity_entry = CTkEntry(self.inventory_window)
        self.quantity_entry.pack(pady=5)

        CTkLabel(self.inventory_window, text="Status").pack(pady=5)
        self.status_entry = CTkEntry(self.inventory_window)
        self.status_entry.pack(pady=5)

        CTkButton(self.inventory_window, text="Add Inventory", command=self.save_inventory).pack(pady=20)

    def save_inventory(self):
        """Save the inventory item to the database"""
        asset_id = int(self.asset_id_entry.get())
        quantity = int(self.quantity_entry.get())
        status = self.status_entry.get()

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                INSERT INTO INVENTORY (a_id, i_qty, status) 
                VALUES (%s, %s, %s)
            """, (asset_id, quantity, status))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Inventory added successfully!")
            self.inventory_window.destroy()
            self.display_inventory()
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding inventory: {e}")

    def update_inventory(self, i_id):
        """Update inventory details"""
        self.inventory_window = Toplevel(self.app)
        self.inventory_window.title("Update Inventory")
        self.inventory_window.geometry("400x400")

        # Fetch current inventory details
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM INVENTORY WHERE i_id = %s", (i_id,))
        inventory_item = cursor.fetchone()

        CTkLabel(self.inventory_window, text="Asset ID").pack(pady=5)
        self.asset_id_entry = CTkEntry(self.inventory_window)
        self.asset_id_entry.insert(0, inventory_item[2])
        self.asset_id_entry.pack(pady=5)

        CTkLabel(self.inventory_window, text="Quantity").pack(pady=5)
        self.quantity_entry = CTkEntry(self.inventory_window)
        self.quantity_entry.insert(0, inventory_item[1])
        self.quantity_entry.pack(pady=5)

        CTkLabel(self.inventory_window, text="Status").pack(pady=5)
        self.status_entry = CTkEntry(self.inventory_window)
        self.status_entry.insert(0, inventory_item[4])
        self.status_entry.pack(pady=5)

        CTkButton(self.inventory_window, text="Update Inventory", command=lambda: self.save_updated_inventory(i_id)).pack(pady=20)

    def save_updated_inventory(self, i_id):
        """Save the updated inventory item to the database"""
        asset_id = int(self.asset_id_entry.get())
        quantity = int(self.quantity_entry.get())
        status = self.status_entry.get()

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                UPDATE INVENTORY SET a_id = %s, i_qty = %s, status = %s 
                WHERE i_id = %s
            """, (asset_id, quantity, status, i_id))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Inventory updated successfully!")
            self.inventory_window.destroy()
            self.display_inventory()
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating inventory: {e}")

    def delete_inventory(self, i_id):
        """Delete an inventory item"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this inventory item?"):
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM INVENTORY WHERE i_id = %s", (i_id,))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Inventory item deleted successfully!")
                self.display_inventory()
            except Error as e:
                messagebox.showerror("Database Error", f"Error deleting inventory item: {e}")

    def display_assets(self):
        """Display assets in a table format"""
        # Clear previous asset display
        self.asset_table.destroy()

        self.asset_table = CTkFrame(self.content_frame)
        self.asset_table.pack(fill="x", expand=True)

        # Table headers
        headers = ["Asset ID", "Asset Name", "Asset Type", "Category", "Quantity", "Market Price", "Actions"]
        for header in headers:
            header_label = CTkLabel(self.asset_table, text=header, font=CTkFont(size=14, weight="bold"))
            header_label.grid(row=0, column=headers.index(header), padx=10, pady=5)

        # Fetch and display assets from the database
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM ASSETS")
            assets = cursor.fetchall()

            for asset in assets:
                for value in asset[:-1]:  # Exclude last_updated column from display
                    asset_label = CTkLabel(self.asset_table, text=str(value))
                    asset_label.grid(row=assets.index(asset) + 1, column=asset.index(value), padx=10, pady=5)

                # Add action buttons for updating and deleting
                update_button = CTkButton(self.asset_table, text="Update", command=lambda a_id=asset[0]: self.update_asset(a_id))
                update_button.grid(row=assets.index(asset) + 1, column=len(asset)-1, padx=10, pady=5)

                delete_button = CTkButton(self.asset_table, text="Delete", command=lambda a_id=asset[0]: self.delete_asset(a_id))
                delete_button.grid(row=assets.index(asset) + 1, column=len(asset), padx=10, pady=5)

        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching assets: {e}")

    def clear_content_frame(self):
        """Clear the content frame for new displays"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.app.mainloop()

# Initialize and run the application
if __name__ == "__main__":
    app = StockManagementApp()
    app.run()
