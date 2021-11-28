"""
A listener class to calculate polymorphism value.

"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Polymorphism(JavaParserLabeledListener):
    def __init__(self):
        self.__result = 0

    @property
    def result(self):
        return self.__result

    def enterAnnotation(self, ctx:JavaParserLabeled.AnnotationContext):
        """

        :param ctx:
        :return:
        """
        for _ in ctx.qualifiedName().IDENTIFIER():
            self.__result += 1

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.__result += 1
