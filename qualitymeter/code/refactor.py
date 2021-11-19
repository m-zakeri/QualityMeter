from antlr4 import *

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class ClassCount(JavaParserLabeledListener):
    def __init__(self):
        self.__dsc = 0

    @property
    def get_design_size(self):
        return self.__dsc

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__dsc += 1
