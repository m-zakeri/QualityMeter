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
            javaBuiltInParents = []
            for parentName in javaClass.parentNameList():
                if self.classContainer.getJavaClass(parentName):
                    javaClass.addParent(parentName, self.classContainer.getJavaClass(parentName))
                else:
                    javaBuiltInParents.append(parentName)

            for builtInParent in javaBuiltInParents:
                # We exclude inheriting Java built-in classes.
                javaClass.removeParent(builtInParent)

        for javaClass in self.classContainer.javaClassList():
            javaBuiltinInterfaces = []
            for interfaceName in javaClass.interfaceNameList():
                if self.interfaceContainer.getJavaInterface(interfaceName):
                    javaClass.addInterface(interfaceName, self.interfaceContainer.getJavaInterface(interfaceName))
                else:
                    javaBuiltinInterfaces.append(interfaceName)

            for javaBuiltinInterface in javaBuiltinInterfaces:
                javaClass.removeInterface(javaBuiltinInterface)

    def setInterfaceParents(self):
        for javaInterface in self.interfaceContainer.javaInterfaceList():
            javaBuiltinInterfaces = []
            for parentName in javaInterface.parentNameList():
                if self.interfaceContainer.getJavaInterface(parentName):
                    javaInterface.addParent(parentName, self.interfaceContainer.getJavaInterface(parentName))
                else:
                    javaBuiltinInterfaces.append(parentName)

            for builtInParent in javaBuiltinInterfaces:
                javaInterface.removeParent(builtInParent)

    def calcAbstraction(self):
        for stream in FileReader.getFileStreams(self.projectPath):
            listener = self.getListener(stream)
            self.extractJavaClasses(listener)
            self.extractJavaInterfaces(listener)
        self.setClassParents()
        self.setInterfaceParents()
