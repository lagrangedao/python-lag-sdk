from swan_lag.model.deployment import JsonDictObject, Space

class Profile(JsonDictObject):
    def __init__(self, space: list[Space] = None):
        self.space = space


class File(JsonDictObject):
    def __init__(self, name: str = None, cid: str = None, url: str = None, created_at: str = None, updated_at: str = None):
        self.name = name
        self.cid = cid
        self.url = url
        self.created_at = created_at
        self.updated_at = updated_at



class MachineConfig(JsonDictObject):
    def __init__(self,id: int = None, name: str = None, price: str =None, type: str =None, status: str=None, description: str=None, region: list[str] = None):
        self.hardware_id = id
        self.hardware_name = name
        self.hardware_price = price
        self.hardware_type = type
        self.hardware_status = status
        self.hardware_description = description
        self.region = region

class MachineResult(JsonDictObject):
    def __init__(self, hardware: list[MachineConfig] = None):
        self.hardware = hardware




