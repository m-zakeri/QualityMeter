import os

from antlr4 import *

from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class flexibilityListener(JavaParserLabeledListener):

    def __init__(self):

        # 
        self.__number_of_defined_class_attribute = 0
        self.primitive_types = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']
        self.__instance_variables = []
        self.__local_variables = []
        self.__non_primitive_classes = []
        # 
        self.__parameters_of_method = []
        # 
        self.__number_of_polymorphic_methods = 0
        self.__is_final = None
        self.__current_class_or_interface = None
        # self.__superclasses = {}
        self.__parent_and_child_classes = {}
        self.__subclasses = {}
        self.__list_of_methods = {}
        self.__non_inheritance_tags = ['private', 'static', 'final']
        self.__number_of_classes = 0
        self.__temp_modifier = 0
        # 
        self.last_number_of_private_attrs = 0
        self.__is_entered_class = False
        self.__entered_nested_class = False
        self.total_classes_for_DAM = {}

    @property
    def get_number_of_classes(self):
        return self.__number_of_classes

    @property
    def get_non_primitive_classes(self):
        return self.__non_primitive_classes

    @property
    def get_variables_list(self):
        variables = self.__instance_variables + self.__local_variables
        return variables

    @property
    def get_attributes_for_DCC(self):
        attributes = self.__instance_variables + self.__parameters_of_method
        return attributes

    @property
    def get_number_of_polymorphic_methods(self):
        return self.__number_of_polymorphic_methods

    @property
    def get_methods_and_classes(self):
        return self.__list_of_methods

    @property
    def get_parents_and_children(self):
        return self.__parent_and_child_classes

    @property
    def calculate_NOP(self):
        return self.get_number_of_polymorphic_methods / self.get_number_of_classes

    @property
    def get_DAM_ratio(self):
        """
        This method returns the Data Access Metric ratio.
        Note that it is likely that a class has no attributes,
        so it returns zero to avoid division by zero.
        Args:
            None
        Returns:
            float: DAM ratio
        """

        dams = list(map(lambda key: self.total_classes_for_DAM[key][0] / self.total_classes_for_DAM[key][1] if
        self.total_classes_for_DAM[key][1] != 0 else 0, self.total_classes_for_DAM.keys()))

        DAM_metric = sum(dams) / len(dams)

        return DAM_metric

    def enterClassOrInterfaceModifier(self, ctx: JavaParserLabeled.ClassOrInterfaceModifierContext):
        """Function to check if parser enter class or interface modifier

        Args:
            ctx (JavaParserLabeled.ClassOrInterfaceModifierContext): [description]
        """
        # if class is final
        if ctx.FINAL():
            self.__is_final = True

    def enterModifier(self, ctx: JavaParserLabeled.ModifierContext):
        """Modifier checks the access specifier of methods

        if method is private, static or final add one to the temp
        to avoid counting private, static or final attributes we use temp_modifier
        at the next stage of traverse if walker enters only the methodDeclaration
        remove the temp from the count of total methods

        Args:
            ctx (JavaParserLabeled.ModifierContext): [description]
        """
        # check method potentials
        if ctx.classOrInterfaceModifier() is not None:
            if ctx.classOrInterfaceModifier().getText() in self.__non_inheritance_tags:
                self.__temp_modifier = 1

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        """Check if parser enters the method

        count the total number of methods
        decrease one if method is private, static, or final

        Args:
            ctx (JavaParserLabeled.MethodDeclarationContext): [description]
        """

        if self.__is_final:
            self.__number_of_polymorphic_methods = 0

        else:
            self.__number_of_polymorphic_methods += 1
            self.__number_of_polymorphic_methods -= self.__temp_modifier

        self.__list_of_methods[self.__current_class_or_interface].append(ctx.IDENTIFIER().getText())

    def enterClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        """[summary]

        Args:
            ctx (JavaParserLabeled.ClassBodyDeclaration2Context): [description]
        """

        #
        if not self.__entered_nested_class:
            prv_attrs, tot_attrs = self.total_classes_for_DAM[self.__current_class_or_interface]
            self.last_number_of_private_attrs = 0

            modifier_list = ctx.modifier()
            # check if we are in the intended class and it has any defined attributes
            if len(modifier_list) > 0:
                # getting the name of the private attribute, returns None is there is no private attribute
                attr_type_private = modifier_list[0].classOrInterfaceModifier().PRIVATE()
                # getting the name of the protected attribute, returns None is there is no protected attribute
                attr_type_protected = modifier_list[0].classOrInterfaceModifier().PROTECTED()

                # increment for private and protected attributes
                if attr_type_private is not None or attr_type_protected is not None:
                    self.last_number_of_private_attrs += 1

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """check if parser enters the class

        Args:
            ctx (JavaParserLabeled.ClassDeclarationContext): [description]
        """
        # increase the total number off classes
        self.__number_of_classes += 1
        self.__current_class_or_interface = ctx.IDENTIFIER().getText()
        # create a list of methods for each class
        self.__list_of_methods[self.__current_class_or_interface] = []

        # ignore classes inside another class
        #
        if not self.__is_entered_class:
            # self.__class_name = ctx.IDENTIFIER().getText()
            self.total_classes_for_DAM[self.__current_class_or_interface] = (0, 0)
            self.__is_entered_class = True
            self.__entered_nested_class = False
        else:
            self.__entered_nested_class = True

        #
        # increase the number of non primitive classes
        if ctx.IDENTIFIER().getText() not in self.primitive_types:
            self.__non_primitive_classes.append(ctx.IDENTIFIER().getText())

        #
        # create a list of classes with their parents
        if ctx.EXTENDS() is not None:
            self.__parent_and_child_classes[ctx.IDENTIFIER().getText()] = ctx.typeType().getText()
            self.__subclasses = {ctx.IDENTIFIER().getText()}

        elif ctx.IMPLEMENTS() is not None:
            self.__parent_and_child_classes[ctx.IDENTIFIER().getText()] = ctx.typeList().getText()
            # print(ctx.typeType().getText())
            self.__subclasses = {ctx.IDENTIFIER().getText()}

    #
    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """
        This method ensures that we have left the intended class,
        as this method is called once the walker is leaving a class in the source code.
        Args:
            ClassDeclaration Context
        Returns:
            None
        """

        if not self.__entered_nested_class:
            self.__is_enter_class = False
            self.__entered_nested_class = False

        if self.__is_final:
            self.__is_final = False

    def enterInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceDeclarationContext):
        """check if parser enters the interface

        Args:
            ctx (JavaParserLabeled.InterfaceDeclarationContext): [description]
        """

        self.__number_of_classes += 1

        #
        if not self.__is_entered_class:
            # self.__class_name = ctx.IDENTIFIER().getText()
            self.total_classes_for_DAM[self.__current_class_or_interface] = (0, 0)
            self.__is_entered_class = True
            self.__entered_nested_class = False
        else:
            self.__entered_nested_class = True

        self.__current_class_or_interface = ctx.IDENTIFIER().getText()
        self.__list_of_methods[self.__current_class_or_interface] = []

        # if a class implements an interface
        # create a list of classes with their parents
        if ctx.EXTENDS() is not None:
            self.__parent_and_child_classes[ctx.IDENTIFIER().getText()] = ctx.typeList().getText()
        else:
            self.__current_class_or_interface = ctx.IDENTIFIER().getText()

    #
    def exitInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceDeclarationContext):
        """check if parser enters interface

        Args:
            ctx (JavaParserLabeled.InterfaceDeclarationContext): [description]
        """

        if not self.__entered_nested_class:
            self.__is_enter_class = False
            self.__entered_nested_class = False

    #
    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        """check the fields of class

        Args:
            ctx (JavaParserLabeled.FieldDeclarationContext): [description]
        """
        # count non primitive instance variables
        if ctx.typeType().getText() not in self.primitive_types:
            self.__instance_variables.append(ctx.typeType().getText())

        # count private attributes
        if not self.__entered_nested_class:
            prv_attrs, tot_attrs = self.total_classes_for_DAM[self.__current_class_or_interface]
            prv_attrs = prv_attrs + self.last_number_of_private_attrs
            tot_attrs = tot_attrs + 1
            self.total_classes_for_DAM[self.__current_class_or_interface] = (prv_attrs, tot_attrs)

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        """check the fields of method

        Args:
            ctx (JavaParserLabeled.LocalVariableDeclarationContext): [description]
        """
        # count non primitive local variables
        if ctx.typeType().getText() not in self.primitive_types:
            self.__local_variables.append(ctx.typeType().getText())

    #
    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        """check arguments of method

        Args:
            ctx (JavaParserLabeled.FormalParameterContext): [description]
        """
        # count non primitive method parametes
        if ctx.typeType().getText() not in self.primitive_types:
            self.__parameters_of_method.append(ctx.typeType().getText())


# todo number of overrided methods
def calculate_nom(methods, classes):
    """calculate the number of overridden methods

    Args:
        methods (dict): class with its methods
        classes (dict): class with its parent

    Returns:
        int result: [description]
    """
    res = 0
    if classes:
        for child in classes:
            sup_methods = methods[classes[child]]
            sub_methods = methods[child]
            for m in sub_methods:
                if m in sup_methods:
                    res += 1

    return res


#
def calculate_MOA_or_DCC(variables, classes, noc):
    """Function to calculate MOA and DCC metric

    Args:
        variables (list): [description]
        classes (list): [description]
        noc (int): [description]

    Returns:
        result: [description]
    """

    res = 0
    for i in variables:
        if i in classes:
            res += 1

    return res / noc


def get_all_filenames(walk_dir, valid_extensions):
    """get all files of a directory

    Args:
        walk_dir ([type]): [description]
        valid_extensions ([type]): [description]

    Yields:
        [type]: [description]
    """
    for root, sub_dirs, files in os.walk(walk_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if any([file_name.endswith(extension) for extension in valid_extensions]) and "test" not in file_path:
                yield file_path


if __name__ == '__main__':

    walk_dir = "path\\of\\directory"
    valid_extensions = ['.java']

    NOP_values = []
    DAM_values = []
    MOA_values = []
    DCC_values = []
    NOM_values = []

    for file_name in get_all_filenames(walk_dir, valid_extensions):
        stream = FileStream(file_name, encoding='utf-8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        pars_tree = parser.compilationUnit()
        walker = ParseTreeWalker()
        fl_listener = flexibilityListener()
        walker.walk(t=pars_tree, listener=fl_listener)

        NOP = fl_listener.calculate_NOP
        DAM = fl_listener.get_DAM_ratio
        MOA = calculate_MOA_or_DCC(fl_listener.get_variables_list, fl_listener.get_non_primitive_classes,
                                   fl_listener.get_number_of_classes)
        DCC = calculate_MOA_or_DCC(fl_listener.get_attributes_for_DCC, fl_listener.get_non_primitive_classes,
                                   fl_listener.get_number_of_classes)

        NOP_values.append(NOP)
        # NOM_values.append(calculate_nom(fl_listener.get_methods_and_classes, fl_listener.get_parents_and_children))
        DAM_values.append(DAM)
        MOA_values.append(MOA)
        DCC_values.append(DCC)

        # Uncomment below lines to display metrics for each file
        # print("metrics for " + file_name)
        # print(f"NOP: {NOP} \nDAM: {DAM} \nMOA: {MOA} \nDCC: {DCC} \n")

    if len(NOP_values) == 0:
        NOP = 0
    else:
        NOP = sum(NOP_values) / len(NOP_values)

    if len(DAM_values) == 0:
        DAM = 0
    else:
        DAM = sum(DAM_values) / len(DAM_values)

    if len(MOA_values) == 0:
        MOA = 0
    else:
        MOA = sum(MOA_values) / len(MOA_values)

    if len(DCC_values) == 0:
        DCC = 0
    else:
        DCC = sum(DCC_values) / len(DCC_values)

    # print("Number of Overridden Methods: ", sum(NOM_values))

    result = 0.25 * DAM - 0.25 * DCC + 0.5 * MOA + 0.5 * NOP
    print("Flexibility: ", result)
