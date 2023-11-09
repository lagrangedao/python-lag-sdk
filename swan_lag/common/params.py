from swan_lag.common.constants import LAG_TESTNET_API, LAG_MAINNET_API


class Params:
    def __init__(self, is_testnet=False):
        if is_testnet:
            self.LAG_API = LAG_TESTNET_API
        else:
            self.LAG_API = LAG_MAINNET_API

    def get_params(self):

        param_vars = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        param_dict = {}
        for i in param_vars:
            param_dict[i] = getattr(self, i)

        return param_dict

    def __str__(self):
        return self.get_params
