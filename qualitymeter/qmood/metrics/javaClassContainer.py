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
