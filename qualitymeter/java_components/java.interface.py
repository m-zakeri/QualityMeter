"""
Class for storing java class Interface.
"""
from javaComponents.java_method import JavaMethod


class JavaInterface:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__methods = []

    @property
    def identifier(self):
        return self.__identifier

    def add_method(self, identifier, parameters, modifier):
        method = JavaMethod(identifier, parameters, modifier)
        self.__methods.append(method)
