import re
import time
import pyperclip
import pandas as pd
from pynput import keyboard
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def findTab(driver, url):
    if driver:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)

            if url in driver.current_url.lower():
                break
    else:
        print("Driver tidak ditemukan!")
        return None

    if driver:
        print(driver.title)
        print(driver.current_url)
        return driver
    return None

def findCompanyKnowledgeButton(driver):
    if driver:
        try:
            company_profile = driver.find_element(
                By.CSS_SELECTOR,
                'button[aria-label="Company Knowledge, click to remove"]'
            )
        except Exception as e:
            print(f"Company Knowledge Kemungkinan Tidak ditemukan")
            return None

        if company_profile:
            print("Company Knowledge ditemukan!")
            return company_profile
        else:
            print("Company Profile tidak ditemukan!")
            return None
    else:
        print("Driver tidak ditemukan!")
        return None
    return None

def findTextArea(driver):
    if driver:
        try:
            prompt = driver.find_element(
                By.ID,
                'prompt-textarea'
            )
        except Exception as e:
            print(f"Text Area Kemungkinan Tidak ditemukan")
            return None

        if prompt:
            print("Text Area ditemukan!")
            return prompt
    else:
        print("Driver tidak ditemukan!")
        return None
    return None

def CopyResponse(driver):
    if driver:
        try:
            copy_btn = driver.find_elements(
                By.CSS_SELECTOR,
                'button[aria-label="Copy response"]'
            )
        except Exception as e:
            print(f"Copy button Kemungkinan Tidak ditemukan")
            return None

        if len(copy_btn) > 0:
            driver.execute_script("arguments[0].click();", copy_btn[-1])
            time.sleep(1)
            text = pyperclip.paste()
            print("Response berhasil dicopy!")
            return text
        else:
            print("Copy button tidak ditemukan!")
            return None
    else:
        print("Driver tidak ditemukan!")
        return None
    return None

def findVoiceChatButton(driver):
    if driver:
        try:
            voiceChat = driver.find_element(
                By.CSS_SELECTOR,
                'button[aria-label="Start Voice"]'
            )
        except Exception as e:
            return None

        if voiceChat:
            print("Voice Chat ditemukan!")
            return voiceChat
        else:
            print("Voice Chat tidak ditemukan!")
            return None
    else:
        print("Driver tidak ditemukan!")
        return None

def WaitVoiceChat(driver, timeout):
    timeout = timeout * 60
    start_time = time.time()
    print(f"Waiting for Voice Chat for {timeout} seconds...")
    while time.time() - start_time < timeout:
        voice_chat = findVoiceChatButton(driver)
        if voice_chat:
            voice_chat.send_keys(Keys.END)
            time.sleep(1)
            return True
        else:
            time.sleep(1)
    return False

def makeNewChat(driver):
    if driver:
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.CONTROL + Keys.SHIFT + "o")
            print("New Chat berhasil dibuat!")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"New Chat Gagal Dibuat")
            return False
    else:
        print("Driver tidak ditemukan!")
        return False

def refreshChat(driver):
    if driver:
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.CONTROL + "r")
            print("Refresh berhasil!")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Refresh Gagal Dibuat")
            return False
    else:
        print("Driver tidak ditemukan!")
        return False

def saveData(data, index, code, textResponse):
    textOrigin = textResponse.replace("\r\n", "\n")
    textCopied = re.split(r"[ ,:/\n()]+|\[.*?\]", textOrigin)
    textCopied = [x for x in textCopied if x]
    if code in textCopied:
        print("Code found in text")
        data.loc[index, "description"] = textOrigin
        data.loc[index, "status"] = "Success"
        data.to_excel("Data/data2.xlsx", index=False, sheet_name="Sheet2")
        return True
    else:
        print("Error, Code not found in text")
        data.loc[index, "description"] = "Code Not Found in Text"
        data.loc[index, "status"] = "Failed"
        data.to_excel("Data/data2.xlsx", index=False, sheet_name="Sheet2")
        return False

def addCompanyKnowledge(driver):
    if driver:
        try:
            text_area = findTextArea(driver)
            if text_area:
                text_area.send_keys("/company")
                text_area.send_keys(Keys.ENTER)
                print("Company Knowledge berhasil ditambahkan!")
                time.sleep(2)
                return True
            else:
                print("Error, textarea tidak ditemukan untuk menambahkan company knowledge!")
                return False
        except Exception as e:
            print(f"Error, add company knowledge gagal! {e}")
            return False
    else:
        print("Driver tidak ditemukan!")
        return False

def isLimit(driver):
    if driver:
        try:
            keywords = [
                "reach the maximum",
                "you've reached the maximum",
                "starting a new chat",
            ]
            page = driver.find_element(By.TAG_NAME, "body").text.lower()[-1000:]
            
            for keyword in keywords:
                if keyword in page:
                    print("Limit reached!")
                    return True
                else:
                    print("Limit not reached!")
                    return False
        except Exception as e:
            print(f"Error, check limit gagal! {e}")
            return False
    else:
        print("Driver tidak ditemukan!")
        return False

def on_press(key):
    try:
        if key.char == "q":
            print("Q pressed. Exiting...")
            exit()
    except AttributeError:
        pass
    except Exception as e:
        print(e)

options = Options()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)

driver = findTab(driver, "chatgpt.com")

page = driver.find_element(By.TAG_NAME, "body").text.lower()
page = page[-1000:]
print(page)
exit()

data = pd.read_excel("Data/data2.xlsx", sheet_name="Sheet2", dtype=str)

listener = keyboard.Listener(on_press=on_press)
listener.start()

for index, row in data.iterrows():
    time.sleep(1)
    company_knowledge = True
    if company_knowledge:
        prompt = findTextArea(driver)
        voice_chat = findVoiceChatButton(driver)
        if prompt and voice_chat:
            prompt.send_keys(row["name"])
            prompt.send_keys(Keys.ENTER)
            time.sleep(1)
            if WaitVoiceChat(driver, 2):
                copy_response = CopyResponse(driver)
                if copy_response:
                    saveData = saveData(data=data, index=index, code=row["code"], textResponse=copy_response)
                    if saveData:
                        print("Data berhasil disimpan!")
                    else:
                        print("Data gagal disimpan!")
                else:
                    print("Error, copy response gagal!")
            else:
                reach_limit = isLimit(driver)
                if reach_limit:
                    new_chat = makeNewChat(driver)
                    if not new_chat:
                        print("Keluar program karena new chat gagal dibuat!")
                        exit()
                else:
                    refresh = refreshChat(driver)
                    if not refresh:
                        print("Keluar program karena refresh gagal!")
                        exit()
        else:
            print("Error, prompt atau voice chat tidak ditemukan!")
            refresh = refreshChat(driver)
            if not refresh:
                print("Keluar program karena refresh gagal!")
                exit()
            continue
    else:
        print("Error, company knowledge tidak ditemukan!")
        add_company_knowledge = addCompanyKnowledge(driver)
        if not add_company_knowledge:
            print("Keluar program karena add company knowledge gagal!")
            exit()
        continue
        
listener.stop()

# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeAutomation\User Data" --profile-directory="Profile 1"
