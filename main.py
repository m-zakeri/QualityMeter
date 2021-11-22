import argparse
from qualitymeter.qmood.extendibility import Extendability


def main():
    print("---Extendability Report---")
    path = 'test/geometry'
    extendabilityMeter = Extendability(path)


if __name__ == "__main__":
    main()
