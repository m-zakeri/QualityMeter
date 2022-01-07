"""
Java Class component.
"""
from .java_method import JavaMethod
from .java_attribute import JavaAttribute


class JavaClass:
    def __init__(self, identifier, package_name=None):
        self.__identifier = identifier
        self.__methods = []
        self.__attributes = []
        self.__parents = []
        self.__implementations = []
        self.__children = []
        self.__package_name = package_name
        self.__outer_class = None

    def add_method(self, identifier, parameters_type, parameters, modifier, variables):
        method = JavaMethod(identifier, parameters_type,
                            parameters, modifier, variables)
        self.__methods.append(method)

    def add_attribute(self, datatype, identifier, modifiers):
        attribute = JavaAttribute(datatype, identifier, modifiers)
        self.__attributes.append(attribute)

    def add_parent(self, identifier):
        parent = JavaClass(identifier)
        self.__parents.append(parent)

    def add_implementation(self, identifier):
        implementation = JavaClass(identifier)
        self.__implementations.append(implementation)

    def add_child(self, child):
        self.__children.append(child)

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

    @property
    def package_name(self):
        return self.__package_name

    @property
    def children(self):
        return self.__children

    @outer_class.setter
    def outer_class(self, value):
        self.__outer_class = value
