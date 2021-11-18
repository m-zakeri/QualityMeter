import argparse
from qualitymeter.qmood.extendibility import Extendability


def main():
    extendabilityMeter = Extendability('test/client')
    print("---Extendability Report---")


if __name__ == "__main__":
    main()


