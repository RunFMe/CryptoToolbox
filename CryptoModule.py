from abc import ABC, abstractmethod


class CryptoModule(ABC):
    """
    Parent class for all algorithms.
    To add algorithm create a child class and implement functions
    _register_arguments and parse_arguments.
    """

    def __init__(self, name):
        self.__name__ = name
        self.supports_visual = False

    def register_subparser(self, subparsers):
        """
        Adds argument handler function and subparser which has a name of the
        instance.
        :param subparsers:
        :return:
        """
        cesar_parser = subparsers.add_parser(self.name)
        self._register_arguments(cesar_parser)
        cesar_parser.set_defaults(parse_func=self.parse_arguments)

    @abstractmethod
    def _register_arguments(self, parser):
        """
        Adds arguments required by the algorithm to a parser
        :param parser:
        :return:
        """
        pass

    @abstractmethod
    def parse_arguments(self, arguments):
        """
        The main function of the algorithm which gets called after parsing
        arguments
        :param arguments:
        :return:
        """
        pass
