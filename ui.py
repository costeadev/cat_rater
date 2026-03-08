import tkinter as tk
import tkinter.font as tkfont
from io import BytesIO
import os
import sys
import pyglet
from PIL import Image, ImageTk, ImageOps, ImageSequence
import db
import api


class CatRaterUI:
    def __init__(self, root):
        db.init_db()

        self.root = root
        self.root.title("Cat Rater")
        self.root.geometry("800x900")
        self.root.config(bg="#fffdd6")
        self.root

        self.setup_fonts()
        self.create_widgets()
        self.current_cat_data = None
        self.load_new_cat()
        self.setup_icons()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def setup_icons(self):
        icon_path = self.resource_path("assets/icon.png")

        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            self.icon_img = ImageTk.PhotoImage(img)

            self.root.iconphoto(False, self.icon_img)

    def setup_fonts(self):
        font_path = self.resource_path("fonts/DynaPuff-Medium.ttf")
        print(f"Looking for font at: {font_path}")

        try:
            pyglet.options["win32_gdi_font"] = True
            pyglet.font.add_file(font_path)
            self.custom_font = tkfont.Font(family="DynaPuff Medium", size=50)
        except Exception as e:
            print(f"Font loading failed: {e}")
            self.custom_font = ("Arial", 50, "bold")

    def create_widgets(self):

        self.main_frame = tk.Frame(self.root, bg="#fffdd6")
        self.main_frame.pack(pady=10)

        # Title
        self.title = tk.Label(self.main_frame, text="Cat Rater", font=self.custom_font, bg="#fffdd6")
        self.title.pack(pady=10)

        # Image Display
        self.cat_label = tk.Label(self.main_frame, text="Loading a fresh cat...", bg="#ffffff", width=650, height=650)
        self.cat_label.pack(expand=True, fill="both", padx=25)

        # Star Rating Frame
        self.stars_frame = tk.Frame(self.main_frame, bg="#fffdd6")
        self.stars_frame.pack(pady=20)
        self.stars_frame.bind("<Leave>", lambda e: self.on_star_leave())

        self.star_labels = []

        # Generate 5 stars using a loop
        for i in range(5):
            lbl = tk.Label(
                self.stars_frame,
                text="★",
                font=("Arial", 35),
                fg="#444444",
                bg="#fffdd6",
                cursor="hand2"
            )
            lbl.grid(row=0, column=i, padx=5)
            lbl.bind("<Enter>", lambda e, idx=i: self.on_star_hover(idx))
            lbl.bind("<Button-1>", lambda e, idx=i: self.rate_and_refresh(idx + 1))
            self.star_labels.append(lbl)

    def on_star_hover(self, index):
        """Highlights the hovered star and all stars to its left."""
        for i in range(5):
            if i <= index:
                self.star_labels[i].config(fg="#FFD600")
            else:
                self.star_labels[i].config(fg="#444444")

    def on_star_leave(self):
        """Resets stars to the dark color when the mouse leave the frame"""
        for lbl in self.star_labels:
            lbl.config(fg="#444444")

    def load_new_cat(self):
        if hasattr(self, "animation_job"):
            self.root.after_cancel(self.animation_job)

        found_new = False
        while not found_new:
            try:
                # Assuming api.get_cat_info() returns {'id': '...', 'url': '...', 'bytes': '...'}
                cat_data = api.get_cat_info()[0]

                if not db.is_cat_rated(cat_data['id']):
                    self.current_cat_data = cat_data
                    found_new = True
                else:
                    print(f"Skipping cat {cat_data['id']}, already rated.")
            except Exception as e:
                print(f"Connection error: {e}")
                break

        """Fetches, processes, and displays a new image."""
        try:
            img_bytes = api.get_cat_bytes()
            with Image.open(BytesIO(img_bytes)) as img:
                self.frames = []
                self.durations = []

                target_size = (600, 600)

                for frame in ImageSequence.Iterator(img):
                    duration = frame.info.get("duration", 100)
                    self.durations.append(duration)

                    processed = frame.convert("RGBA")
                    if processed.width > 600 or processed.height > 600:
                        processed = ImageOps.fit(processed, target_size, Image.Resampling.LANCZOS)
                    else:
                        processed = ImageOps.pad(processed, target_size, color="#ffffff")

                    self.frames.append(ImageTk.PhotoImage(processed))

            self.frame_index = 0
            self.animate_cat()
        except Exception as e:
            print(f"Error: {e}")

    def animate_cat(self):
        if hasattr(self, "frames") and self.frames:
            frame = self.frames[self.frame_index]
            duration = self.durations[self.frame_index]

            self.cat_label.config(image=frame)
            self.frame_index = (self.frame_index + 1) % len(self.frames)

            # Schedule the next update (e.g., 50 ms for ~20fps)
            self.animation_job = self.root.after(duration, self.animate_cat)

    def rate_and_refresh(self, rating):
        db.save_rating(
            self.current_cat_data['id'],
            self.current_cat_data['url'],
            rating
        )
        print(f"You rated this cat: {rating}/5 stars!")
        self.load_new_cat()
