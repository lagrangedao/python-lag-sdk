from web3 import Web3, Account
from web3.middleware import geth_poa_middleware
from swan_lag.common.constants import STATUS_SUCCESS
from swan_lag.config import *
import logging
import traceback
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir+ "/abi/SwanToken.json", "r") as f:
    swan_token_abi = f.read()
f.close()

with open(current_dir+ "/abi/SpacePaymentV6.json", "r") as pf:
    payment_contract_abi = pf.read()
pf.close()


class SwanContract(object):
    def __init__(self, chain: Chain, private_key: str, is_calibration: bool = False):
        env_name = 'prod'
        if is_calibration:
            env_name = 'calibration'
        sdk_env = Envs[env_name]
        self.chain_id = chain.id
        self.private_key = private_key
        account = Account.from_key(private_key)
        self.public_address = account.address
        self.token_address = Web3.to_checksum_address(sdk_env.token_contract_address)
        self.payment_address = Web3.to_checksum_address(sdk_env.payment_contract_address)
        web3 = Web3(Web3.HTTPProvider(chain.rpc))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        if not web3.is_connected:
            raise Exception("rpc is connected failed")
        self.web3 = web3
        self.swan_token = web3.eth.contract(
            address=self.token_address,
            abi=swan_token_abi
        )
        self.payment_contract = web3.eth.contract(
            address=self.payment_address,
            abi=payment_contract_abi
        )

    def pay_approve(self, space_uuid: str, hardware_id: int, duration: int) -> (str,str, str, str):
        hours = int(duration / 3600)
        try:
            hardware_info = self.payment_contract.functions.hardwareInfo(
                hardware_id).call()
            logging.info(f"hardware_info : {hardware_info}")
            price_per_hour = Web3.from_wei(hardware_info[1], 'ether')
            approveAmount = price_per_hour * hours
            logging.info(f"approve amount : {approveAmount}")
            logging.info(f"public address : {self.public_address}")
            gas_limit = self.swan_token.functions.approve(self.payment_address, Web3.to_wei(approveAmount, 'ether')).estimate_gas({
                "from": self.public_address
            })
            nonce = self.web3.eth.get_transaction_count(self.public_address)
            tx = self.swan_token.functions.approve(self.payment_address, Web3.to_wei(approveAmount, 'ether')).build_transaction({
                'chainId': self.chain_id,
                "gas": gas_limit,
                "nonce": nonce,
                "from": self.public_address,
            })
            signed_tx = self.web3.eth.account.sign_transaction(
                tx, self.private_key)
            self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logging.info(f"token transaction hash: {signed_tx.hash.hex()}")

            # transaction for gas
            # gas_limit = self.payment_contract.functions.makePayment(
            #     space_uuid, hardware_id, hours).estimate_gas({"from": self.public_address})
            nonce = self.web3.eth.get_transaction_count(self.public_address)
            gas_tx = self.payment_contract.functions.makePayment(space_uuid, hardware_id, hours).build_transaction({
                'chainId': self.chain_id,
                "gas": gas_limit,
                "nonce": nonce,
                "from": self.public_address,
                "gasPrice": int(self.web3.eth.gas_price*1.5)
            })
            gas_signed_tx = self.web3.eth.account.sign_transaction(
                gas_tx, self.private_key)
            self.web3.eth.send_raw_transaction(gas_signed_tx.rawTransaction)
            return STATUS_SUCCESS, hardware_info[0], approveAmount, gas_signed_tx.hash.hex()
        except Exception as e:
            traceback.format_exc()
            logging.error(f"approve error: {str(e)} \n" + traceback.format_exc())
            return str(e), None, None, None
