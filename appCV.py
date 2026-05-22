import os
import sys
import cv2
import gspread
import pyautogui
import pyperclip
import numpy as np
from os import stat
from mss import MSS
import pandas as pd
from pynput import keyboard
from time import time, sleep
from dotenv import load_dotenv
from appOCR import scanTextInRoi

load_dotenv()

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
    while not exit_flag:
        found = findObject(targets['VoicePosition'])
        if found:
            pyautogui.moveTo(found[0], found[1] - 50, duration=0.2)
            pyautogui.click()
            pyautogui.press('end')
            sleep(1)
            break
        sleep(1)

def handleAsk(name):
    if exit_flag:
        sys.exit(0)
    pyautogui.click()
    sleep(0.2)
    pyautogui.write(name, interval=0.01)
    sleep(0.2)
    pyautogui.press('enter')
    sleep(3)

def handleCopy(idx):
    if exit_flag:
        sys.exit(0)
    pyautogui.click()
    sleep(0.2)
    df.loc[idx, 'description'] = pyperclip.paste().replace('\r\n', '\n')
    df.loc[idx, 'status'] = "Success"
    df.to_excel('Data/data.xlsx', index=False)

def getDataSpreadsheet():
    try:
        gc = gspread.service_account(filename='Credentials/credentials-spread.json')
        sh = gc.open_by_key(os.getenv("spread_sheet_key"))
        worksheet = sh.sheet1
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error getting data from spreadsheet: {e}")
        return pd.DataFrame()

def updateDataSpreadsheet(df):
   try:
        gc = gspread.service_account(filename='Credentials/credentials-spread.json')
        sh = gc.open_by_key(os.getenv("spread_sheet_key"))
        worksheet = sh.sheet1
        header = df.columns.tolist()
        values = df.values.tolist()
        data_to_upload = [header] + values
        worksheet.update(range_name='A1', values=data_to_upload) 
        return "success"
   except Exception as e:
        print(f"Error updating data to spreadsheet: {e}")
        return "error"

def on_press(key):
    global exit_flag
    try:
        if key == keyboard.Key.esc:
            print("\nESC pressed. Exiting...")
            exit_flag = True
            sys.exit(0)
    except AttributeError:
        pass

state = "running"
exit_flag = False

df = pd.read_excel(
    'Data/data.xlsx',
    dtype={'name': str, 'code': str, 'status': str, 'description': str},
    sheet_name='Sheet1'
)

sct = MSS()
monitor = sct.monitors[1]

targets = {
    'AskPosition': cv2.imread('TargetObject/AskPosition.png', cv2.IMREAD_GRAYSCALE),
    'VoicePosition': cv2.imread('TargetObject/VoicePosition.png', cv2.IMREAD_GRAYSCALE),
    'CopyPosition': cv2.imread('TargetObject/CopyPosition.png', cv2.IMREAD_GRAYSCALE)
}

listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    for idx, row in df.iterrows():
        if exit_flag:
            break
        
        if row['status'] == "Success":
            continue
        
        print(f"Processing row {idx}")
        
        for target_type in ['AskPosition', 'VoicePosition', 'CopyPosition']:
            if exit_flag:
                break
            
            if target_type == 'VoicePosition':
                handleVoice()
                continue

            found = findObject(targets[target_type])
            if not found:
                print(f"Error, Object {target_type} tidak ditemukan")
                state = "crash"
                break
            
            x, y = findCenter(found, targets[target_type])
            print(f"Found at: {x}, {y}")
            pyautogui.moveTo(x, y, duration=0.2)
            
            if target_type == 'AskPosition':
                handleAsk(row['name'])
            elif target_type == 'CopyPosition':
                codeExist = scanTextInRoi(row['code'])
                if not codeExist:
                    print(f"Error, Code {row['code']} tidak ditemukan")
                    state = "crash"
                    exit_flag = True
                handleCopy(idx)
        
        if state == "crash":
            print(f"Status: {state}")
            break

except KeyboardInterrupt:
    print("\nProgram interrupted")
finally:
    listener.stop()
    sys.exit(0)