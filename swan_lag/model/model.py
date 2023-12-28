import json
from enum import Enum


class ResponseResult:
    def __init__(self, data=None, message='', status=''):
        self.data = data
        self.message = message
        self.status = status

    def to_dict(self):
        return {
            "data": self.data,
            "message": self.message,
            "status": self.status
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def success(data):
        return ResponseResult(data, '', "success").to_json()

    @staticmethod
    def failed(message: str, status: str):
        return ResponseResult(message=message, status=status).to_json()


class CreateSpaceResult:
    def __init__(self, uuid: str, name: str, status_code: int, create_time: str):
        self.uuid = uuid
        self.name = name
        self.status_code = status_code
        self.create_time = create_time

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "status_code": int(self.status_code),
            "create_time": str(self.create_time)
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class SpaceType(Enum):
    PRIVATE = 0
    PUBLIC = 1


class CreateSpaceParams:
    def __init__(self, name: str, space_type: SpaceType, space_license: str, sdk: str, hours: int):
        self.name = name
        self.is_public = space_type.value
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


class Hardware:
    def __init__(self, hardware_id: int, hardware_name: str, hardware_price: str, status: str, hardware_type: str,
                 description: str, region: list[str]):
        self.id = hardware_id
        self.name = hardware_name
        self.price = hardware_price
        self.status = status
        self.type = hardware_type
        self.description = description
        self.region = region

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "status": self.status,
            "type": self.type,
            "description": self.description,
            "region": self.region
        }


class MachinesConfig:
    def __init__(self, hardwares: list[Hardware]):
        self.hardwares = hardwares

    def to_dict(self):
        return {
            "hardwares": self.hardwares,
        }


