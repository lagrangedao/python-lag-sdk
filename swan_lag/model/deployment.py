from swan_lag.model.json_object import *


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
    def __init__(self, name: str = None, uuid: str = None, status: str = None, job_result_uri: str = None, bidder_id: str = None, build_log: str = None, container_log: str = None, duration: int = None, job_source_uri: str = None, storage_source: str = None, hardware: str = None, created_at: str = None, updated_at: str = None):
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
    def __init__(self, config: Config = None, duration: int = None, region: str = None, created_at: str = None, started_at: int = None, ended_at: int = None):
        self.config = config
        self.duration = duration
        self.region = region
        self.created_at = created_at
        self.started_at = started_at
        self.ended_at = ended_at


class Space(JsonDictObject):
    def __init__(self, order: Order = None, name: str = None, uuid: str = None, is_public: bool = None, license: str = None, status: str = None, expiration_time: str = None, likes: int = None, forked_space_uuid: str = None, created_at: str = None, updated_at: str = None, task_uuid: str = None, last_stop_reason: str = None):
        self.activeOrder = order
        self.name = name
        self.uuid = uuid
        self.is_public = is_public
        self.license = license
        self.status = status
        self.expiration_time = expiration_time
        self.likes = likes
        self.forked_space_uuid = forked_space_uuid
        self.created_at = created_at
        self.updated_at = updated_at
        self.task_uuid = task_uuid
        self.last_stop_reason = last_stop_reason


class SpaceDeployment(JsonDictObject):
    def __init__(self, space: Space = None, jobs: list[Job] = None, task: Task = None):
        self.space: Space = space
        self.job: list[Job] = jobs
        self.task: Task = task


class DeploymentRenewResult(JsonDictObject):
    def __init__(self, jobs: list[Job] = None):
        self.job = jobs


class DeploymentTask(JsonDictObject):
    def __init__(self, task: Task = None):
        self.task = task


class DeploymentPayment(JsonDictObject):
    def __init__(self, id: int = None, space_uuid: str = None, amount: str = None, chain_id: int = None, transaction_hash: str = None, order: Order = None, status: str = None, refundable_amount: str = None, refund_reason: str = None, denied_reason: str = None, created_at: str = None, updated_at: str = None, ended_at: str = None):
        self.id = id
        self.space_uuid = space_uuid
        self.amount = amount
        self.chain_id = chain_id
        self.transaction_hash = transaction_hash
        self.order = order
        self.status = status
        self.refundable_amount = refundable_amount
        self.refund_reason = refund_reason
        self.denied_reason = denied_reason
        self.created_at = created_at
        self.updated_at = updated_at
        self.ended_at = ended_at


class DeploymentPaymentsResult(JsonDictObject):
    def __init__(self, payments: list[DeploymentPayment] = None):
        self.payments = payments


class_key_dict["activeOrder"] = Order
class_key_dict["config"] = Config
class_key_dict["space"] = Space
class_key_dict["task"] = Task
class_key_dict["job"] = Job
class_key_dict["payments"] = DeploymentPayment
