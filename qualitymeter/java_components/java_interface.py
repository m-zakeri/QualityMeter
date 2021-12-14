"""
Class for storing java class Interface.
"""
from .java_method import JavaMethod


class JavaInterface:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__methods = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def methods(self):
        return self.__methods

    def add_method(self, identifier):
        method = JavaMethod(identifier)
        self.__methods.append(method)
