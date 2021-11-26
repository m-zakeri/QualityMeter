"""
A Listener class to calculate number of method.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Complexity(JavaParserLabeledListener):
    def __init__(self):
        self.__result = 0

    # creating property for result.
    @property
    def result(self):
        return self.__result

    # counting method
    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        """
        Add to result for each method.

        :param ctx:
        :return:
        """
        self.__result += 1


