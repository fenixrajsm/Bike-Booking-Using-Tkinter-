import tkinter as tk
from PIL import Image, ImageTk
import os

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        # Configure grid to center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container
        main_container = tk.Frame(self, bg="white")
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # --- LEFT SECTION: Text & CTA ---
        text_frame = tk.Frame(main_container, bg="white", padx=60)
        text_frame.grid(row=0, column=0, sticky="nsew")
        
        # Spacer
        tk.Frame(text_frame, bg="white").pack(expand=True)
        
        tk.Label(text_frame, text="EXPERIENCE\nTHE THRILL", font=("Helvetica", 40, "bold"), 
                 bg="white", fg="#2C3E50", justify="left").pack(anchor="w")
        
        tk.Label(text_frame, text="Discover the world's most premium superbikes.\nEngineered for speed, designed for passion.", 
                 font=("Arial", 14), bg="white", fg="#7f8c8d", justify="left").pack(anchor="w", pady=(15, 30))
        
        cta_btn = tk.Button(text_frame, text="VIEW COLLECTION →", bg="#E74C3C", fg="white", 
                            font=("Arial", 12, "bold"), padx=25, pady=12, bd=0, cursor="hand2",
                            activebackground="#c0392b", activeforeground="white",
                            command=lambda: controller.show_frame("ModelsFrame"))
        cta_btn.pack(anchor="w")

        # Spacer
        tk.Frame(text_frame, bg="white").pack(expand=True)

        # --- RIGHT SECTION: Hero Image ---
        img_frame = tk.Frame(main_container, bg="white")
        img_frame.grid(row=0, column=1, sticky="nsew")
        
        # Load Image
        try:
            # Construct path to assets relative to main.py
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Adjust path: views/home.py -> ../assets -> main dir is one level up
            assets_dir = os.path.join(base_dir, "..", "assets")
            img_path = os.path.join(assets_dir, "ducati_panigale.png")
            
            # Using try-except block specifically for image loading
            if os.path.exists(img_path):
                original_img = Image.open(img_path)
                # Resize keeping aspect ratio
                width = 600
                ratio = width / float(original_img.size[0])
                height = int((float(original_img.size[1]) * float(ratio)))
                
                # Check for Resampling attribute (older Pillow versions use ANTIALIAS)
                if hasattr(Image, "Resampling"):
                     resample_method = Image.Resampling.LANCZOS
                else:
                     resample_method = Image.ANTIALIAS

                resized_img = original_img.resize((width, height), resample_method)
                self.photo = ImageTk.PhotoImage(resized_img)
                
                img_lbl = tk.Label(img_frame, image=self.photo, bg="white")
                img_lbl.pack(expand=True)
            else:
                tk.Label(img_frame, text="Image not found", bg="white").pack(expand=True)
        except Exception as e:
            tk.Label(img_frame, text=f"Error loading image: {e}", bg="white").pack(expand=True)

        # About / Footer text (Optional, at bottom)
        footer_frame = tk.Frame(self, bg="#ecf0f1", height=60)
        footer_frame.grid(row=1, column=0, sticky="ew")
        tk.Label(footer_frame, text="© 2026 PHOENIX BIKES | Driven by Performance", 
                 bg="#ecf0f1", fg="#95a5a6", font=("Arial", 10)).pack(pady=10)

