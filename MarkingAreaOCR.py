import tkinter as tk
import json
import pyautogui
import time

class ROISnipper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3) # Transparansi overlay
        self.root.config(cursor="cross")
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.root.destroy()
        self.save_coordinates()

    def save_coordinates(self):
        # Memastikan koordinat tidak terbalik saat drag
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        w = abs(self.start_x - self.end_x)
        h = abs(self.start_y - self.end_y)
        
        if w < 5 or h < 5:
            print("Area terlalu kecil, gagal menyimpan.")
            return

        # Data koordinat format PyAutoGUI (x, y, width, height)
        roi_data = {
            "x": x,
            "y": y,
            "width": w,
            "height": h
        }
        
        # Simpan ke file JSON
        with open('config_ocr.json', 'w', encoding='utf-8') as f:
            json.dump(roi_data, f, indent=4)
            
        print("\n[SUKSES] Koordinat ROI berhasil disimpan ke config_ocr.json!")
        print(f"Data: {roi_data}")

if __name__ == "__main__":
    print("Silakan drag area layar yang berisi teks target...")
    app = ROISnipper()
    app.root.mainloop()