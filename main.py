import argparse
from utils.file_reader import FileReader


def main():
    path = 'test/client'
    for stream in FileReader.getFileStreams(path):
        pass

if __name__ == "__main__":
    main()


