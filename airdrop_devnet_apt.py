import requests
import threading
import json


def get_devnet_apt(apt_address, apt_count):
    for i in range(apt_count):
        def temp_func():
            try:
                get_devnet_apt_url = f"https://faucet.devnet.aptoslabs.com/mint?address={apt_address}&amount=100000000"
                get_devnet_apt_response = requests.request("POST", get_devnet_apt_url)
                print(get_devnet_apt_response.json()[0])
            except json.decoder.JSONDecodeError:
                print(get_devnet_apt_response.text)

        t = threading.Thread(target=temp_func)
        t.start()


if __name__ == '__main__':
    get_devnet_apt('0xb1db7ab8f912cb374411037a3a4145f6ff954b90549d0c3942ec45491a480080', 2)
