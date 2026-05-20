from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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
prompt = driver.find_element(
    By.CLASS_NAME,
    "e33vkq_waveDot"
)

prompt.click()