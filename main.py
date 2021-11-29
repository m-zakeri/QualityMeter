"""
Entry point of the program.

"""

import argparse
import sys
import shutil
from tabulate import tabulate
from qualitymeter.utils.file_reader import FileReader
from qualitymeter.qmood.understandability import Understandability


def main(arguments):
    """
    getting the file address from user and giving back the result in a table

    :param arguments:
    :return:
    """

    # creating the streams of files to be walked by the Undestandability class
    streams = FileReader.getFileStreams(arguments.file)
    understandability, coupling, cohesion, design_size, abstraction, \
        encapsulation, polymorphism, complexity = Understandability(streams).get_value()

    # make the table of results to be printed
    table = [["understandability", understandability], ["coupling", coupling], ["cohesion", cohesion],
             ["design_size", design_size], ["abstraction", abstraction], ["encapsulation", encapsulation],
             ["polymorphism", polymorphism], ["complexity", complexity]]
    headers = ["design metric", "value"]

    # printing the result of the program in the center of the program.
    columns = shutil.get_terminal_size().columns
    print("The Project Report For: {0} \n\n".format(arguments.file).center(columns))
    print(tabulate(table, headers, tablefmt="presto").center(columns))


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
    main()
