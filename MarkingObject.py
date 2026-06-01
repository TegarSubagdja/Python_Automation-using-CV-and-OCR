import os
import time
import tkinter as tk
import pyautogui
from pynput import keyboard

stop = False
current_snipper = None


class ScreenSnipper:
    def __init__(self, filename):
        self.filename = filename

        self.screenshot = pyautogui.screenshot()

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(
            self.root,
            cursor="cross",
            bg="grey"
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.canvas.bind(
            "<ButtonPress-1>",
            self.on_button_press
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.on_move_press
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.on_button_release
        )

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            1,
            1,
            outline="red",
            width=2
        )

    def on_move_press(self, event):
        self.end_x = event.x
        self.end_y = event.y

        self.canvas.coords(
            self.rect,
            self.start_x,
            self.start_y,
            self.end_x,
            self.end_y
        )

    def on_button_release(self, event):
        global stop

        self.end_x = event.x
        self.end_y = event.y

        if not stop:
            self.crop_and_save()

        try:
            self.root.quit()
        except:
            pass

        try:
            self.root.destroy()
        except:
            pass

    def crop_and_save(self):
        x1 = min(
            self.start_x,
            self.end_x
        )

        y1 = min(
            self.start_y,
            self.end_y
        )

        x2 = max(
            self.start_x,
            self.end_x
        )

        y2 = max(
            self.start_y,
            self.end_y
        )

        if (x2 - x1) < 5 or (y2 - y1) < 5:
            print("Area terlalu kecil")
            return

        cropped_image = self.screenshot.crop(
            (x1, y1, x2, y2)
        )

        cropped_image.save(
            self.filename
        )

        print(
            f"Berhasil menyimpan '{self.filename}' "
            f"({x2 - x1}x{y2 - y1})"
        )

    def start(self):
        try:
            self.root.mainloop()
        except:
            pass


def on_press(key):
    global stop
    global current_snipper

    if key == keyboard.Key.esc:
        print("\nESC pressed. Exiting...")

        stop = True

        if current_snipper is not None:
            try:
                current_snipper.root.quit()
            except:
                pass

            try:
                current_snipper.root.destroy()
            except:
                pass

        return False


def capture_template(template_name):
    global current_snipper

    if stop:
        return

    print(f"\nCapture {template_name}")
    print("Drag area yang ingin disimpan")

    time.sleep(0.5)

    current_snipper = ScreenSnipper(
        f"TargetObject/{template_name}.png"
    )

    current_snipper.start()

    current_snipper = None


if __name__ == "__main__":

    os.makedirs(
        "TargetObject",
        exist_ok=True
    )

    templates = {
        "1": "AskPosition",
        "2": "VoicePosition",
        "3": "CopyPosition",
        "4": "CompanyKnowledgePosition"
    }

    listener = keyboard.Listener(
        on_press=on_press
    )

    listener.start()

    while not stop:

        print("\n" + "=" * 50)
        print("TEMPLATE MANAGER")
        print("=" * 50)

        for idx, name in templates.items():

            path = f"TargetObject/{name}.png"

            status = (
                "✓"
                if os.path.exists(path)
                else "X"
            )

            print(
                f"{idx}. [{status}] {name}"
            )

        print()
        print("A. Update Semua")
        print("Q. Keluar")

        try:
            choice = input(
                "\nPilih menu: "
            ).strip().upper()

        except KeyboardInterrupt:
            stop = True
            break

        if choice == "Q":
            break

        if choice == "A":

            for template_name in templates.values():

                if stop:
                    break

                capture_template(
                    template_name
                )

            continue

        if choice in templates:

            capture_template(
                templates[choice]
            )

            continue

        print("Pilihan tidak valid")

    try:
        listener.stop()
    except:
        pass

    print("Program selesai")