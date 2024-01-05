from base64 import b64decode

from swan_lag.api_client import APIClient
from swan_lag.model.deployment import *
from swan_lag.common.constants import *

METHOD_SPACE_DEPLOYMENT = "/spaces/{}/deployment"


class DeploymentAPI(APIClient):
    def __init__(self, api_key=None, is_calibration=False):
        api_client = APIClient(
            api_key=api_key, is_testnet=is_calibration, login=False)
        self.with_client(api_client)

    @classmethod
    def with_client(self, api_client: APIClient):
        self.api_client = api_client
        self.LAG_API = api_client.LAG_API
        self.token = self.api_client.token
        self.account = self.api_client.account
        self.rpc = self.api_client.rpc

    def create_deployment(self, space_uuid: str, duration: int, paid, tx_hash: str, chain_id: str):
        response = self.api_client.post_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain_id,
        })
        result = DeploymentTask()
        message = self.parse_response_to_obj(response, result)
        return message, result.task

    def get_deployment(self, space_uuid: str) -> (str, SpaceDeployment):
        response = self.api_client.get_request(
            METHOD_SPACE_DEPLOYMENT.format(space_uuid))
        deployment = SpaceDeployment()
        message = self.parse_response_to_obj(response, deployment)
        return message, deployment

    def renew_deployment(self, space_uuid: str, duration: int, paid, tx_hash: str, chain_id: str) -> (str, list[Job]):
        response = self.api_client.put_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain_id,
        })
        result = DeploymentRenewResult()
        message = self.parse_response_to_obj(response, result)
        return message, result.job

    def terminate_deployment(self, space_uuid: str) -> str:
        response = self.api_client.delete_request(
            METHOD_SPACE_DEPLOYMENT.format(space_uuid))
        message = self.parse_response_to_obj(response)
        return message

    def parse_response_to_obj(self, response, obj: JsonDictObject = None) -> str:
        if response['status'] != STATUS_SUCCESS:
            return response['message']
        if not obj:
            return STATUS_SUCCESS
        data = response['data']
        if not data:
            return 'response data missed'
        obj.parse_dict_to_obj(data)
        return STATUS_SUCCESS
