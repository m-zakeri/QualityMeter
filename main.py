import argparse
import sys
from tabulate import tabulate
from utils.file_reader import FileReader
from qualitymeter.qmood.understandability import Understandability
from qualitymeter.qmood.extendibility import Extendability


def analyze_undrestandibility(project_path):
    """
    getting the file address from user and giving back the result in a table

    :param arguments:
    :return:
    """

    # creating the streams of files to be walked by the Understandability class
    streams = FileReader.get_file_streams(project_path)
    understandability, coupling, cohesion, design_size, abstraction, \
        encapsulation, polymorphism, complexity = Understandability(streams).get_value()

    # make the table of results to be printed
    table = [["understandability", understandability], ["coupling", coupling], ["cohesion", cohesion],
             ["design_size", design_size], ["abstraction", abstraction], ["encapsulation", encapsulation],
             ["polymorphism", polymorphism], ["complexity", complexity]]
    headers = ["metric name", "value"]

    # printing the results.
    title = "\n\n\nThe Project Report for: {0}\n\n".format(project_path)
    table_result = tabulate(table, headers, tablefmt="presto")
    print(title)
    print(table_result)
    print("\n\n")


def analyze_extendability(project_path):
    extendability_meter = Extendability(project_path)
    extendability_meter.display_result()


def main(arguments):
    analyze_undrestandibility(arguments.path)
    analyze_extendability(arguments.path)


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
