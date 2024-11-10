import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import messagebox, simpledialog
import mysql.connector
from mysql.connector import Error

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "secure_password1234"

db_connection = None
db_cursor = None

try:
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='******',  # Your actual root password here
        database='StockManagementDB'
    )
    if db_connection.is_connected():
        print("Successfully connected to the database")
        db_cursor = db_connection.cursor()
except Error as e:
    print(f"Error: {e}")
    messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")


class StockManagementApp:
    def __init__(self):
        global db_connection, db_cursor
        
        print("App starting...")
        self.app = CTk()
        print("App created...")
        self.app.geometry("1250x645")
        self.app.resizable(0, 0)

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        set_appearance_mode("dark")
        
        self.table_data = []
        
        self.main_content_frame = CTkFrame(self.app)
        self.main_content_frame.pack(fill="both", expand=True)
        
        self.sidebar = None
        self.content_frame = None
        
        self.login_view()
        self.app.mainloop()

    def on_closing(self):
        """Handle cleanup when app is closed"""
        global db_connection, db_cursor
        if db_cursor:
            db_cursor.close()
        if db_connection and db_connection.is_connected():
            db_connection.close()
            print("Database connection closed.")
        self.app.destroy()

    def clear_main_content(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    def login_view(self):
        self.clear_main_content()
        
        self.frame = CTkFrame(master=self.main_content_frame, width=506, height=645, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", fill="both", expand=True)

        side_img_data = Image.open(r"project\shopping-cart-with-bag.jpg")
        self.side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 645))
        self.image_label = CTkLabel(master=self.main_content_frame, text="", image=self.side_img)
        self.image_label.pack(expand=False, side="left")

        h1_font = CTkFont(family="Helvetica", size=34, weight="bold")
        h1_font_italics = CTkFont(family="Helvetica", size=23, weight="bold", slant="italic")
        h2_font = CTkFont(family="Arial Bold", size=17, weight="bold")

        CTkLabel(master=self.frame, text="Sign In", text_color="#D75B36", anchor="w", font=h1_font).pack(anchor="w", pady=(120, 0), padx=(65, 0))
        CTkLabel(master=self.frame, text="Stock Management Application", text_color="#636E79", anchor="w", font=h1_font_italics).pack(anchor="w", pady=(15, 0), padx=(65, 0))

        CTkLabel(master=self.frame, text="    Email:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(60, 0), padx=(65, 0))
        self.email_entry = CTkEntry(master=self.frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", padx=(87, 0))

        CTkLabel(master=self.frame, text="    Password:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(30, 0), padx=(65, 0))
        self.password_entry = CTkEntry(master=self.frame, width=400, show="*", fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.password_entry.pack(anchor="w", padx=(87, 0))

        CTkButton(master=self.frame, text="Login", fg_color="#D2502E", hover_color="#B0C3CD", font=("Helvetica", 18, "bold"), text_color="#ffffff", width=400, command=self.authenticate).pack(anchor="w", pady=(40, 0), padx=(87, 0))

    def homepage(self):
        self.clear_main_content()
        
        self.container_frame = CTkFrame(self.main_content_frame)
        self.container_frame.pack(fill="both", expand=True)
        
        self.create_sidebar()
        
        self.content_frame = CTkFrame(self.container_frame)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        self.show_dashboard()

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        self.sidebar = CTkFrame(self.container_frame, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_label = CTkLabel(self.sidebar, text="Stock Management System", 
                            font=CTkFont(size=20, weight="bold"),
                            wraplength=180)
        logo_label.pack(pady=(20, 30))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Assets", self.show_assets),
            ("Inventory", self.show_inventory),
            ("Asset Movement", self.show_asset_movement),
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

    def show_inventory(self):
        self.clear_content_frame()
        self.create_inventory_header()
        self.create_inventory_table()

    def show_asset_movement(self):
        self.clear_content_frame()
        self.show_asset_inventory_details()

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
        self.clear_main_content()
        self.login_view()

    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.homepage()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

    
    def show_asset_inventory_details(self):
        self.clear_content_frame()

        header = CTkLabel(self.content_frame, text="Asset Inventory Details", font=CTkFont(size=24, weight="bold"))
        header.pack(pady=(0, 20))

        table_frame = CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True)

        try:
            query = """
            SELECT ASSETS.a_id, ASSETS.a_name, ASSETS.a_qty, ASSETS.asset_status, INVENTORY.i_qty, INVENTORY.movement_date,
                INVENTORY.status, INVENTORY.acquired_price, INVENTORY.market_value, INVENTORY.profit_loss, INVENTORY.remarks
            FROM ASSETS
            LEFT JOIN INVENTORY ON ASSETS.a_id = INVENTORY.a_id
            ORDER BY ASSETS.a_id, INVENTORY.movement_date DESC;
            """
            db_cursor.execute(query)
            rows = db_cursor.fetchall()
            
            column_names = ["Asset ID", "Name",  "Quantity", "Status", "Inventory Qty", "Movement Date",
                            "I/O Status", "Acquired Price", "Market Value", "Profit/Loss", "Remarks"]
            
            for col_index, col_name in enumerate(column_names):
                header_label = CTkLabel(table_frame, text=col_name, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="nsew")
            
            for row_index, row in enumerate(rows, start=1):
                for col_index, value in enumerate(row):
                    if isinstance(value, float):
                        value = f"{value:.2f}"
                    elif isinstance(value, str) and value.isdigit():
                        value = str(int(value))
                    label = CTkLabel(table_frame, text=value)
                    label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="nsew")


        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error fetching asset-inventory details: {e}")



    def create_assets_header(self):
        assets_label = CTkLabel(self.content_frame, text="Assets", 
                              font=CTkFont(size=24, weight="bold"))
        assets_label.pack(pady=(0, 20))

        stats_frame = CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats = {"Assets\n123": 0, "Shipping\n91": 1, "Delivered\n23": 2}
        for text in stats.keys():
            stat_label = CTkLabel(stats_frame, text=text, 
                                font=CTkFont(size=16))
            stat_label.pack(side="left", expand=True, pady=5)

        CTkButton(self.content_frame, text="+ New Asset", 
                 width=100, command=self.add_new_asset).pack(pady=(0, 20))

    def create_assets_table(self):
        """Create the assets table."""
        self.table_frame = CTkFrame(self.content_frame)
        self.table_frame.pack(fill="both", expand=True)

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.refresh_assets()

    def refresh_assets(self):
        global db_cursor
        self.clear_assets_table()

        try:
            db_cursor.execute("SELECT * FROM Assets")
            column_names = [desc[0] for desc in db_cursor.description]
            print(column_names)
            for col_index, col_name in enumerate(column_names):
                header_label = CTkLabel(
                    self.table_frame, text=col_name, font=("Arial", 12, "bold")
                )
                header_label.grid(row=0, column=col_index, padx=10, pady=5, sticky="nsew")

            self.table_data = db_cursor.fetchall()

            for row_index, row in enumerate(self.table_data, start=1):
                for col_index, value in enumerate(row):
                    if isinstance(value, float):
                        value = f"{value:.2f}"
                    elif isinstance(value, str) and value.isdigit():
                        value = str(int(value))
                    label = CTkLabel(self.table_frame, text=value)
                    label.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="nsew")
                delete_button = CTkButton(
                    self.table_frame,
                    text="-",
                    command=lambda asset_id=row[0]: self.delete_asset(asset_id),
                    width=30,
                    fg_color="red",
                    text_color="white",
                    font=("Arial", 14, "bold")
                )
                delete_button.grid(row=row_index, column=len(column_names), padx=10, pady=5, sticky="nsew")
                edit_button = CTkButton(
                    self.table_frame,
                    text="✎",
                    command=lambda asset_id=row[0]: self.update_asset(asset_id),
                    width=20,
                    fg_color="green",
                    text_color="white",
                    font=("Arial", 20, "bold")
                )
                edit_button.grid(row=row_index, column=len(column_names)+1, padx=15, pady=5, sticky="nsew")

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error fetching assets: {e}")

    def clear_assets_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()


    def delete_asset(self, asset_id):
        global db_cursor
        try:
            db_cursor.execute("DELETE FROM Assets WHERE a_id = %s", (asset_id,))
            db_connection.commit()
            messagebox.showinfo("Success", "Asset deleted successfully.")
            self.refresh_assets()
        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error deleting asset: {e}")


    def update_asset(self, asset_id):
        global db_cursor
        try:
            db_cursor.execute("SELECT * FROM Assets WHERE a_id = %s", (asset_id,))
            asset_data = db_cursor.fetchone()
            
            if asset_data:
                self.asset_dialog = CTkToplevel(self.app)
                self.asset_dialog.title("Update Asset")
                self.asset_dialog.geometry("400x450")

                self.asset_dialog.grab_set()

                left_frame = CTkFrame(self.asset_dialog)
                left_frame.pack(side="left", padx=20, pady=20)

                right_frame = CTkFrame(self.asset_dialog)
                right_frame.pack(side="right", padx=20, pady=20)

                CTkLabel(left_frame, text="Asset Name:").pack(pady=5)
                self.asset_name_entry = CTkEntry(left_frame)
                self.asset_name_entry.insert(0, asset_data[1])
                self.asset_name_entry.pack(pady=5)

                CTkLabel(right_frame, text="Asset Type:").pack(pady=5)
                self.asset_type_entry = CTkEntry(right_frame)
                self.asset_type_entry.insert(0, asset_data[2])
                self.asset_type_entry.pack(pady=5)

                CTkLabel(left_frame, text="Category:").pack(pady=5)
                self.category_entry = CTkEntry(left_frame)
                self.category_entry.insert(0, asset_data[3])
                self.category_entry.pack(pady=5)

                CTkLabel(right_frame, text="Quantity:").pack(pady=5)
                self.quantity_entry = CTkEntry(right_frame)
                self.quantity_entry.insert(0, str(asset_data[4]))
                self.quantity_entry.pack(pady=5)

                CTkLabel(left_frame, text="Market Price:").pack(pady=5)
                self.market_price_entry = CTkEntry(left_frame)
                self.market_price_entry.insert(0, str(asset_data[5]))
                self.market_price_entry.pack(pady=5)

                CTkLabel(right_frame, text="Purchase Cost:").pack(pady=5)
                self.purchase_cost_entry = CTkEntry(right_frame)
                if asset_data[6]:
                    self.purchase_cost_entry.insert(0, str(asset_data[6]))
                self.purchase_cost_entry.pack(pady=5)

                CTkLabel(left_frame, text="Status:").pack(pady=5)
                self.status_entry = CTkEntry(left_frame)
                self.status_entry.insert(0, asset_data[7])
                self.status_entry.pack(pady=5)

                CTkLabel(right_frame, text="Description:").pack(pady=5)
                self.description_entry = CTkEntry(right_frame)
                if asset_data[9]:
                    self.description_entry.insert(0, asset_data[9])
                self.description_entry.pack(pady=5)

                CTkButton(
                    left_frame, 
                    text="Update Asset", 
                    command=lambda: self.submit_asset_update(asset_id)
                ).pack(pady=20)

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error fetching asset data: {e}")

    def submit_asset_update(self, asset_id):
        """Submit the updated asset information to the database."""
        global db_connection, db_cursor
        
        asset_name = self.asset_name_entry.get()
        asset_type = self.asset_type_entry.get()
        category = self.category_entry.get()
        qty = self.quantity_entry.get()
        market_price = self.market_price_entry.get()
        purchase_cost = self.purchase_cost_entry.get()
        status = self.status_entry.get()
        description = self.description_entry.get()

        if asset_name and status and asset_type in ['Tangible', 'Intangible'] and category in ['Buildings', 'Machinery', 'Cash', 'Inventory', 'Equipment', 'Vehicles', 'Furniture', 'Valuable Antiques', 'Copyrights', 'Brand Recognition', 'Trademarks', 'Patents', 'Intellectual Property', 'Goodwill', 'Franchises', 'Cash Equivalents']:
            try:
                qty = int(qty)
                market_price = float(market_price)
                purchase_cost = float(purchase_cost) if purchase_cost else None

                db_cursor.execute("""
                    UPDATE Assets 
                    SET a_name = %s, 
                        a_type = %s,
                        category = %s,
                        a_qty = %s,
                        market_price = %s,
                        a_purchasecost = %s,
                        asset_status = %s,
                        a_description = %s
                    WHERE a_id = %s
                """, (asset_name, asset_type, category, qty, market_price, 
                    purchase_cost, status, description, asset_id))
                
                db_connection.commit()
                messagebox.showinfo("Success", "Asset updated successfully!")
                self.asset_dialog.destroy()
                self.refresh_assets()
            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Failed to update asset.")
        else:
            messagebox.showwarning("Input Error", "Could Not Find Asset Information")


    def add_new_asset(self):
        self.asset_dialog = CTkToplevel(self.app)
        self.asset_dialog.title("Add New Asset")
        self.asset_dialog.geometry("400x450")

        self.asset_dialog.grab_set()

        left_frame = CTkFrame(self.asset_dialog)
        left_frame.pack(side="left", padx=20, pady=20)

        right_frame = CTkFrame(self.asset_dialog)
        right_frame.pack(side="right", padx=20, pady=20)

        CTkLabel(left_frame, text="Asset Name:").pack(pady=5)
        self.asset_name_entry = CTkEntry(left_frame)
        self.asset_name_entry.pack(pady=5)

        CTkLabel(right_frame, text="Asset Type:").pack(pady=5)
        self.asset_type_entry = CTkEntry(right_frame)
        self.asset_type_entry.pack(pady=5)

        CTkLabel(left_frame, text="Category:").pack(pady=5)
        self.category_entry = CTkEntry(left_frame)
        self.category_entry.pack(pady=5)

        CTkLabel(right_frame, text="Quantity:").pack(pady=5)
        self.quantity_entry = CTkEntry(right_frame)
        self.quantity_entry.pack(pady=5)

        CTkLabel(left_frame, text="Market Price:").pack(pady=5)
        self.market_price_entry = CTkEntry(left_frame)
        self.market_price_entry.pack(pady=5)

        CTkLabel(right_frame, text="Purchase Cost:").pack(pady=5)
        self.purchase_cost_entry = CTkEntry(right_frame)
        self.purchase_cost_entry.pack(pady=5)

        CTkLabel(left_frame, text="Status:").pack(pady=5)
        self.status_entry = CTkEntry(left_frame)
        self.status_entry.pack(pady=5)

        CTkLabel(right_frame, text="Description:").pack(pady=5)
        self.description_entry = CTkEntry(right_frame)
        self.description_entry.pack(pady=5)

        CTkButton(left_frame, text="Add Asset", command=self.submit_asset).pack(pady=20)

    def submit_asset(self):
        """Submit the asset information to the database."""
        global db_connection, db_cursor
        
        asset_name = self.asset_name_entry.get()
        asset_type = self.asset_type_entry.get()
        category = self.category_entry.get()
        qty = self.quantity_entry.get()
        market_price = self.market_price_entry.get()
        purchase_cost = self.purchase_cost_entry.get()
        status = self.status_entry.get()
        description = self.description_entry.get()

        if asset_name and status and asset_type in ['Tangible', 'Intangible'] and category in ['Buildings', 'Machinery', 'Cash', 'Inventory', 'Equipment', 'Vehicles', 'Furniture', 'Valuable Antiques', 'Copyrights', 'Brand Recognition', 'Trademarks', 'Patents', 'Intellectual Property', 'Goodwill', 'Franchises', 'Cash Equivalents']:
            try:
                qty = int(qty)
                market_price = float(market_price)
                purchase_cost = float(purchase_cost) if purchase_cost else None  # Allow NULL for purchase cost
            
                db_cursor.execute(
                    "INSERT INTO ASSETS (a_name, a_type ,category ,a_qty, market_price ,a_purchasecost ,asset_status, a_description )VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (asset_name, asset_type, category, qty, market_price, purchase_cost, status, description)
                )
                db_connection.commit()
                messagebox.showinfo("Success", "New asset added successfully!")
                self.asset_dialog.destroy()
                self.refresh_assets()
            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Failed to add new asset.")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out correctly.")


    def create_inventory_header(self):
        inventory_label = CTkLabel(self.content_frame, text="Inventory", 
                              font=CTkFont(size=24, weight="bold"))
        inventory_label.pack(pady=(0, 20))

        stats_frame = CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", pady=(0, 20))
        # come back and fix
        stats = {"Assets\n123": 0, "Shipping\n91": 1, "Delivered\n23": 2}
        for text in stats.keys():
            stat_label = CTkLabel(stats_frame, text=text, 
                                font=CTkFont(size=16))
            stat_label.pack(side="left", expand=True, pady=5)

        CTkButton(self.content_frame, text="+ Add Inventory", 
                 width=100, command=self.add_new_inventory).pack(pady=(0, 20))

    def create_inventory_table(self):
        self.table_frame = CTkFrame(self.content_frame)
        self.table_frame.pack(fill="both", expand=True)

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.refresh_inventory()

    def refresh_inventory(self):
        global db_cursor
        self.clear_inventory_table()

        try:
            db_cursor.execute("SELECT * FROM Inventory")
            column_names = [desc[0] for desc in db_cursor.description]
            print(column_names)
            for col_index, col_name in enumerate(column_names):
                header_label = CTkLabel(
                    self.table_frame, text=col_name, font=("Arial", 12, "bold")
                )
                header_label.grid(row=0, column=col_index, padx=10, pady=5, sticky="nsew")

            self.table_data = db_cursor.fetchall()

            for row_index, row in enumerate(self.table_data, start=1):
                for col_index, value in enumerate(row):
                    if isinstance(value, float):
                        value = f"{value:.2f}"
                    elif isinstance(value, str) and value.isdigit():
                        value = str(int(value))
                    label = CTkLabel(self.table_frame, text=value)
                    label.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="nsew")
                delete_button = CTkButton(
                    self.table_frame,
                    text="-",
                    command=lambda inventory_id=row[0]: self.delete_inventory(inventory_id),
                    width=30,
                    fg_color="red",
                    text_color="white",
                    font=("Arial", 14, "bold")
                )
                delete_button.grid(row=row_index, column=len(column_names), padx=10, pady=5, sticky="nsew")
                edit_button = CTkButton(
                    self.table_frame,
                    text="✎",
                    command=lambda inventory_id=row[0]: self.update_inventory(inventory_id),
                    width=20,
                    fg_color="green",
                    text_color="white",
                    font=("Arial", 20, "bold")
                )
                edit_button.grid(row=row_index, column=len(column_names)+1, padx=15, pady=5, sticky="nsew")

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error fetching inventory item: {e}")

    def clear_inventory_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()


    def delete_inventory(self, inventory_id):
        global db_cursor
        try:
            db_cursor.execute("DELETE FROM inventory WHERE i_id = %s", (inventory_id,))
            db_connection.commit()
            messagebox.showinfo("Success", "Inventory item deleted successfully.")
            self.refresh_inventory()
        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error deleting Inventory Item: {e}")


    def update_inventory(self, inventory_id):
        global db_cursor
        try:
            db_cursor.execute("SELECT * FROM inventory WHERE i_id = %s", (inventory_id,))
            inventory_data = db_cursor.fetchone()
            
            if inventory_data:
                self.inventory_dialog = CTkToplevel(self.app)
                self.inventory_dialog.title("Update Inventory")
                self.inventory_dialog.geometry("400x450")

                self.inventory_dialog.grab_set()

                left_frame = CTkFrame(self.inventory_dialog)
                left_frame.pack(side="left", padx=20, pady=20)

                right_frame = CTkFrame(self.inventory_dialog)
                right_frame.pack(side="right", padx=20, pady=20)

                CTkLabel(left_frame, text="Asset ID:").pack(pady=5)
                self.inventory_aid_entry = CTkEntry(left_frame)
                self.inventory_aid_entry.insert(0, inventory_data[2])
                self.inventory_aid_entry.pack(pady=5)

                CTkLabel(right_frame, text="Invetory Qty:").pack(pady=5)
                self.inventory_qty_entry = CTkEntry(right_frame)
                self.inventory_qty_entry.insert(0, inventory_data[1])
                self.inventory_qty_entry.pack(pady=5)

                CTkLabel(left_frame, text="Movement Date:").pack(pady=5)
                self.movement_date_entry = CTkEntry(left_frame)
                self.movement_date_entry.insert(0, inventory_data[3])
                self.movement_date_entry.pack(pady=5)

                CTkLabel(right_frame, text="Status (In/Out):").pack(pady=5)
                self.inventory_status_entry = CTkEntry(right_frame)
                self.inventory_status_entry.insert(0, str(inventory_data[4]))
                self.inventory_status_entry.pack(pady=5)

                CTkLabel(left_frame, text="Acquired Price: ").pack(pady=5)
                self.acq_price_entry = CTkEntry(left_frame)
                self.acq_price_entry.insert(0, str(inventory_data[5]))
                self.acq_price_entry.pack(pady=5)

                CTkLabel(right_frame, text="Market Value:").pack(pady=5)
                self.market_value_entry = CTkEntry(right_frame)
                if inventory_data[6]:
                    self.market_value_entry.insert(0, str(inventory_data[6]))
                self.market_value_entry.pack(pady=5)

                CTkLabel(left_frame, text="Remarks:").pack(pady=5)
                self.remarks_entry = CTkEntry(left_frame)
                if inventory_data[8]:
                    self.remarks_entry.insert(0, inventory_data[8])
                self.remarks_entry.pack(pady=5)

                CTkButton(
                    right_frame, 
                    text="Update Inventory", 
                    command=lambda: self.submit_inventory_update(inventory_id)
                ).pack(pady=20)

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Database Error", f"Error fetching Inventory data: {e}")

    def submit_inventory_update(self, inventory_id):
        global db_connection, db_cursor
        
        inventory_aid = self.inventory_aid_entry.get()
        inventory_qty = self.inventory_qty_entry.get()
        movement_date = self.movement_date_entry.get()
        inventory_status = self.inventory_status_entry.get()
        acq_price = self.acq_price_entry.get()
        market_value = self.market_value_entry.get()
        remarks = self.remarks_entry.get()

        if inventory_aid and inventory_status in ['In', 'Out']:
            try:
                inventory_qty = int(inventory_qty)
                market_value = float(market_value)
                acq_price = float(acq_price)

                db_cursor.execute("""
                    UPDATE Inventory 
                    SET i_qty = %s, 
                        a_id = %s,
                        movement_date = %s,
                        status = %s,
                        acquired_price = %s,
                        market_value = %s,
                        remarks = %s
                    WHERE i_id = %s
                """, (inventory_qty, inventory_aid, movement_date, inventory_status, acq_price, market_value, remarks, inventory_id))
                
                db_connection.commit()
                messagebox.showinfo("Success", "Inventory updated successfully!")
                self.inventory_dialog.destroy()
                self.refresh_inventory()
            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Failed to update inventory.")
        else:
            messagebox.showwarning("Input Error", "Could Not Find Inventory Information")


    def add_new_inventory(self):
        self.inventory_dialog = CTkToplevel(self.app)
        self.inventory_dialog.title("Add New Item to Inventory")
        self.inventory_dialog.geometry("400x450")

        self.inventory_dialog.grab_set()

        left_frame = CTkFrame(self.inventory_dialog)
        left_frame.pack(side="left", padx=20, pady=20)

        right_frame = CTkFrame(self.inventory_dialog)
        right_frame.pack(side="right", padx=20, pady=20)

        CTkLabel(left_frame, text="Asset ID:").pack(pady=5)
        self.inventory_aid_entry = CTkEntry(left_frame)
        self.inventory_aid_entry.pack(pady=5)

        CTkLabel(right_frame, text="Invetory Qty:").pack(pady=5)
        self.inventory_qty_entry = CTkEntry(right_frame)
        self.inventory_qty_entry.pack(pady=5)

        CTkLabel(left_frame, text="Movement Date:").pack(pady=5)
        self.movement_date_entry = CTkEntry(left_frame)
        self.movement_date_entry.pack(pady=5)

        CTkLabel(right_frame, text="Status (In/Out):").pack(pady=5)
        self.inventory_status_entry = CTkEntry(right_frame)
        self.inventory_status_entry.pack(pady=5)

        CTkLabel(left_frame, text="Acquired Price: ").pack(pady=5)
        self.acq_price_entry = CTkEntry(left_frame)
        self.acq_price_entry.pack(pady=5)

        CTkLabel(right_frame, text="Market Value:").pack(pady=5)
        self.market_value_entry = CTkEntry(right_frame)
        self.market_value_entry.pack(pady=5)

        CTkLabel(left_frame, text="Remarks:").pack(pady=5)
        self.remarks_entry = CTkEntry(left_frame)
        self.remarks_entry.pack(pady=5)

        CTkButton(left_frame, text="Add Inventory", command=self.submit_inventory).pack(pady=20)

    def submit_inventory(self):
        global db_connection, db_cursor
        
        inventory_aid = self.inventory_aid_entry.get()
        inventory_qty = self.inventory_qty_entry.get()
        movement_date = self.movement_date_entry.get()
        inventory_status = self.inventory_status_entry.get()
        acq_price = self.acq_price_entry.get()
        market_value = self.market_value_entry.get()
        remarks = self.remarks_entry.get()

        if inventory_aid and inventory_status in ['In', 'Out']:
            try:
                inventory_qty = int(inventory_qty)
                market_value = float(market_value)
                acq_price = float(acq_price)

                db_cursor.execute(
                    "INSERT INTO INVENTORY (i_qty, a_id, status, acquired_price, market_value, remarks) VALUES (%s, %s, %s, %s, %s, %s)",
                    (inventory_qty, inventory_aid, inventory_status, acq_price, market_value, remarks)
                )
                db_connection.commit()
                messagebox.showinfo("Success", "New Inventory Item added successfully!")
                self.inventory_dialog.destroy()
                self.refresh_inventory()
            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Failed to add new item to Inventory.")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out correctly.")


if __name__ == "__main__":
    StockManagementApp()

