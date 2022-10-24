from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
import threading

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_extension('./src/Martian-Aptos-Wallet.crx')

# Because I use M1 Mac it has error
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)

driver.maximize_window()
wait = WebDriverWait(driver, 5)
parent = driver.window_handles[0]


def wait_popup():
    while True:
        if len(driver.window_handles) > 1:
            break

    windows = driver.window_handles
    for w in windows:
        if w != parent:
            driver.switch_to.window(w)

    approve_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[2]/div/div[5]/button')))

    approve_btn.click()


input('Ready for auto approve (Press Enter)? ')

t = threading.Thread(target=wait_popup)
t.start()

driver.get('https://www.topaz.so/')
