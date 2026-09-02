import tkinter as tk
from tkinter import messagebox, ttk
import db_connection

class BookingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f6fa") # Light grey background
        self.controller = controller
        self.selected_bike = None

        # Center Container (The Card)
        card_frame = tk.Frame(self, bg="white", padx=40, pady=40, bd=1, relief="solid")
        card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6)

        # Header
        tk.Label(card_frame, text="Secure Checkout", font=("Helvetica", 24, "bold"), 
                 bg="white", fg="#2C3E50").pack(pady=(0, 20))
        
        # --- Order Summary Section ---
        summary_frame = tk.Frame(card_frame, bg="#ecf0f1", padx=20, pady=15)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(summary_frame, text="Order Summary", font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w")
        
        self.lbl_bike_model = tk.Label(summary_frame, text="No Bike Selected", font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2C3E50")
        self.lbl_bike_model.pack(anchor="w", pady=(5, 0))
        
        self.lbl_bike_price = tk.Label(summary_frame, text="$0.00", font=("Arial", 14), bg="#ecf0f1", fg="#E74C3C")
        self.lbl_bike_price.pack(anchor="w")

        # --- Customer Details Section ---
        details_frame = tk.Frame(card_frame, bg="white")
        details_frame.pack(fill="x")

        # Row 1: Name & Phone
        r1 = tk.Frame(details_frame, bg="white")
        r1.pack(fill="x", pady=10)
        
        container_name, self.entry_name = self.create_input(r1, "Full Name", 0.48)
        container_name.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        container_phone, self.entry_phone = self.create_input(r1, "Phone Number", 0.48)
        container_phone.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Row 2: Payment Method
        tk.Label(details_frame, text="Payment Method", font=("Arial", 10, "bold"), bg="white", fg="#7f8c8d").pack(anchor="w", pady=(10, 5))
        
        self.payment_var = tk.StringVar(value="Card")
        style = ttk.Style()
        style.configure("TRadiobutton", background="white", font=("Arial", 11))
        
        pay_frame = tk.Frame(details_frame, bg="white")
        pay_frame.pack(fill="x", anchor="w")
        
        ttk.Radiobutton(pay_frame, text="Credit/Debit Card", variable=self.payment_var, value="Card", 
                        command=self.toggle_payment_fields).pack(side="left", padx=(0, 20))
        ttk.Radiobutton(pay_frame, text="Cash on Delivery", variable=self.payment_var, value="Cash", 
                        command=self.toggle_payment_fields).pack(side="left")

        # --- Payment Details (Card) ---
        self.card_details_frame = tk.Frame(card_frame, bg="white", pady=10)
        self.card_details_frame.pack(fill="x")
        
        # Card Number
        container_card, self.entry_card_num = self.create_input(self.card_details_frame, "Card Number", 1.0)
        container_card.pack(fill="x", pady=(5, 0))
        
        # Expiry & CVV
        r_card = tk.Frame(self.card_details_frame, bg="white")
        r_card.pack(fill="x", pady=10)
        
        container_expiry, self.entry_card_expiry = self.create_input(r_card, "Expiry (MM/YY)", 0.48)
        container_expiry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        container_cvv, self.entry_card_cvv = self.create_input(r_card, "CVV", 0.48)
        container_cvv.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Confirm Button
        tk.Button(card_frame, text="CONFIRM BOOKING", bg="#E74C3C", fg="white", font=("Arial", 12, "bold"),
                  pady=12, bd=0, cursor="hand2", activebackground="#c0392b", activeforeground="white",
                  command=self.submit_booking).pack(fill="x", pady=(20, 0))

    def create_input(self, parent, label, rel_width):
        # Creates a container with label and entry
        # Returns (container, entry_widget) so caller can pack container and use entry
        container = tk.Frame(parent, bg="white")
        # rel_width is used by caller to gauge packing, but we can set min width if needed
        
        tk.Label(container, text=label, font=("Arial", 10, "bold"), bg="white", fg="#7f8c8d").pack(anchor="w")
        entry = tk.Entry(container, font=("Arial", 11), bg="#f9f9f9", bd=1, relief="solid")
        entry.pack(fill="x", ipady=8, pady=(5, 0))
        
        return container, entry

    def toggle_payment_fields(self):
        if self.payment_var.get() == "Card":
            self.card_details_frame.pack(fill="x")
        else:
            self.card_details_frame.pack_forget()

    def select_bike(self, bike):
        self.selected_bike = bike
        self.lbl_bike_model.config(text=bike.get('model_name', 'Unknown Model'))
        self.lbl_bike_price.config(text=f"${bike.get('price', '0.00')}")

    def on_show(self):
        # Auto-fill name if logged in
        if self.controller.current_user:
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, self.controller.current_user.get('name', ''))
            
            # Since phone might not be in user object yet (based on schema), we leave it or check
            self.entry_phone.delete(0, tk.END)
            # If phone exists in user dict
            if 'phone' in self.controller.current_user:
                 self.entry_phone.insert(0, str(self.controller.current_user['phone']))

    def submit_booking(self):
        # Basic validation logic similar to before
        if not self.selected_bike:
            messagebox.showerror("Error", "Please select a bike from the Models page first.")
            return

        if not self.controller.current_user:
            messagebox.showwarning("Login Required", "You must be logged in to book a bike.\nPlease login and try again.")
            self.controller.show_frame("LoginRegisterFrame")
            return
        
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        
        if not name or not phone:
             messagebox.showerror("Error", "Name and Phone are required.")
             return
             
        payment_method = self.payment_var.get()
        if payment_method == "Card":
             if not self.entry_card_num.get() or not self.entry_card_expiry.get() or not self.entry_card_cvv.get():
                 messagebox.showerror("Error", "Please fill in all card details.")
                 return

        # Insert into DB
        conn = db_connection.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO bookings (user_id, bike_id, customer_name, customer_phone, payment_method) VALUES (%s, %s, %s, %s, %s)"
                user_id = self.controller.current_user['id']
                cursor.execute(query, (user_id, self.selected_bike['id'], name, phone, payment_method))
                conn.commit()
                messagebox.showinfo("Success", "Booking Confirmed! Reference ID: #PHX" + str(cursor.lastrowid))
                self.controller.show_frame("HomeFrame")
            except Exception as e:
                messagebox.showerror("Error", f"Booking failed: {e}")
            finally:
                conn.close()

