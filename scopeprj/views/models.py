import tkinter as tk
from tkinter import ttk
import db_connection

class ModelsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        header = tk.Label(self, text="Bike Details", font=("Helvetica", 24, "bold"), bg="white", pady=20)
        header.pack(fill="x")

        # Scrollable Area
        canvas = tk.Canvas(self, bg="white")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_show(self):
        # Refresh bike list from DB
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bikes")
            bikes = cursor.fetchall()
            conn.close()
            
            row_idx = 0
            col_idx = 0
            for bike in bikes:
                self.create_bike_card(bike, row_idx, col_idx)
                col_idx += 1
                if col_idx > 2: # 3 columns
                    col_idx = 0
                    row_idx += 1
        else:
            lbl = tk.Label(self.scrollable_frame, text="Database Connection Failed. Ensure MySQL is running.", fg="red", bg="white")
            lbl.pack(pady=20)

    def create_bike_card(self, bike, row, col):
        card = tk.Frame(self.scrollable_frame, bg="#ecf0f1", bd=1, relief="solid", padx=10, pady=10)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        # Image Handling
        img_path = bike.get('image_path')
        self.img_refs = getattr(self, 'img_refs', []) # Keep refs

        if img_path:
            try:
                from PIL import Image, ImageTk
                img = Image.open(img_path)
                img = img.resize((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.img_refs.append(photo)
                tk.Label(card, image=photo, bg="#ecf0f1").pack()
            except Exception as e:
                print(f"Error checking/loading image {img_path}: {e}")
                tk.Label(card, text="[Image Not Found]", bg="grey", fg="white", width=30, height=10).pack()
        else:
            tk.Label(card, text="[Image]", bg="grey", fg="white", width=30, height=10).pack()

        tk.Label(card, text=bike['model_name'], font=("Arial", 14, "bold"), bg="#ecf0f1").pack(pady=5)
        tk.Label(card, text=f"Engine: {bike['engine_cc']}", bg="#ecf0f1").pack()
        tk.Label(card, text=f"Mileage: {bike['mileage']}", bg="#ecf0f1").pack()
        tk.Label(card, text=f"Price: ${bike['price']}", font=("Arial", 12, "bold"), fg="#E74C3C", bg="#ecf0f1").pack(pady=5)

        tk.Button(card, text="View Details", bg="#3498DB", fg="white", font=("Arial", 10, "bold"),
                  command=lambda b=bike: self.go_to_details(b)).pack(pady=5)
                  
        tk.Button(card, text="Book Now", bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
                  command=lambda b=bike: self.go_to_booking(b)).pack(pady=5)

    def go_to_details(self, bike):
        details_frame = self.controller.frames["BikeDetailsFrame"]
        details_frame.set_bike(bike)
        self.controller.show_frame("BikeDetailsFrame")

    def go_to_booking(self, bike):
        booking_frame = self.controller.frames["BookingFrame"]
        booking_frame.select_bike(bike)
        self.controller.show_frame("BookingFrame")
