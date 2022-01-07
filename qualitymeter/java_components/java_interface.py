"""
Class for storing java class Interface.
"""
from .java_method import JavaMethod


class JavaInterface:
    def __init__(self, identifier, package_name=None):
        self.__identifier = identifier
        self.__package_name = package_name
        self.__methods = []
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def package_name(self):
        return self.__package_name

    @property
    def methods(self):
        return self.__methods

    @property
    def children(self):
        return self.__children

    def add_method(self, identifier):
        method = JavaMethod(identifier)
        self.__methods.append(method)

    def add_child(self, child):
        self.__children.append(child)
