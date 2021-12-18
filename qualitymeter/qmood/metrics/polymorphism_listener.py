"""
class PolymorphismListener:
- Extracts the structure of a class that contains the classes it extends, the interfaces it implements
  and its methods.
- Extracts the structure of an interface that contains the interfaces it extends, and its methods.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import *
from .java_interface import JavaInterface
from .java_class import JavaClass
from .java_method import JavaMethod
from .java_modifier import JavaModifier


class PolymorphismListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_list = []
        self.interface_list = []

        self.current_class = None
        self.current_interface = None

        self.class_modifier_stack = []
        self.classStack = []

        self.interface_modifier_stack = []
        self.interface_stack = []

    def get_class_list(self):
        assert(len(self.class_modifier_stack) == 0)
        return self.class_list

    def get_interface_list(self):
        return self.interface_list

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.current_class = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.current_class.add_parent(parent.getText())

        if ctx.IMPLEMENTS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    self.current_class.addInterface(token.getText())

        self.class_list.append(self.current_class)
        self.classStack.append(self.current_class)

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.classStack.pop()
        if self.classStack:
            self.current_class = self.classStack[-1]
        else:
            self.current_class = None

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
                    modifier.set_private_flag(True)
                if m.classOrInterfaceModifier().FINAL():
                    modifier.set_final_flag(True)
                if m.classOrInterfaceModifier().STATIC():
                    modifier.set_static_flag(True)
        self.class_modifier_stack.append(modifier)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.class_modifier_stack:
            raise Exception("modifier stack for method is empty. this should not happen")

        method_modifier = self.class_modifier_stack[-1]
        self.class_modifier_stack.pop()
        # a method may be out of a class, in an enum for example. we only care about methods inside a class.
        if not self.current_class:
            return

        java_method = JavaMethod(ctx.IDENTIFIER().getText())
        java_method.set_parameter_list(ctx.formalParameters().formalParameterList())
        java_method.set_modifier(method_modifier)
        self.current_class.add_method(java_method)

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.current_interface = JavaInterface(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    self.current_interface.add_parent(token.getText())
        self.interface_list.append(self.current_interface)
        self.interface_stack.append(self.current_interface)

    def enterInterfaceBodyDeclaration(self, ctx:JavaParserLabeled.InterfaceBodyDeclarationContext):
        # we only care about modifiers of methods in interfaces
        if not isinstance(ctx.interfaceMemberDeclaration(), JavaParserLabeled.InterfaceMemberDeclaration1Context):
            return
        modifier = JavaModifier()
        for m in ctx.modifier():
            if m.classOrInterfaceModifier().PRIVATE():
                modifier.set_private_flag(True)
            if m.classOrInterfaceModifier().FINAL():
                modifier.set_final_flag(True)
            if m.classOrInterfaceModifier().STATIC():
                modifier.set_static_flag(True)
        self.interface_modifier_stack.append(modifier)

    def exitInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.interface_stack.pop()
        if self.interface_stack:
            self.current_interface = self.interface_stack[-1]
        else:
            self.current_interface = None

    def enterInterfaceMethodDeclaration(self, ctx:JavaParserLabeled.InterfaceMethodDeclarationContext):
        if not self.interface_modifier_stack:
            raise Exception("modifier stack for method is empty. this should not happen")
        method_modifier = self.interface_modifier_stack[-1]
        self.interface_modifier_stack.pop()

        java_method = JavaMethod(ctx.IDENTIFIER().getText())
        java_method.set_parameter_list(ctx.formalParameters().formalParameterList())
        java_method.set_modifier(method_modifier)
        self.current_interface.add_method(java_method)
