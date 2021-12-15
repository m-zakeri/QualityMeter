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

        for stream in FileReader.getFileStreams(self.projectPath):
            listener = self.getListener(stream)
            self.extractStreamClasses(listener)
            self.extractStreamInterfaces(listener)

        self.setInterfaceParents()
        self.setClassParents()

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
        totalMethodsCanBeOverriden = 0
        for javaClass in self.javaClassContainer.javaClassList():
            inheritedMethods = javaClass.getInheritedMethodList()
            for method in javaClass.methodList():
                isInherited = False
                for iMethod in inheritedMethods:
                    if iMethod == method:
                        isInherited = True
                        break
                if not isInherited and not(
                    method.getModifier().isPrivate()
                    or method.getModifier().isFinal()
                    or method.getModifier().isStatic()
                ):
                    totalMethodsCanBeOverriden += 1

        for javaInterface in self.javaInterfaceContainer.javaInterfaceList():
            inheritedMethods = javaInterface.getInheritedMethodList()
            for method in javaInterface.methodList():
                isInherited = False
                for iMethod in inheritedMethods:
                    if iMethod == method:
                        isInherited = True
                        break
                if not isInherited and not(
                    method.getModifier().isPrivate()
                    or method.getModifier().isFinal()
                    or method.getModifier().isStatic()
                ):
                    totalMethodsCanBeOverriden += 1

        if self.javaClassContainer.getSize() == 0 and self.javaInterfaceContainer.getSize():
            return 0
        return totalMethodsCanBeOverriden / (self.javaClassContainer.getSize() + self.javaInterfaceContainer.getSize())

    def calcInheritence(self):
        sumMetricForClassAndInterface = 0
        for javaClass in self.javaClassContainer.javaClassList():
            inheritedMethods = javaClass.getInheritedMethodList()
            countInherited = len(inheritedMethods)
            countMethods = countInherited

            for method in javaClass.methodList():
                isOverriden = False
                for iMethod in inheritedMethods:
                    if iMethod == method:
                        isOverriden = True
                        break
                if not isOverriden:
                    countMethods += 1

            if countMethods != 0:
                sumMetricForClassAndInterface += countInherited / countMethods

        for javaInterface in self.javaInterfaceContainer.javaInterfaceList():
            inheritedMethods = javaInterface.getInheritedMethodList()
            countInherited = len(inheritedMethods)
            countMethods = countInherited

            for method in javaInterface.methodList():
                isOverriden = False
                for iMethod in inheritedMethods:
                    if iMethod == method:
                        isOverriden = True
                        break
                if not isOverriden:
                    countMethods += 1

            if countMethods != 0:
                sumMetricForClassAndInterface += countInherited / countMethods

        if self.javaClassContainer.getSize() == 0 and self.javaInterfaceContainer.getSize() == 0:
            return 0
        return sumMetricForClassAndInterface / (self.javaClassContainer.getSize() + self.javaInterfaceContainer.getSize())