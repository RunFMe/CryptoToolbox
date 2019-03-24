import sys
from collections import Counter
from math import log

from modules.VigenereAlgorithm import VigenereAlgorithm
from utils import read_input, write_output


class CesarAlgorithm(VigenereAlgorithm):
    """
    Implementation of Cesar Crypto Algorithm. It can encrypt, decrypt and hack
    codes by matching character distributions between train text and encrypted
    text.
    """

    def __init__(self, name):
        super().__init__(name)

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

    def parse_arguments(self, arguments):
        # read input
        input_text = read_input(arguments.input)

        # process input
        output_text = ''
        if arguments.action == 'encrypt':
            output_text = self.encrypt(input_text, [arguments.shift])
        if arguments.action == 'decrypt':
            output_text = self.decrypt(input_text, [arguments.shift])
        if arguments.action == 'hack':
            if arguments.train is None:
                raise ValueError('Train text was not provided. It is required '
                                 'for hack option.')
            with open(arguments.train, 'r') as f:
                train_text = f.read()
            output_text = self.hack(input_text, train_text)

        # write to output file
        write_output(output_text, arguments.output)

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

        for char in self.lower_alphas():
            if input_distr[char] == 0.0 or train_distr[char] == 0.0:
                continue

            divergence += train_distr[char] * log(
                train_distr[char] / input_distr[char])

        return divergence

    def calc_distribution(self, text):
        """
        Finds probability distribution for alphabetic characters. Text is
        lowercased before calculations.
        :param text:
        :return char_distribution:
        """
        counter = Counter(text.lower())
        distribution = {}

        # put number of alphabetic characters in dict
        for char in self.lower_alphas():
            distribution[char] = counter.get(char, 0.0)

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
        for shift in range(0, 26):
            shifted_input_distr = {self.shift_char(char, shift): prob for
                                   char, prob in input_distr.items()}
            divergence = self.calc_divergence(train_distr, shifted_input_distr)

            if min_divergence is None or divergence < min_divergence:
                best_shift = shift
                min_divergence = divergence

        return best_shift

    def lower_alphas(self):
        """
        Returns list of all lowercase characters
        :return lowercase_list:
        """
        return [chr(i) for i in range(ord('a'), ord('a') + 26)]
