"""
class JavaMethod:
- keeps the information about a method defined in java. the information contains
  method name and a list that includes the type of parameters in the order that
  they appear in the method.
- it also overloads the == operator. two methods are equal when they have the
  same method names and an equal number of parameters. when the number of
  parameters is equal, the parameter types should also match. if all of these
  cases happened, then the methods are considered equal.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class JavaMethod:
    def __init__(self, method_name=""):
        self.method_name = method_name
        self.parameter_list = []

    def get_num_of_parameters(self):
        return len(self.parameter_list)

    def set_parameter_list(self, parameter_list):
        if not parameter_list:
            return

        try:
            formal_parameters = parameter_list.formalParameter()
            for parameter in formal_parameters:
                self.parameter_list.append(self.get_type_of_parameter(parameter))
        except AttributeError:
            parameter = parameter_list.lastFormalParameter()
            self.parameter_list.append(self.get_type_of_parameter(parameter))

    def get_type_of_parameter(self, parameter):
        if parameter.typeType().classOrInterfaceType():
            for classOrInterface in parameter.typeType().classOrInterfaceType().IDENTIFIER():
                return classOrInterface.getText()
        if parameter.typeType().primitiveType():
            primitive = parameter.typeType().primitiveType()
            return self.get_primitive_type(primitive)

    def get_primitive_type(self, primitive):
        if primitive.BOOLEAN():
            return primitive.BOOLEAN().getText()
        if primitive.CHAR():
            return primitive.CHAR().getText()
        if primitive.BYTE():
            return primitive.BYTE().getText()
        if primitive.SHORT():
            return primitive.SHORT().getText()
        if primitive.INT():
            return primitive.INT().getText()
        if primitive.LONG():
            return primitive.LONG().getText()
        if primitive.FLOAT():
            return primitive.FLOAT().getText()
        if primitive.DOUBLE():
            return primitive.DOUBLE().getText()

    # if two function signatures are equal, __eq__ returns true
    def __eq__(self, other):
        if other.method_name != self.method_name:
            return False
        if other.get_num_of_parameters() != other.get_num_of_parameters():
            return False

        for parameter in zip(self.parameter_list, other.parameter_list):
            if parameter[0] != parameter[1]:
                return False
        return True

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier
