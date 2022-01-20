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
        self.interfaces = []
        self.classOrInterface = []
        self.hierarchies = []

        for stream in streams:
            # Step 1: Create an instance of lexer
            lexer = JavaLexer(stream)
            # Step 2: Convert the input source into a list of tokens
            token_stream = CommonTokenStream(lexer)
            # Step 3: Create an instance of parser
            parser = JavaParserLabeled(token_stream)
            # Step 4: Create parse tree
            parse_tree = parser.compilationUnit()
            # Step 5: Create an instance of listener
            listener = Listener()
            # Step 6: Create an instance of walker
            walker = ParseTreeWalker()
            # Step 7: Traverse parse tree
            walker.walk(listener, parse_tree)
            # Step 7: Save the tree's classes and interfaces
            self.classes += listener.classes
            self.interfaces += listener.interfaces
            self.hierarchies += listener.hierarchies
        self.classOrInterface = self.classes + self.interfaces

    def find_parent(self, parent):
        return [cls for cls in self.classes if cls.identifier.getText() == parent.identifier]

    def find_implementation(self, implementation):
        for clf in self.classOrInterface:
            if implementation and clf:
                if clf.identifier.getText() == implementation.identifier.getText():
                    return clf
