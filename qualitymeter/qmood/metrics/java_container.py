"""
class JavaClassContainer:
- this keeps a list of java classes and allows inserting a class,
  deleting a class, and querying for the existence of a class in the container.

class JavaInterfaceContainer:
- this keeps a list of java interfaces and allows inserting an interface,
  deleting an interface, and querying for the existence of an interface in the container.
"""

from .java_class import JavaClass

class JavaCLassContainer:
    def __init__(self):
        self.container = {}

    def add_java_class(self, java_class):
        self.container[java_class.class_name] = java_class

    def get_java_class(self, class_name):
        if class_name in self.container:
            return self.container[class_name]

    def java_class_list(self):
        for _, java_class in self.container.items():
            yield java_class

    def get_size(self):
        return len(self.container)


class JavaInterfaceContaienr:
    def __init__(self):
        self.container = {}

    def add_java_interface(self, java_interface):
        self.container[java_interface.interface_name] = java_interface

    def get_java_interface(self, interface_name):
        if interface_name in self.container:
            return self.container[interface_name]

    def java_interface_list(self):
        for _, java_interface in self.container.items():
            yield java_interface

    def get_size(self):
        return len(self.container)
