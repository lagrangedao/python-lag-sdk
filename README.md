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

#Get_job_uri
res = lag_client.get_result_uri_from_space_uuid(space_uuid)

```

### Space API

#### General response

generally, the API response contains one or two parameters, the first one is the status message, `success` means a successful response, and the second parameter (if has) is the last result. Otherwise, the message is the reason why it failed.

#### Init Space client

```json
client =  APIClient("<YOUR_LAGRANGE_API_KEY>", <"YOUR_PRIVATE_KEY">, "<YOUR_MUMBAI_RPC>",True, True)
space_client = SpaceAPI(api_client=client)
```

if you don't need the payment function, just use like below:

```json
space_client = SpaceAPI(api_key="<YOUR_LAGRANGE_API_KEY>", is_calibration=False)
```

#### Create Space

```json
msg, space = space_client.create_space("name", True, License.apache_2_0, SDK.Docker)
```

references: [Space](API_Reference.md#space)

note: `space.uuid` is the most useful parameter and will be continuously used in the future

#### Get Space

```python
msg, space = space_client.get_space("space_uuid")
```

if you want to get others public space, just use like below:

```python
msg, space = space_client.get_space("owner_address", "space_name")
```

references: [Space](API_Reference.md#space)

#### Get Space List

```python
msg, spaces = space_client.get_space_list()
```

references: [Space](API_Reference.md#space)

#### Update Space

rename space or update space visibility for public

```python
msg = space_client.update_space("space_uuid","new-name", False)
```

#### Delete Space

```python
msg = space_client.delete_space("space_uuid")
```

#### Upload files to Space

support files and folders, if the file name is the same as the previous one, just overwrite it

```python
msg = space_client.upload_space_files("space_uuid", ["files_path"])
```

#### Get Space files

```python
msg, files = space_client.get_space_files("space_uuid")
```

references: [File](API_Reference.md#space-file)

#### Delete file from Space

```python
msg = space_client.delete_space_file("space_uuid","file.name")
```

note: the `file.name` is the parameter `name` of the file from [Get Space files](#get-space-files)

#### Get Machine Configs

```python
msg, configs = space_client.get_machine_configs()
```

references: [Machine Config](API_Reference.md#machine-config)

#### Create space deployment

```python
msg, task = space_client.create_space_deployment("space_uuid", 3600, '0.0','tx_hash', '80001', 'C1ae.small', 'Global', 300)
```

note: the unit of `duration` and `start_in` is `second`

references: [Deployment Task](API_Reference.md#deployment-task)

#### Get space deployment

```python
msg, space_deployment = space_client.get_space_deployment("space_uuid")
```

references: [Space Deployment](API_Reference.md#space-deployment)

#### Renew space deployment

extend space deployment duration

```python
msg, jobs = space_client.renew_space_deployment("space_uuid", 3600, '0.0', 'tx_hash', '80001')
```

references: [Deployment Job](API_Reference.md#deployment-job)

#### Terminate space deployment

```python
msg = space_client.terminate_space_deployment("space_uuid")
```

#### Get space deployment payments

only for paid deployments

```python
msg, payments = space_client.get_space_deployment_payments()
```

references: [Deployment Payment](API_Reference.md#deployment-payment)

#### Space deployment payment claim review

```python
msg = space_client.claim_review('tx_hash', '80001')
```

#### 

## Contributing
Guidelines for how others can contribute to the `python-lag-sdk` project. This section can include instructions on submitting issues, pull requests, and any coding standards or requirements.

## License
Information about the project's license. Specify the type of license and include a brief summary or a link to the full license text.

## Contact
Provide contact information or links for project maintainers, or how to join the community, if applicable.