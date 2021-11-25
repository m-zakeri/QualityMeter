"""


"""

from antlr4 import CommonTokenStream, ParseTreeWalker
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.utils.common_listener import CommonListener


class QualityAttribute:
    def __init__(self, stream):
        self.lexer = JavaLexer(stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = JavaParserLabeled(self.token_stream)
        self.parse_tree = self.parser.compilationUnit()
        self.walker = ParseTreeWalker()

        self.common_listener = CommonListener()
        self.walker.walk(self.common_listener, self.parse_tree)

        print('Classes name: ')
        print(self.common_listener.classes_name)

        print('Classes: ')
        print(self.common_listener.classes)

