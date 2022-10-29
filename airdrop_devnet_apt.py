import requests
import requests.auth
import threading
import json
import random
import os
import requests
import time

from urllib.request import urlopen
urlopen('https://www.howsmyssl.com/a/check').read()
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

with open("./proxies", "r") as f:
    proxies = f.read().split('\n')

def temp_func(apt_address):
            global proxies
            rand_proxy = random.choice(proxies)
            try:
                get_devnet_apt_url = f"https://faucet.devnet.aptoslabs.com/mint?address={apt_address}&amount=100000000"
                get_devnet_apt_response = requests.post(get_devnet_apt_url)
                if (get_devnet_apt_response.status_code == 429):
                    print(f"{bcolors.WARNING}CHANGE NETWORK, REQUEST REJECTED{bcolors.ENDC}")
                if (len(get_devnet_apt_response.json()[0]) == 64):
                    print(f"[{i}/{len(json_files)}]{bcolors.OKGREEN}SUCCESS, deposited 1APT to {jfile['address']}{bcolors.ENDC}")
            except json.decoder.JSONDecodeError:
                print(get_devnet_apt_response.text)
                return (0)
            except Exception as err:
                print(f"{bcolors.FAIL}ERROR OCCURED: {err}{bcolors.ENDC}")
                return (0)

def get_devnet_apt(apt_address, apt_count):
    
    threads = []
    for i in range(apt_count):
        

        t = threading.Thread(target=temp_func, args=[apt_address])
        threads.append(t)
        t.start()
        t.join()

    return (1)


json_files = os.listdir("seeds/")
random.shuffle(json_files)

def check_wallet_amount(address):
    try:
        r = requests.get(f"https://api-devnet.aptoscan.com/api?module=account&action=balance&address={address}")
        if (r.json()['status'] == '0'):
            return (0)
        return(int(r.json()['result']))
    except Exception as err:
        print(f"{bcolors.FAIL}ERROR IN CHECK WALLET {err} return:{r}{bcolors.ENDC}")
        return (0)

if __name__ == '__main__':
    for i, file in enumerate(json_files):
        with open(f"seeds/{file}", "r") as f:
            jfile = json.loads(f.read())
            amount = random.randint(10, 16)
            if (check_wallet_amount(f'{jfile["address"]}') < 9):
                print(f"{bcolors.OKGREEN}STARTING DEPOSIT PROCESS {file}{bcolors.ENDC}")
                status_code = get_devnet_apt(jfile["address"], amount)
            else:
                print(f"{bcolors.WARNING}SKIPPED DEPOSIT TO {file}{bcolors.ENDC}")

                