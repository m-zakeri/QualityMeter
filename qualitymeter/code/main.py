from antlr4 import *

from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from refactor import ClassCount

import argparse


def main(arg):
    # Step 1: Load input source into stream
    stream = FileStream(arg.file, encoding='utf8')
    # input_stream = StdinStream()
    print('Input stream:')
    print(stream)

    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParserLabeled(token_stream)

    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    # Step 6: Create an instance of AssignmentStListener

   #------------------------------------
    my_listener = ClassCount()
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)
    print('Compiler result:')
    print(f'DSC={my_listener.get_design_size}')


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        '-n', '--file', help='Input source', default=r'AB.java')
    args = argParser.parse_args()
    main(args)
