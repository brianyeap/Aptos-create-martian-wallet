import requests
import threading


def get_devnet_apt(apt_address, apt_count):
    for i in range(apt_count):
        def temp_func():
            get_devnet_apt_url = f"https://faucet.devnet.aptoslabs.com/mint?address={apt_address}&amount=100000000"
            get_devnet_apt_response = requests.request("POST", get_devnet_apt_url)
            print(get_devnet_apt_response.json()[0])

        t = threading.Thread(target=temp_func)
        t.start()


get_devnet_apt('0x41153fa6da35961bba5417ff8c981390512e57f32312a8d96fa2c892a80ab0d6', 1)
