import json

from falcon import Request, Response, HTTP_202, HTTPUnprocessableEntity, HTTP_412
from application.controllers.base_controller import BaseController

from application.services.message import MessageService

from application.exceptions.pubsub import PubSubBaseException
from configs.vars import REQUEST_ID


class MessagesController(BaseController):
    """
    Handle all the messages that are send by the publishers
    Steps:

    1. Topic Validation (not done)
    2. Message structure validation (not done)
    3. Published messages
    """

    def on_post(self, req: Request, resp: Response) -> Response:

        service = MessageService()

        try:
            service.validate(req)
            msg_guid = service.publish(req)

            # process request and build response
            response = {
                'status': HTTP_202,
                'data': {
                    'msg_guid': msg_guid,
                    'reqId': resp.get_header(REQUEST_ID)
                }
            }

            resp.body = json.dumps(response)
            resp.status = HTTP_202
        except PubSubBaseException as e:
            self.manage_application_exception(e, resp)
        except HTTPUnprocessableEntity as e:
            raise e

    def manage_application_exception(self, e: PubSubBaseException, resp: Response) -> None:
        """
        Manage ApplicationBaseException

        :param e: ApplicationBaseException
        :param resp: Response
        :return: none
        """
        error_code = HTTP_412

        if e.code:
            error_code = e.code

        message = e
        if hasattr(e, 'message'):
            message = self.error_message_format(e)

        resp.status = error_code
        resp.body = json.dumps({
            'status': error_code,
            'message': message
        })
