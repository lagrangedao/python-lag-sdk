from swan_lag.api_client import APIClient
from swan_lag.common.constants import *
import logging

class LagAPI(object):
    def __init__(self, api_client=None, api_key=None, is_calibration=False):
        if api_client is None:
            api_client = APIClient("placeholder_api_key","sample_wallet_address")
        self.api_client = api_client
        self.LAG_API = api_client.LAG_API
        #TODO: once authentication added we can modify this
        self.token = self.api_client.token
        #self.token = None

    def data_nft_request(self, tx_hash,chain_id, wallet_address,space_name):
        params = {
            "tx_hash":tx_hash,
            "chain_id": chain_id,
            "wallet_address": wallet_address,
            "space_name": space_name
            }
        try:
            response = self.api_client._request_with_params(POST,CREATE_DATA_NFT_REQUEST,self.api_client.LAG_API, params, self.token, None)
            return response
        except:
            logging.error("An error occurred while executing data_nft_request")
            return None
        
    def data_nft_request_status(self, wallet_address, space_name):
        params = {
            "wallet_address": wallet_address,
            "space_name": space_name
            }
        url = '/spaces/' + wallet_address + space_name + '/nft'
        try:
            result = self.api_client._request_without_params(GET,url,self.api_client.LAG_API, self.token)
            return result
        except:
            logging.error("An error occurred while executing data_nft_request_status()")
            return None

    def create_space_license(self,tx_hash,contract_address,chain_id,recipient,ipfs_uri):
        params = {
            "tx_hash":tx_hash,
            "contract_address":contract_address,
            "chain_id":chain_id,
            "recipient": recipient,
            "ipfs_uri":ipfs_uri,
        }
        try:
            response = self.api_client._request_with_params(POST,CREATE_SPACE_LICENSE,self.api_client.LAG_API,params,self.token, None)
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None

    def create_dataset_license(self, tx_hash,contract_address,chain_id,recipient,ipfs_uri):
        params = {
            "tx_hash":tx_hash,
            "contract_address":contract_address,
            "chain_id":chain_id,
            "recipient": recipient,
            "ipfs_uri":ipfs_uri,
        }
        try:
            response = self.api_client._request_with_params(POST,CREATE_DATASET_LICENSE,self.api_client.LAG_API,params,self.token, None)
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None
        
    def copy_nft_request(self, source_id, source_address, destination_id,destination_address,
                         license_id,is_deleted,collection_address,tx_hash):
        params = {
            "source_id":source_id,
            "source_address":source_address,
            "destination_id":destination_id,
            "destination_address":destination_address,
            "license_id":license_id,
            "is_deleted":is_deleted,
            "collection_address":collection_address,
            "tx_hash":tx_hash,
        }
        try:
            response = self.api_client._request_with_params(POST,COPY_NFT_REQUEST,self.api_client.LAG_API,params,self.token, None)
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None
        
    def copy_nft_request_status(self, license_id,wallet_address,destination_id, contract_address):
        params = {
            "license_id": license_id,
            "wallet_address": wallet_address,
            "destination_id": destination_id,
            "contract_address": contract_address
        }
        try:
            response = self.api_client._request_with_params(GET,COPY_NFT_STATUS,self.api_client.LAG_API,params,self.token, None)
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None
