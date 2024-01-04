import json


class JsonDictObject(object):
    def __setattr__(self, key, value):
        if key == '__dict__' and isinstance(value, dict):
            for k, v in value.items():
                if k not in class_key_dict:
                    self.__dict__[k] = v
                    continue

                if isinstance(v, list):
                    cls = class_key_dict[k]
                    data_list = []
                    for data in v:
                        obj = cls()
                        obj.__dict__ = data
                        data_list.append(obj)

                    self.__dict__[k] = data_list
                elif isinstance(v, dict):
                    cls = class_key_dict[k]
                    obj = cls()
                    obj.__dict__ = v
                    self.__dict__[k] = obj
                else:
                    self.__dict__[k] = v
        else:
            self.__dict__[key] = value

    def parse_dict_to_obj(self, data: dict):
        self.__dict__ = data

    def parse_json_to_obj(self, data: str):
        parseData = json.loads(data.strip('\t\r\n'))
        self.__dict__ = parseData


class Task(object):
    def __init__(self, name: str = None, uuid: str = None, status: str = None, leading_job_id=None,  task_detail_cid: str = None, created_at=None, updated_at=None):
        self.name = name
        self.uuid = uuid
        self.status = status
        self.leading_job_id = leading_job_id
        self.task_detail_cid = task_detail_cid
        self.created_at = created_at
        self.updated_at = updated_at


class Job(object):
    def __init__(self, name:str =None, uuid: str = None, status: str = None, job_result_uri: str = None, bidder_id: str = None, build_log: str = None,container_log:str = None,duration: int = None, job_source_uri:str = None,storage_source: str = None,hardware: str = None,created_at: str = None,updated_at: str = None):
        self.name = name
        self.uuid = uuid
        self.status = status
        self.job_result_uri = job_result_uri
        self.job_source_uri = job_source_uri
        self.bidder_id = bidder_id
        self.build_log = build_log
        self.container_log = container_log
        self.duration = duration
        self.storage_source = storage_source
        self.hardware = hardware
        self.created_at = created_at
        self.updated_at = updated_at


class Config(object):
    def __init__(self, name: str = None, hardware_id: int = None, hardware: str = None, hardware_type: str = None, memory: int = None, vcpu: int = None, price_per_hour: float = None, description: str = None):
        self.name = name
        self.hardware_id = hardware_id
        self.hardware = hardware
        self.hardware_type = hardware_type
        self.memory = memory
        self.vcpu = vcpu
        self.price_per_hour = price_per_hour
        self.description = description


class Order(JsonDictObject):
    def __init__(self, config: Config = None, duration: int = None, region: str = None):
        self.config = config
        self.duration = duration
        self.region = region


class Space(JsonDictObject):
    def __init__(self, order: Order = None, name: str = None, uuid: str = None, is_public: bool = None, license: str = None, expiration_time: str = None, likes: int = None, forked_space_uuid: str = None):
        self.activeOrder = order
        self.name = name
        self.uuid = uuid
        self.is_public = is_public
        self.license = license
        self.expiration_time = expiration_time
        self.likes = likes
        self.forked_space_uuid = forked_space_uuid


class SpaceDeployment(JsonDictObject):
    def __init__(self, space: Space = None, jobs: list[Job] = None, task: Task = None):
        self.space: Space = space
        self.job: list[Job] = jobs
        self.task: Task = task

class DeploymentRenewResult(JsonDictObject):
    def __init__(self,jobs: list[Job] = None):
        self.job = jobs


class DeploymentTask(JsonDictObject):
    def __init__(self, task: Task = None):
        self.task = task


class_key_dict = {
    "activeOrder": Order,
    "config": Config,
    "space": Space,
    "task": Task,
    "job": Job,
}
