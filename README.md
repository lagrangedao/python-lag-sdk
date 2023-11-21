# python-lag-sdk

## Description
A brief description of what `python-lag-sdk` is and its purpose. This section should provide a high-level overview of the project's functionality and use cases.

## Installation
Instructions on how to install the `python-lag-sdk`. This will typically include steps to clone the repository, navigate to the project directory, and any commands to run, such as `pip install` if it's a Python package.

```bash
git clone [repository-url]
cd python-lag-sdk
pip install -r requirements.txt
```

## Usage
Examples and code snippets showing how to use `python-lag-sdk`. This could include basic usage examples, initializing the SDK, making API calls, or other relevant use cases.

```python
# Example Python code showing how to use python-lag-sdk
from swan_lag.api_client import APIClient
from swan_lag.api.lag_client import LagAPI


api_client = APIClient("GnWAOmfnNa",True, True)
lag_client = LagAPI(api_client)
#Examples:
res = lag_client.data_nft_request(tx_hash,chain_id,wallet_address,space_name)
res = lag_client.data_nft_request_status(wallet_address,space_name)
res = lag_client.create_space_license(tx_hash,contract_address,chain_id,recipient,ipfs_uri)
res = lag_client.copy_nft_request(tx_hash,contract_address,chain_id,recipient,ipfs_uri)
res = lag_client.copy_nft_request_status(tx_hash,chain_id,wallet_address,space_name)


```

## Contributing
Guidelines for how others can contribute to the `python-lag-sdk` project. This section can include instructions on submitting issues, pull requests, and any coding standards or requirements.

## License
Information about the project's license. Specify the type of license and include a brief summary or a link to the full license text.

## Contact
Provide contact information or links for project maintainers, or how to join the community, if applicable.