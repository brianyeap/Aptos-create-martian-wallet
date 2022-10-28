import time
import random

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
chrome_options.add_extension('./src/Petra-Aptos-Wallet.crx')

# Because I use M1 Mac it has error
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)

password = '12Testing34'
temp_seed = 'repeat tortoise limb chest initial catalog worry velvet deputy bridge word manual'

driver.maximize_window()
wait = WebDriverWait(driver, 10)
parent = driver.window_handles[0]


def switch_tab():
    windows = driver.window_handles
    for w in windows:
        if w != parent:
            driver.switch_to.window(w)


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
            (By.XPATH, '/html/body/div[1]/div/div[3]/button[2]')))
    approve_btn.click()


def import_petra_wallet(seed_phrase):
    driver.get('chrome-extension://ejjladinnckdgjemekebdpeokbikhfci/index.html')

    import_wallet_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[2]/a[2]/button')))
    import_wallet_btn.click()

    import_mnemonic_btn_wallet_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/button[2]')))
    import_mnemonic_btn_wallet_btn.click()

    seed_phrase_count = 1
    second_seed_phrase_count = 1
    for seed_text in seed_phrase.split(' '):
        if seed_phrase_count <= 6:
            seed_text_input = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, f'/html/body/div[1]/div/div[2]/form/div/div/div/div[1]/div[{seed_phrase_count}]/input')))
            seed_phrase_count += 1
        else:
            seed_text_input = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH,
                     f'/html/body/div[1]/div/div[2]/form/div/div/div/div[2]/div[{second_seed_phrase_count}]/input')))
            second_seed_phrase_count += 1
        seed_text_input.send_keys(seed_text)

    continue_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[3]/button')))
    continue_btn.click()

    enter_password_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[1]/div[1]/div/input')))
    enter_password_input.send_keys(password)

    confirm_password_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[1]/div[2]/div/input')))
    confirm_password_input.send_keys(password)

    agree_terms_checkbox = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[2]/label/span[1]')))
    agree_terms_checkbox.click()

    continue_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[3]/button')))
    continue_btn.click()

    petra_wallet_home = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/p')))

    if petra_wallet_home.text == 'Home':
        petra_wallet_settings_btn = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/a')))
        petra_wallet_settings_btn.click()

        petra_wallet_network_btn = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[2]/a')))
        petra_wallet_network_btn.click()

        petra_wallet_network_devnet_btn = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[1]/label[3]')))

        while True:
            petra_wallet_network_devnet_btn.click()
            if 'data-checked' in petra_wallet_network_devnet_btn.get_attribute("innerHTML"):
                break

        return 1
    return 0


def main_func():
    if not import_petra_wallet(temp_seed):
        return 0

    driver.get('https://arcoprotocol.tech/')

    connect_wallet_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/button')))
    connect_wallet_btn.click()

    select_petra_wallet = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/div[3]')))
    select_petra_wallet.click()

    wait_popup()
    driver.switch_to.window(parent)

    # Deposit
    arco_deposit_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/main/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[5]/button[1]')))
    arco_deposit_btn.click()

    arco_deposit_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/input')))
    arco_deposit_input.send_keys(random.randint(25, 30))

    arco_deposit_supply_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/button')))
    # arco_deposit_supply_btn.click()

    # Exit modal
    driver.find_element(By.CSS_SELECTOR, ".icon").click()

    # Borrow
    arco_borrow_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/main/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[5]/button[2]')))
    arco_borrow_btn.click()

    arco_borrow_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/input')))
    arco_borrow_input.send_keys(random.randint(25, 30))

    arco_borrow_supply_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/button')))
    # arco_borrow_supply_btn.click()

    # Exit modal
    driver.find_element(By.CSS_SELECTOR, ".icon").click()

    # withdraw
    arco_withdraw_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/main/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td[5]/button[1]')))
    arco_withdraw_btn.click()

    arco_withdraw_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/input')))
    arco_withdraw_input.send_keys(random.randint(25, 30))

    arco_withdraw_supply_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/button')))
    # arco_withdraw_supply_btn.click()

    # Exit modal
    driver.find_element(By.CSS_SELECTOR, ".icon").click()

    # repay
    arco_repay_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/main/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td[5]/button[2]')))
    arco_repay_btn.click()

    arco_repay_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/input')))
    arco_repay_input.send_keys(random.randint(25, 30))

    arco_repay_supply_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[3]/button')))
    # arco_repay_supply_btn.click()

    # Exit modal
    driver.find_element(By.CSS_SELECTOR, ".icon").click()


if not main_func():
    print("Error")
