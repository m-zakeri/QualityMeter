"""
class PolymorphismListener:
- Extracts the structure of a class that contains the classes it extends, the interfaces it implements
  and its methods.
- Extracts the structure of an interface that contains the interfaces it extends, and its methods.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import *
from .javaInterface import JavaInterface
from .javaClass import JavaClass
from .javaMethod import JavaMethod
from .javaModifier import JavaModifier


class PolymorphismListener(JavaParserLabeledListener):
    def __init__(self):
        self.classList = []
        self.interfaceList = []

        self.currentClass = None
        self.currentInterface = None

        self.classModifierStack = []
        self.classStack = []

        self.interfaceModifierStack = []
        self.interFaceStack = []

    def getClassList(self):
        assert(len(self.classModifierStack) == 0)
        return self.classList

    def getInterfaceList(self):
        return self.interfaceList

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.currentClass = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.currentClass.addParent(parent.getText())

        if ctx.IMPLEMENTS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    self.currentClass.addInterface(token.getText())

        self.classList.append(self.currentClass)
        self.classStack.append(self.currentClass)

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.classStack.pop()
        if self.classStack:
            self.currentClass = self.classStack[-1]
        else:
            self.currentClass = None

    def enterClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        # we only care about method modifiers of classes
        if not (
            isinstance(ctx.memberDeclaration(), JavaParserLabeled.MemberDeclaration0Context)
            or isinstance(ctx.memberDeclaration(), JavaParserLabeled.MemberDeclaration1Context)
        ):
            return

        modifier = JavaModifier()
        for m in ctx.modifier():
            if m.classOrInterfaceModifier():
                if m.classOrInterfaceModifier().PRIVATE():
                    modifier.setPrivateFlag(True)
                if m.classOrInterfaceModifier().FINAL():
                    modifier.setFinalFlag(True)
                if m.classOrInterfaceModifier().STATIC():
                    modifier.setStaticFlag(True)

        self.classModifierStack.append(modifier)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.classModifierStack:
            raise Exception("modifier stack for method is empty. this should not happen")

        methodModifier = self.classModifierStack[-1]
        self.classModifierStack.pop()
        # a method may be out of a class, in an enum for example. we only care about methods inside a class.
        if not self.currentClass:
            return

        javaMethod = JavaMethod(ctx.IDENTIFIER().getText())
        javaMethod.setParameterList(ctx.formalParameters().formalParameterList())
        javaMethod.setModifier(methodModifier)
        self.currentClass.addMethod(javaMethod)

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.currentInterface = JavaInterface(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    self.currentInterface.addParent(token.getText())
        self.interfaceList.append(self.currentInterface)
        self.interFaceStack.append(self.currentInterface)

    def enterInterfaceBodyDeclaration(self, ctx:JavaParserLabeled.InterfaceBodyDeclarationContext):
        # we only care about modifiers of methods in interfaces
        if not isinstance(ctx.interfaceMemberDeclaration(), JavaParserLabeled.InterfaceMemberDeclaration1Context):
            return
        modifier = JavaModifier()
        for m in ctx.modifier():
            if m.classOrInterfaceModifier().PRIVATE():
                modifier.setPrivateFlag(True)
            if m.classOrInterfaceModifier().FINAL():
                modifier.setFinalFlag(True)
            if m.classOrInterfaceModifier().STATIC():
                modifier.setStaticFlag(True)

        self.interfaceModifierStack.append(modifier)
        assert(len(self.interfaceModifierStack) <= 1)


    def exitInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.interFaceStack.pop()
        if self.interFaceStack:
            self.currentInterface = self.interFaceStack[-1]
        else:
            self.currentInterface = None

    def enterInterfaceMethodDeclaration(self, ctx:JavaParserLabeled.InterfaceMethodDeclarationContext):
        if not self.interfaceModifierStack:
            raise Exception("modifier stack for method is empty. this should not happen")
        methodModifier = self.interfaceModifierStack[-1]
        self.interfaceModifierStack.pop()

        javaMethod = JavaMethod(ctx.IDENTIFIER().getText())
        javaMethod.setParameterList(ctx.formalParameters().formalParameterList())
        javaMethod.setModifier(methodModifier)
        self.currentInterface.addMethod(javaMethod)
