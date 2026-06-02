import cv2
import sys
import numpy as np
from mss import MSS
from pynput import keyboard
import pyautogui

exit_flag = False

def findObject(target, threshold=0.8, screenshot_gray=None):
    if exit_flag:
        sys.exit(0)
        
    if screenshot_gray is None:
        screenshot_gray = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2GRAY)
    
    res = cv2.matchTemplate(screenshot_gray, target, cv2.TM_CCOEFF_NORMED)
    locations = np.where(res >= threshold)
    points = list(zip(*locations[::-1]))
    return max(points, key=lambda p: p[1]) if points else None

def findCenter(point, target):
    h, w = target.shape
    return point[0] + w // 2, point[1] + h // 2

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
    sct = MSS()
    monitor = sct.monitors[1]

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    targets = {
        'AskPosition': cv2.imread('TargetObject/AskPosition.png', cv2.IMREAD_GRAYSCALE),
        'VoicePosition': cv2.imread('TargetObject/VoicePosition.png', cv2.IMREAD_GRAYSCALE),
        'CopyPosition': cv2.imread('TargetObject/CopyPosition.png', cv2.IMREAD_GRAYSCALE)
    }

    screenshot_gray = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2GRAY)

    for target in targets:
        point = findObject(targets[target], screenshot_gray=screenshot_gray)
        if point:
            x, y = findCenter(point, targets[target])
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click()
        else:
            print(f"Error, position {target} not found...")
