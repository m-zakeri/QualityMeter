from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .polymorphismListener import PolymorphismListener

class Polymorphism:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        for stream in FileReader.getFileStreams(projectPath):
            self.calcPolymorphim(stream)

    def calcPolymorphim(self, stream):
        lexer = JavaLexer(stream)
        tokenStream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokenStream)
        parser.getTokenStream()
        parseTree = parser.compilationUnit()

        listener =PolymorphismListener()
        walker = ParseTreeWalker()
        walker.walk(t=parseTree, listener=listener)
