import sys

from CryptoAlgorithm import CryptoAlgorithm


class VernamAlgorithm(CryptoAlgorithm):
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
        input_bytes = self.read_input_bytes(arguments.input)
        key_bytes= self.read_input_bytes(arguments.key)

        # process input
        if len(input_bytes) != len(key_bytes):
            raise ValueError('input and key should have the same length')
        xored_bytes = self.xor_bytes(input_bytes, key_bytes)

        self.write_output_bytes(xored_bytes, arguments.output)

    def xor_bytes(self, first_bytes, second_bytes):
        """
        Takes two bytes objects, turns them into int and applies xor.
        :param first_bytes:
        :param second_bytes:
        :return xored_bytes:
        """
        first_int = int.from_bytes(first_bytes, sys.byteorder)
        second_int = int.from_bytes(second_bytes, sys.byteorder)

        xored_int = first_int ^ second_int
        output_bytes = xored_int.to_bytes(len(first_bytes), sys.byteorder)

        return output_bytes

    def read_input_bytes(self, input_name):
        """
        Reads input bytes from file input_name or stdin if input_name is None
        :param input_name:
        :return input_bytes:
        """
        # read input bytes
        if input_name is None:
            input_f = sys.stdin.buffer
        else:
            input_f = open(input_name, 'rb')
        input_bytes = input_f.read()
        input_f.close()

        return input_bytes

    def write_output_bytes(self, output, output_name):
        """
        Writes output bytes to output_name file or stdout if output_name is
        None
        :param output:
        :param output_name:
        """
        if output_name is None:
            output_f = sys.stdout.buffer
        else:
            output_f = open(output_name, 'wb+')
        output_f.write(output)
        output_f.close()
