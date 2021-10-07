from web3 import Web3
from threading import Thread
import time
import asyncio

def handle_event(event):
    print(event['args'])
    # and whatever

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_all_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e51a791200b94e5e9fdcb8bc7a84e7c0'))
    print(w3.isConnected())
    abi = open("Treasury.json", "r").read()
    address = '0x31F8Cc382c9898b273eff4e0b7626a6987C846E8'
    contract_instance = w3.eth.contract(address=address, abi=abi)
    print(contract_instance.functions.manager().call())
    change_queued_filter = contract_instance.events.ChangeQueued.createFilter(fromBlock=13372791) #12525281
    reserves_managed_filter = contract_instance.events.ReservesManaged.createFilter(fromBlock=13372791) #12525281
    rewards_minted_filter = contract_instance.events.RewardsMinted.createFilter(fromBlock=13372791) #12525281
    change_activated_filter = contract_instance.events.ChangeActivated.createFilter(fromBlock=13372791) #12525281
    deposit_filter = contract_instance.events.ReservesUpdated.createFilter(fromBlock=13372791) #12525281
    #print(len(deposit_filter.get_all_entries()))
    block_filter = w3.eth.filter('latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(
            log_loop(deposit_filter, 2),
            log_loop(change_queued_filter, 2),
            log_loop(reserves_managed_filter, 2),
            log_loop(rewards_minted_filter, 2),
            log_loop(change_activated_filter, 2),
            log_loop(deposit_filter, 2)
            ))
    finally:
        loop.close()
if __name__ == '__main__':
    main()
