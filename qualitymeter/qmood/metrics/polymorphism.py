from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .polymorphismListener import PolymorphismListener
from .javaContainer import JavaCLassContainer, JavaInterfaceContaienr

class Polymorphism:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.javaClassContainer = JavaCLassContainer()
        self.javaInterfaceContainer = JavaInterfaceContaienr()

    def getListener(self, stream):
        lexer = JavaLexer(stream)
        tokenStream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokenStream)
        parser.getTokenStream()
        parseTree = parser.compilationUnit()

        listener =PolymorphismListener()
        walker = ParseTreeWalker()
        walker.walk(t=parseTree, listener=listener)
        return listener

    def extractStreamClasses(self, listener):
        javaClassList = listener.getClassList()
        for javaClass in javaClassList:
            self.javaClassContainer.addJavaClass(javaClass)

    def extractStreamInterfaces(self, listener):
        javaInterfaceList = listener.getInterfaceList()
        for javaInterface in javaInterfaceList:
            self.javaInterfaceContainer.addJavaInterface(javaInterface)

    def setClassParents(self):
        for javaClass in self.javaClassContainer.javaClassList():
            javaBuiltInParents = []
            for parentName in javaClass.parentNameList():
                if self.javaClassContainer.getJavaClass(parentName):
                    javaClass.addParent(parentName, self.javaClassContainer.getJavaClass(parentName))
                else:
                    javaBuiltInParents.append(parentName)

            for builtInParent in javaBuiltInParents:
                # We exclude inheriting Java built-in classes.
                javaClass.removeParent(builtInParent)

        for javaClass in self.javaClassContainer.javaClassList():
            javaBuiltinInterfaces = []
            for interfaceName in javaClass.interfaceNameList():
                if self.javaInterfaceContainer.getJavaInterface(interfaceName):
                    javaClass.addInterface(interfaceName, self.javaInterfaceContainer.getJavaInterface(interfaceName))
                else:
                    javaBuiltinInterfaces.append(interfaceName)

            for javaBuiltinInterface in javaBuiltinInterfaces:
                javaClass.removeInterface(javaBuiltinInterface)

    def setInterfaceParents(self):
        for javaInterface in self.javaInterfaceContainer.javaInterfaceList():
            javaBuiltinInterfaces = []
            for parentName in javaInterface.parentNameList():
                if self.javaInterfaceContainer.getJavaInterface(parentName):
                    javaInterface.addParent(parentName, self.javaInterfaceContainer.getJavaInterface(parentName))
                else:
                    javaBuiltinInterfaces.append(parentName)

            for builtInParent in javaBuiltinInterfaces:
                javaInterface.removeParent(builtInParent)


    def calcPolymorphism(self):
        for stream in FileReader.getFileStreams(self.projectPath):
            listener = self.getListener(stream)
            self.extractStreamClasses(listener)
            self.extractStreamInterfaces(listener)

        self.setInterfaceParents()
        self.setClassParents()

        countMethods = 0
        countOverLoaded = 0
        for javaClass in self.javaClassContainer.javaClassList():
            if not javaClass.hasParent():
                countMethods += javaClass.getNumMethods()
                continue

            for method in javaClass.methodList():
                for parentClass in javaClass.parentObjectList():
                    if parentClass.hasMethod(method):
                        countOverLoaded += 1
                        countMethods += 1

        print("total number of methods = ", countMethods, "number of overloaded methods = ", countOverLoaded)
