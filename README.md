# python-lag-sdk

## Description
A brief description of what `python-lag-sdk` is and its purpose. This section should provide a high-level overview of the project's functionality and use cases.

## Installation
Instructions on how to install the `python-lag-sdk`. This will typically include steps to clone the repository, navigate to the project directory, and any commands to run, such as `pip install` if it's a Python package.

```bash
pip install -i https://test.pypi.org/simple/ lag-sdk==0.4.3
```

## Usage
Examples and code snippets showing how to use `python-lag-sdk`. This could include basic usage examples, initializing the SDK, making API calls, or other relevant use cases.

IMPORTANT, You should be able to get your private key from Metamask -> Account Details -> show private key

THESE COMMANDS SHOULD BE RUN SEPERATELY, to allow for time in between them.

```python
# Example Python code showing how to use python-lag-sdk
from swan_lag.api_client import APIClient
from swan_lag.api.lag_client import LagAPI

api_client = APIClient("<YOUR_LAGRANGE_API_KEY>", <"YOUR_PRIVATE_KEY">, "<YOUR_MUMBAI_RPC>",True, True)
lag_client = LagAPI(api_client)

#Workflow for creating a SpaceNFT:
#This creates a request for the contract to create an NFT, this returns the tx_hash for requesting the nft
res = lag_client.space_nft_request(chain_id,wallet_address,space_name)
#This attempts to claim the space nft and if it is not possible it fails, this returns the tx_hash for claiming the nft, as well as the contract address for the nft
res = lag_client.try_claim_space_nft(wallet_address,space_name)
#Once the nft is claimed, we should be able to view it on the chain, which this function allows for. This function returns info in the form of a dictionary
res = lag_client.get_space_nft_info(wallet_address,space_name)
#Once the Nft is created, we should be able to create a license. Recipient is usually going to be the same as wallet_address. Contract address comes from try_claim_space_nft
res = lag_client.create_space_license(wallet_address,space_name,contract_address,chain_id,recipient)

#Workflow for creating a dataNFT, similar return values as SpaceNFT:
res = lag_client.data_nft_request(chain_id,wallet_address,space_name)
res = lag_client.try_claim_data_nft(wallet_address,space_name)
res = lag_client.get_data_nft_info(wallet_address,space_name)
res = lag_client.create_dataset_license(wallet_address,space_name,contract_address,chain_id,recipient)

```

## Contributing
Guidelines for how others can contribute to the `python-lag-sdk` project. This section can include instructions on submitting issues, pull requests, and any coding standards or requirements.

## License
Information about the project's license. Specify the type of license and include a brief summary or a link to the full license text.

## Contact
Provide contact information or links for project maintainers, or how to join the community, if applicable.