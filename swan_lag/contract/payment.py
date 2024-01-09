from web3 import Web3, Account
from web3.middleware import geth_poa_middleware

with open("./swan_lag/contract/abi/SwanToken.json", "r") as f:
    swan_token_abi = f.read()
f.close()

with open("./swan_lag/contract/abi/SpaceHardware.json", "r") as pf:
    payment_contract_abi = pf.read()
pf.close()

class SwanTokenContract(object):
    def __init__(self, rpc:str, private_key:str):
        self.private_key = private_key
        account = Account.from_key(private_key)
        print(f"account : {account} {account.address}")
        self.public_address = account.address
        self.token_address = Web3.to_checksum_address("0x3CF24790B3af64029564E81B67aF299dB83Fd9e3")
        self.payment_address = Web3.to_checksum_address("0x2108e71280b825131220cd710813c25874f0e718")
        web3 = Web3(Web3.HTTPProvider(rpc))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        print(f"web3 is connected: {web3.is_connected}")
        self.web3 = web3
        self.swan_token = web3.eth.contract(
            address = self.token_address,
            abi = swan_token_abi
        )
        self.payment_contract = web3.eth.contract(
            address = self.payment_address,
            abi = payment_contract_abi
        )

    def approve(self, space_uuid: str,hardware_id: int, duration: int,chain_id: int):
        hours = int(duration / 3600)
        hardware_info = self.payment_contract.functions.hardwareInfo(hardware_id).call()
        print(f"hardware_info : {hardware_info}")
        price_per_hour =  Web3.from_wei(hardware_info[1], 'ether')
        approveAmount = price_per_hour * hours
        print(f"self.payment_address {self.payment_address}")
        gas_limit = self.swan_token.functions.approve(self.payment_address, Web3.to_wei(approveAmount,'ether')).estimate_gas({
            "from": self.public_address
        })
        nonce = self.web3.eth.get_transaction_count(self.public_address) 
        tx = self.swan_token.functions.approve(self.payment_address, Web3.to_wei(approveAmount,'ether')).build_transaction({
            'chainId': chain_id,
            "gas": gas_limit,
            "nonce": nonce,
            "from": self.public_address,
            "type":2
        })
        print(f" Transaction: {tx}")
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        print(f"signed Transaction: {signed_tx}")
        self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"sent signed transaction hash: {signed_tx.hash.hex()}")


        # transaction for gas
        gas_limit =  self.payment_contract.functions.makePayment(space_uuid, hardware_id, hours).estimate_gas({ "from": self.public_address })
        nonce = self.web3.eth.get_transaction_count(self.public_address) 
        gas_tx = self.payment_contract.functions.makePayment(space_uuid, hardware_id, hours).build_transaction({
            'chainId': chain_id,
            "gas": int(gas_limit * 100),
            "nonce": nonce,
            "from": self.public_address,
            "gasPrice": int(self.web3.eth.gas_price*1.5)
        })
        print(f" Transaction: {gas_tx}")
        gas_signed_tx = self.web3.eth.account.sign_transaction(gas_tx, self.private_key)
        print(f"signed Transaction: {gas_signed_tx}")
        self.web3.eth.send_raw_transaction(gas_signed_tx.rawTransaction)
        return gas_signed_tx.hash.hex()


