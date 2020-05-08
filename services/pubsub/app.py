from __future__ import annotations
from typing import Any

import falcon
from falcon import Response

from application.controllers.healthcheck import HealthCheckController
from application.utils.logger import LoggerUtils

from application.middlewares.jsonify import JsonifyMiddleware

from application.controllers.messages import MessagesController
from application.middlewares.logger import LoggerMiddleware
from application.middlewares.request_id import RequestIdMiddleware

LoggerUtils.get_instance()

# Elasticsearch
LoggerUtils.info('\x1b[33mStarting API')


# Serializes all error messages as JSON before sending them.
def json_serializer(_, resp: Response, exception: Any):
    resp.body = exception.to_json()


# Falcon
api = falcon.API(middleware=[JsonifyMiddleware(), LoggerMiddleware(), RequestIdMiddleware()])
api.set_error_serializer(json_serializer)

# routes
api.add_route('/health-check', HealthCheckController())
api.add_route('/messages', MessagesController())