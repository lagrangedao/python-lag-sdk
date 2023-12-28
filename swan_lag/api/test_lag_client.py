from unittest import TestCase
from swan_lag.api_client import APIClient
from swan_lag.api.lag_client import LagAPI
from swan_lag.model.model import CreateSpaceParams, SpaceType, CreateSpaceResult


class TestLagAPI(TestCase):
    def test_create_space(self):
        api_client = APIClient("5G232JaAjq", "c3e47d07d520fd3022a4b61764cfcb831cdafc3352e97c21acb0138684c5d703",
                               "https://rpc-mumbai.maticvigil.com", True)
        lag_client = LagAPI(api_client)

        create_space = CreateSpaceParams('sonictest', SpaceType.PUBLIC, 'apache-2.0', 'docker', 360)
        resp = lag_client.create_space(create_space)
        print(resp)

    def test_upload_or_update_file_to_space(self):
        api_client = APIClient("5G232JaAjq", "c3e47d07d520fd3022a4b61764cfcb831cdafc3352e97c21acb0138684c5d703",
                               "https://rpc-mumbai.maticvigil.com", True)
        lag_client = LagAPI(api_client)

        files = ['/Users/sonic/Desktop/ccc/test-script.js', '/Users/sonic/Desktop/ccc/polygon-eth_blockNumber.pdf',
                 '/Users/sonic/Desktop/ccc/polygon_eth_cal.pdf']
        resp = lag_client.upload_or_update_file_to_space('sonictest', files=files)
        print(resp)

    def test_get_machines(self):
        api_client = APIClient("5G232JaAjq", "c3e47d07d520fd3022a4b61764cfcb831cdafc3352e97c21acb0138684c5d703",
                               "https://rpc-mumbai.maticvigil.com", True)
        lag_client = LagAPI(api_client)
        resp = lag_client.get_machines()
        print(resp)
