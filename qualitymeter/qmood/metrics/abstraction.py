"""
class Abstraction
- this class calculates the meter of abstraction by finding the number of parent
  classes for each class. it then returns the average number of parents for each
  class as the metric for Abstraction.
"""


from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .abstractionListener import AbstractionListener
from .javaContainer import JavaCLassContainer, JavaInterfaceContaienr

class Abstraction:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.classContainer = JavaCLassContainer()
        self.interfaceContainer = JavaInterfaceContaienr()

    def getListener(self, stream):
        lexer = JavaLexer(stream)
        tokenStream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokenStream)
        parser.getTokenStream()
        parseTree = parser.compilationUnit()

        listener = AbstractionListener()
        walker = ParseTreeWalker()
        walker.walk(t=parseTree, listener=listener)
        return listener

    def extractJavaClasses(self, listener):
        javaClasses = listener.getJavaClassList()
        for javaClass in javaClasses:
            self.classContainer.addJavaClass(javaClass)

    def extractJavaInterfaces(self, listener):
        javaInterfaces = listener.getJavaInterfaceList()
        for javaInterface in javaInterfaces:
            self.interfaceContainer.addJavaInterface(javaInterface)

    def setClassParents(self):
        for javaClass in self.classContainer.javaClassList():
            for parentName in javaClass.parentNameList():
                if self.classContainer.getJavaClass(parentName):
                    javaClass.addParent(parentName, self.classContainer.getJavaClass(parentName))

        for javaClass in self.classContainer.javaClassList():
            for interfaceName in javaClass.interfaceNameList():
                if self.interfaceContainer.getJavaInterface(interfaceName):
                    javaClass.addInterface(interfaceName, self.interfaceContainer.getJavaInterface(interfaceName))

    def setInterfaceParents(self):
        for javaInterface in self.interfaceContainer.javaInterfaceList():
            for parentName in javaInterface.parentNameList():
                if self.interfaceContainer.getJavaInterface(parentName):
                    javaInterface.addParent(parentName, self.interfaceContainer.getJavaInterface(parentName))

    def calcAbstraction(self):
        for stream in FileReader.getFileStreams(self.projectPath):
            listener = self.getListener(stream)
            self.extractJavaClasses(listener)
            self.extractJavaInterfaces(listener)
        self.setClassParents()
        self.setInterfaceParents()

        totalNumberOfAncestors = 0
        for javaClass in self.classContainer.javaClassList():
            ancestors = javaClass.getAllParents()
            totalNumberOfAncestors += len(ancestors)

        for javaInterface in self.interfaceContainer.javaInterfaceList():
            ancestors = javaInterface.getAllParents()
            totalNumberOfAncestors += len(ancestors)

        if self.classContainer.getSize() == 0 and self.interfaceContainer.getSize() == 0:
            return 0
        return totalNumberOfAncestors / (self.classContainer.getSize() + self.interfaceContainer.getSize())
