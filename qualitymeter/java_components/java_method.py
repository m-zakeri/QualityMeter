"""
Java Method component
"""


class JavaMethod:
    def __init__(self, identifier, parameters, modifiers):
        self.__identifier = identifier
        self.__parameters = parameters
        self.__modifiers = modifiers

    @property
    def identifier(self):
        return self.__identifier

    @property
    def parameters(self):
        return self.__parameters

    @property
    def modifiers(self):
        return self.__modifiers
