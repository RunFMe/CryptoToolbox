from CryptoModule import CryptoModule

from utils import read_input, write_output


class VigenereAlgorithm(CryptoModule):
    """
    Implementation of Vigenere Crypto Algorithm. It can encrypt, decrypt texts.
    """

    def _register_arguments(self, parser):
        parser.add_argument('action', choices=['encrypt', 'decrypt'],
                            help='specifies which action to take')
        parser.add_argument('--input', '-i',
                            help='path to input file, stdin used if not '
                                 'provided')
        parser.add_argument('--output', '-o',
                            help='path yo output file, stdout is used if not '
                                 'provided')
        parser.add_argument('--key', '-k', required=True,
                            help='String used as a key for encryption')

    def parse_arguments(self, arguments):
        # read input
        input_text = read_input(arguments.input)

        if not all([char.isalpha() for char in arguments.key]):
            raise ValueError('Key can only contain alphabetical characters')
        shifts = [ord(key_char) - ord('a') for key_char in
                  arguments.key.lower()]
        # process input
        output_text = ''
        if arguments.action == 'encrypt':
            output_text = self.encrypt(input_text, shifts)
        if arguments.action == 'decrypt':
            output_text = self.decrypt(input_text, shifts)

        # write to output file
        write_output(output_text, arguments.output)

    def encrypt(self, input_text, shifts):
        """
        Shifts every alphabetical character by shift.
        :param input_text:
        :param shifts:
        :return encrypted_text:
        """
        output = []
        for i, char in enumerate(input_text):
            output.append(self.shift_char(char, shifts[i % len(shifts)]))

        return ''.join(output)

    def decrypt(self, input_text, shifts):
        """
        Reverses encryption by shifting characters by -shift.
        :param input_text:
        :param shifts:
        :return decrypted_text:
        """
        return self.encrypt(input_text, [-shift for shift in shifts])

    def shift_char(self, char, offset):
        """
        Shifts alphabetical character by offset in cycle preserving whether
        is is capital or not and does nothing on non-alphabetical ones.
        :param char:
        :param offset:
        :return shifted_char:
        """
        if char.isalpha():
            char_num = ord(char.lower()) - ord('a')
            first_char_ord = ord(char) - char_num
            new_char_num = first_char_ord + (char_num + offset) % 26
            return chr(new_char_num)
        else:
            return char
