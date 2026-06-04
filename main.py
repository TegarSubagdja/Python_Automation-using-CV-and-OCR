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

    if "chatgpt.com" in driver.current_url.lower():
        break

print(driver.title)
print(driver.current_url)

time.sleep(3)

# cari textarea prompt ChatGPT
prompt = driver.find_elements(
    By.ID,
    'prompt-textarea'
)

voiceChat = driver.find_elements(
    By.CSS_SELECTOR,
    'button[aria-label="Start Voice"]'
)

copy_btn = driver.find_elements(
    By.CSS_SELECTOR,
    'button[aria-label="Copy"]'
)

copy_btn[-1].click()
text = pyperclip.paste()
print(f"{text}")

exit()

for i in range(2):
    print(f"{prompt[-1].text}")
    # prompt[-1].send_keys("Halo ")
    # time.sleep(1)
    # Ctrl+A
    prompt[-1].send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    # Hapus teks yang terseleksi
    prompt[-1].send_keys(Keys.DELETE)
    time.sleep(1)

for i in range(2):
    voiceChat = driver.find_elements(
        By.CSS_SELECTOR,
        'button[aria-label="Start Voice"]'
    )

    if voiceChat:
        print(f"Tombol ditemukan")

    time.sleep(3)