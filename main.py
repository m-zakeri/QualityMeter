import argparse
import sys
from tabulate import tabulate
from qualitymeter.refactoring_opportunities.pushdown_method_identification import DetectPushDownMethod
from utils.file_reader import FileReader
from qualitymeter.qmood.understandability import Understandability
from qualitymeter.qmood.extendibility import Extendability


def analyze_undrestandibility(project_path):
    """
    getting the file address from user and giving back the result in a table

    :param arguments:
    :return:
    """

    # calculating understandability
    understandability, coupling, cohesion, design_size, abstraction, \
        encapsulation, polymorphism, complexity = Understandability(project_path).get_value()

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

def detect_push_down_method(project_path, heuristic, output_name):
    DetectPushDownMethod(project_path, heuristic, output_name)


def main(arguments):
    if arguments.pdmp and arguments.pdmo and 1 <= int(arguments.pdmp) <= 100:
        detect_push_down_method(arguments.path, int(arguments.pdmp), arguments.pdmo)
    if arguments.understandability:
        analyze_undrestandibility(arguments.path)
    if arguments.extendability:
        analyze_extendability(arguments.path)


# Taking the arguments from user and starting the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        help='path for project.')
    parser.add_argument(
        '--pdmp',
        help="(push-down method percent) give a value between 1 to 100 as a percentage to be used as heuristic."
    )
    parser.add_argument(
        '--pdmo',
        help="(push-down method output) the name of the output file."
    )
    parser.add_argument(
        '--understandability',
        help="give this argument to calculate understandabiliy of the project."
    )
    parser.add_argument(
        '--extendability',
        help="give this argument to calculate the extendability of the project."
    )
    args = parser.parse_args()
    if not args.path:
        parser.print_help()
        sys.exit(1)
    main(args)
