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

    # creating the streams of files to be walked by the Understandability class
    streams = FileReader.getFileStreams(arguments.path)
    understandability, coupling, cohesion, design_size, abstraction, \
        encapsulation, polymorphism, complexity = Understandability(streams).get_value()

    # make the table of results to be printed
    table = [["understandability", understandability], ["coupling", coupling], ["cohesion", cohesion],
             ["design_size", design_size], ["abstraction", abstraction], ["encapsulation", encapsulation],
             ["polymorphism", polymorphism], ["complexity", complexity]]
    headers = ["metric name", "value"]

    # printing the results.
    print("\n\n\nThe Project Report For: {0} \n\n".format(arguments.path))
    print(tabulate(table, headers, tablefmt="presto"))
    print("\n\n")


# Taking the arguments from user and starting the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        help='path for project')
    args = parser.parse_args()
    if not args.path:
        parser.print_help()
        sys.exit(1)
    main(args)
