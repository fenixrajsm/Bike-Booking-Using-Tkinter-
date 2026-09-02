import tkinter as tk
from tkinter import ttk, messagebox
import db_connection

class LoginRegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load Background Image
        try:
            from PIL import Image, ImageTk
            self.bg_image_raw = Image.open(r"C:\Users\fbxfn\OneDrive\Desktop\scopeprj\assets\wp5691386.webp")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image_raw)
            
            # Load Eye Icons
            self.eye_open_img = ImageTk.PhotoImage(Image.open(r"assets/eye_open.png").resize((20, 20), Image.Resampling.LANCZOS))
            self.eye_closed_img = ImageTk.PhotoImage(Image.open(r"assets/eye_closed.png").resize((20, 20), Image.Resampling.LANCZOS))
            
        except Exception as e:
            print(f"Error loading assets: {e}")
            self.bg_photo = None
            self.eye_open_img = None
            self.eye_closed_img = None

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        if self.bg_photo:
            self.bg_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            self.bind("<Configure>", self.resize_bg)
        
        # Center Frame for Notebook - Professional Look attempt
        # We use a white frame with some padding, maybe no bold borders but shadow-like
        self.center_frame = tk.Frame(self.canvas, bg="white", padx=40, pady=40, bd=0)
        # Place it in center relative to window size
        self.center_window_id = self.canvas.create_window(400, 300, window=self.center_frame, anchor="center")

        # Header
        tk.Label(self.center_frame, text="Welcome Back", font=("Helvetica", 24, "bold"), bg="white", fg="#333").pack(pady=(0, 20))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", background="#ecf0f1", foreground="black", padding=[20, 10], font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected", "#3498DB")], foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(self.center_frame)
        self.notebook.pack(expand=True, fill="both")

        # Login Tab
        login_tab = tk.Frame(self.notebook, bg="white", padx=30, pady=30)
        self.notebook.add(login_tab, text="Login")
        self.create_login_ui(login_tab)

        # Register Tab
        register_tab = tk.Frame(self.notebook, bg="white", padx=30, pady=30)
        self.notebook.add(register_tab, text="Register")
        self.create_register_ui(register_tab)

    def resize_bg(self, event):
        if self.bg_photo:
            from PIL import Image, ImageTk
            new_width = event.width
            new_height = event.height
            image = self.bg_image_raw.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_photo_resized = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.bg_id, image=self.bg_photo_resized)
            
            # Re-center the window
            self.canvas.coords(self.center_window_id, new_width//2, new_height//2)

    def create_login_ui(self, parent):
        tk.Label(parent, text="Email", bg="white", font=("Arial", 11), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        self.login_email = tk.Entry(parent, width=35, font=("Arial", 12), relief="solid", bd=1)
        self.login_email.pack(pady=(0, 15), ipady=5)

        tk.Label(parent, text="Password", bg="white", font=("Arial", 11), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        
        # Password Container for Eye Icon
        pass_frame = tk.Frame(parent, bg="white")
        pass_frame.pack(pady=(0, 5))
        
        self.login_pass = tk.Entry(pass_frame, show="*", width=30, font=("Arial", 12), relief="solid", bd=1)
        self.login_pass.pack(side="left", ipady=5)
        
        if getattr(self, 'eye_closed_img', None):
            self.btn_eye_login = tk.Button(pass_frame, image=self.eye_closed_img, bg="white", bd=0, cursor="hand2", 
                                           command=lambda: self.toggle_password(self.login_pass, self.btn_eye_login))
            self.btn_eye_login.pack(side="left", padx=5)

        # Forgot Password
        lbl_forgot = tk.Label(parent, text="Forgot Password?", bg="white", fg="#3498DB", cursor="hand2", font=("Arial", 9, "underline"))
        lbl_forgot.pack(anchor="e", pady=(0, 20))
        lbl_forgot.bind("<Button-1>", lambda e: self.show_forgot_password())

        tk.Button(parent, text="LOGIN", bg="#3498DB", fg="white", font=("Arial", 12, "bold"), 
                  relief="flat", cursor="hand2", command=self.do_login).pack(fill="x", pady=10, ipady=5)

        # Admin Login Link
        lbl_admin = tk.Label(parent, text="Admin Login", bg="white", fg="#7f8c8d", cursor="hand2", font=("Arial", 9))
        lbl_admin.pack(pady=(10, 0))
        lbl_admin.bind("<Button-1>", lambda e: self.controller.show_frame("AdminLoginFrame"))

    def toggle_password(self, entry, btn):
        if entry.cget('show') == '*':
            entry.config(show='')
            btn.config(image=self.eye_open_img)
        else:
            entry.config(show='*')
            btn.config(image=self.eye_closed_img)

    def show_forgot_password(self):
        # Mock Forgot Password Flow
        top = tk.Toplevel(self)
        top.title("Reset Password")
        top.geometry("400x300")
        top.configure(bg="white")
        
        tk.Label(top, text="Start Password Recovery", font=("Arial", 14, "bold"), bg="white").pack(pady=20)
        tk.Label(top, text="Enter your email address:", bg="white").pack(pady=5)
        
        entry_email = tk.Entry(top, width=30)
        entry_email.pack(pady=10)
        
        def send_code():
            email = entry_email.get()
            if not email:
                messagebox.showerror("Error", "Please enter valid email")
                return
            messagebox.showinfo("Sent", f"A recovery code has been sent to {email}\n(This is a simulation)")
            top.destroy()
            
        tk.Button(top, text="Send Code", bg="#27AE60", fg="white", command=send_code).pack(pady=20)

    def create_register_ui(self, parent):
        tk.Label(parent, text="Full Name", bg="white", font=("Arial", 11), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        self.reg_name = tk.Entry(parent, width=35, font=("Arial", 12), relief="solid", bd=1)
        self.reg_name.pack(pady=(0, 15), ipady=5)

        tk.Label(parent, text="Email", bg="white", font=("Arial", 11), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        self.reg_email = tk.Entry(parent, width=35, font=("Arial", 12), relief="solid", bd=1)
        self.reg_email.pack(pady=(0, 15), ipady=5)

        tk.Label(parent, text="Password", bg="white", font=("Arial", 11), fg="#7f8c8d").pack(anchor="w", pady=(0, 5))
        
        # Password Frame
        pass_frame = tk.Frame(parent, bg="white")
        pass_frame.pack(pady=(0, 20))

        self.reg_pass = tk.Entry(pass_frame, show="*", width=30, font=("Arial", 12), relief="solid", bd=1)
        self.reg_pass.pack(side="left", ipady=5)

        if getattr(self, 'eye_closed_img', None):
            self.btn_eye_reg = tk.Button(pass_frame, image=self.eye_closed_img, bg="white", bd=0, cursor="hand2", 
                                           command=lambda: self.toggle_password(self.reg_pass, self.btn_eye_reg))
            self.btn_eye_reg.pack(side="left", padx=5)

        tk.Button(parent, text="REGISTER", bg="#2ECC71", fg="white", font=("Arial", 12, "bold"),
                  relief="flat", cursor="hand2", command=self.do_register).pack(fill="x", pady=10, ipady=5)

    def do_login(self):
        email = self.login_email.get().strip()
        password = self.login_pass.get().strip()
        
        print(f"Debug: Attempting login for '{email}'")

        if not email or not password:
            messagebox.showerror("Login Failed", "Please enter both email and password.")
            return

        conn = db_connection.create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                # 1. Check if user exists by Email
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
                
                if user:
                    # 2. Check Password
                    if user['password'] == password:
                        print("Debug: Password MATCH. Logging in.")
                        self.controller.login_user(user)
                    else:
                        print(f"Debug: Password MISMATCH for {email}")
                        self.login_pass.delete(0, tk.END) # Clear password field
                        messagebox.showerror("Login Failed", "Invalid Password. Please try again.")
                else:
                    print(f"Debug: User '{email}' NOT found in DB.")
                    messagebox.showerror("Login Failed", "Invalid Email. No user found with this email.")

            except Exception as e:
                print(f"Debug: Login Error: {e}")
                messagebox.showerror("Error", f"Login error: {e}")
            finally:
                if conn.is_connected():
                    conn.close()
        else:
            print("Debug: DB Connection Failed in Login")
            messagebox.showerror("Error", "Database connection failed. Please check your database server.")

    def do_register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_pass.get().strip()
        
        print(f"Debug: Attempting register for {email}")

        if not name or not email or not password:
             messagebox.showerror("Error", "All fields are required")
             return

        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
                conn.commit()
                print("Debug: Registration successful")
                messagebox.showinfo("Success", "Registration successful! Please enter your password to login.")
                
                # Switch to Login Tab (Index 0)
                self.notebook.select(0)
                
                # Pre-fill Email
                self.login_email.delete(0, tk.END)
                self.login_email.insert(0, email)
                
                # Focus Password and Clear it
                self.login_pass.delete(0, tk.END)
                self.login_pass.focus_set()
            except Exception as e:
                print(f"Debug: Registration Error: {e}")
                messagebox.showerror("Error", f"Registration failed: {e}")
            finally:
                conn.close()
        else:
             print("Debug: DB Connection Failed in Register")
             messagebox.showerror("Error", "DB connection failed")
