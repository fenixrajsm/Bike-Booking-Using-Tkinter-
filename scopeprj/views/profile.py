import tkinter as tk
from tkinter import messagebox
import db_connection

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Header
        tk.Label(self, text="My Profile", font=("Helvetica", 24, "bold"), bg="white").pack(pady=30)

        # Form Container
        self.form_frame = tk.Frame(self, bg="white")
        self.form_frame.pack(pady=20)

        # Name
        tk.Label(self.form_frame, text="Full Name", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.ent_name = tk.Entry(self.form_frame, width=40, font=("Arial", 12))
        self.ent_name.pack(pady=(0, 15))

        # Email (Read-only usually, but editable here if we want)
        tk.Label(self.form_frame, text="Email", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.ent_email = tk.Entry(self.form_frame, width=40, font=("Arial", 12))
        self.ent_email.pack(pady=(0, 15))
        
        # Phone
        tk.Label(self.form_frame, text="Phone Number", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.ent_phone = tk.Entry(self.form_frame, width=40, font=("Arial", 12))
        self.ent_phone.pack(pady=(0, 15))

        # Address
        tk.Label(self.form_frame, text="Address", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.ent_addr = tk.Entry(self.form_frame, width=40, font=("Arial", 12))
        self.ent_addr.pack(pady=(0, 15))

        # Password
        tk.Label(self.form_frame, text="New Password (leave blank to keep current)", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.ent_pass = tk.Entry(self.form_frame, width=40, font=("Arial", 12), show="*")
        self.ent_pass.pack(pady=(0, 15))

        # Buttons
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Update Profile", bg="#27AE60", fg="white", font=("Arial", 12),
                  command=self.update_profile).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Logout", bg="#c0392b", fg="white", font=("Arial", 12),
                  command=self.logout).pack(side="left", padx=10)

    def on_show(self):
        # Populate fields with current user data
        user = self.controller.current_user
        if user:
            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, user['name'])
            
            self.ent_email.delete(0, tk.END)
            self.ent_email.insert(0, user['email'])
            
            self.ent_phone.delete(0, tk.END)
            self.ent_phone.insert(0, user.get('phone') or "")

            self.ent_addr.delete(0, tk.END)
            self.ent_addr.insert(0, user.get('address') or "")
            
            self.ent_pass.delete(0, tk.END) # Always clear password field
        else:
            # Should not happen if strictly controlled, but redirect if so
            self.controller.show_frame("LoginRegisterFrame")

    def update_profile(self):
        if not self.controller.current_user:
            return

        new_name = self.ent_name.get().strip()
        new_email = self.ent_email.get().strip()
        new_phone = self.ent_phone.get().strip()
        new_addr = self.ent_addr.get().strip()
        new_pass = self.ent_pass.get().strip()
        
        if not new_name or not new_email:
             messagebox.showerror("Error", "Name and Email cannot be empty.")
             return

        user_id = self.controller.current_user['id']
        
        conn = db_connection.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                if new_pass:
                    # Update with password
                    query = "UPDATE users SET name=%s, email=%s, phone=%s, address=%s, password=%s WHERE id=%s"
                    params = (new_name, new_email, new_phone, new_addr, new_pass, user_id)
                else:
                    # Update without password
                    query = "UPDATE users SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
                    params = (new_name, new_email, new_phone, new_addr, user_id)
                
                cursor.execute(query, params)
                conn.commit()
                
                # Update Session Data
                self.controller.current_user['name'] = new_name
                self.controller.current_user['email'] = new_email
                self.controller.current_user['phone'] = new_phone
                self.controller.current_user['address'] = new_addr
                if new_pass:
                    self.controller.current_user['password'] = new_pass
                
                messagebox.showinfo("Success", "Profile Updated Successfully!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Database connection failed.")

    def logout(self):
        self.controller.logout_user()
