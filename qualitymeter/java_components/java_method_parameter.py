"""
Class for storing method parameters.
"""


class JavaMethodParameter:
    def __init__(self, identifier, parameter_type):
        self.__identifier = identifier
        self.__type = parameter_type

    @property
    def identifier(self):
        return self.__identifier

    @property
    def parameter_type(self):
        return self.__type
