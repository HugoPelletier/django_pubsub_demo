import json
from json import JSONDecodeError

from falcon import Request, Response, HTTPBadRequest

from urllib.parse import parse_qsl


class JsonifyMiddleware:

    def process_request(self, req: Request, _: Response) -> None:
        """
        Jsonify the request

        :param req: Request object
        :param _: Response (unused)
        :return None
        """

        req.json = {}

        if req.method.upper() != 'POST':
            return

        if req.content_type is not None and 'multipart/form-data' in req.content_type:
            req.json = req.params
        elif req.content_type is not None and 'application/json' in req.content_type:
            try:
                body = req.stream.read(req.content_length or 0).decode("utf-8")
                req.json = json.loads(body)
            except (JSONDecodeError, UnicodeDecodeError, ValueError):
                raise HTTPBadRequest('Error', 'Invalid JSON structure. ({})'.format(body))
        elif req.content_type is not None and 'x-www-form-urlencoded' in req.content_type:
            body = req.stream.read(req.content_length or 0).decode("utf-8")
            req.json = dict(parse_qsl(body))
        else:
            raise HTTPBadRequest('Error',
                                 'Unsupported content-type. ({}). Body: {}'.format(
                                     req.content_type, req.stream.read(req.content_length or 0).decode("utf-8")))
