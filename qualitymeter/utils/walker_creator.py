"""
This file contains the creation of the walker for commonListener

"""

from antlr4 import CommonTokenStream, ParseTreeWalker

from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.listener.listener import Listener


class WalkerCreator:
    def __init__(self, streams):
        self.classes = []

        for stream in streams:
            # Create lexer from data stream.
            lexer = JavaLexer(stream)
            # Create token from lexer.
            token_stream = CommonTokenStream(lexer)
            # Create parser from tokens.
            parser = JavaParserLabeled(token_stream)
            # Create a tree from the first rule of the parser.
            parse_tree = parser.compilationUnit()
            # Import common listener to be walked.
            listener = Listener()
            # Create walker
            walker = ParseTreeWalker()
            # Walk the tree.
            walker.walk(listener, parse_tree)
            # Save the tree's classes
            for cls in listener.classes:
                self.classes.append(cls)

    def find_parent(self, parent):
        return [cls for cls in self.classes if cls.identifier.getText() == parent.identifier]
