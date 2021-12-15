from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .couplingListener import CouplingListener

class Coupling:
    def __init__(self, projectPath):
        self.projectPath = projectPath

    def getListener(self, stream):
        lexer = JavaLexer(stream)
        tokenStream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokenStream)
        parser.getTokenStream()
        parseTree = parser.compilationUnit()

        listener = CouplingListener()
        walker = ParseTreeWalker()
        walker.walk(t=parseTree, listener=listener)
        return listener

    def calcCoupling(self):
        countCoupling = 0
        totalNumClassesAndInterfaces = 0
        for stream in FileReader.getFileStreams(self.projectPath):
            listener = self.getListener(stream)
            countCoupling += listener.get_coupling_size()
            totalNumClassesAndInterfaces += listener.getNumClasses()
            totalNumClassesAndInterfaces += listener.getNumInterfaces()

        if totalNumClassesAndInterfaces == 0:
            return 0
        return countCoupling / totalNumClassesAndInterfaces
