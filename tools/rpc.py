from web3 import Web3
import json

rpc = "https://matic-mainnet.chainstacklabs.com"
w3 = Web3(Web3.HTTPProvider(rpc))

miner_manager_address = "0xA7f7f2122d1758696B7c25191EC095AdC35fE4E1"
with open("miner_manager_rover.json") as json_file:
    abi = json.load(json_file)
miner_manager_contract = w3.eth.contract(miner_manager_address, abi=abi)

comet_manager_address = "0x78f3b8403A85A4c27E6a635Ec012De3eB8f1a072"
with open("comet_manager_rover.json") as json_file:
    abi = json.load(json_file)
comet_manager_contract = w3.eth.contract(comet_manager_address, abi=abi)
