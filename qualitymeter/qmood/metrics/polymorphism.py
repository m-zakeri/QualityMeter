"""
class Polymorphism:
- measures the value of polymorphism using the structure of classes and interfaces.
  it uses class polymorphismListener to obtain the information needed for classes
  and interfaces.
- when structures became available, for each method in a class, it recursively checks
  for the existence of the method in the parent class itself, or in interfaces that
  the parent class implements.
  it also checks for the existence of the method in interfaces the class itself implements.
  if any of the two cases happened, the method has been overridden, otherwise, it has not.
"""

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
            countMethods += javaClass.getNumMethods()

            for method in javaClass.methodList():
                found = False
                for interface in javaClass.interfaceObjectList():
                    if interface.hasMethod(method):
                        found = True
                        break

                if not found:
                    for parentClass in javaClass.parentObjectList():
                        if parentClass.hasMethod(method):
                            found = True
                            break

                if found:
                    countOverLoaded += 1

        return countOverLoaded
