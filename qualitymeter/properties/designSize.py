"""
A Listener class to calculate design size.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class DesignSize(JavaParserLabeledListener):
    def __init__(self):
        self.__result = 0

    # creating property for result.
    @property
    def result(self):
        return self.__result

    # counting all the classes in file.
    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.__result += 1
