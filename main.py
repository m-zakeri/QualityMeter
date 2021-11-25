"""


"""

from qualitymeter.utils.file_reader import FileReader
from qualitymeter.qmood.understandability import Understandability


def main():
    stream = FileReader.get_file_stream(r'input.java')
    understandability = Understandability(stream).get_value()


if __name__ == '__main__':
    main()
