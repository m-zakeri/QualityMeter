from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .polymorphismListener import PolymorphismListener
from .javaClassContainer import JavaCLassContainer

class Polymorphism:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.javaClassContainer = JavaCLassContainer()

    def getJavaClasses(self, stream):
        lexer = JavaLexer(stream)
        tokenStream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokenStream)
        parser.getTokenStream()
        parseTree = parser.compilationUnit()

        listener =PolymorphismListener()
        walker = ParseTreeWalker()
        walker.walk(t=parseTree, listener=listener)
        javaClassList = listener.getClassList()
        javaInterfaceList = listener.getInterfaceList()
        for javaClass in javaClassList:
            self.javaClassContainer.addJavaClass(javaClass)

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

    def setInterfaceParents(self):
        pass

    def calcPolymorphism(self):
        for stream in FileReader.getFileStreams(self.projectPath):
            self.getJavaClasses(stream)
        self.setClassParents()
        self.setInterfaceParents()

        countMethods = 0
        countOverLoaded = 0
        for javaClass in self.javaClassContainer.javaClassList():
            if not javaClass.parentList:
                countMethods += javaClass.getNumMethods()
                continue

            for method in javaClass.methodList():
                for parentClass in javaClass.parentObjectList():
                    if parentClass.hasMethod(method):
                        countOverLoaded += 1
                        countMethods += 1

        print("total number of methods = ", countMethods, "number of overloaded methods = ", countOverLoaded)
