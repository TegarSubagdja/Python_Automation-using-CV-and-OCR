from sys import executable
from time import time
from os import stat
import pyautogui
import cv2
import time
import pyperclip
import pyautogui
import numpy as np
import pandas as pd
from mss import mss

# =========================
# LOAD
# =========================

state = "running"

df = pd.read_excel(
    'Data/data.xlsx',
    dtype={
        'name': str,
        'code': str,
        'status': str,
        'description': str
    },
    sheet_name='Sheet1'
)

print(df.info())

AskPosition = {
    'type': 'AskPosition',
    'image': cv2.imread(
        'TargetObject/AskPosition.png',
        cv2.IMREAD_GRAYSCALE
    )
}

VoicePosition = {
    'type': 'VoicePosition',
    'image': cv2.imread(
        'TargetObject/VoicePosition.png',
        cv2.IMREAD_GRAYSCALE
    )
}

CopyPosition = {
    'type': 'CopyPosition',
    'image': cv2.imread(
        'TargetObject/CopyPosition.png',
        cv2.IMREAD_GRAYSCALE
    )
}

# =========================
# MSS INIT
# =========================

sct = mss()

monitor = sct.monitors[1]

# =========================
# FUNCTIONS
# =========================

def findObject(target, threshold=0.8):

    screenshot = np.array(sct.grab(monitor))

    screenshot_gray = cv2.cvtColor(
        screenshot,
        cv2.COLOR_BGRA2GRAY
    )

    res = cv2.matchTemplate(
        screenshot_gray,
        target,
        cv2.TM_CCOEFF_NORMED
    )

    locations = np.where(res >= threshold)

    points = list(zip(*locations[::-1])) 

    print(f"Point yang ditemukan adalah : {points}")

    if points:
        return max(points, key=lambda point: point[1])

    return None


def findCenter(point, target):

    h, w = target.shape

    x = point[0] + int(w / 2)
    y = point[1] + int(h / 2)

    return x, y

# =========================
# MAIN
# =========================

skus = [AskPosition, VoicePosition, CopyPosition]

for iddf, row in df.iterrows():

    print(f"Processing row {iddf}")

    for idsku, sku in enumerate(skus):

        if sku['type'] == 'VoicePosition':
            while True:
                voiceFound = findObject(VoicePosition['image'])
                if voiceFound:
                    x,y = voiceFound
                    pyautogui.moveTo(x, y-100, duration=0.2)
                    pyautogui.click()
                    pyautogui.press('end')
                    time.sleep(1)
                    break
                else:
                    time.sleep(1)
            continue

        found = findObject(sku['image'])

        if found:

            x, y = findCenter(found, sku['image'])

            print(f"Found at: {x}, {y}")

            pyautogui.moveTo(
                x,
                y,
                duration=0.2
            )

            if sku['type'] == 'AskPosition':
                pyautogui.click()
                pyautogui.sleep(0.2)
                pyautogui.write(row['name'], interval=0.01)
                pyautogui.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(3)
            
            if sku['type'] == 'CopyPosition':
                pyautogui.click()
                pyautogui.sleep(0.2)
                df.loc[iddf, 'description'] = pyperclip.paste()
                df.to_excel('Data/data.xlsx', index=False)

        else:

            print("Object not found")
            state = "crash"
            break

    if iddf >= 1 or state == "crash":
        print(f"status : {state}")
        break

exit()
