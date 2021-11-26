from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class encapsulationListener(JavaParserLabeledListener):

    """
    This class is a custom listener for Encapsulation (DAM) metric assessment.
    """

    def __init__(self, class_name):
        self.__number_of_private_attrs = 0
        self.__number_of_total_attrs = 0
        self.__class_name = class_name
        self.__is_enter_class = False

    def get_number_of_private_attrs(self):
        return self.__number_of_private_attrs

    def get_number_of_total_attrs(self):
        return self.__number_of_total_attrs

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.__class_name:
            self.__is_enter_class = True

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.__class_name and self.__is_enter_class:
            self.__is_enter_class = False

    def enterFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        if self.__is_enter_class:
            self.__number_of_total_attrs += 1

    def enterClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        modifier_list = ctx.modifier()
        if self.__is_enter_class and len(modifier_list) > 0:
            attr_type_private = modifier_list[0].classOrInterfaceModifier().PRIVATE()
            attr_type_protected = modifier_list[0].classOrInterfaceModifier().PROTECTED()
            
            # increment for private and protected attributes
            if attr_type_private is not None or attr_type_protected is not None:
                self.__number_of_private_attrs += 1
    

if __name__ == "__main__":
    walker = ParseTreeWalker()

    stream = FileStream("test.java", encoding="utf-8")
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parse_tree = parser.compilationUnit()

    listener = encapsulationListener(class_name="DemoClass")
    walker.walk(t=parse_tree, listener=listener)

    data_access_metric = listener.get_number_of_private_attrs() / listener.get_number_of_total_attrs()
    print("DemoClass DAM =", data_access_metric)

    listener = encapsulationListener(class_name="TestClass")
    walker.walk(t=parse_tree, listener=listener)

    data_access_metric = listener.get_number_of_private_attrs() / listener.get_number_of_total_attrs()
    print("TestClass DAM =", data_access_metric)
