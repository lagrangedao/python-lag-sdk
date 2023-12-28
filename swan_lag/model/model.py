
class CreateSpace:
    def __init__(self, name: str, is_public: bool, space_license: str, sdk: str, hours: int):
        self.name = name
        self.is_public = is_public
        self.space_license = space_license
        self.sdk = sdk
        self.hours = hours

    def to_dict(self):
        return {
            "name": self.name,
            "is_public": self.is_public,
            "space_license": self.space_license,
            "sdk": self.sdk,
            "hours": self.hours
        }


class SpaceDeploy:
    def __init__(self, paid: float, space_name: str, cfg_name: str, duration: int, region: str, start_in: int,
                 chain_id: int, tx_hash: str):
        self.paid = paid
        self.space_name = space_name
        self.cfg_name = cfg_name
        self.duration = duration
        self.region = region
        self.start_in = start_in
        self.chain_id = chain_id
        self.tx_hash = tx_hash

    def to_dict(self):
        return {
            "paid": self.paid,
            "space_name": self.space_name,
            "cfg_name": self.cfg_name,
            "duration": self.duration,
            "region": self.region,
            "start_in": self.start_in,
            "chain_id": self.chain_id,
            "tx_hash": self.tx_hash
        }
