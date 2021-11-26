"""


"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Coupling(JavaParserLabeledListener):
    def __init__(self, classes):
        self.__classes = classes
        self.__current_cls = ''
        self.__dcc = 0
        self.__counted = []
        self.__result = []

    @property
    def result(self):
        return self.__result

    def __calc_dcc(self, ctx):
        ctx = ctx.typeType().classOrInterfaceType()
        
        if ctx is None:
            return
        
        text = ctx.IDENTIFIER(0).getText()
        
        if text != self.__current_cls and text not in self.__counted and text in self.__classes:
            self.__dcc += 1
            self.__counted.append(text)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__current_cls = ctx.IDENTIFIER().getText()
        self.__dcc = 0
        self.__counted = []

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__result.append(self.__dcc)

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.__calc_dcc(ctx)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        ctx = ctx.formalParameters().formalParameterList()

        if ctx:
            for item in ctx.formalParameter():
                self.__calc_dcc(item)
