import base64
import os
import logging

from swan_lag.api_client import APIClient
from swan_lag.model.deployment import *
from swan_lag.model.space import *
from swan_lag.common.constants import *
from swan_lag.common.utils import *


class SpaceAPI(APIClient):
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

    def create_space(self, name: str, is_public: bool, license: str, sdk: str) -> (str, Space):
        public = 0
        if is_public:
            public = 1
        response = self.api_client.post_request(METHOD_SPACES, {
            "name": name,
            "is_public": public,
            "license": license,
            "sdk": sdk,
        })
        result = Space()
        message = self.parse_response_to_obj(response, result)
        return message, result

    def fork_space(self, space_uuid: str, name: bool) -> (str, Space):
        response = self.api_client.post_request(METHOD_SPACES_FORK.format(space_uuid), {
            "new_name": name,
        })
        result = Space()
        message = self.parse_response_to_obj(response, result)
        return message, result

    def get_space(self, space_uuid: str) -> (str, SpaceDeployment):
        response = self.api_client.get_request(
            METHOD_SPACES_OPERATION.format(space_uuid))
        deployment = SpaceDeployment()
        message = self.parse_response_to_obj(response, deployment)
        return message, deployment

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
            public = 0
            if is_public:
                public = 1
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

    def create_space_deployment(self, space_uuid: str, duration: int, paid: str, tx_hash: str, chain_id: str, cfg_name: str, region: str, start_in: int):
        response = self.api_client.post_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "space_uuid": space_uuid,
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain_id,
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

    def renew_space_deployment(self, space_uuid: str, duration: int, paid, tx_hash: str, chain_id: str) -> (str, list[Job]):
        response = self.api_client.put_request(METHOD_SPACE_DEPLOYMENT.format(space_uuid), {
            "duration": duration,
            "paid":     paid,
            "tx_hash": tx_hash,
            "chain_id": chain_id,
        })
        result = DeploymentRenewResult()
        message = self.parse_response_to_obj(response, result)
        return message, result.job

    def terminate_space_deployment(self, space_uuid: str) -> str:
        response = self.api_client.delete_request(
            METHOD_SPACE_DEPLOYMENT.format(space_uuid))
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
