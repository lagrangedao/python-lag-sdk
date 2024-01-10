# API Reference

## Space API

### [Space](swan_lag/model/deployment.py#L54)


| field            | type                       | description                                 |
| ---------------- | -------------------------- | ------------------------------------------- |
| activeOrder      | [Order](#deployment-order) | last deployment order                       |
| name             | string                     | space name                                  |
| uuid             | string                     | space uuid                                  |
| is_public        | int                        | space visible for public, 1: true, 0: false |
| license          | string                     | space license                               |
| status           | string                     | space status                                |
| expiration_time  | string                     | space expiration time                       |
| likes            | int                        | space likes                                 |
| created_at       | string                     | space created at unix string, unit: second  |
| updated_at       | string                     | space updated at unix string, unit: second  |
| task_uuid        | string                     | space last deployed task uuid               |
| last_stop_reason | string                     | space last stop reason                      |

### [Space File](swan_lag/model/space.py#L10)

| field      | type   | description                               |
| ---------- | ------ | ----------------------------------------- |
| name       | string | file name                                 |
| cid        | string | file cid                                  |
| url        | string | file url                                  |
| created_at | string | file created at unix string, unit: second |
| updated_at | string | file updated at unix string, unit: second |

### [Machine Config](swan_lag/model/space.py#L19)

| field                | type        | description             |
| -------------------- | ----------- | ----------------------- |
| hardware_id          | int         | config id               |
| hardware_name        | string      | config name             |
| hardware_type        | string      | config type             |
| hardware_status      | string      | config available status |
| hardware_description | string      | config description      |
| region               | string list | config available region |

### [Deployment Config](swan_lag/model/deployment.py#L32)

| field          | type   | description               |
| -------------- | ------ | ------------------------- |
| name           | string | config name               |
| hardware_id    | int    | config id                 |
| hardware_type  | string | config type               |
| hardware       | string | config hardware           |
| memory         | string | config memory description |
| vcpu           | string | config vcpu description   |
| price_per_hour | string | config price per hour     |
| description    | string | config description        |


### [Deployment Order](swan_lag/model/deployment.py#L44)
| field      | type                                    | description                               |
| ---------- | --------------------------------------- | ----------------------------------------- |
| config     | [Deployment Config](#deployment-config) | deployment config                         |
| duration   | int                                     | deployment duration                       |
| region     | string                                  | deployment region                         |
| created_at | string                                  | file created at unix string, unit: second |
| started_at | int                                     | file created at unix, unit: second        |
| ended_at   | int                                     | file created at unix, unit: second        |


### [Deployment Task](swan_lag/model/deployment.py#L4)

| field           | type   | description                               |
| --------------- | ------ | ----------------------------------------- |
| name            | string | task name                                 |
| uuid            | string | task uuid                                 |
| status          | string | task status                               |
| leading_job_id  | string | task leading job id                       |
| task_detail_cid | string | task detail cid                           |
| created_at      | string | task created at unix string, unit: second |
| updated_at      | string | task created at unix string, unit: second |

### [Deployment Job](swan_lag/model/deployment.py#L15)

| field          | type   | description                                 |
| -------------- | ------ | ------------------------------------------- |
| name           | string | job name                                    |
| uuid           | string | job uuid                                    |
| status         | string | job status                                  |
| job_result_uri | string | job uri                                     |
| job_source_uri | string | job source uri                              |
| bidder_id      | string | job provider id                             |
| build_log      | string | job build log websocket uri                 |
| container_log  | string | job container log websocket uri             |
| duration       | string | job duration                                |
| storage_source | string | job storage source                          |
| hardware       | string | job hardware                                |
| created_at     | string | job created at unix string, unit: second    |
| updated_at     | string | job updated_at at unix string, unit: second |

### [Space Deployment](swan_lag/model/deployment.py#L71)

| field | type                        | description   |
| ----- | --------------------------- | ------------- |
| space | [Space](#space)             | space info    |
| job   | [Job](#deployment-job) list | job list info |
| task  | [Task](#deployment-task)    | task info     |


### [Deployment Payment](swan_lag/model/deployment.py#L88)

| field             | type                       | description                             |
| ----------------- | -------------------------- | --------------------------------------- |
| id                | int                        | payment id                              |
| space_uuid        | string                     | space uuid                              |
| amount            | string                     | payment amount                          |
| chain_id          | string                     | payment chain id                        |
| transaction_hash  | string                     | payment transaction_hash                |
| order             | [Order](#deployment-order) | payment order                           |
| status            | string                     | payment status                          |
| refundable_amount | string                     | payment refundable amount               |
| refund_reason     | string                     | payment refund reason                   |
| denied_reason     | string                     | payment refund denied reason            |
| created_at        | string                     | created at unix string, unit: second    |
| updated_at        | string                     | updated_at at unix string, unit: second |
| ended_at          | string                     | ended_at at unix string, unit: second   |

### [Chain](swan_lag/config.py#L5)

| field | type   | description   |
| ----- | ------ | ------------- |
| id    | int    | chain id      |
| rpc   | string | chain rpc url |