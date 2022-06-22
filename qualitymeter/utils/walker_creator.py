"""
This file contains the creation of the walker for commonListener

"""

from antlr4 import CommonTokenStream, ParseTreeWalker

from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.core.symbols import ProgramSymbolModel
from qualitymeter.utils.file_reader import FileReader


class WalkerCreator:
    def __init__(self, path):
        self.classes = []
        self.interfaces = []
        self.classOrInterface = []
        self.walk(path)

    def walk(self, path):
        streams = FileReader.get_file_streams(path)

        for stream in streams:
            # Create lexer from data stream.
            lexer = JavaLexer(stream)
            # Create token from lexer.
            token_stream = CommonTokenStream(lexer)
            # Create parser from tokens.
            parser = JavaParserLabeled(token_stream)
            # Create a tree from the first rule of the parser.
            parse_tree = parser.compilationUnit()
            # Import common core to be walked.
            listener = ProgramSymbolModel()
            # Create walker
            walker = ParseTreeWalker()
            # Walk the tree.
            walker.walk(listener, parse_tree)
            # Save the tree's classes and interfaces
            self.classes += listener.classes
            self.interfaces += listener.interfaces
        self.classOrInterface = self.classes + self.interfaces

    def find_parent(self, parent):
        return [cls for cls in self.classes if cls.identifier.getText() == parent.identifier]

    def find_implementation(self, implementation):
        for clf in self.classOrInterface:
            if implementation and clf:
                if clf.identifier.getText() == implementation.identifier.getText():
                    return clf

    def intersection(self, lst1, lst2):
        # Use of hybrid method
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3
