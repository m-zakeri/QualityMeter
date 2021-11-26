from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


# listener for NOP metric
class polymorphismListener(JavaParserLabeledListener):

    def __init__(self):
        self.__number_of_polymorphic_methods = 0

    @property
    def get_number_of_extended_classes(self):
        return self.__number_of_polymorphic_methods

    # count the number of polymorphic methods
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # check if method overriding occurs
        if ctx.EXTENDS() is not None or ctx.IMPLEMENTS() is not None:
            self.__number_of_polymorphic_methods += 1

    def enterInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceDeclarationContext):
        # if a class implements an interface
        if ctx.EXTENDS() is not None:
            self.__number_of_polymorphic_methods += 1


if __name__ == '__main__':
    stream = FileStream("your file path", encoding='utf-8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    pars_tree = parser.compilationUnit()
    my_listener = polymorphismListener()
    walker = ParseTreeWalker()
    walker.walk(t=pars_tree, listener=my_listener)
    print("Number of Polymorphic Methods:", my_listener.get_number_of_extended_classes)
