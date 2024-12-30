import requests
from bitcoin import *
import random
import time

# Banner
banner = """
Bitcoin Wallet Generator and Balance Checker
Author: Tyler777

*This program generates random private keys in the hopes of finding a loaded wallet to extract bitcoins from it only logs wallets with bitcoin greater than 0 and stores them* 
**WARNING STEALING BTC IS ILLEGAL THIS IS A PROOF OF CONECEPT AND THE CREATOR HOLDS NO RESPONSIBILITY FOR MISSUSE OF THIS CODE**
"""
print(banner)

# Function to generate a random private key
def generate_private_key():
    return random.randint(1, 2**256)

# Function to get the Bitcoin address from a private key
def get_address_from_private_key(private_key):
    public_key = encode_pubkey(privtopub(private_key), 'hex_compressed')
    address = pubtoaddr(public_key)
    return address

# Function to check the balance on a Bitcoin address
def check_balance(address, proxies=None, proxy_list=None):
    if proxy_list:
        for proxy in proxy_list:
            try:
                url = f"https://www.blockchain.com/explorer/addresses/btc/{address}"
                response = requests.get(url, proxies=proxy)
                if "Oops! We couldn't find what you are looking for." in response.text:
                    return 0
                else:
                    balance = response.text.split('balance">')[1].split(' BTC</span>')[0]
                    return float(balance)
            except:
                proxy_list.remove(proxy)
    else:
        url = f"https://www.blockchain.com/explorer/addresses/btc/{address}"
        try:
            response = requests.get(url, proxies=proxies)
            if "Oops! We couldn't find what you are looking for." in response.text:
                return 0
            else:
                balance = response.text.split('balance">')[1].split(' BTC</span>')[0]
                return float(balance)
        except:
            return 0

# Function to log the private key, address, and balance
def log_data(private_key, address, balance, filename):
    if balance > 0:
        with open(filename, 'a') as file:
            file.write(f"{private_key}:{address}:{balance}\n")

# Interactive options
num_keys = int(input("Enter the number of keys to generate: "))
filename = input("Enter the name of the text file to log the data: ")
use_proxies = input("Do you want to use proxies? (y/n): ").lower() == 'y'
use_tor = input("Do you want to use Tor for privacy? (y/n): ").lower() == 'y'
delay_time = int(input("Enter the delay time in seconds between requests: "))

# Proxy list
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

proxy_list = []
if use_proxies:
    proxy_file = input("Enter the path to the proxy list file: ")
    with open(proxy_file, 'r') as file:
        for line in file:
            proxy_list.append({'http': line.strip(), 'https': line.strip()})

# Generate and check keys with delay
for i in range(num_keys):
    private_key = generate_private_key()
    address = get_address_from_private_key(private_key)
    balance = check_balance(address, proxies if use_tor else None, proxy_list)
    log_data(private_key, address, balance, filename)
    print(f"Progress: {i+1}/{num_keys} | Private Key: {private_key} | Address: {address} | Balance: {balance}")
    time.sleep(delay_time)  # Add the delay between requests

print("Process completed.")