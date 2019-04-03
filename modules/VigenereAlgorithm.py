from CryptoModule import CryptoModule
from utils import read_input, write_output, Alphabet, en_letters, ru_letters


class VigenereAlgorithm(CryptoModule):
    """
    Implementation of Vigenere Crypto Algorithm. It can encrypt, decrypt texts.
    """

    def __init__(self, name, config_file):
        super().__init__(name, config_file)
        self.alphabet = None

    def parse_arguments(self, arguments):
        if arguments.lang == 'en':
            self.alphabet = Alphabet(en_letters)
        elif arguments.lang == 'ru':
            self.alphabet = Alphabet(ru_letters)

        # read input
        input_text = read_input(arguments.input)

        # process input
        try:
            action = getattr(self, arguments.action + '_action')
        except AttributeError:
            raise NotImplementedError("Action {0} is not implemented. You have"
                                      "to add method {0}_action"
                                      .format(arguments.action))

        output_text = action(input_text, arguments)

        # write to output file
        write_output(output_text, arguments.output)

    def encrypt_action(self, input_text, arguments):
        shifts = self.get_shifts(arguments.key)
        return self.encrypt(input_text, shifts)

    def decrypt_action(self, input_text, arguments):
        shifts = self.get_shifts(arguments.key)
        return self.decrypt(input_text, shifts)

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
        Shifts character from alphabet by offset in cycle preserving whether
        is is capital or not and does nothing on non-alphabetical ones.
        :param char:
        :param offset:
        :return shifted_char:
        """
        if char.lower() in self.alphabet:
            char_index = self.alphabet.index(char.lower())
            shifted_index = self.shift_index(char_index, offset)
            shifted_char = self.alphabet[shifted_index]

            return shifted_char if char.islower() else shifted_char.upper()
        else:
            return char

    def shift_index(self, alph_index, offset):
        """
        Returns alphabet index of character shifted in cycle by offset.
        :param alph_index:
        :param offset:
        :return:
        """
        return (alph_index + offset) % len(self.alphabet)

    def get_shifts(self, key):
        """
        Transforms string into array of character positions in english alphabet
        :param key:
        :return:
        """
        if not all([char in self.alphabet for char in key.lower()]):
            raise ValueError('Key can only contain characters from selected'
                             ' alphabet')
        shifts = [self.alphabet.index(char) for char in key.lower()]

        return shifts
