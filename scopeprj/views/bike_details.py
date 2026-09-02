import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class BikeDetailsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        self.bike = None
        
        # Main Scrollable Canvas Container
        self.canvas = tk.Canvas(self, bg="#ffffff", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Content frame must be centered or fill
        self.content_frame = tk.Frame(self.canvas, bg="#ffffff")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def set_bike(self, bike):
        self.bike = bike
        self.refresh_ui()

    def refresh_ui(self):
        # Tools to clear
        for w in self.content_frame.winfo_children():
            w.destroy()

        if not self.bike: return

        # === 1. Top Navigation Bar (breadcrumb style) ===
        nav_bar = tk.Frame(self.content_frame, bg="#ffffff", pady=20, padx=40)
        nav_bar.pack(fill="x")
        
        tk.Button(nav_bar, text="← Back to Showroom", command=lambda: self.controller.show_frame("ModelsFrame"),
                  bg="#ffffff", fg="#7f8c8d", bd=0, font=("Segoe UI", 11), cursor="hand2", anchor="w").pack(side="left")

        # === 2. Main Split Container ===
        main_container = tk.Frame(self.content_frame, bg="#ffffff", padx=40)
        main_container.pack(fill="both", expand=True)
        
        # Grid Configuration: Left (Image) 55%, Right (Info) 45%
        main_container.grid_columnconfigure(0, weight=6)
        main_container.grid_columnconfigure(1, weight=4)

        # --- LEFT COLUMN: IMAGE ---
        left_col = tk.Frame(main_container, bg="#ffffff")
        left_col.grid(row=0, column=0, sticky="n", padx=(0, 40), pady=20)
        
        img_path = self.bike.get('image_path')
        if img_path:
            try:
                img = Image.open(img_path)
                # Dynamic resize logic could be better, but fixed large width is safe for now
                target_w = 600
                ratio = target_w / float(img.size[0])
                target_h = int(float(img.size[1]) * float(ratio))
                
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.img_ref = photo # Keep reference
                
                # Image Frame with simple border/shadow effect (using nested frames)
                img_border = tk.Frame(left_col, bg="#ecf0f1", padx=1, pady=1)
                img_border.pack()
                tk.Label(img_border, image=photo, bg="white").pack()
                
            except Exception as e:
                tk.Label(left_col, text="[Image Unavailable]", bg="#ecf0f1", width=60, height=20).pack()
        else:
             tk.Label(left_col, text="[No Image]", bg="#ecf0f1", width=60, height=20).pack()

        # --- RIGHT COLUMN: INFO ---
        right_col = tk.Frame(main_container, bg="#ffffff")
        right_col.grid(row=0, column=1, sticky="n", pady=20)

        # Title
        tk.Label(right_col, text=self.bike['model_name'].upper(), font=("Segoe UI", 28, "bold"), 
                 bg="#ffffff", fg="#2C3E50", anchor="w").pack(fill="x")
        
        # Price Tag
        price_frame = tk.Frame(right_col, bg="#ffffff")
        price_frame.pack(fill="x", pady=(10, 30))
        tk.Label(price_frame, text="Ex-Showroom Price", font=("Segoe UI", 10), fg="#95a5a6", bg="white").pack(anchor="w")
        tk.Label(price_frame, text=f"${self.bike['price']:,.2f}", font=("Segoe UI", 24, "bold"), fg="#E74C3C", bg="white").pack(anchor="w")

        # Technical Specs Refined
        tk.Label(right_col, text="SPECIFICATIONS", font=("Segoe UI", 10, "bold"), fg="#95a5a6", bg="white").pack(anchor="w", pady=(0, 10))
        
        specs_grid = tk.Frame(right_col, bg="#ffffff")
        specs_grid.pack(fill="x", pady=(0, 30))
        
        # Helper to create spec item
        def add_spec(parent, label, value, icon_char, r, c):
            f = tk.Frame(parent, bg="#f8f9fa", padx=15, pady=10, bd=0)
            f.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
            
            tk.Label(f, text=icon_char, font=("Arial", 16), bg="#f8f9fa", fg="#E74C3C").pack(side="left", padx=(0, 10))
            
            txt_f = tk.Frame(f, bg="#f8f9fa")
            txt_f.pack(side="left")
            tk.Label(txt_f, text=label.upper(), font=("Segoe UI", 8), fg="#95a5a6", bg="#f8f9fa").pack(anchor="w")
            tk.Label(txt_f, text=value, font=("Segoe UI", 11, "bold"), fg="#2C3E50", bg="#f8f9fa").pack(anchor="w")
            
            parent.grid_columnconfigure(c, weight=1)

        # Specs Data
        add_spec(specs_grid, "Engine", self.bike['engine_cc'], "⚙", 0, 0)
        add_spec(specs_grid, "Mileage", self.bike['mileage'], "⛽", 0, 1)
        add_spec(specs_grid, "Color", self.bike['color'], "🎨", 1, 0)
        add_spec(specs_grid, "Stock", str(self.bike['stock']) + " Units", "📦", 1, 1)

        # Description
        tk.Label(right_col, text="OVERVIEW", font=("Segoe UI", 10, "bold"), fg="#95a5a6", bg="white").pack(anchor="w", pady=(0, 10))
        desc_txt = self.bike.get('description', "Experience the thrill of the ride with this masterpiece of engineering.")
        tk.Label(right_col, text=desc_txt, font=("Segoe UI", 11), fg="#34495E", bg="white", 
                 wraplength=400, justify="left").pack(fill="x", pady=(0, 30))

        # CTA Button
        btn_book = tk.Button(right_col, text="BOOK NOW", bg="#E74C3C", fg="white", 
                             font=("Segoe UI", 12, "bold"), padx=20, pady=12, bd=0, cursor="hand2",
                             activebackground="#c0392b", activeforeground="white",
                             command=self.go_to_booking)
        btn_book.pack(fill="x")
        
        tk.Label(right_col, text="* 100% Refundable Booking Amount", font=("Segoe UI", 8), fg="#bdc3c7", bg="white").pack(pady=10)

    def go_to_booking(self):
        booking_frame = self.controller.frames["BookingFrame"]
        booking_frame.select_bike(self.bike)
        self.controller.show_frame("BookingFrame")
