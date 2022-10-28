import json
import time
import random
import os

# Own file import
from airdrop_devnet_apt import get_devnet_apt

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

password = '12Testing34'


def debug():
    print("paused to debug")
    time.sleep(10000)


def switch_tab(driver, parent):
    windows = driver.window_handles
    for w in windows:
        if w != parent:
            driver.switch_to.window(w)


def wait_popup(driver, parent):
    wait = WebDriverWait(driver, 10)
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


def import_petra_wallet(driver, seed_phrase):
    wait = WebDriverWait(driver, 10)

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
    for seed_text in seed_phrase:
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


def main_func(seed_phrase):
    # Because I use M1 Mac it has error
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)

    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    parent = driver.window_handles[0]

    if not import_petra_wallet(driver, seed_phrase):
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

    wait_popup(driver, parent)
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

    return 1


if __name__ == '__main__':
    seed_files_directory = 'seeds'
    seed_files = os.listdir(seed_files_directory)
    count = 0
    total_needed = 1000
    thread_times = 2


    def temp_func(seed_phrase):
        while True:
            start_time = time.time()
            if main_func(seed_phrase):
                print(f'Executed in: {round(time.time() - start_time)}S')
                break
            else:
                print('Retrying...')


    while count < total_needed:
        thread_list = []
        temp_count = 0

        if (total_needed - count) < thread_times:
            thread_times = total_needed - count
        while temp_count < thread_times:
            with open(f'{seed_files_directory}/{seed_files[count]}') as seed_file:
                data = json.load(seed_file)
                apt_address = data['address']
                apt_seed_array = data['seed_phrase']

            t = threading.Thread(target=temp_func, args=[apt_seed_array])
            thread_list.append(t)

            count += 1
            temp_count += 1
            print(f'Count: {count}/{total_needed}')

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    print(f'Finished: {count}/{total_needed}')
