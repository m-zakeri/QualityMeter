"""
class AbstractionListener
- this class extracts java classes and the classes they extend or the interfaces
  they implement.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.qmood.metrics.javaClass import JavaClass
from qualitymeter.qmood.metrics.javaInterface import JavaInterface


class AbstractionListener(JavaParserLabeledListener):
    def __init__(self):
        self.javaClassList = []
        self.javaInterfaceList = []

    def getJavaClassList(self):
        return self.javaClassList

    def getJavaInterfaceList(self):
        return self.javaInterfaceList

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        javaClass = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                javaClass.addParent(parent.getText())

        if ctx.IMPLEMENTS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    javaClass.addInterface(token.getText())
        self.javaClassList.append(javaClass)

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        javaInterface = JavaInterface(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    javaInterface.addParent(token.getText())
        self.javaInterfaceList.append(javaInterface)
