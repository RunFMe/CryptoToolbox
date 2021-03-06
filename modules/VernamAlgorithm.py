from CryptoModule import CryptoModule
from utils import read_input, write_output


class VernamAlgorithm(CryptoModule):
    """
    Implementation of Vernam Crypto Algorithm. Takes two files and applies xor
    to their byte representations. To encrypt or decrypt use xor with the
    same key.
    """

    def parse_arguments(self, arguments):
        input_bytes = read_input(arguments.input, use_bytes=True)
        key_bytes = read_input(arguments.key, use_bytes=True)

        # process input
        xored_bytes = self.xor_bytes(input_bytes, key_bytes)

        write_output(xored_bytes, arguments.output, use_bytes=True)

    def xor_bytes(self, input_bytes, key_bytes):
        """
        Takes two bytes objects, turns them into int and applies xor.
        :param input_bytes:
        :param key_bytes:
        :return: xored_bytes
        """
        input_bytes = bytearray(input_bytes)
        key_bytes = bytearray(key_bytes)
        output = bytearray()

        for i in range(len(input_bytes)):
            output.append(input_bytes[i] ^ key_bytes[i % len(key_bytes)])

        return bytes(output)
