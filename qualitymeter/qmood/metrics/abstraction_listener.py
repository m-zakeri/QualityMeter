"""
class AbstractionListener
- this class extracts java classes and the classes they extend or the interfaces
  they implement.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.qmood.metrics.java_class import JavaClass
from qualitymeter.qmood.metrics.java_interface import JavaInterface


class AbstractionListener(JavaParserLabeledListener):
    def __init__(self):
        self.java_class_list = []
        self.java_interface_list = []

    def get_java_class_list(self):
        return self.java_class_list

    def get_java_interface_list(self):
        return self.java_interface_list

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        java_class = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                java_class.add_parent(parent.getText())

        if ctx.IMPLEMENTS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    java_class.addInterface(token.getText())
        self.java_class_list.append(java_class)

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        java_interface = JavaInterface(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for interface in ctx.typeList().typeType():
                for token in interface.classOrInterfaceType().IDENTIFIER():
                    java_interface.add_parent(token.getText())
        self.java_interface_list.append(java_interface)
