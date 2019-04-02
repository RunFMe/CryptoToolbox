import sys


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
