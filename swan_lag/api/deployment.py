from base64 import b64decode

from swan_lag.api_client import APIClient
from swan_lag.model.deployment import *
from swan_lag.common.constants import *

METHOD_SPACE_DEPLOYMENT="/spaces/{}/deployment"

class DeploymentAPI(APIClient):
    def __init__(self, api_key=None, is_calibration=False):
        api_client = APIClient(api_key=api_key,is_testnet=is_calibration,login=False)
        self.WithClient(api_client)

    @classmethod
    def WithClient(self, api_client: APIClient):
        self.api_client = api_client
        self.LAG_API = api_client.LAG_API
        self.token = self.api_client.token
        self.account = self.api_client.account
        self.rpc = self.api_client.rpc

    def get_deployment(self, space_uuid: str):
        self.api_client.get_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid))

    def renew_deployment(self, space_uuid: str, duration: int, paid, tx_hash: str, chain_id:str):
        self.api_client.post_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain_id,
        })




