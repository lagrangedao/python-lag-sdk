
import tomllib
import os


class Chain(object):
    def __init__(self, name: str, id: int, rpc: str):
        self.name = name
        self.id = id
        self.rpc = rpc

class SDKEnv(object):
    def __init__(self, token_contract_address: str, payment_contract_address: str):
        self.token_contract_address = token_contract_address
        self.payment_contract_address = payment_contract_address

ChainsSupported = dict[str, Chain]()
Envs = dict[str, SDKEnv]()

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir+ "/config.toml", "rb") as f:
    data = tomllib.load(f)
    chain_data = data['chain']
    for name in chain_data:
        val = chain_data[name]
        val['name'] = name
        chain = Chain('', 0, '')
        chain.__dict__ = val
        ChainsSupported[name] = chain

    env_data = data['env']
    for name in env_data:
        sdk_env = SDKEnv('','')
        sdk_env.__dict__ = env_data[name]
        Envs[name] = sdk_env
