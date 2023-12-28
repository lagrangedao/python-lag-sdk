import json
import requests
import time

from swan_lag.api_client import APIClient
from swan_lag.common.constants import *
from swan_lag.model.model import CreateSpaceParams, CreateSpaceResult, ResponseResult
from swan_lag.service.lag_service import *


class LagAPI(object):
    def __init__(self, api_client=None, api_key=None, is_calibration=False):
        if api_client is None:
            api_client = APIClient("placeholder_api_key", "sample_wallet_address")
        self.api_client = api_client
        self.LAG_API = api_client.LAG_API
        # TODO: once authentication added we can modify this
        self.token = self.api_client.token
        self.account = self.api_client.account
        self.rpc = self.api_client.rpc
        # self.token = None

    def space_nft_request(self, chain_id, wallet_address, space_name):
        request_id, tx_hash = request_data_nft(self.account, space_name, self.rpc, 1)
        time.sleep(10)
        params = {
            "tx_hash": tx_hash,
            "chain_id": chain_id,
            "wallet_address": wallet_address,
            "space_name": space_name
        }
        try:
            response = self.api_client._request_with_params(POST, CREATE_SPACE_NFT_REQUEST, self.api_client.LAG_API,
                                                            params, self.token, None)
            return response
        except:
            logging.error("An error occurred while executing space_nft_request")
            return None

    def try_claim_space_nft(self, wallet_address, space_name):
        data = check_request_status(wallet_address, space_name, self.rpc, 1)
        if data["fulfilled"] is False or data["claimable"] is False:
            logging.info("SpaceNFT is not claimable")
            return {"message": "SpaceNFT is not claimable", "status": "Failed"}

        contract_address, tx_hash = claim_data_nft(self.account, space_name, self.rpc, 1)

        data = {
            "tx_hash": tx_hash,
            "chain_id": 80001
        }
        headers = {
            "Authorization": "Bearer " + self.token
        }
        mintHash = "/spaces/" + wallet_address + "/" + space_name + "/mint_hash"
        try:
            res = requests.post(f"https://test-api.lagrangedao.org{mintHash}", headers=headers, data=data)
        except Exception as e:
            logging.error("An error occured while saving mintHash")
            return None
        res_data = {
            "contract_address": contract_address,
            "tx_hash": tx_hash
        }
        return {"message": "SpaceNFT claimed", "status": "Success", "data": res_data}

    def get_space_nft_info(self, wallet_address, space_name):
        url = '/spaces/' + wallet_address + "/" + space_name + '/nft'
        try:
            result = self.api_client._request_without_params(GET, url, self.api_client.LAG_API, self.token)
            return result
        except:
            logging.error("An error occurred while executing get_space_nft_info()")
            return None

    def create_space_license(self, wallet_address, space_name, contract_address, chain_id, recipient):
        metadata = "/spaces/" + wallet_address + "/" + space_name + "/license/metadata/generate"

        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
        data = {
            "author": wallet_address,
            "created_at": int(time.time()),
            "updated_at": int(time.time()),
            "description": "",
            "links": [],
            "recipient": recipient,
            "tags": [],
            "type": "space"

        }
        try:
            res = requests.post(f"https://test-api.lagrangedao.org{metadata}", headers=headers, data=json.dumps(data))
        except Exception as e:
            logging.error("An error occured while generating metadata")
            return None
        if res.status_code != 200:
            logging.error("An error occured while generating metadata")
            return None
        json_data = res.json()
        print(json_data)
        data = json_data["data"]
        ipfs_uri = data["ipfs_url"]
        gateway = data["gateway"]
        metadata_cid = data["metadata_cid"]
        tx_hash = create_license(self.account, contract_address, recipient, ipfs_uri, self.rpc)
        headers = {
            "Authorization": "Bearer " + self.token,
        }
        body = {
            "tx_hash": tx_hash,
            "chain_id": chain_id
        }
        mintHash = "/spaces/" + wallet_address + "/" + space_name + "/license/mint_hash"
        try:
            res = requests.post(f"https://test-api.lagrangedao.org{mintHash}", headers=headers, data=body)
        except Exception as e:
            logging.error("An error occured while saving mintHash")
            return None
        params = {
            "tx_hash": tx_hash,
            "contract_address": contract_address,
            "chain_id": chain_id,
            "recipient": recipient,
            "ipfs_uri": ipfs_uri,
        }
        try:
            response = self.api_client._request_with_params(POST, CREATE_SPACE_LICENSE, self.api_client.LAG_API, params,
                                                            self.token, None)
            return response
        except:
            logging.error("An error occurred while executing create_space_license()")
            return None

    def data_nft_request(self, chain_id, wallet_address, dataset_name):
        request_id, tx_hash = request_data_nft(self.account, dataset_name, self.rpc, 0)
        params = {
            "tx_hash": tx_hash,
            "chain_id": chain_id,
            "wallet_address": wallet_address,
            "dataset_name": dataset_name
        }
        try:
            response = self.api_client._request_with_params(POST, CREATE_DATA_NFT_REQUEST, self.api_client.LAG_API,
                                                            params, self.token, None)
            return response
        except:
            logging.error("An error occurred while executing data_nft_request")
            return None

    def try_claim_data_nft(self, wallet_address, dataset_name):

        data = check_request_status(wallet_address, dataset_name, self.rpc, 0)
        if data["fulfilled"] is False or data["claimable"] is False:
            logging.info("DataNFT is not claimable")
            return {"message": "DataNFT is not claimable", "status": "Failed"}

        contract_address, tx_hash = claim_data_nft(self.account, dataset_name, self.rpc, 0)
        data = {
            "tx_hash": tx_hash,
            "chain_id": 80001
        }
        headers = {
            "Authorization": "Bearer " + self.token
        }
        mintHash = "/datasets/" + wallet_address + "/" + dataset_name + "/mint_hash"
        try:
            res = requests.post(f"https://test-api.lagrangedao.org{mintHash}", headers=headers, data=data)
        except Exception as e:
            logging.error("An error occured while saving mintHash")
            return None
        if res.status_code != 200:
            return None
        res_data = {
            "contract_address": contract_address,
            "tx_hash": tx_hash
        }
        return {"message": "DataNFT claimed", "status": "Success", "data": res_data}

    def get_data_nft_info(self, wallet_address, dataset_name):
        url = '/datasets/' + wallet_address + "/" + dataset_name
        try:
            result = self.api_client._request_without_params(GET, url, self.api_client.LAG_API, self.token)
            return result
        except:
            logging.error("An error occurred while executing get_data_nft_info()")
            return None

    def create_dataset_license(self, wallet_address, dataset_name, contract_address, chain_id, recipient):
        metadata = "/datasets/" + wallet_address + "/" + dataset_name + "/license/metadata/generate"

        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
        data = {
            "author": wallet_address,
            "created_at": int(time.time()),
            "updated_at": int(time.time()),
            "description": "",
            "links": [],
            "recipient": recipient,
            "tags": [],
            "type": "space"

        }
        try:
            res = requests.post(f"https://test-api.lagrangedao.org{metadata}", headers=headers, data=json.dumps(data))
        except Exception as e:
            logging.error("An error occured while generating metadata")
            return None
        if res.status_code != 200:
            logging.error("An error occured while generating metadata")
            return None
        json_data = res.json()
        print(json_data)
        data = json_data["data"]
        ipfs_uri = data["ipfs_url"]
        gateway = data["gateway"]
        metadata_cid = data["metadata_cid"]
        tx_hash = create_license(self.account, contract_address, recipient, ipfs_uri, self.rpc)
        headers = {
            "Authorization": "Bearer " + self.token,
        }
        body = {
            "tx_hash": tx_hash,
            "chain_id": chain_id
        }
        mintHash = "/spaces/" + wallet_address + "/" + dataset_name + "/license/mint_hash"
        try:
            res = requests.post(f"https://test-api.lagrangedao.org{mintHash}", headers=headers, data=body)
        except Exception as e:
            logging.error("An error occured while saving mintHash")
            return None
        params = {
            "tx_hash": tx_hash,
            "contract_address": contract_address,
            "chain_id": chain_id,
            "recipient": recipient,
            "ipfs_uri": ipfs_uri,
        }
        try:
            response = self.api_client._request_with_params(POST, CREATE_DATASET_LICENSE, self.api_client.LAG_API,
                                                            params, self.token, None)
            return response
        except:
            logging.error("An error occurred while executing create_dataset_license()")
            return None

    def copy_nft_request(self, source_id, source_address, destination_id, destination_address,
                         license_id, is_deleted, collection_address, tx_hash):
        params = {
            "source_id": source_id,
            "source_address": source_address,
            "destination_id": destination_id,
            "destination_address": destination_address,
            "license_id": license_id,
            "is_deleted": is_deleted,
            "collection_address": collection_address,
            "tx_hash": tx_hash,
        }
        try:
            response = self.api_client._request_with_params(POST, COPY_NFT_REQUEST, self.api_client.LAG_API, params,
                                                            self.token, None)
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None

    def copy_nft_request_status(self, license_id, wallet_address, destination_id, contract_address):
        params = {
            "license_id": license_id,
            "wallet_address": wallet_address,
            "destination_id": destination_id,
            "contract_address": contract_address
        }
        try:
            response = self.api_client._request_with_params(GET, COPY_NFT_STATUS, self.api_client.LAG_API, params,
                                                            self.token, None)
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None

    def get_result_uri_from_space_uuid(self, space_uuid):
        url = '/get_job_uri/' + space_uuid
        try:
            response = self.api_client._request_without_params(GET, url, self.api_client.LAG_API, self.token)

            return response
        except:
            logging.error("An error occurred while executing get_result_uri_from_space_uuid()")
            return None

    def create_space(self, space: CreateSpaceParams):
        data = {
            "name": space.name,
            "is_public": space.is_public,
            "license": space.space_license,
            "hardware": 0,
            "sdk": space.sdk,
            "hours": space.hours
        }
        try:
            response = self.api_client._request_with_params(POST, CREATE_SPACE, self.api_client.LAG_API, data,
                                                            self.token, None)
            if response is None:
                return response
            uuid = response['data']['space']['uuid']
            name = response['data']['space']['name']
            status_code = response['data']['space']['status_code']
            created_at = response['data']['space']['created_at']
            return CreateSpaceResult(uuid, name, status_code, created_at).to_json()
        except Exception as e:
            logging.error("An error occurred while executing create_space, error: {e}")
            return None

    def upload_or_update_file_to_space(self, space_name: str, base_dir=None, files=None):
        if not base_dir and not files:
            logging.error("Error: Neither base directory nor file paths provided.")
            return

        if base_dir:
            files = files or []
            files_in_base_dir = []
            for root, dirs, files_list in os.walk(base_dir):
                for file in files_list:
                    file_path = os.path.join(root, file)
                    files_in_base_dir.append(file_path)
            files.extend(files_in_base_dir)

        if not files:
            print("Error: No files found for upload.")
            return
        # try:
        response = self.api_client._request_with_params(POST, SPACE_UPLOAD_FILE % space_name, self.api_client.LAG_API,
                                                        None, self.token, files)
        return response
        # except Exception as e:
        #     logging.error("An error occurred while executing upload_file_to_space, error: {e}")
        #     return None

    def delete_space_files(self, space_name: str, filename=None):
        if not filename:
            logging.error("Error: no filename provided.")
            return
        data = {
            'filename': filename,
        }

        try:
            response = self.api_client._request_with_params(POST, SPACE_DELETE_FILE % space_name, self.api_client.LAG_API,
                                                            data, self.token, None)
            return response
        except Exception as e:
            logging.error("An error occurred while executing upload_file_to_space, error: {e}")
            return None

    def get_machines(self):
        try:
            response = self.api_client._request_without_params(GET, GET_MACHINES_CONFIG, self.api_client.LAG_API,
                                                               self.token)
            return response
        except Exception as e:
            logging.error("An error occurred while executing upload_file_to_space, error: {e}")
            return None