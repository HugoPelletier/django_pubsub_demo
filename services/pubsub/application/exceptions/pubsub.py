
class PubSubBaseException(BaseException):
    def __init__(self, message: str, code: str = None):
        self.code = code
        self.message = message
