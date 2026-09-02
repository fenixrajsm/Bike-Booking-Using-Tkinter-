import tkinter as tk
from tkinter import messagebox
from views.home import HomeFrame
from views.models import ModelsFrame
from views.booking import BookingFrame
from views.login_register import LoginRegisterFrame
from views.contact import ContactFrame
from views.admin import AdminFrame
from views.profile import ProfileFrame
from views.bike_details import BikeDetailsFrame # Import
from views.admin_login import AdminLoginFrame # Import
import db_connection

class BikeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phoenix Bikes - Premium Showroom")
        self.geometry("1100x700")
        self.state('zoomed') # Start maximized
        self.configure(bg="#f0f0f0")
        
        # Session State
        self.current_user = None # None or dict {'id':..., 'name':..., 'role':...}

        # Initialize Database
        db_connection.setup_database()

        # Styles & Colors
        self.colors = {
            "primary": "#E74C3C",   # Red
            "secondary": "#2C3E50", # Dark Blue/Grey
            "text": "#333333",
            "bg": "#ffffff",
            "nav_bg": "#1abc9c"     # Teal
        }

        # Container for Frames
        self.container = tk.Frame(self, bg=self.colors["bg"])
        
        self.create_navbar() # Navbar first
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold frames
        self.frames = {}
        
        # Initialize Frames
        for F in (HomeFrame, LoginRegisterFrame, ModelsFrame, BookingFrame, AdminFrame, ProfileFrame, ContactFrame, BikeDetailsFrame, AdminLoginFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeFrame")

    def create_navbar(self):
        nav_frame = tk.Frame(self, bg=self.colors["secondary"], height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False) # Maintain height

        # Logo / Title
        title_lbl = tk.Label(nav_frame, text="PHOENIX BIKES", bg=self.colors["secondary"], fg="white",
                             font=("Helvetica", 24, "bold"))
        title_lbl.pack(side="left", padx=20)

        # Navigation Buttons
        btn_frame = tk.Frame(nav_frame, bg=self.colors["secondary"])
        btn_frame.pack(side="right", padx=20)

        # Requests: 1. About, 2. Login, 3. Bike Details, 4. Booking, 5. Contact
        nav_items = [
            ("About", "HomeFrame"),
            ("Login", "LoginRegisterFrame"),
            ("Bike Details", "ModelsFrame"),
            ("Booking", "BookingFrame"),
            ("Contact", "ContactFrame")
        ]

        self.nav_buttons = {}

        for text, frame_name in nav_items:
            # We use a closure or lambda carefully here
            btn = tk.Button(btn_frame, text=text, bg=self.colors["secondary"], fg="white",
                            font=("Arial", 12), bd=0, activebackground=self.colors["primary"],
                            activeforeground="white", cursor="hand2",
                            command=lambda name=frame_name: self.show_frame(name))
            btn.pack(side="left", padx=10, pady=10)
            self.nav_buttons[frame_name] = btn

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        
        # Redirect if trying to access Login/Register while logged in -> Go to Profile
        if (page_name == "LoginRegisterFrame" or page_name == "AdminLoginFrame") and self.current_user:
            page_name = "ProfileFrame"

        frame = self.frames[page_name]
        
        # Refresh logic if needed (e.g., if logging in changed state)
        if hasattr(frame, 'on_show'):
            frame.on_show()

        frame.tkraise()
        self.update_nav_highlight(page_name)

    def update_nav_highlight(self, active_page):
        # Reset all
        for name, btn in self.nav_buttons.items():
            btn.config(bg=self.colors["secondary"])
        
        # Highlight active
        # Map ProfileFrame back to LoginRegisterFrame button for highlighting
        target_btn_name = active_page
        if active_page == "ProfileFrame" or active_page == "AdminLoginFrame":
             target_btn_name = "LoginRegisterFrame"
        elif active_page == "AdminFrame":
             target_btn_name = "BookingFrame"

        if target_btn_name in self.nav_buttons:
             self.nav_buttons[target_btn_name].config(bg=self.colors["primary"])

    def login_user(self, user_data):
        self.current_user = user_data
        messagebox.showinfo("Login", f"Welcome back, {user_data['name']}!")
        
        # Update 'Login' button to 'Profile'
        if "LoginRegisterFrame" in self.nav_buttons:
             self.nav_buttons["LoginRegisterFrame"].config(text="Profile")

        if user_data['role'] == 'admin':
            # Change Booking to Dashboard
            if "BookingFrame" in self.nav_buttons:
                 btn = self.nav_buttons["BookingFrame"]
                 btn.config(text="Dashboard", command=lambda: self.show_frame("AdminFrame"))
            
            self.show_frame("AdminFrame")
        else:
            # Go to ModelsFrame (Bike Details)
            self.show_frame("ModelsFrame")

    def logout_user(self):
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out.")
        
        if "LoginRegisterFrame" in self.nav_buttons:
             self.nav_buttons["LoginRegisterFrame"].config(text="Login")

        if "BookingFrame" in self.nav_buttons:
             btn = self.nav_buttons["BookingFrame"]
             btn.config(text="Booking", command=lambda: self.show_frame("BookingFrame"))
             
        self.show_frame("HomeFrame")

if __name__ == "__main__":
    app = BikeApp()
    app.mainloop()
