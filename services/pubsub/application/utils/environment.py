from application.models.enums.environment import EnvironmentEnum
from configs.vars import ENV


class EnvironmentUtils:

    @staticmethod
    def is_dev(self) -> bool:
        """
        Check if the environment is dev

        :return: bool
        """
        return ENV == EnvironmentEnum.DEV.value
