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
