LAG_TESTNET_API = "http://test-lag-api.storefrontiers.cn"
LAG_MAINNET_API = "https://api.lagrangedao.org"

## api method
GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


## api
API_KEY_LOGIN = "/login_by_api_key"

CREATE_SPACE = '/spaces'
SPACE_UPLOAD_FILE = '/spaces/%s/files/upload'
SPACE_DELETE_FILE = '/spaces/%s/files/delete'
GET_MACHINES_CONFIG = '/cp/machines'

CREATE_SPACE_NFT_REQUEST = '/spaces/nft/request'
CREATE_SPACE_LICENSE = '/spaces/create_license'
CREATE_DATA_NFT_REQUEST = '/spaces/nft/request'
CHECK_DATA_NFT_STATUS = '/spaces/<string:wallet_address>/<string:name>/nft'
CREATE_DATA_NFT_REQUEST = '/datasets/request_datanft'
CREATE_DATASET_LICENSE = '/datasets/create_license'
COPY_NFT_REQUEST = '/copynft/request'
COPY_NFT_STATUS = '/copynft/status'