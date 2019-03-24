import sys

from CryptoModule import CryptoModule
from utils import read_input_bytes, write_output_bytes


class VernamAlgorithm(CryptoModule):
    """
    Implementation of Vernam Crypto Algorithm. Takes two files and applies xor
    to their byte representations. To encrypt or decrypt use xor with the
    same key.
    """

    def __init__(self, name):
        super().__init__(name)

    def _register_arguments(self, parser):
        parser.add_argument('--input', '-i',
                            help='path to input file, stdin used if not '
                                 'provided')
        parser.add_argument('--output', '-o',
                            help='path to output file, stdout is used if not '
                                 'provided')
        parser.add_argument('--key', '-k', required=True,
                            help='path to key file, required to encrypt/'
                                 'decrypt')

    def parse_arguments(self, arguments):
        input_bytes = read_input_bytes(arguments.input)
        key_bytes= read_input_bytes(arguments.key)

        # process input
        if len(input_bytes) != len(key_bytes):
            raise ValueError('input and key should have the same length')
        xored_bytes = self.xor_bytes(input_bytes, key_bytes)

        write_output_bytes(xored_bytes, arguments.output)

    def xor_bytes(self, first_bytes, second_bytes):
        """
        Takes two bytes objects, turns them into int and applies xor.
        :param first_bytes:
        :param second_bytes:
        :return xored_bytes:
        """
        first_bytes = bytearray(first_bytes)
        second_bytes = bytearray(second_bytes)
        output = bytearray()

        for byte1, byte2 in zip(first_bytes, second_bytes):
            output.append(byte1 ^ byte2)

        return bytes(output)
