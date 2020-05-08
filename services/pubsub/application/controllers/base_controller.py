from application.exceptions.pubsub import PubSubBaseException


class BaseController:

    # overwrite this property to skip the logger middleware
    bypass_logger_middleware: bool = False

    def error_message_format(self, e: PubSubBaseException) -> str:
        return '{message} ({class_name})'.format(message=e.message, class_name=e.__class__.__name__)
