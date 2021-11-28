"""
Java Class component.
"""
from .java_method import JavaMethod
from .java_attribute import JavaAttribute


class JavaClass:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__methods = []
        self.__attributes = []
        self.__parents = []
        self.__implementations = []
        self.__outer_class = None

    def add_method(self, identifier, parameters, modifier):
        method = JavaMethod(identifier, parameters, modifier)
        self.__methods.append(method)

    def add_attribute(self, identifier, modifiers):
        attribute = JavaAttribute(identifier, modifiers)
        self.__attributes.append(attribute)

    def add_parent(self, identifier):
        parent = JavaClass(identifier)
        self.__parents.append(parent)

    def add_implementation(self, identifier):
        implementation = JavaClass(identifier)
        self.__implementations.append(implementation)

    @property
    def identifier(self):
        return self.__identifier

    @property
    def methods(self):
        return self.__methods

    @property
    def attribute(self):
        return self.__attributes

    @property
    def parents(self):
        return self.__parents

    @property
    def implementations(self):
        return self.__implementations

    @property
    def outer_class(self):
        return self.__outer_class

    @outer_class.setter
    def outer_class(self, value):
        self.__outer_class = value
