from application.exceptions.pubsub import PubSubBaseException


class QueueException(PubSubBaseException):
    def __init__(self, message, code: str = None):
        self.code = code
        self.message = message
