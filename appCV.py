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

df = pd.read_excel('Data/data.xlsx', sheet_name='Sheet1')
df = df[['name', 'code']]

print(df.head())
exit()

AskPosition = cv2.imread(
    'TargetObject/AskPosition.png',
    cv2.IMREAD_GRAYSCALE
)

VoicePosition = cv2.imread(
    'TargetObject/VoicePosition.png',
    cv2.IMREAD_GRAYSCALE
)

CopyPosition = cv2.imread(
    'TargetObject/CopyPosition.png',
    cv2.IMREAD_GRAYSCALE
)

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

    return points


def findCenter(point, target):

    h, w = target.shape

    x = point[0] + int(w / 2)
    y = point[1] + int(h / 2)

    return x, y

# =========================
# MAIN
# =========================

skus = [AskPosition, VoicePosition, CopyPosition]

iterasi = 0

while True:

    for sku in skus:
        found = findObject(sku)

        if found:

            x, y = findCenter(found[0], sku)

            print(f"Found at: {x}, {y}")

            pyautogui.moveTo(
                x,
                y,
                duration=0.2
            )

        else:

            print("Object not found")

    iterasi += 1

    if iterasi >= 3:
        break

exit()
