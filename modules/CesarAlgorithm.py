from collections import Counter
from math import log

from modules.VigenereAlgorithm import VigenereAlgorithm


class CesarAlgorithm(VigenereAlgorithm):
    """
    Implementation of Cesar Crypto Algorithm. It can encrypt, decrypt and hack
    codes by matching character distributions between train text and encrypted
    text.
    """

    def _register_arguments(self, parser):
        parser.add_argument('action', choices=['encrypt', 'decrypt', 'hack'],
                            help='specifies which action to take')
        parser.add_argument('--input', '-i',
                            help='path to input file, stdin used if not '
                                 'provided')
        parser.add_argument('--output', '-o',
                            help='path to output file, stdout is used if not '
                                 'provided')
        parser.add_argument('--shift', '-s', type=int,
                            help='shift used for encryption, required for '
                                 'actions encrypt and decrypt')
        parser.add_argument('--train', '-t',
                            help='path to a file which will be used to '
                                 'calculate model character distribution for '
                                 'statistical analysis, required for hack '
                                 'action')
        parser.add_argument('--lang', '-l', choices=['en', 'ru'], default='en',
                            help='Which language letters to encode')

    def encrypt_action(self, input_text, arguments):
        return self.encrypt(input_text, [arguments.shift])

    def decrypt_action(self, input_text, arguments):
        return self.decrypt(input_text, [arguments.shift])

    def hack_action(self, input_text, arguments):
        if arguments.train is None:
            raise ValueError('Train text was not provided. It is required '
                             'for hack option.')
        with open(arguments.train, 'r') as f:
            train_text = f.read()

        return self.hack(input_text, train_text)

    def hack(self, input_text, train_text):
        """
        Approximates shift which was used to encrypt the text and decrypts it.
        :param input_text:
        :param train_text:
        :return decrypted_text:
        """
        best_shift = self.finds_best_shift(input_text, train_text)
        return self.decrypt(input_text, [best_shift])

    def calc_divergence(self, train_distr, input_distr):
        """
        Finds Kullback-leibler divergence over characters that appear in both
        distribution.
        :param train_distr:
        :param input_distr:
        :return divergence:
        """
        divergence = 0

        for index in range(len(self.alphabet)):
            if input_distr[index] == 0.0 or train_distr[index] == 0.0:
                continue

            divergence += train_distr[index] * log(
                train_distr[index] / input_distr[index])

        return divergence

    def calc_distribution(self, text):
        """
        Finds probability distribution for alphabetic characters. Text is
        lowercased before calculations.
        :param text:
        :return char_distribution:
        """
        counter = Counter(text.lower())

        # put number of alphabetic characters in dict
        distribution = {index: counter.get(char, 0.0) for index, char
                        in enumerate(self.alphabet)}

        # normalise values in dict to get real distribution
        # num_alpha is set to 1 in case there was no alphabetical characters in
        # text to prevent division by zero errors
        num_alpha = max(sum(distribution.values()), 1)
        distribution = {key: value / num_alpha for key, value in
                        distribution.items()}

        return distribution

    def finds_best_shift(self, input_text, train_text):
        """
        Finds best shift which minimizes kullback-leibler divergence between
        decoded text and train text alphabetic symbol distributions.
        :param input_text:
        :param train_text:
        :return best_shift:
        """
        train_distr = self.calc_distribution(input_text)
        input_distr = self.calc_distribution(train_text)

        best_shift = None
        min_divergence = None
        for shift in range(len(self.alphabet)):
            shifted_input_distr = {self.shift_index(index, shift): prob for
                                   index, prob in input_distr.items()}
            divergence = self.calc_divergence(train_distr, shifted_input_distr)

            if min_divergence is None or divergence < min_divergence:
                best_shift = shift
                min_divergence = divergence

        return best_shift
