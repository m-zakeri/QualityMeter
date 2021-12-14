"""
Class for storing java class attributes.
"""


class JavaAttribute:
    def __init__(self, datatype, identifier, modifiers):
        self.__datatype = datatype
        self.__identifier = identifier
        self.__modifiers = modifiers

    @property
    def datatype(self):
        return self.__datatype

    @property
    def identifier(self):
        return self.__identifier

    @property
    def modifier(self):
        return self.__modifiers
