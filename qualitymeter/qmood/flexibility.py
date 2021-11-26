from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class encapsulationListener(JavaParserLabeledListener):

    """
    This class is a custom listener for Encapsulation (DAM) metric assessment.
    """

    def __init__(self, class_name):
        """
        This method initializes the object and attributes.

        Args:
            class_name (str): name of the class to investigate

        Returns:
            None
        """

        self.__number_of_private_attrs = 0
        self.__number_of_total_attrs = 0
        self.__class_name = class_name
        self.__is_enter_class = False

    def get_number_of_private_attrs(self):
        """
        This method is the getter of the number of private attributes.

        Args:
            None

        Returns:
            int: number of private attributes
        """

        return self.__number_of_private_attrs

    def get_number_of_total_attrs(self):
        """
        This method is the getter of the number of total attributes,
        including public, private, and protected attributes.

        Args:
            None

        Returns:
            int: number of private attributes
        """

        return self.__number_of_total_attrs

    def get_DAM_ratio(self):
        """
        This method retruns the Data Access Metric ratio.
        Note that it is likely that a class has no attributes,
        so it returns zero to avoid division by zero.

        Args:
            None

        Returns:
            float: DAM ratio
        """

        return self.__number_of_private_attrs / self.__number_of_total_attrs if self.__number_of_total_attrs > 0 else 0

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        """
        This method ensures that we have entered to the intended class,
        by checking the name (identifier) of the class.

        Args:
            ClassDeclaration Context

        Returns:
            None
        """

        if ctx.IDENTIFIER().getText() == self.__class_name:
            self.__is_enter_class = True

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        """
        This method ensures that we have left the intended class,
        as this method is called once the walker is leaving a class in the source code.

        Args:
            ClassDeclaration Context

        Returns:
            None
        """

        if ctx.IDENTIFIER().getText() == self.__class_name and self.__is_enter_class:
            self.__is_enter_class = False

    def enterFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        """
        This method counts the number of attributes, whether it be private, public, or protected.
        Once this is method is called, we increment the number_of_total_attrs by one.

        Args:
            FieldDeclaration Context

        Returns:
            None
        """

        if self.__is_enter_class:
            self.__number_of_total_attrs += 1

    def enterClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        """
        This method counts the number of private and protected attributes.
        Once this is method is called, we increment the number_of_private_attrs by one.

        Args:
            ClassBodyDeclaration2 Context

        Returns:
            None
        """

        modifier_list = ctx.modifier()
        # check if we are in the intented class and it has any defined attributes 
        if self.__is_enter_class and len(modifier_list) > 0:
            # getting the name of the private attribute, returns None is there is no private attribute
            attr_type_private = modifier_list[0].classOrInterfaceModifier().PRIVATE()
            # getting the name of the protected attribute, returns None is there is no protected attribute
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
    print("DemoClass DAM =", listener.get_DAM_ratio())

    listener = encapsulationListener(class_name="TestClass")
    walker.walk(t=parse_tree, listener=listener)
    print("TestClass DAM =", listener.get_DAM_ratio())
