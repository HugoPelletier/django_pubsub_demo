import json
import time
from datetime import datetime

import math
from json import JSONDecodeError

from falcon import Request, Response

from application.controllers.base_controller import BaseController
from configs.vars import REQUEST_ID
from application.utils.logger import LoggerUtils


class LoggerMiddleware:
    def process_request(self, req: Request, resp: Response) -> None:
        resp.set_header('timer', time.time())

    def process_response(self, req: Request, resp: Response, resource: BaseController, _: bool) -> None:

        # check if the controller allow logging
        if resource is not None and resource.bypass_logger_middleware:
            return

        _res_size = 1
        if resp is not None and resp.body is not None:
            _res_size = len(resp.body)

        log = {
            'app': 'pubsub',
            'date': str(datetime.now()),
            'reqId': resp.get_header(REQUEST_ID),
            'resCode': int(resp.status[:3]),
            'resTime': math.ceil((time.time() - float(resp.get_header('timer'))) * 1000),
            'resSize': _res_size,
            'method': req.method,
            'route': req.relative_uri,
            'details': {}
        }

        # if there is an error, add the message to the log
        if self._is_info_response(resp):
            try:
                body = json.loads(resp.body)
                body['payload'] = req.json
            except (TypeError, AttributeError, JSONDecodeError):
                body = {}

            log['details'] = body

            log['level'] = 'error'
            LoggerUtils.error(json.dumps(log))
        else:
            # generate stdout
            log['level'] = 'info'
            log['details'] = req.json
            LoggerUtils.info(json.dumps(log))

    def _is_info_response(self, resp: Response) -> bool:
        """
        Check if the status code is 2** or 308 (POST redirection coming from the Supervisor backward compatibility
        and the service messages endpoint)

        :param resp: Falcon Response object
        :return: bool
        """
        return int(''.join(filter(str.isdigit, resp.status))) not in [200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
                                                                      308] and hasattr(resp, 'body')
