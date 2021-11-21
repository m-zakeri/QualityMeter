from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import *
from .javaClass import JavaClass
from .javaMethod import JavaMethod

class PolymorphismListener(JavaParserLabeledListener):
    def __init__(self):
        self.javaClassList = []
        self.currentJavaClass = None
        self.classStack = []


    def getClassList(self):
        return self.javaClassList


    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.currentJavaClass = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.currentJavaClass.addParent(parent.getText())
        self.javaClassList.append(self.currentJavaClass)
        self.classStack.append(self.currentJavaClass)


    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.classStack.pop()
        if self.classStack:
            self.currentJavaClass = self.classStack[-1]
        else:
            self.currentJavaClass = None


    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        javaMethod = JavaMethod(ctx.IDENTIFIER().getText())
        javaMethod.setParameterList(ctx.formalParameters().formalParameterList())
        self.currentJavaClass.addMethod(javaMethod)
