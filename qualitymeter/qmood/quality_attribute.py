"""
This file contains the creation of the walker for commonListener
"""

from antlr4 import CommonTokenStream, ParseTreeWalker
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.utils.common_listener import CommonListener


class QualityAttribute:
    def __init__(self, stream):
        # create lexer from data stream.
        self.lexer = JavaLexer(stream)
        # create token from lexer.
        self.token_stream = CommonTokenStream(self.lexer)
        # create parser from tokens.
        self.parser = JavaParserLabeled(self.token_stream)
        # create tree from the first rule of the parser.
        self.parse_tree = self.parser.compilationUnit()
        # create Walker
        self.walker = ParseTreeWalker()
        # import common listener to be walked.
        self.common_listener = CommonListener()
        # walk the tree.
        self.walker.walk(self.common_listener, self.parse_tree)
