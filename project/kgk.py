import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import messagebox, StringVar

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "12345"

class StockManagementApp:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("856x645")
        self.app.resizable(0, 0)

        ctk.set_appearance_mode("dark")
        self.current_orders_table_frame = None  # Keep track of the orders table frame
        self.orders_data = []  # Initialize the orders data

        # Frame for main content
        self.frame = CTkFrame(master=self.app, width=506, height=645, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(side="right", fill="both", expand=True)

        self.image_label = None  # For later use
        self.current_frame = None  # To keep track of current visible frame

        self.login_view()
        self.app.mainloop()

    def login_view(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        side_img_data = Image.open(r"C:\Users\Keerthana Prasad\Downloads\Stock-Manager-main (1)\Stock-Manager-main\project\shopping-cart-with-bag.jpg")
        self.side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 645))

        self.image_label = CTkLabel(master=self.app, text="", image=self.side_img)
        self.image_label.pack(expand=True, side="left")

        # Fonts
        h1_font = ctk.CTkFont(family="Helvetica", size=34, weight="bold")
        h1_font_italics = ctk.CTkFont(family="Helvetica", size=23, weight="bold", slant="italic")
        h2_font = ctk.CTkFont(family="Arial Bold", size=17, weight="bold")

        # Title
        CTkLabel(master=self.frame, text="Sign In", text_color="#D75B36", anchor="w", font=h1_font).pack(anchor="w", pady=(120, 0), padx=(25, 0))
        CTkLabel(master=self.frame, text="Stock Management Application", text_color="#636E79", anchor="w", font=h1_font_italics).pack(anchor="w", pady=(15, 0), padx=(25, 0))

        # Email
        CTkLabel(master=self.frame, text="    Email:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(60, 0), padx=(25, 0))
        self.email_entry = CTkEntry(master=self.frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", padx=(47, 0))

        # Password
        CTkLabel(master=self.frame, text="    Password:", text_color="#9A4220", anchor="w", font=h2_font).pack(anchor="w", pady=(30, 0), padx=(25, 0))
        self.password_entry = CTkEntry(master=self.frame, width=400, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show='*')
        self.password_entry.pack(anchor="w", padx=(47, 0))

        # Login button
        CTkButton(master=self.frame, text="Login", fg_color="#D2502E", hover_color="#B0C3CD", font=("Helvetica", 18, "bold"), text_color="#ffffff", width=400, command=self.authenticate).pack(anchor="w", pady=(40, 0), padx=(47, 0))

    def homepage(self):
        if self.image_label:
            self.image_label.destroy()  
        for widget in self.frame.winfo_children():
            widget.destroy() 

        self.create_sidebar()
        self.show_dashboard()  # Show the default page

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar_frame = CTkFrame(self.frame, width=200, corner_radius=0)
        sidebar_frame.pack(side="left", fill="y")

        # Sidebar logo and buttons
        logo_label = CTkLabel(sidebar_frame, text="Stock Management System", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.pack(pady=(20, 10))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Orders", self.show_orders),
            ("Returns", self.show_returns),
            ("Settings", self.show_settings),
            ("Account", self.show_account)
        ]
        for btn_text, command in buttons:
            CTkButton(sidebar_frame, text=btn_text, fg_color="transparent", text_color=("gray10", "gray90"), command=command).pack(pady=10, padx=20, fill='x')

    def show_dashboard(self):
        """Display the dashboard frame."""
        self.switch_frame("Dashboard")
        CTkLabel(self.current_frame, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        CTkLabel(self.current_frame, text="Welcome to the Stock Management Dashboard.").pack(pady=10)

    def show_orders(self):
        """Display the orders frame."""
        self.switch_frame("Orders")
        self.create_order_table()

    def show_returns(self):
        """Display the returns frame."""
        self.switch_frame("Returns")
        CTkLabel(self.current_frame, text="Returns", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        # Add return handling functionality here

    def show_settings(self):
        """Display the settings frame."""
        self.switch_frame("Settings")
        CTkLabel(self.current_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        # Add settings handling functionality here

    def show_account(self):
        """Display the account frame."""
        self.switch_frame("Account")
        CTkLabel(self.current_frame, text="Account", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        # Add account handling functionality here

    def switch_frame(self, page_name):
        """Clear the current frame for navigation."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = CTkFrame(self.frame)
        self.current_frame.pack(expand=True, fill='both')

    def create_order_table(self):
        """Create the orders table and the new order button."""
        CTkLabel(self.current_frame, text="Orders", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        # Sample order data
        self.orders_data = [
            ["3833", "Smartphone", "Alice", "123 Main St", "Confirmed", "8"],
            ["6432", "Laptop", "Bob", "456 Elm St", "Packing", "5"],
            ["2180", "Tablet", "Crystal", "789 Oak St", "Delivered", "1"]
        ]

        self.create_orders_table()  # Create initial orders table

        CTkButton(self.current_frame, text="+ New Order", command=self.open_new_order_dialog).pack(pady=20)

    def create_orders_table(self):
        """Create the orders table with headers and data."""
        # Clear the existing table frame if it exists
        for widget in self.current_frame.winfo_children():
            widget.destroy()  # Clear previous table and button

        # Create new frame for the orders table
        table_frame = CTkFrame(self.current_frame)
        table_frame.pack(pady=10)

        columns = ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"]
        for i, col in enumerate(columns):
            CTkLabel(table_frame, text=col, font=ctk.CTkFont(weight="bold")).grid(row=0, column=i, padx=5, pady=5)

        for row_index, row_data in enumerate(self.orders_data):
            for col_index, item in enumerate(row_data):
                CTkLabel(table_frame, text=item).grid(row=row_index + 1, column=col_index, padx=5, pady=5)

    def open_new_order_dialog(self):
        """Open a dialog to add a new order."""
        new_order_window = CTkToplevel(self.app)
        new_order_window.title("Add New Order")

        fields = [("Order ID", ""), ("Item Name", ""), ("Customer Name", ""), ("Address", ""), ("Status", "Pending"), ("Quantity", "")]
        vars = [StringVar(value=val) for _, val in fields]

        for i, (label, var) in enumerate(zip(fields, vars)):
            CTkLabel(new_order_window, text=label[0]).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            CTkEntry(new_order_window, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        CTkButton(new_order_window, text="Add Order", command=lambda: self.save_new_order(new_order_window, vars)).grid(row=len(fields), columnspan=2, pady=10)

    def save_new_order(self, window, variables):
        """Save the new order data to the table."""
        values = [var.get() for var in variables]
        if any(not v for v in values):  # Check for empty values
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        self.orders_data.append(values)
        self.create_orders_table()  # Refresh the order table
        window.destroy()  # Close the new order window

    def authenticate(self):
        """Authenticate user login."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.homepage()  # Redirect to the homepage
        else:
            messagebox.showerror("Login Error", "Incorrect email or password.")

if __name__ == "__main__":
    StockManagementApp()
