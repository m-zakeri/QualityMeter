"""
A listener class to calculate encapsulation value.

"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Encapsulation(JavaParserLabeledListener):
    def __init__(self):
        self.__result = 0
        self.__attributes_count = 0
        self.__private_count = 0

    # creating property for result.
    @property
    def result(self):
        return self.__result

    def enterClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        # extracting attributes in classes.
        if isinstance(ctx.memberDeclaration(), JavaParserLabeled.MemberDeclaration2Context):
            for _ in ctx.memberDeclaration().fieldDeclaration().variableDeclarators().variableDeclarator():
                self.__attributes_count += 1
                for i in ctx.modifier():
                    # counting private and protected attributes.
                    if i.classOrInterfaceModifier().getText() == "private" or\
                            i.classOrInterfaceModifier().getText() == "protected":
                        self.__private_count += 1

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        # calculating ratio for private attributes to all attributes.
        if self.__attributes_count != 0:
            self.__result = self.__private_count / self.__attributes_count
        else:
            return 0
