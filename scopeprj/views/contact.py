import tkinter as tk
from tkinter import messagebox
import db_connection

class ContactFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # Main Container with padding
        main_container = tk.Frame(self, bg="#f0f0f0")
        main_container.pack(expand=True, fill="both", padx=50, pady=40)
        
        # Center the content
        content_wrapper = tk.Frame(main_container, bg="white", bd=0, highlightthickness=0)
        content_wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)
        
        # Grid layout for split view (Left: Info, Right: Form)
        content_wrapper.grid_columnconfigure(0, weight=4) # 40%
        content_wrapper.grid_columnconfigure(1, weight=6) # 60%
        content_wrapper.grid_rowconfigure(0, weight=1)

        # --- LEFT PANEL: Contact Info ---
        left_panel = tk.Frame(content_wrapper, bg="#2C3E50")
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Content in Left Panel
        lp_content = tk.Frame(left_panel, bg="#2C3E50")
        lp_content.pack(expand=True, fill="x", padx=40)

        tk.Label(lp_content, text="Get in Touch", font=("Helvetica", 26, "bold"), 
                 bg="#2C3E50", fg="white", anchor="w").pack(fill="x", pady=(0, 30))
        
        self.create_info_item(lp_content, "📍 Address", "14/305 Thiruvattar,\nKanyakumari District")
        self.create_info_item(lp_content, "📞 Phone", "+91 9385762182")
        self.create_info_item(lp_content, "✉ Email", "phoenix@gmail.com")
        self.create_info_item(lp_content, "🕒 Hours", "Mon - Sat: 9:00 AM - 8:00 PM")

        # --- RIGHT PANEL: Contact Form ---
        right_panel = tk.Frame(content_wrapper, bg="white")
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        rp_content = tk.Frame(right_panel, bg="white")
        rp_content.pack(expand=True, fill="both", padx=50, pady=40)

        tk.Label(rp_content, text="Send us a Message", font=("Helvetica", 22, "bold"), 
                 bg="white", fg="#333").pack(anchor="w", pady=(0, 20))

        # Form Fields
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.create_label_entry(rp_content, "Full Name", self.name_var)
        self.create_label_entry(rp_content, "Email Address", self.email_var)
        
        tk.Label(rp_content, text="Message", font=("Arial", 11, "bold"), bg="white", fg="#555").pack(anchor="w", pady=(10, 5))
        self.msg_text = tk.Text(rp_content, height=5, font=("Arial", 11), bg="#f9f9f9", bd=1, relief="solid")
        self.msg_text.pack(fill="x")

        # Send Button
        send_btn = tk.Button(rp_content, text="SEND MESSAGE", font=("Arial", 11, "bold"),
                             bg="#E74C3C", fg="white", activebackground="#c0392b", activeforeground="white",
                             bd=0, padx=20, pady=10, cursor="hand2", command=self.send_msg)
        send_btn.pack(pady=30, anchor="w")

    def create_info_item(self, parent, title, value):
        container = tk.Frame(parent, bg="#2C3E50")
        container.pack(fill="x", pady=15)
        
        tk.Label(container, text=title, font=("Arial", 12, "bold"), 
                 bg="#2C3E50", fg="#E74C3C", anchor="w").pack(fill="x")
        tk.Label(container, text=value, font=("Arial", 11), 
                 bg="#2C3E50", fg="#ecf0f1", anchor="w", justify="left").pack(fill="x", pady=(2, 0))

    def create_label_entry(self, parent, label_text, variable):
        tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), bg="white", fg="#555").pack(anchor="w", pady=(10, 5))
        entry = tk.Entry(parent, textvariable=variable, font=("Arial", 11), bg="#f9f9f9", bd=1, relief="solid")
        entry.pack(fill="x", ipady=8)

    def on_show(self):
        # Pre-fill data if user is logged in
        current_user = self.controller.current_user
        if current_user:
            # We assume current_user has 'name' and 'email' keys based on main.py analysis
            # If keys might be missing, use .get()
            self.name_var.set(current_user.get('name', ''))
            self.email_var.set(current_user.get('email', ''))
        else:
            self.name_var.set("")
            self.email_var.set("")
        
        # Clear message
        self.msg_text.delete("1.0", tk.END)

    def send_msg(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        msg = self.msg_text.get("1.0", tk.END).strip()
        
        if not name or not email or not msg:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        conn = db_connection.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)", 
                               (name, email, msg))
                conn.commit()
                messagebox.showinfo("Success", "Your message has been sent successfully!")
                self.msg_text.delete("1.0", tk.END)
                # clear fields if not logged in? Optional. 
                # If logged in, we keep them filled.
                if not self.controller.current_user:
                    self.name_var.set("")
                    self.email_var.set("")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")
            finally:
                conn.close()
        else:
             messagebox.showerror("Error", "Database connection failed.")
