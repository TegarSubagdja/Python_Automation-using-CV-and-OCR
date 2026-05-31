import pyautogui
import os
import re
import sys
import cv2
import gspread
import pyautogui
import pyperclip
import numpy as np
from mss import MSS
import pandas as pd
from pynput import keyboard
from time import time, sleep
from dotenv import load_dotenv
from appOCR import scanTextInRoi

load_dotenv()

# Initialize variables
state = "running"
exit_flag = False
waitingErrorTime = 3

def findObject(target, threshold=0.8):
    if exit_flag:
        sys.exit(0)
    screenshot_gray = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2GRAY)
    res = cv2.matchTemplate(screenshot_gray, target, cv2.TM_CCOEFF_NORMED)
    locations = np.where(res >= threshold)
    points = list(zip(*locations[::-1]))
    return max(points, key=lambda p: p[1]) if points else None

def findCenter(point, target):
    h, w = target.shape
    return point[0] + w // 2, point[1] + h // 2

def handleVoice():
    if exit_flag:
        sys.exit(0)
    waitingTime = 0
    while not exit_flag:
        found = findObject(targets['VoicePosition'])
        if found:
            pyautogui.moveTo(found[0], found[1] - 50, duration=0.2)
            pyautogui.click()
            pyautogui.press('end')
            sleep(1)
            break
        sleep(1)
        waitingTime += 1
        if waitingTime > 120:
            print("Error, Voice button not found")
            state = "crash"
            return "crash"
    return "success"

def handleAsk(name):
    if exit_flag:
        sys.exit(0)
    pyautogui.click()
    sleep(0.2)
    pyautogui.write(name, interval=0.01)
    sleep(0.2)
    pyautogui.press('enter')
    sleep(3)

def handleCopy(idx, code):
    if exit_flag:
        sys.exit(0)
    pyautogui.click()
    sleep(0.2)
    textOrigin = pyperclip.paste().replace('\r\n', '\n')
    textCopied = re.split(r"[ ,:/\n()]+|\[.*?\]", textOrigin)
    textCopied = [x for x in textCopied if x]
    if code in textCopied:
        print("Code found in text")
        df.loc[idx, 'description'] = textOrigin
        df.loc[idx, 'status'] = "Success"
        df.to_excel('Data/data.xlsx', index=False)
        waitingErrorTime = 1
    else:
        print("Error, Code not found in text")
        df.loc[idx, 'description'] = "Code Not Found in Text"
        df.loc[idx, 'status'] = "Failed"
        df.to_excel('Data/data.xlsx', index=False)

def checkCondition(targets):
    if exit_flag:
        sys.exit(0)
    
    for target in targets:
        if findObject(target):
            return target
    return None


def on_press(key):
    global exit_flag
    try:
        if key == keyboard.Key.esc:
            print("\nESC pressed. Exiting...")
            exit_flag = True
            sys.exit(0)
    except AttributeError:
        pass

if __name__ == "__main__":
    
    # Initialize screen shotter
    sct = MSS()
    monitor = sct.monitors[1]

    # Initialize data
    df = pd.read_excel(
        'Data/data.xlsx',
        dtype={'name': str, 'code': str, 'status': str, 'description': str},
        sheet_name='Sheet1'
    )

    # Initialize targets
    targets = {
        'AskPosition': cv2.imread('TargetObject/AskPosition.png', cv2.IMREAD_GRAYSCALE),
        'VoicePosition': cv2.imread('TargetObject/VoicePosition.png', cv2.IMREAD_GRAYSCALE),
        'CopyPosition': cv2.imread('TargetObject/CopyPosition.png', cv2.IMREAD_GRAYSCALE),
        'KnowledgePosition': cv2.imread('TargetObject/KnowledgePosition.png', cv2.IMREAD_GRAYSCALE)
    }
    
    # Initialize keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Main loop
    try:
        for idx, row in df.iterrows():
            if exit_flag:
                break

            if row['status'] == "Success":
                continue

            # Check condition to prompt
            condition = checkCondition(targets=[targets['AskPosition'], targets['VoicePosition']])

            if condition:
                break
    except:
        print("Error program keluar")
            

