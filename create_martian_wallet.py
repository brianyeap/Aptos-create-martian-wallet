import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import threading
import json
import random

# Because I use M1 Mac it has error
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

glob_num = 0
password = '12Testing34'


def debug():
    print("paused to debug")
    time.sleep(10000)

def switch_tab(driver):
    windows = driver.window_handles
    parent = driver.window_handles[0]
    for w in windows:
        if w != parent:
            driver.switch_to.window(w)

def initialise_wallet(driver, wait):
    address = ""
    seed_phrase = []

    time.sleep(3)
    switch_tab(driver)
    driver.get('chrome-extension://ejjladinnckdgjemekebdpeokbikhfci/index.html')


    btn_create = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[2]/a[1]/button')))
    btn_create.click()


    wallet_password_field = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[1]/div[1]/div/input')))
    wallet_password_field.send_keys(password)


    wallet_password_field = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[1]/div[2]/div/input')))
    wallet_password_field.send_keys(password)


    tick = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[2]/label/span[1]')))
    tick.click()


    btn_cont = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div/div/button')))
    btn_cont.click()


    btn_reveal_seed = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[2]/div/div[3]/div')))
    btn_reveal_seed.click()
    
    seeds = wait.until(
            ec.visibility_of_all_elements_located(
                (By.CLASS_NAME, 'chakra-input__group')))

    for seed_box in seeds:
        seed = seed_box.find_element(By.TAG_NAME, "input")
        seed_phrase.append(seed.get_attribute('value'))
    
    btn_cont = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div/div/button')))
    btn_cont.click()

    i = 1
    while i < 7:
        inpt = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, f'/html/body/div[1]/div/div[2]/form/div/div[2]/div/div[1]/div[{i}]/input')))
        inpt.send_keys(seed_phrase[i - 1])
        i += 1

    i = 1
    while i < 7:
        inpt = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, f'/html/body/div[1]/div/div[2]/form/div/div[2]/div/div[2]/div[{i}]/input')))
        inpt.send_keys(seed_phrase[5 + i])
        i += 1

    btn_cont = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div/div/button')))
    btn_cont.click()

    btn_done = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[4]/div/div[2]/button[2]')))
    btn_done.click()

    btn_stngs = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]')))
    btn_stngs.click()

    btn_expl = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[7]/a/div')))
    btn_expl.click()
    driver.switch_to.window(driver.window_handles[-1])
    url = driver.current_url.split('/')
    print(url[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


    return ({"address":address, "seed_phrase":seed_phrase})


def setup_wallet(amount):
    global glob_num

    try:
        chrome_options = Options()
        chrome_options.add_extension('./src/Petra-Aptos-Wallet.crx')
        driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)
        initialise_wallet(driver, wait)
        while (amount > 0):
            amount -= 1
            btn_swt = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[8]/a/div/div/div[1]')))
            btn_swt.click()


            btn_add = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/button')))
            btn_add.click()

            btn_new = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div[2]/div/button[1]')))
            btn_new.click()


            btn_reveal_seed = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/form/div[1]/div[1]/div/div[2]/div/div[3]/div')))
            btn_reveal_seed.click()

            seed_phrase = []
            i = 1
            while i < 7:
                inpt = wait.until(
                    ec.visibility_of_element_located(
                        (By.XPATH, f'/html/body/div[1]/div/div[2]/form/div[1]/div[1]/div/div[2]/div/div[1]/div[{i}]/input')))
                seed_phrase.append(inpt.get_attribute('value'))
                i += 1

            i = 1
            while i < 7:
                inpt = wait.until(
                    ec.visibility_of_element_located(
                        (By.XPATH, f'/html/body/div[1]/div/div[2]/form/div[1]/div[1]/div/div[2]/div/div[2]/div[{i}]/input')))
                seed_phrase.append(inpt.get_attribute('value'))
                i += 1


            btn_cont = wait.until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[2]/form/div[1]/div[2]/button')))
            btn_cont.click()

            btn_done = wait.until(
                        ec.visibility_of_element_located(
                            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div/div[2]/button[2]')))
            btn_done.click()


            btn_stngs = wait.until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]')))
            btn_stngs.click()


            btn_expl = wait.until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[7]/a/div')))
            btn_expl.click()


            driver.switch_to.window(driver.window_handles[-1])
            url = driver.current_url.split('/')
            address = url[-1]
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            json_text = json.dumps({"address":address, "seed_phrase":seed_phrase})
            with open(f"seeds/petra-{random.randint(1000000, 9999999)}.json", "w+") as outfile:
                outfile.write(json_text)
            glob_num += 1
            print(f'#{glob_num} created')
    except Exception as err:
        print(err)


amount_needed = 100
threads = 2
def begin(amount_needed, threads):
    count = 0
    thread_list = []
    while count < threads:
        t = threading.Thread(target=setup_wallet, args=[int(amount_needed/threads)])
        thread_list.append(t)
        count += 1
        print(f'created thread: {count}/{threads}')

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    print("JOB COMPLETE")

begin(amount_needed, threads)