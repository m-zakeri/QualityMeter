import argparse
from qualitymeter.qmood.extendibility import Extendability


def main():
    path = 'test/geometry'
    extendabilityMeter = Extendability(path)
    print("---Extendability Report---")


if __name__ == "__main__":
    main()


