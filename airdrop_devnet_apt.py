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
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36']
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    try:
        get_devnet_apt_url = f"https://faucet.devnet.aptoslabs.com/mint?address={apt_address}&amount=100000000"
        get_devnet_apt_response = requests.post(get_devnet_apt_url)
        if (get_devnet_apt_response.status_code == 429):
            print(f"{bcolors.WARNING}CHANGE NETWORK, REQUEST REJECTED{bcolors.ENDC}")
        if (len(get_devnet_apt_response.json()[0]) == 64):
            print(
                f"[{i}/{len(json_files)}]{bcolors.OKGREEN}SUCCESS, deposited 1APT to {jfile['address']}{bcolors.ENDC}")
            print(jfile['seed_phrase'])
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

    return (1)


json_files = os.listdir("seeds")
random.shuffle(json_files)


def check_wallet_amount(address):
    try:
        r = requests.get(f"https://api-devnet.aptoscan.com/api?module=account&action=balance&address={address}")
        if (r.json()['status'] == '0'):
            print(f"{bcolors.WARNING}{address} has 0APT")
            return (0)
        print(f"{bcolors.OKGREEN}{address} has {r.json()['result']}{bcolors.ENDC}")
        return (int(r.json()['result']))
    except Exception as err:
        print(f"{bcolors.FAIL}ERROR IN CHECK WALLET {err} return:{r}{bcolors.ENDC}")
        return (0)


total_apt = 0
apt_not_detected = 0


def check_multi_wallet_address(addresses: list):
    global total_apt
    global apt_not_detected

    addr_str = ""
    for adr in addresses:
        addr_str += f"{adr},"
    addr_str = addr_str[:-2]
    r = requests.get(f"https://api-devnet.aptoscan.com/api?module=account&action=balancemulti&address={addr_str}")
    for result in r.json()['result']:
        if result["balance"] == None:
            result["balance"] = 0
            apt_not_detected += 1
        total_apt += int(result["balance"]) / 100000000
        print(f"{result['account']} has {result['balance']}APT")


import os

# if __name__ == '__main__':
#     for i, file in enumerate(json_files):
#         with open(f"seeds/{file}", "r") as f:
#             jfile = json.loads(f.read())
#             amount = random.randint(10, 16)
#             if (check_wallet_amount(f'{jfile["address"]}') < 9):
#                 print(f"{bcolors.OKGREEN}STARTING DEPOSIT PROCESS {file}{bcolors.ENDC}")
#                 status_code = get_devnet_apt(jfile["address"], amount)
#             else:
#                 os.system(f"rm filtered_seeds/remains/{file}")
#                 print(f"{bcolors.WARNING}SKIPPED DEPOSIT TO {file}{bcolors.ENDC}")
ls = []
if __name__ == '__main__':
    counter = 0
    for i, file in enumerate(json_files):
        try:
            with open(f"seeds/{file}", "r") as f:
                jfile = json.loads(f.read())
                ls.append(jfile['address'])
                counter += 1
            if counter == 20:
                counter = 0
                check_multi_wallet_address(ls)
                time.sleep(2)
                ls = []
        except Exception as err:
            print(f"ERROED {err}")
    print(f"AVERAGE APT IN WALLET: {total_apt / len(json_files)}APT")
    print(f"NOT DETECTED WALLETS: {apt_not_detected}")
    print(ls)
