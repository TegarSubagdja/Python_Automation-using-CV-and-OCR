import re
import pyautogui
import pytesseract
import cv2
import numpy as np
import json
import os
import time

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def loadRoiConfig():

    if not os.path.exists("config_ocr.json"):
        print("config_ocr.json tidak ditemukan!")
        return None

    with open("config_ocr.json", "r", encoding="utf-8") as f:
        return json.load(f)


def scanTextInRoi(teks_target):

    roi = loadRoiConfig()

    if not roi:
        return False

    print(
        f"Mengambil screenshot ROI: "
        f"x={roi['x']} "
        f"y={roi['y']} "
        f"w={roi['width']} "
        f"h={roi['height']}"
    )

    start_time = time.time()

    # SCREENSHOT

    screenshot = pyautogui.screenshot(
        region=(roi["x"], roi["y"], roi["width"], roi["height"])
    )

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # PREPROCESS IMAGE

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # resize agar OCR lebih akurat
    scale = 2

    gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # OCR

    data = pytesseract.image_to_data(
        thresh, output_type=pytesseract.Output.DICT, config="--oem 3 --psm 11"
    )

    # SIMPAN SEMUA KATA

    words = []

    for i in range(len(data["text"])):

        text = data["text"][i].strip()

        if text == "":
            continue

        try:
            conf = float(data["conf"][i])
        except:
            conf = -1

        # skip confidence jelek
        if conf < 50:
            continue

        clean_text = re.sub(r"[^a-zA-Z0-9]", "", text).lower()

        if clean_text == "":
            continue

        words.append(
            {
                "text": clean_text,
                "x": data["left"][i],
                "y": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i],
            }
        )

    # TARGET

    target_words = [re.sub(r"[^a-zA-Z0-9]", "", w).lower() for w in teks_target.split()]

    # CARI KALIMAT

    found = False

    for i in range(len(words) - len(target_words) + 1):

        match = True

        for j in range(len(target_words)):

            if words[i + j]["text"] != target_words[j]:
                match = False
                break

        if match:

            found = True

            # AMBIL AREA GABUNGAN

            first = words[i]
            last = words[i + len(target_words) - 1]

            x1 = first["x"]
            y1 = first["y"]

            x2 = last["x"] + last["w"]

            y2 = max(word["y"] + word["h"] for word in words[i : i + len(target_words)])

            # CENTER POSITION

            center_x = int(((x1 + x2) / 2) / scale)

            center_y = int(((y1 + y2) / 2) / scale)

            # convert ke layar asli
            screen_x = roi["x"] + center_x
            screen_y = roi["y"] + center_y

            # MOVE MOUSE

            pyautogui.moveTo(screen_x, screen_y, duration=0.2)

            end_time = time.time()

            print(f"[SUKSES] " f"'{teks_target}' ditemukan")

            print(f"Koordinat: " f"X={screen_x} " f"Y={screen_y}")

            print(f"Waktu proses: " f"{end_time - start_time:.2f} detik")

            return [screen_x, screen_y]

    # TIDAK DITEMUKAN

    if not found:

        end_time = time.time()

        print(f"Teks '{teks_target}' " f"tidak ditemukan")

        print(f"Waktu proses: " f"{end_time - start_time:.2f} detik")

        return False


# MAIN

if __name__ == "__main__":

    scanTextInRoi("Ready when")
