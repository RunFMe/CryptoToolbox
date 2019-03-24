import sys

def read_input_bytes(input_name):
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


def write_output_bytes(output, output_name):
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


def read_input(input_name):
    """
    Reads input from file input_name or stdin if input_name is None
    :param input_name:
    :return input_text:
    """
    # read input bytes
    if input_name is None:
        input_f = sys.stdin
    else:
        input_f = open(input_name, 'r')
    input_bytes = input_f.read()
    input_f.close()

    return input_bytes


def write_output(output, output_name):
    """
    Writes output to output_name file or stdout if output_name is None
    :param output:
    :param output_name:
    """
    if output_name is None:
        output_f = sys.stdout
    else:
        output_f = open(output_name, 'w+')
    output_f.write(output)
    output_f.close()
