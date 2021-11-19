import argparse
from qualitymeter.qmood.extendibility import Extendability


def main():
    print("---Extendability Report---")
    path = 'test/SF110-20130704-src/SF110-20130704-src/4_rif/src/main'
    extendabilityMeter = Extendability(path)


if __name__ == "__main__":
    main()


