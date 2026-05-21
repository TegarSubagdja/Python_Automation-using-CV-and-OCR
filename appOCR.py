from re import RegexFlag
import pyautogui
import pytesseract
import cv2
import numpy as np
import json
import os
import time

def loadRoiConfig():

    if not os.path.exists('config_ocr.json'):
        print("config_ocr.json tidak ditemukan!")
        return None

    with open('config_ocr.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def scanTextInRoi(teks_target):

    roi = loadRoiConfig()

    if not roi:
        return

    print(
        f"Mengambil screenshot ROI: "
        f"x={roi['x']} "
        f"y={roi['y']} "
        f"w={roi['width']} "
        f"h={roi['height']}"
    )

    start_time = time.time()

    screenshot = pyautogui.screenshot(
        region=(
            roi['x'],
            roi['y'],
            roi['width'],
            roi['height']
        )
    )

    img = cv2.cvtColor(
        np.array(screenshot),
        cv2.COLOR_RGB2BGR
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    data = pytesseract.image_to_data(
        thresh,
        output_type=pytesseract.Output.DICT,
        config='--oem 3 --psm 6'
    )

    ditemukan = False

    for i in range(len(data['text'])):

        text = data['text'][i].strip()

        if text == "":
            continue

        conf = int(float(data['conf'][i]))

        print(f"Terdeteksi: {text} ({conf})")

        if teks_target.lower() in text.lower():

            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            center_x = int((x + w / 2) / 2)
            center_y = int((y + h / 2) / 2)

            screen_x = roi['x'] + center_x
            screen_y = roi['y'] + center_y

            end_time = time.time()

            print(f"\n[SUKSES] '{text}' ditemukan")
            print(f"Confidence: {conf}")
            print(f"Waktu: {end_time - start_time:.2f} detik")
            print(f"Koordinat: X={screen_x} Y={screen_y}")

            return True

    if not ditemukan:

        end_time = time.time()

        print(f"\nTeks '{teks_target}' tidak ditemukan")
        print(f"Waktu proses: {end_time - start_time:.2f} detik")

        return False

if __name__ == "__main__":

    scanTextInRoi("sample")
    