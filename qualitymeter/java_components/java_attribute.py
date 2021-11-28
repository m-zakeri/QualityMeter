"""
Class for storing java class attributes.
"""


class JavaAttribute:
    def __init__(self, identifier, modifiers):
        self.__identifier = identifier
        self.__modifiers = modifiers

    @property
    def identifier(self):
        return self.__identifier

    @property
    def modifier(self):
        return self.__modifiers
