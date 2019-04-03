import json
import os.path as path
import string
import sys


class Alphabet(tuple):
    """
    Tuple-like object with improved index function.
    """

    def __new__(cls, letters):
        return super().__new__(cls, letters)

    def __init__(self, letters):
        super().__init__()
        self.indexes = {char: i for i, char in enumerate(letters)}

    def index(self, value, start=None, end=None):
        if start is not None or end is not None:
            raise NotImplementedError
        return self.indexes[value]


class ConfigParser:
    """
    Opens config file and parses arguments from it. Supports parent configs
    whose arguments are concatenated to the child's arguments.
    To specify basic type (int, str, float etc.) include it as string. It will
    be looked for in global scope.
    Config file must be JSON and have the following structure:
    {"arguments":[
            {"names": ['input', 'i'], "help": 'Some help'}
        ]
    "parents": ["parent_config1.json", "parent_config2.json"]
    }
    """

    def __init__(self, filename):
        with open(filename, 'r') as f:
            raw_json = json.load(f)
        if not isinstance(raw_json['arguments'], list):
            raise TypeError

        self.filename = filename
        self.arguments = raw_json['arguments']
        self.resolve_types()
        if 'parents' in raw_json:
            self.append_parents(raw_json['parents'])

    def resolve_types(self):
        """
        If arguments include type, then find it in globals and replace string
        :return:
        """
        for argument_options in self.arguments:
            if 'type' in argument_options:
                type_func = TypeCaster().cast(argument_options['type'])
                argument_options['type'] = type_func

    def append_parents(self, parents):
        if not isinstance(self.arguments, list):
            raise TypeError
        for parent in parents:
            config_dir = path.dirname(self.filename)
            parent_config_path = path.join(config_dir, parent)

            parent_parser = ConfigParser(parent_config_path)
            self.arguments.extend(parent_parser.arguments)


class TypeCaster:
    """
    Singleton used for casting strings to types they encode. Singleton allows
    external modules register new types before parsing their config.
    """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance._mapping = {
                'int': int,
                'float': float,
                'str': str,
            }
        return cls.instance

    def register_type(self, name, func):
        if not isinstance(name, str):
            raise ValueError
        if name in self._mapping:
            raise NameError
        self._mapping[name] = func

    def cast(self, name):
        return self._mapping[name]


def read_input(input_name, use_bytes=False):
    """
    Reads input from file input_name or stdin if input_name is None
    :param input_name:
    :param use_bytes:
    :return input_text:
    """
    # read input bytes
    if input_name is None:
        input_f = sys.stdin.buffer if use_bytes else sys.stdin
    else:
        input_f = open(input_name, 'rb' if use_bytes else 'r')
    input_bytes = input_f.read()
    input_f.close()

    return input_bytes


def write_output(output, output_name, use_bytes=False):
    """
    Writes output to output_name file or stdout if output_name is None
    :param output:
    :param use_bytes:
    :param output_name:
    """
    if output_name is None:
        output_f = sys.stdout.buffer if use_bytes else sys.stdout
    else:
        output_f = open(output_name, 'wb+' if use_bytes else 'w+')
    output_f.write(output)
    output_f.close()


en_letters = string.ascii_lowercase
ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщэюя'
