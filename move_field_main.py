import argparse
import os.path
import refactoringListener


def main(args):
    refactoringListener.listener(args)


if __name__ == '__main__':

    for dirpath, dirnames, filenames in os.walk("path"):
        for filename in [f for f in filenames if f.endswith(".java")]:
            if filename.endswith('Test.java'):
                continue
            else:
                argparser = argparse.ArgumentParser()
                print("path: ", end="")
                print(os.path.join(dirpath, filename))
                argparser.add_argument(
                    '-n', '--file',
                    help='Input source', default=os.path.join(dirpath, filename))
                args = argparser.parse_args()
                main(args)
