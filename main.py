from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip

options = Options()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)

# cari tab ChatGPT yang sudah terbuka
for handle in driver.window_handles:
    driver.switch_to.window(handle)

    if "https://chatgpt.com/" in driver.current_url.lower():
        break

print(driver.title)
print(driver.current_url)

time.sleep(3)

# cari textarea prompt ChatGPT
prompt = driver.find_element(
    By.ID,
    'prompt-textarea'
)

print(f"Text pada prompt saat ini adalah \"{prompt.text}\"")
time.sleep(1)

copy_btn = driver.find_elements(
    By.CSS_SELECTOR,
    'button[aria-label="Copy response"]'
)

if len(copy_btn) > 0:
    # copy_btn[-1].click()
    driver.execute_script("arguments[0].click();", copy_btn[-1])
    time.sleep(1)
    text = pyperclip.paste()
    print(f"{text}")

for i in range(2):
    prompt.send_keys("Halo ")
    print(f"Text pada prompt saat ini adalah \"{prompt.text}\"")
    time.sleep(1)
    # Ctrl+A
    prompt.send_keys(Keys.CONTROL, "a")
    # Hapus teks yang terseleksi
    prompt.send_keys(Keys.DELETE)

for i in range(2):
    voiceChat = driver.find_elements(
        By.CSS_SELECTOR,
        'button[aria-label="Start Voice"]'
    )

    if voiceChat:
        print(f"Button Voice Chat ditemukan!")

    time.sleep(1)