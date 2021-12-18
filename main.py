import sys
import argparse
from qualitymeter.qmood.extendibility import Extendability


def main(args):
    print("---Extendability Report---")
    path = args.dir
    extendabilityMeter = Extendability(path)
    print(extendabilityMeter.get_extendability_measure())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Measures quality factors of a java project')
    parser.add_argument(
        '--dir',
        help='the directory in which program source code is located')
    args = parser.parse_args()
    if not args.dir:
        parser.print_help()
        sys.exit(1)
    main(args)
