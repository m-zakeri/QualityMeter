"""
Entry point of the program.

"""

import argparse
import sys
from tabulate import tabulate

from qualitymeter.utils.file_reader import FileReader
from qualitymeter.qmood.understandability import Understandability


def main(arguments):
    """
    getting the file address from user and giving back the result in a table

    :param arguments:
    :return:
    """

    stream = FileReader.get_file_stream(arguments.file)
    understandability, coupling, cohesion, design_size, abstraction, \
        encapsulation, polymorphism, complexity = Understandability(stream).get_value()

    table = [["understandability", understandability], ["coupling", coupling], ["cohesion", cohesion],
             ["design_size", design_size], ["abstraction", abstraction], ["encapsulation", encapsulation],
             ["polymorphism", polymorphism], ["complexity", complexity]]
    headers = ["design metric", "value"]

    print(tabulate(table, headers, tablefmt="presto"))


# Taking the arguments from user and starting the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file',
        help='file address')
    args = parser.parse_args()
    if not args.file:
        parser.print_help()
        sys.exit(1)
    main(args)
