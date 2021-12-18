"""
Java Method component
"""


class JavaMethod:
    def __init__(self, identifier, parameters_type=[], parameters=[], modifiers=[], variables=[]):
        self.__identifier = identifier
        self.__parameters_type = parameters_type
        self.__parameters = parameters
        self.__modifiers = modifiers
        self.__variables = variables

    @property
    def identifier(self):
        return self.__identifier

    @property
    def parameters_type(self):
        return self.__parameters_type

    @property
    def parameters(self):
        return self.__parameters

    @property
    def modifiers(self):
        return self.__modifiers

    @property
    def variables(self):
        return self.__variables
