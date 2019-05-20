from abc import ABCMeta, abstractmethod

from utils import ConfigParser


class CryptoModule(metaclass=ABCMeta):
    """
    Parent class for all algorithms.
    To add algorithm create a child class and implement functions
    _register_arguments and parse_arguments.
    """

    def __init__(self, name, config_file):
        self.__name__ = name
        self.config = ConfigParser(config_file)
        self.supports_visual = False

    def register_subparser(self, subparsers):
        """
        Adds argument handler function and subparser which has a name of the
        instance.
        :param subparsers:
        :return:
        """
        subparser = subparsers.add_parser(self.__name__)
        for argument_options in self.config.arguments:
            names = argument_options['names']
            del argument_options['names']

            subparser.add_argument(*names, **argument_options)
        subparser.set_defaults(parse_func=self.parse_arguments)

    @abstractmethod
    def parse_arguments(self, arguments):
        """
        The main function of the algorithm which gets called after parsing
        arguments
        :param arguments:
        :return:
        """
