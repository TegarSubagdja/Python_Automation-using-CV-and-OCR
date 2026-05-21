from time import time, sleep
from os import stat
import pyautogui
import cv2
import pyperclip
import numpy as np
import pandas as pd
from mss import mss

state = "running"
df = pd.read_excel(
    'Data/data.xlsx',
    dtype={'name': str, 'code': str, 'status': str, 'description': str},
    sheet_name='Sheet1'
)

sct = mss()
monitor = sct.monitors[1]

targets = {
    'AskPosition': cv2.imread('TargetObject/AskPosition.png', cv2.IMREAD_GRAYSCALE),
    'VoicePosition': cv2.imread('TargetObject/VoicePosition.png', cv2.IMREAD_GRAYSCALE),
    'CopyPosition': cv2.imread('TargetObject/CopyPosition.png', cv2.IMREAD_GRAYSCALE)
}

def findObject(target, threshold=0.7):
    screenshot_gray = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2GRAY)
    res = cv2.matchTemplate(screenshot_gray, target, cv2.TM_CCOEFF_NORMED)
    locations = np.where(res >= threshold)
    points = list(zip(*locations[::-1]))
    return max(points, key=lambda p: p[1]) if points else None

def findCenter(point, target):
    h, w = target.shape
    return point[0] + w // 2, point[1] + h // 2

def handleVoice():
    print(f"Menunggu voice chat selesai")
    while True:
        found = findObject(targets['VoicePosition'])
        if found:
            print(f"Found voice chat at: {found[0]}, {found[1]}")
            pyautogui.moveTo(found[0], found[1] - 30, duration=0.1)
            pyautogui.click()
            pyautogui.press('end')
            break
        sleep(1)

def handleAsk(name):
    pyautogui.click()
    sleep(0.1)
    pyautogui.write(name, interval=0.01)
    sleep(0.1)
    pyautogui.press('enter')
    sleep(1)

def handleCopy(idx):
    pyautogui.click()
    sleep(0.2)
    df.loc[idx, 'description'] = pyperclip.paste().replace('\r\n', '\n')
    df.loc[idx, 'status'] = "Success"
    df.to_excel('Data/data.xlsx', index=False)

for idx, row in df.iterrows():
    if row['status'] == "Success":
        continue
    
    print(f"Processing row {idx}")
    
    for target_type in ['AskPosition', 'VoicePosition', 'CopyPosition']:
        if target_type == 'VoicePosition':
            handleVoice()
            continue
        
        found = findObject(targets[target_type])
        if not found:
            print("Object not found")
            state = "crash"
            break
        
        x, y = findCenter(found, targets[target_type])
        print(f"Found at: {x}, {y}")
        pyautogui.moveTo(x, y, duration=0.2)
        
        if target_type == 'AskPosition':
            handleAsk(row['name'])
        elif target_type == 'CopyPosition':
            handleCopy(idx)
    
    if state == "crash":
        print(f"Status: {state}")
        break

exit()