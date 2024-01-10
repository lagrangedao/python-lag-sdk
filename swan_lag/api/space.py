import base64
import os
import logging

from swan_lag.api_client import APIClient
from swan_lag.model.deployment import *
from swan_lag.model.space import *
from swan_lag.common.constants import *
from swan_lag.common.utils import *
from swan_lag.common.enums import *
from swan_lag.config import *
from swan_lag.contract.payment import *


class SpaceAPI(APIClient):
    def __init__(self, api_key: str = None, private_key=None, is_calibration=False, api_client: APIClient = None):
        if not api_client:
            if not private_key:
                logging.warning(
                    "private_key is not set, payment relevant functions not work")
            api_client = APIClient(
                api_key=api_key, private_key=private_key, is_testnet=is_calibration, login=False)
        self.with_client(api_client)

    def with_client(self, api_client: APIClient):
        self.api_client = api_client
        self.LAG_API = api_client.LAG_API
        self.token = api_client.token
        self.account = api_client.account
        self.rpc = api_client.rpc
        self.private_key = api_client.private_key
        self.is_calibration = api_client.is_testnet

    def create_space(self, name: str, is_public: bool, license: License, sdk: SDK) -> (str, Space):
        public = 1 if is_public else 0
        response = self.api_client.post_request(METHOD_SPACES, {
            "name": name,
            "is_public": public,
            "license": license.value,
            "sdk": sdk.value,
        })
        result = Space()
        message = self.parse_response_to_obj(response, result)
        return message, result

    def fork_space(self, space_uuid: str, new_name: str) -> (str, Space):
        response = self.api_client.post_request(METHOD_SPACES_FORK.format(space_uuid), {
            "new_name": new_name,
        })
        result = Space()
        message = self.parse_response_to_obj(response, result)
        return message, result

    def get_space(self, space_uuid: str) -> (str, Space):
        response = self.api_client.get_request(
            METHOD_SPACES_OPERATION.format(space_uuid))
        deployment = SpaceDeployment()
        message = self.parse_response_to_obj(response, deployment)
        return message, deployment.space

    def get_public_space(self, wallet: str, space_name: str) -> (str, SpaceDeployment):
        response = self.api_client.get_request(
            METHOD_SPACES_PUBLIC.format(wallet, space_name))
        deployment = SpaceDeployment()
        message = self.parse_response_to_obj(response, deployment)
        return message, deployment

    def update_space(self, space_uuid: str, new_name: str = None, is_public: bool = None) -> str:
        if not new_name and is_public is None:
            return "new_name or is_public is required"
        data = {}
        if new_name:
            data["new_name"] = new_name
        if is_public is not None:
            public = 1 if is_public else 0
            data["is_public"] = public
        response = self.api_client.put_request(
            METHOD_SPACES_OPERATION.format(space_uuid), data)
        message = self.parse_response_to_obj(response)
        return message

    def delete_space(self, space_uuid: str):
        response = self.api_client.delete_request(
            METHOD_SPACES_OPERATION.format(space_uuid))
        message = self.parse_response_to_obj(response)
        return message

    def get_space_list(self) -> (str, list[Space]):
        response = self.api_client.get_request(METHOD_PROFILE)
        result = Profile()
        message = self.parse_response_to_obj(response, result)
        return message, result.space

    def upload_space_files(self, space_uuid: str, file_or_dir_paths: list[str]) -> str:
        for path in file_or_dir_paths:
            if not os.path.exists(path):
                raise Exception(f"{path} not exists")

        files = []
        for path in file_or_dir_paths:
            filepaths = []
            if os.path.isdir(path):
                dirname = os.path.basename(path)
                parent_dirpath = path.removesuffix("/"+dirname)
            else:
                parent_dirpath = os.path.dirname(path)
            for (dir_path, dir_names, file_names) in os.walk(path):
                relevant_dirname = dir_path.removeprefix(parent_dirpath+"/")
                for filename in file_names:
                    file_relevant_path = relevant_dirname+'/'+filename
                    filepaths.append(file_relevant_path)

            # size = 0 means file not dir
            if len(filepaths) == 0:
                filename = os.path.basename(path)
                filepaths.append(filename)

            for filepath in filepaths:
                print(f"upload file {filepath}")
                files.append(
                    ("file", (filepath, open(parent_dirpath+'/'+filepath, 'rb'))))

        response = self.api_client.post_request(
            METHOD_SPACES_FILES.format(space_uuid), files, files=True)
        message = self.parse_response_to_obj(response)
        return message

    def get_space_files(self, space_uuid: str) -> (str, list[File]):
        response = self.api_client.get_request(
            METHOD_SPACES_FILES.format(space_uuid))
        message, files = self.parse_response_to_obj_list(response, File)
        return message, files

    def delete_space_file(self, space_uuid: str, file_name) -> str:
        response = self.api_client.delete_request(METHOD_SPACES_FILES.format(space_uuid), {
            "filename": file_name
        }, json=True)
        message = self.parse_response_to_obj(response)
        return message

    def get_machine_configs(self) -> (str, list[MachineConfig]):
        response = self.api_client.get_request(METHOD_MACHINES)
        result = MachineResult()
        message = self.parse_response_to_obj(response, result)
        return message, result.hardware

    def get_supported_chains(self) -> dict[str, Chain]:
        return ChainsSupported

    def create_space_deployment(self, space_uuid: str, duration: int, cfg_id: int, region: str,  start_in: int, chain: Chain) -> (str, DeploymentTask):
        if not self.private_key:
            return 'private_key is required', None

        message, cfg_name, paid, tx_hash = SwanContract(
            chain, self.private_key, self.is_calibration).pay_approve(space_uuid, cfg_id, duration)
        logging.info(
            f"pay approve response: {message} {cfg_name} {paid} {tx_hash}")
        if message != STATUS_SUCCESS:
            return message, None
        response = self.api_client.post_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "space_uuid": space_uuid,
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain.id,
            "cfg_name": cfg_name,
            "region": region,
            "start_in": start_in
        })
        result = DeploymentTask()
        message = self.parse_response_to_obj(response, result)
        return message, result.task

    def get_space_deployment(self, space_uuid: str) -> (str, SpaceDeployment):
        response = self.api_client.get_request(
            METHOD_SPACE_DEPLOYMENT.format(space_uuid))
        deployment = SpaceDeployment()
        message = self.parse_response_to_obj(response, deployment)
        return message, deployment

    def renew_space_deployment(self, space_uuid: str, duration: int, chain: Chain) -> (str, list[Job]):
        if not self.private_key:
            return 'private_key is required', None

        message, space = self.get_space(space_uuid)
        if message != STATUS_SUCCESS:
            return message, None
        if space.status != STATUS_RUNNING:
            return 'can not renew non-running space deployment', None
        logging.info(f"hardware id: {space.activeOrder.config.hardware_id}")
        message, cfg_name, paid, tx_hash = SwanContract(chain, self.private_key, self.is_calibration).pay_approve(
            space_uuid, space.activeOrder.config.hardware_id, duration)
        logging.info(
            f"pay approve response: {message} {cfg_name} {paid} {tx_hash}")
        if message != STATUS_SUCCESS:
            return message, None
        response = self.api_client.put_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain.id,
        })
        result = DeploymentRenewResult()
        message = self.parse_response_to_obj(response, result)
        return message, result.job

    def terminate_space_deployment(self, space_uuid: str) -> str:
        response = self.api_client.delete_request(
            METHOD_SPACE_DEPLOYMENT.format(space_uuid))
        message = self.parse_response_to_obj(response)
        return message

    def get_space_deployment_payments(self) -> (str, list[DeploymentPayment]):
        response = self.api_client.get_request(METHOD_SPACE_PAYMENTS)
        result = DeploymentPaymentsResult()
        message = self.parse_response_to_obj(response, result)
        return message, result.payments

    def claim_review(self, tx_hash: str, chain_id: str) -> str:
        response = self.api_client.post_request(METHOD_CLAIM_REVIEW, {
            "tx_hash": tx_hash,
            "chain_id": chain_id
        })
        message = self.parse_response_to_obj(response)
        return message

    def parse_response_to_obj(self, response, obj: JsonDictObject = None) -> str:
        if response['status'] != STATUS_SUCCESS:
            return response['message']
        if obj is None:
            return STATUS_SUCCESS
        data = response['data']
        if not data:
            return 'response data missed'
        obj.parse_dict_to_obj(data)
        return STATUS_SUCCESS

    def parse_response_to_obj_list(self, response, cls=None) -> (str, list[JsonDictObject]):
        if response['status'] != STATUS_SUCCESS:
            return response['message'], None
        if cls is None:
            return STATUS_SUCCESS, None
        data = response['data']
        if not data:
            return 'response data missed', None
        objs = list[cls]()
        if isinstance(data, list):
            for dt in data:
                obj = cls()
                obj.parse_dict_to_obj(dt)
                objs.append(obj)
        return STATUS_SUCCESS, objs
