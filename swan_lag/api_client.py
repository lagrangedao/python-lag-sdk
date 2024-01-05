from swan_lag.common.params import Params
import logging
import json
import requests
from swan_lag.common import utils
from swan_lag.common import constants as c
from web3 import HTTPProvider, Web3, Account

class APIClient(object):
    def __init__(self, api_key, private_key = None,rpc = None, is_testnet=False, login=True):
        self.token = None
        self.api_key = api_key
        self.is_testnet = is_testnet
        self.LAG_API = Params(self.is_testnet).LAG_API
        self.account = None
        if private_key:
            self.account = Account.from_key(private_key)
        self.rpc = rpc
        if login:
            self.api_key_login()


    def api_key_login(self):
        params = {'api_key': self.api_key}
        try:
            result = self._request_with_params(
                c.POST, c.API_KEY_LOGIN, self.LAG_API, params, None, None)
            self.token = result['data']
            logging.info("\033[32mLogin successful\033[0m")
            return self.token
        except:
            logging.error("\033[31m Please check your APIkey.\033[0m")
            return

    def _request(self, method, request_path, lag_api, params, token, files=False, json=False):
        if method == c.GET and params:
            request_path = request_path + utils.parse_params_to_str(params)
        url = lag_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        response = None
        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.PUT:
            # body = json.dumps(params)
            response = requests.put(url, data=params, headers=header)
        elif method == c.POST:
            # header["Content-Type"] = "application/json"
            if files:
                response = requests.post(url, headers=header, files=params)
            else:
                # body = json.dumps(params) if method == c.POST else ""
                response = requests.post(url, data=params, headers=header)
        elif method == c.DELETE:
            if params:
                # body = json.dumps(params)
                if json:
                    response = requests.delete(url, json=params, headers=header)
                else:
                    response = requests.delete(url, data=params, headers=header)
            else:
                response = requests.delete(url, headers=header)
        print(f"{method} {url} Response: {response.content.decode()}")
        # exception handle
        # if not str(response.status_code).startswith('2'):
        #     return None
        return response.json()

    def _request_without_params(self, method, request_path, lag_api, token):
        return self._request(method, request_path, lag_api, {}, token)

    def _request_with_params(self, method, request_path, lag_api, params, token, files):
        return self._request(method, request_path, lag_api, params, token, files)
    
    def get_request(self, method_path, params=None):
        return self._request(c.GET, method_path, self.LAG_API, params, self.api_key)
    
    def post_request(self, method_path, params=None, files=False):
        return self._request(c.POST, method_path, self.LAG_API, params, self.api_key, files)
    
    def put_request(self, method_path, params=None):
        return self._request(c.PUT, method_path, self.LAG_API, params, self.api_key)
    
    def delete_request(self, method_path, params=None, json=False):
        return self._request(c.DELETE, method_path, self.LAG_API, params, self.api_key,json=json)
