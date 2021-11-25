"""


"""

import glob
from antlr4 import FileStream


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def get_file_stream(file):
        return FileStream(file, encoding='utf-8')

    @classmethod
    def get_path_stream(cls, path, extension):
        for file in glob.glob(path + r'\**\*.' + extension, recursive=True):
            yield cls.get_file_stream(file)
