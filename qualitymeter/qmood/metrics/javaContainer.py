"""
class JavaClassContainer:
- this keeps a list of java classes and allows inserting a class,
  deleting a class, and querying for the existence of a class in the container.

class JavaInterfaceContainer:
- this keeps a list of java interfaces and allows inserting an interface,
  deleting an interface, and querying for the existence of an interface in the container.
"""

from .javaClass import JavaClass

class JavaCLassContainer:
    def __init__(self):
        self.container = {}

    def addJavaClass(self, javaClass):
        self.container[javaClass.className] = javaClass

    def getJavaClass(self, className):
        if className in self.container:
            return self.container[className]

    def javaClassList(self):
        for _, javaClass in self.container.items():
            yield javaClass

    def getSize(self):
        return len(self.container)


class JavaInterfaceContaienr:
    def __init__(self):
        self.container = {}

    def addJavaInterface(self, javaInterface):
        self.container[javaInterface.interfaceName] = javaInterface

    def getJavaInterface(self, interfaceName):
        if interfaceName in self.container:
            return self.container[interfaceName]

    def javaInterfaceList(self):
        for _, javaInterface in self.container.items():
            yield javaInterface

    def getSize(self):
        return len(self.container)
