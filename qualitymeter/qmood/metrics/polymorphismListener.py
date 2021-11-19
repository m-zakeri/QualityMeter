from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import *
from .javaClass import JavaClass

class PolymorphismListener(JavaParserLabeledListener):
    def __init__(self):
        self.javaClassList = []
        self.currentJavaClass = None


    @property
    def getClassList(self):
        return self.javaClassList


    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.currentJavaClass = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.currentJavaClass.addParent(parent.getText())
        self.javaClassList.append(self.currentJavaClass)


    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.currentJavaClass = None


    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        pass
