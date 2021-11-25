"""


"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class CommonListener(JavaParserLabeledListener):
    def __init__(self):
        self.__current_cls = ''
        self.__classes = []
        self.__classes_name = []
        self.__fields_name = []
        self.__methods_name = []

    @property
    def classes(self):
        return self.__classes

    @property
    def classes_name(self):
        return self.__classes_name

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__current_cls = ctx.IDENTIFIER().getText()

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__classes_name.append(self.__current_cls)
        self.__classes.append([self.__current_cls, self.__fields_name, self.__methods_name])
        self.__fields_name = []
        self.__methods_name = []

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        for item in ctx.variableDeclarators().variableDeclarator():
            text = item.variableDeclaratorId().IDENTIFIER().getText()
            self.__fields_name.append(text)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        text = ctx.IDENTIFIER().getText()
        self.__methods_name.append(text)
