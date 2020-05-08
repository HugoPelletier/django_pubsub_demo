import abc


class InterfaceBaseService(abc.ABC):

    @abc.abstractmethod
    def create(self) -> None:
        """This method needs to be implemented by classes using this interface"""
