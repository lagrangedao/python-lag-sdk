class Task(object):
    def __init__(self, name: str, uuid: str, status: str, leading_job_id,  task_detail_cid: str, created_at, updated_at):
        self.name = name
        self.uuid = uuid
        self.status = status
        self.leading_job_id = leading_job_id
        self.task_detail_cid = task_detail_cid
        self.created_at = created_at
        self.updated_at = updated_at


class Job(object):
    def __init__(self, uuid, status, job_result_uri):
        self.uuid = uuid
        self.status = status
        self.job_result_uri = job_result_uri


class Config(object):
    def __init__(self, name: str, hardware_id: int, hardware: str, hardware_type: str, memory: int, vcpu: int, price_per_hour: float, description: str):
        self.name = name
        self.hardware_id = hardware_id
        self.hardware = hardware
        self.hardware_type = hardware_type
        self.memory = memory
        self.vcpu = vcpu
        self.price_per_hour = price_per_hour
        self.description = description


class Order(object):
    def __init__(self, config: Config, duration: int, region: str):
        self.config = config
        self.duration = duration
        self.region = region


class Space(object):
    def __init__(self, order: Order, name: str, uuid: str, is_public: bool, license: str, expiration_time: str, likes: int, forked_space_uuid: str):
        self.order = order
        self.name = name
        self.uuid = uuid
        self.is_public = is_public
        self.license = license
        self.expiration_time = expiration_time
        self.likes = likes
        self.forked_space_uuid = forked_space_uuid


class SpaceDeployment(object):
    def __init__(self, space: Space, jobs: list[Job], task: Task):
        self.space = space
        self.jobs = jobs
        self.task = task


class Result(object):
    def __init__(self, code: int, msg: str, data: any):
        self.code = code
        self.msg = msg
        self.data = data
