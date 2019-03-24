import argparse

from CesarAlgorithm import CesarAlgorithm
from VernamAlgorithm import VernamAlgorithm
from VigenereAlgorithm import VigenereAlgorithm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='algorithm')
    subparsers.required = True

    cesar = CesarAlgorithm('cesar')
    cesar.register_subparser(subparsers)

    vigenere = VigenereAlgorithm('vigenere')
    vigenere.register_subparser(subparsers)

    vernam = VernamAlgorithm('vernam')
    vernam.register_subparser(subparsers)

    args = parser.parse_args()
    args.parse_func(args)
