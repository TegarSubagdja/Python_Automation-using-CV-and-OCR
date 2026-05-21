import os
import time
import tkinter as tk
import pyautogui
from PIL import Image, ImageTk

class ScreenSnipper:
    def __init__(self, filename):

        self.filename = filename

        # 1. Ambil screenshot layar penuh terlebih dahulu sebagai latar belakang
        self.screenshot = pyautogui.screenshot()
        
        # 2. Inisialisasi jendela Tkinter
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True) # Buat fullscreen
        self.root.attributes("-alpha", 0.3)        # Buat agak transparan (overlay)
        self.root.config(cursor="cross")          # Ubah kursor jadi tanda plus (+)
        
        # Canvas untuk menggambar kotak seleksi
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        # Bind event mouse
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Koordinat awal dan akhir drag
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None

    def on_button_press(self, event):
        # Simpan koordinat awal saat klik kiri ditekan
        self.start_x = event.x
        self.start_y = event.y
        # Buat kotak persegi panjang awal
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        # Update ukuran kotak selama mouse di-drag
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        # Saat klik kiri dilepas, simpan koordinat akhir
        self.end_x = event.x
        self.end_y = event.y
        
        # Tutup jendela overlay setelah selesai drag
        self.root.destroy()
        
        # Proses crop gambar berdasarkan koordinat drag
        self.crop_and_save()

    def crop_and_save(self):
        # Memastikan koordinat benar meskipun drag dari kanan ke kiri atau bawah ke atas
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        
        # Cek jika area yang di-drag terlalu kecil (tidak sengaja terklik)
        if (x2 - x1) < 5 or (y2 - y1) < 5:
            print("Area terlalu kecil, pembatalan simpan.")
            return

        # Potong gambar berdasarkan koordinat seleksi kotak
        cropped_image = self.screenshot.crop((x1, y1, x2, y2))
        
        # Simpan hasil crop menjadi file PNG

        cropped_image.save(self.filename)
        print(f"Berhasil! Gambar ikon disimpan dengan nama: '{self.filename}'")
        print(f"Ukuran ikon: {x2-x1}x{y2-y1} pixel.")

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Silakan drag area ikon di layarmu...")
    for filename in ['AskPosition', 'VoicePosition', 'CopyPosition']:
        time.sleep(2)
        snipper = ScreenSnipper(f"TargetObject/{filename}.png")
        snipper.start()