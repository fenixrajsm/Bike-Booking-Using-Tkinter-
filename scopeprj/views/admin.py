import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import db_connection

class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ecf0f1")
        self.controller = controller
        
        # Color Palette
        self.colors = {
            "sidebar_bg": "#2C3E50",
            "sidebar_fg": "#ECF0F1",
            "active_bg": "#34495E",
            "content_bg": "#ECF0F1",
            "card_bg": "#FFFFFF",
            "primary": "#E74C3C",   # Red accent
            "success": "#27AE60",   # Green
            "warning": "#F39C12",   # Orange
            "text": "#2C3E50"
        }

        # Layout: Sidebar (Left) + Content (Right)
        self.create_sidebar()
        self.create_content_area()

        # Initial View
        self.current_view = None
        self.show_view("Dashboard")

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg=self.colors["sidebar_bg"], width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Title / Brand
        title_lbl = tk.Label(self.sidebar, text="ADMIN PANEL", bg=self.colors["sidebar_bg"], 
                             fg=self.colors["sidebar_fg"], font=("Helvetica", 18, "bold"))
        title_lbl.pack(pady=(30, 40))

        # Navigation Menu
        self.nav_buttons = {}
        menu_items = ["Dashboard", "Inventory", "Bookings", "Messages"]
        
        for item in menu_items:
            btn = tk.Button(self.sidebar, text=item, bg=self.colors["sidebar_bg"], fg=self.colors["sidebar_fg"],
                            font=("Segoe UI", 12), bd=0, relief="flat", activebackground=self.colors["active_bg"],
                            activeforeground=self.colors["sidebar_fg"], cursor="hand2", anchor="w", padx=20,
                            command=lambda x=item: self.show_view(x))
            btn.pack(fill="x", pady=2)
            self.nav_buttons[item] = btn

        # Logout at bottom
        logout_btn = tk.Button(self.sidebar, text="Logout", bg=self.colors["primary"], fg="white",
                               font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2",
                               command=self.controller.logout_user)
        logout_btn.pack(side="bottom", fill="x", pady=20, padx=20)

    def create_content_area(self):
        self.content = tk.Frame(self, bg=self.colors["content_bg"])
        self.content.pack(side="right", fill="both", expand=True)

    def show_view(self, view_name):
        # Update Sidebar Styling
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.config(bg=self.colors["active_bg"], font=("Segoe UI", 12, "bold"))
            else:
                btn.config(bg=self.colors["sidebar_bg"], font=("Segoe UI", 12))

        # Clear Content
        for widget in self.content.winfo_children():
            widget.destroy()

        # Render View
        header = tk.Label(self.content, text=view_name, font=("Segoe UI", 24, "bold"), 
                          bg=self.colors["content_bg"], fg=self.colors["text"])
        header.pack(anchor="w", padx=30, pady=(30, 20))

        if view_name == "Dashboard":
            self.render_dashboard()
        elif view_name == "Inventory":
            self.render_inventory()
        elif view_name == "Bookings":
            self.render_bookings()
        elif view_name == "Messages":
            self.render_messages()

    # ========================== DASHBOARD ==========================
    def render_dashboard(self):
        stats_frame = tk.Frame(self.content, bg=self.colors["content_bg"])
        stats_frame.pack(fill="x", padx=30)
        
        # Get Stats from DB
        stats = self.fetch_stats()

        self.create_stat_card(stats_frame, "Total Income", f"${stats['income']:,.0f}", "#27AE60", 0)
        self.create_stat_card(stats_frame, "Total Bookings", str(stats['bookings']), "#2980B9", 1)
        self.create_stat_card(stats_frame, "Bikes in Stock", str(stats['stock']), "#8E44AD", 2)
        self.create_stat_card(stats_frame, "Messages", str(stats['messages']), "#F39C12", 3)

        # Recent Activity (Simple List)
        lbl = tk.Label(self.content, text="Recent Bookings", font=("Segoe UI", 14, "bold"), 
                       bg=self.colors["content_bg"], fg=self.colors["text"])
        lbl.pack(anchor="w", padx=30, pady=(30, 10))
        
        cols = ("Customer", "Bike", "Date", "Status")
        tree = ttk.Treeview(self.content, columns=cols, show='headings', height=8)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
            
        tree.pack(fill="x", padx=30)

        # Populate Recent Bookings
        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.customer_name, bikes.model_name, b.booking_date, b.status 
                FROM bookings b 
                JOIN bikes ON b.bike_id = bikes.id 
                ORDER BY b.booking_date DESC LIMIT 5
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

    def create_stat_card(self, parent, title, value, color, col_idx):
        card = tk.Frame(parent, bg="white", padx=20, pady=20, bd=1, relief="solid")
        card.grid(row=0, column=col_idx, padx=10, sticky="ew")
        
        tk.Label(card, text=title, font=("Segoe UI", 10), fg="#7f8c8d", bg="white").pack(anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), fg=color, bg="white").pack(anchor="w")
        
        parent.grid_columnconfigure(col_idx, weight=1)

    def fetch_stats(self):
        stats = {"income": 0, "bookings": 0, "stock": 0, "messages": 0}
        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor()
            
            # Booking Count
            cursor.execute("SELECT COUNT(*) FROM bookings")
            stats['bookings'] = cursor.fetchone()[0]
            
            # Stock Count
            cursor.execute("SELECT SUM(stock) FROM bikes")
            res = cursor.fetchone()[0]
            stats['stock'] = res if res else 0

            # Estimate Income (Sum of price of booked bikes)
            cursor.execute("""
                SELECT SUM(bikes.price) 
                FROM bookings 
                JOIN bikes ON bookings.bike_id = bikes.id
            """)
            res_income = cursor.fetchone()[0]
            stats['income'] = res_income if res_income else 0

            # Messages
            cursor.execute("SELECT COUNT(*) FROM contact_messages")
            stats['messages'] = cursor.fetchone()[0]

            conn.close()
        return stats

    # ========================== INVENTORY ==========================
    def render_inventory(self):
        # Toolbar
        toolbar = tk.Frame(self.content, bg=self.colors["content_bg"])
        toolbar.pack(fill="x", padx=30, pady=10)
        
        tk.Button(toolbar, text="+ Add New Bike", bg=self.colors["success"], fg="white", 
                  font=("Segoe UI", 10, "bold"), command=self.open_add_bike_modal).pack(side="right")
        
        tk.Button(toolbar, text="Refresh", command=lambda: self.show_view("Inventory")).pack(side="left")

        # Table
        cols = ("ID", "Model", "Price", "Stock", "Color", "Mileage")
        tree = ttk.Treeview(self.content, columns=cols, show='headings')
        
        for col in cols:
            tree.heading(col, text=col)
            if col == "ID": tree.column(col, width=50)
            else: tree.column(col, width=100)
            
        tree.pack(fill="both", expand=True, padx=30, pady=10)

        # Context Menu
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Edit Stock/Price", command=lambda: self.edit_selected_bike(tree))
        menu.add_command(label="Delete Bike", command=lambda: self.delete_selected_bike(tree))
        
        tree.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

        # Data
        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, model_name, price, stock, color, mileage FROM bikes")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

    def open_add_bike_modal(self):
        top = Toplevel(self)
        top.title("Add New Bike")
        top.geometry("400x500")
        top.configure(bg="white")
        
        fields = ["Model Name", "Engine CC", "Mileage", "Price", "Color", "Stock", "Image Path", "Description"]
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(top, text=field, bg="white").pack(anchor="w", padx=20, pady=(5,0))
            e = tk.Entry(top)
            e.pack(fill="x", padx=20)
            entries[field] = e
            
        def submit():
            data = {f: entries[f].get() for f in fields}
            # Simple validation
            if not data["Model Name"] or not data["Price"]:
                messagebox.showerror("Error", "Model Name and Price are required.")
                return

            try:
                conn = db_connection.create_connection()
                cursor = conn.cursor()
                sql = """INSERT INTO bikes (model_name, engine_cc, mileage, price, color, stock, image_path, description) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (data["Model Name"], data["Engine CC"], data["Mileage"], data["Price"], 
                       data["Color"], data["Stock"], data["Image Path"], data["Description"])
                cursor.execute(sql, val)
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Bike Added successfully!")
                top.destroy()
                self.show_view("Inventory")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(top, text="Save Bike", bg="#27AE60", fg="white", command=submit).pack(pady=20)

    def edit_selected_bike(self, tree):
        selected = tree.selection()
        if not selected: return
        item = tree.item(selected[0])
        bike_id = item['values'][0]
        curr_price = item['values'][2]
        curr_stock = item['values'][3]
        
        top = Toplevel(self)
        top.title(f"Edit Bike ID: {bike_id}")
        
        tk.Label(top, text="New Price:").pack()
        e_price = tk.Entry(top)
        e_price.insert(0, curr_price)
        e_price.pack()
        
        tk.Label(top, text="New Stock:").pack()
        e_stock = tk.Entry(top)
        e_stock.insert(0, curr_stock)
        e_stock.pack()
        
        def save():
            try:
                conn = db_connection.create_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE bikes SET price=%s, stock=%s WHERE id=%s", 
                               (e_price.get(), e_stock.get(), bike_id))
                conn.commit()
                conn.close()
                top.destroy()
                self.show_view("Inventory")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        tk.Button(top, text="Update", command=save).pack(pady=10)

    def delete_selected_bike(self, tree):
        selected = tree.selection()
        if not selected: return
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this bike?"): return
        
        bike_id = tree.item(selected[0])['values'][0]
        try:
            conn = db_connection.create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bikes WHERE id=%s", (bike_id,))
            conn.commit()
            conn.close()
            self.show_view("Inventory")
        except Exception as e:
            messagebox.showerror("Error", "Could not delete. Check if booked.")

    # ========================== BOOKINGS ==========================
    def render_bookings(self):
        # Table
        cols = ("Booking ID", "Customer", "Phone", "Bike Model", "Date", "Status", "Payment")
        tree = ttk.Treeview(self.content, columns=cols, show='headings')
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Actions
        btn_frame = tk.Frame(self.content, bg=self.colors["content_bg"])
        btn_frame.pack(fill="x", padx=30, pady=10)
        
        def update_status(new_status):
            selected = tree.selection()
            if not selected: return
            bk_id = tree.item(selected[0])['values'][0]
            
            try:
                conn = db_connection.create_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE bookings SET status=%s WHERE id=%s", (new_status, bk_id))
                conn.commit()
                conn.close()
                self.show_view("Bookings")
            except Exception as e: messagebox.showerror("Error", str(e))

        tk.Button(btn_frame, text="Mark Confirmed", bg="#27AE60", fg="white", command=lambda: update_status("Confirmed")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Mark Completed", bg="#2980B9", fg="white", command=lambda: update_status("Completed")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel Booking", bg="#C0392B", fg="white", command=lambda: update_status("Cancelled")).pack(side="left", padx=5)

        # Data
        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.id, b.customer_name, b.customer_phone, bk.model_name, b.booking_date, b.status, b.payment_method
                FROM bookings b
                JOIN bikes bk ON b.bike_id = bk.id
                ORDER BY b.booking_date DESC
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

    # ========================== MESSAGES ==========================
    def render_messages(self):
        cols = ("ID", "Name", "Email", "Message", "Date")
        tree = ttk.Treeview(self.content, columns=cols, show='headings')
        
        tree.heading("ID", text="ID"); tree.column("ID", width=50)
        tree.heading("Name", text="Name"); tree.column("Name", width=150)
        tree.heading("Email", text="Email"); tree.column("Email", width=200)
        tree.heading("Message", text="Message"); tree.column("Message", width=400)
        tree.heading("Date", text="Date"); tree.column("Date", width=150)
        
        tree.pack(fill="both", expand=True, padx=30, pady=20)

        conn = db_connection.create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, message, sent_at FROM contact_messages ORDER BY sent_at DESC")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
    
    def on_show(self):
        """Called when frame is brought to top"""
        self.show_view("Dashboard")
