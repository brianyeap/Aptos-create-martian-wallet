import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from cryptography.fernet import Fernet
import threading

chrome_options = Options()
chrome_options.add_extension('./src/Martian-Aptos-Wallet.crx')

# Because I use M1 Mac it has error
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)

password = '12Testing34'

driver.maximize_window()
wait = WebDriverWait(driver, 5)
parent = driver.window_handles[0]

driver.get('https://www.google.com')

time.sleep(1000)
