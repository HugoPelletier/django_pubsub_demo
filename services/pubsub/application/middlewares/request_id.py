import uuid

from falcon import Request, Response

from configs.vars import REQUEST_ID


class RequestIdMiddleware:

    def process_request(self, req: Request, resp: Response) -> None:
        """
        Request Id generator. This is used for the tracing between services
        Check if the request id is part of the header. If not, create a uuid

        :param req: Request
        :param resp: Response
        :return: None
        """

        x_request_id = req.get_header(REQUEST_ID)

        if x_request_id is None:
            _uuid = str(uuid.uuid4())
            req._params[REQUEST_ID] = _uuid
            resp.set_header(REQUEST_ID, _uuid)
        else:
            req._params[REQUEST_ID] = x_request_id
            resp.set_header(REQUEST_ID, x_request_id)
