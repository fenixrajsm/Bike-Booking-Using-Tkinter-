import tkinter as tk
from tkinter import messagebox
import db_connection

class AdminLoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        
        # Center the Login Box
        container = tk.Frame(self, bg="white", padx=40, pady=40, bd=1, relief="solid")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header
        tk.Label(container, text="ADMIN PORTAL", font=("Helvetica", 20, "bold"), bg="white", fg="#2C3E50").pack(pady=(0, 30))
        
        # Email
        tk.Label(container, text="Email Address", bg="white", font=("Segoe UI", 10), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        self.email_entry = tk.Entry(container, width=30, font=("Segoe UI", 12), bd=1, relief="solid")
        self.email_entry.pack(pady=(0, 20), ipady=4)

        # Password
        tk.Label(container, text="Password", bg="white", font=("Segoe UI", 10), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        self.pass_entry = tk.Entry(container, width=30, font=("Segoe UI", 12), bd=1, relief="solid", show="*")
        self.pass_entry.pack(pady=(0, 30), ipady=4)

        # Login Button
        tk.Button(container, text="SECURE LOGIN", bg="#E74C3C", fg="white", font=("Segoe UI", 11, "bold"), 
                  cursor="hand2", command=self.do_login, relief="flat").pack(fill="x", pady=10, ipady=5)

        # Back to User Login
        lbl_back = tk.Label(container, text="← Back to User Login", bg="white", fg="#3498DB", cursor="hand2", font=("Segoe UI", 9))
        lbl_back.pack(pady=10)
        lbl_back.bind("<Button-1>", lambda e: controller.show_frame("LoginRegisterFrame"))

    def do_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter credentials.")
            return
            
        conn = db_connection.create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
                
                if user and user['password'] == password:
                    if user['role'] == 'admin':
                        self.controller.login_user(user) # This will redirect to AdminDashboard based on role
                    else:
                        messagebox.showerror("Access Denied", "You do not have administrative privileges.")
                else:
                    messagebox.showerror("Error", "Invalid Email or Password.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
