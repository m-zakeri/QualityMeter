"""
This file contains the creation of the walker for commonListener

"""

from antlr4 import CommonTokenStream, ParseTreeWalker

from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.utils.common_listener import CommonListener


class QualityAttribute:
    def __init__(self, stream):
        # Create lexer from data stream.
        self.lexer = JavaLexer(stream)
        # Create token from lexer.
        self.token_stream = CommonTokenStream(self.lexer)
        # Create parser from tokens.
        self.parser = JavaParserLabeled(self.token_stream)
        # Create tree from the first rule of the parser.
        self.parse_tree = self.parser.compilationUnit()
        # Create walker
        self.walker = ParseTreeWalker()
        # Import common listener to be walked.
        self.common_listener = CommonListener()
        # Walk the tree.
        self.walker.walk(self.common_listener, self.parse_tree)
