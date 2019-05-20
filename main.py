import argparse

from modules.CesarAlgorithm import CesarAlgorithm
from modules.VernamAlgorithm import VernamAlgorithm
from modules.VigenereAlgorithm import VigenereAlgorithm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='algorithm')
    subparsers.required = True

    cesar = CesarAlgorithm('cesar', 'configs/CesarConfig.json')
    cesar.register_subparser(subparsers)

    vigenere = VigenereAlgorithm('vigenere', 'configs/VigenereConfig.json')
    vigenere.register_subparser(subparsers)

    vernam = VernamAlgorithm('vernam', 'configs/VernamConfig.json')
    vernam.register_subparser(subparsers)

    args = parser.parse_args()
    args.parse_func(args)
