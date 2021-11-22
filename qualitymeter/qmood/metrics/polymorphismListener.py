from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import *
from .javaInterface import JavaInterface
from .javaClass import JavaClass
from .javaMethod import JavaMethod


class PolymorphismListener(JavaParserLabeledListener):
    def __init__(self):
        self.classList = []
        self.interfaceList = []

        self.currentClass = None
        self.currentInterface = None

        self.classStack = []
        self.interFaceStack = []

    def getClassList(self):
        return self.classList

    def getInterfaceList(self):
        return self.interfaceList

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.currentClass = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.currentClass.addParent(parent.getText())
        self.classList.append(self.currentClass)
        self.classStack.append(self.currentClass)

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.classStack.pop()
        if self.classStack:
            self.currentClass = self.classStack[-1]
        else:
            self.currentClass = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        # a method may be out of a class, in an enum for example. we only care about methods inside a class.
        if not self.currentClass:
            return

        javaMethod = JavaMethod(ctx.IDENTIFIER().getText())
        javaMethod.setParameterList(ctx.formalParameters().formalParameterList())
        self.currentClass.addMethod(javaMethod)

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.currentInterface = JavaInterface(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    self.currentInterface.addParent(token.getText())
        self.interfaceList.append(self.currentInterface)
        self.interFaceStack.append(self.currentInterface)

    def exitInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.interFaceStack.pop()
        if self.interFaceStack:
            self.currentInterface = self.interFaceStack[-1]
        else:
            self.currentInterface = None

    def enterInterfaceMethodDeclaration(self, ctx:JavaParserLabeled.InterfaceMethodDeclarationContext):
        javaMethod = JavaMethod(ctx.IDENTIFIER().getText())
        javaMethod.setParameterList(ctx.formalParameters().formalParameterList())
        self.currentInterface.addMethod(javaMethod)
