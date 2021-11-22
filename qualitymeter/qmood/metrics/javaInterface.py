class JavaInterface:
    def __init__(self, interfaceName=""):
        self.interfaceName = interfaceName
        self.methods = []
        # in java, an interface can extend another interface
        self.parentList = {}

    def addParent(self, parentName, parentObject=None):
        self.parentList[parentName] = parentObject

    def addMethod(self, method):
        self.methods.append(method)
