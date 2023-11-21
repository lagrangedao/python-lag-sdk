from web3 import HTTPProvider, Web3, Account
from web3.middleware import geth_poa_middleware
from web3.logs import DISCARD
import os
import logging

# connect to RPC

# token for this ex does not need whole abi, just the approve function
approve_abi = '''[{
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }]'''

nft_abi= '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkCancelled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"string","name":"datasetName","type":"string"},{"indexed":false,"internalType":"address","name":"dataNFTAddress","type":"address"}],"name":"CreateDataNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"requestId","type":"bytes32"},{"indexed":false,"internalType":"string","name":"uri","type":"string"}],"name":"OracleResult","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"addressToString","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"baseUrl","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"requestType","type":"uint8"},{"internalType":"string","name":"datasetName","type":"string"}],"name":"claimDataNFT","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"a","type":"string"},{"internalType":"string","name":"b","type":"string"}],"name":"concat","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"","type":"uint8"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"name":"dataNFTAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"requestId","type":"bytes32"},{"internalType":"bytes","name":"uriBytes","type":"bytes"}],"name":"fulfill","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"idToArgs","outputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"requestType","type":"uint8"},{"internalType":"address","name":"requestor","type":"address"},{"internalType":"string","name":"assetName","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"jobId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"","type":"uint8"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"name":"requestData","outputs":[{"internalType":"address","name":"requestor","type":"address"},{"internalType":"string","name":"datasetName","type":"string"},{"internalType":"string","name":"uri","type":"string"},{"internalType":"bool","name":"fulfilled","type":"bool"},{"internalType":"bool","name":"claimable","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"requestType","type":"uint8"},{"internalType":"string","name":"datasetName","type":"string"}],"name":"requestDataNFT","outputs":[{"internalType":"bytes32","name":"requestId","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"url","type":"string"}],"name":"setBaseUrl","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_fee","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"job","type":"bytes32"}],"name":"setJobId","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"setLinkToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"oracle","type":"address"}],"name":"setOracleAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newPath","type":"string"}],"name":"setPath","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"targetPath","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawLink","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
# nft_factory_abi = '''[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkCancelled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"string","name":"datasetName","type":"string"},{"indexed":false,"internalType":"address","name":"dataNFTAddress","type":"address"}],"name":"CreateDataNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"requestId","type":"bytes32"},{"indexed":false,"internalType":"string","name":"uri","type":"string"}],"name":"OracleResult","type":"event"},{"inputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"requestType","type":"uint8"},{"internalType":"string","name":"datasetName","type":"string"}],"name":"requestDataNFT","outputs":[{"internalType":"bytes32","name":"requestId","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enum DataNFTFactoryConsumer.RequestType","name":"","type":"uint8"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"name":"requestData","outputs":[{"internalType":"address","name":"requestor","type":"address"},{"internalType":"string","name":"datasetName","type":"string"},{"internalType":"string","name":"uri","type":"string"},{"internalType":"bool","name":"fulfilled","type":"bool"},{"internalType":"bool","name":"claimable","type":"bool"}],"stateMutability":"view","type":"function"}]'''


data_nft_abi = '''[
  {
    "anonymous": false,
    "inputs": [{
        "indexed": false,
        "internalType": "uint256",
        "name": "tokenId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "recipient",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "uri",
        "type": "string"
      }
    ],
    "name": "CreateLicense",
    "type": "event"
  },{
      "inputs": [
        {
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "uri",
          "type": "string"
        }
      ],
      "name": "createLicense",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }]'''

# # example of read function
# def get_hardware(id):
#     # Build the transaction
#     hardware_info = contract.functions.hardwareInfo(id).call()

#     print(hardware_info)

# # example of write function
# def make_payment(space_id, hardware_id, num_hours):
#     # Build the transaction
#     nonce = web3.eth.get_transaction_count(account.address)
#     tx = contract.functions.lockRevenue(space_id, hardware_id, num_hours).build_transaction({
#         'from': account.address,
#         'gas': 100000,
#         'gasPrice': web3.to_wei('10', 'gwei'),
#         'nonce': nonce,
#     })
#     signed_tx = account.sign_transaction(tx)
#     tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

#     # Wait for the transaction to be mined, and get the transaction receipt
#     txn_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

#     print('Transaction successful with transaction hash:', tx_hash.hex())
#     print('Gas used:', txn_receipt['gasUsed'])

def get_web3(rpc):
    
  web3 = Web3(Web3.HTTPProvider(rpc))
  web3.middleware_onion.inject(geth_poa_middleware, layer=0)
  return web3

def get_factory(web3):
  mumbai_nft_factory_address = '0xcE9b3df9c3F5bEd0f84f1B3B1ab78568E7fEFF5A'
  mumbai_nft_factory_contract = web3.eth.contract(address=mumbai_nft_factory_address, abi=nft_abi)
  return mumbai_nft_factory_contract

def get_payment(web3):
  mumbai_usdc_address = '0x1da5E8c36dc967bE47C55C600b79220F191B1202'
  mumbai_usdc_contract = web3.eth.contract(address=mumbai_usdc_address, abi=approve_abi)
  return mumbai_usdc_contract

def build_tx_config(account,rpc):
    web3 = get_web3(rpc)
    nonce = web3.eth.getTransactionCount(account.address)
    tx_config = {
        'from': account.address,
        'nonce': nonce,
        'gasPrice': int(web3.eth.gas_price * 1.4),
    }

    return tx_config

def approve_spending_on_mumbai(account,spender, amount, rpc):
    web3 = get_web3(rpc)
    mumbai_usdc_contract = get_payment(web3)
    tx_config = build_tx_config(account,rpc)

    tx = mumbai_usdc_contract.functions.approve(spender, amount).build_transaction(tx_config)
    signed_tx = account.signTransaction(tx)

    web3.eth.send_raw_transaction(signed_tx.rawTransaction)


def request_data_nft(account,space_name, rpc):
    web3 = get_web3(rpc)
    mumbai_nft_factory_contract = get_factory(web3)
    tx_config = build_tx_config(account,rpc)

    tx = mumbai_nft_factory_contract.functions.requestDataNFT(1, space_name).buildTransaction(tx_config)
    signed_tx = account.signTransaction(tx)
    print(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Waiting for tx_hash {tx_hash.hex()} to complete")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print('Transaction successful with transaction hash:', tx_hash.hex())

    # Decode event logs
    event_logs = mumbai_nft_factory_contract.events.ChainlinkRequested().processReceipt(tx_receipt, errors=DISCARD)

    for log in event_logs:
        request_id = log.args.id.hex()


    print('Chainlink request id: 0x', request_id)
    return(request_id,tx_hash.hex())

def check_request_status(wallet_address, space_name, rpc):
    web3 = get_web3(rpc)
    mumbai_nft_factory_contract = get_factory(web3)

    request_data = mumbai_nft_factory_contract.functions.requestData(1, wallet_address, space_name).call()

    # fulfilled true means the oracle has processed this request
    # claimable true means  the request was successful
    # so both true is good. 
    # fulfilled and not claimable is bad.
    # no fulfilled means you still need to wait.
    data = {'requestor': request_data[0],
        'name': request_data[1],
        'uri': request_data[2],
        'fulfilled': request_data[3],
        'claimable': request_data[4]}

    print(data)

    return data

def claim_data_nft(account,space_name, rpc):
    web3 = get_web3(rpc)
    mumbai_nft_factory_contract = get_factory(web3)
    tx_config = build_tx_config(account,rpc)

    tx = mumbai_nft_factory_contract.functions.claimDataNFT(1, space_name).buildTransaction(tx_config)
    signed_tx = account.signTransaction(tx)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print('Transaction successful with transaction hash:', tx_hash.hex())

    # Decode event logs
    event_logs = mumbai_nft_factory_contract.events.CreateDataNFT().processReceipt(tx_receipt, errors=DISCARD)

    for log in event_logs:
        data_nft_contract_address = log.args.dataNFTAddress


    print('Data NFT contract address:', data_nft_contract_address)
    return (data_nft_contract_address,tx_hash.hex())


def create_license(account,data_nft_contract, recipient, license_uri, rpc):
    web3 = get_web3(rpc)
    data_nft_address = data_nft_contract
    data_nft_contract = web3.eth.contract(address=data_nft_address, abi=data_nft_abi)

    ## need to upload license info to IPFS to get uri
    tx_config = build_tx_config(account,rpc)

    tx = data_nft_contract.functions.createLicense(recipient, license_uri).buildTransaction(tx_config)
    signed_tx = account.signTransaction(tx)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print('Transaction successful with transaction hash:', tx_hash.hex())
    return tx_hash.hex()