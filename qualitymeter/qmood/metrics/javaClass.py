class JavaClass:
    def __init__(self, className=""):
        self.className = className
        self.methods = []
        self.parentClassList = {}
        self.interfaceList = {}

    def setClassName(self, clsName):
        self.className = clsName

    def addMethod(self, method):
        self.methods.append(method)

    def addParent(self, parentName, parentObject=None):
        self.parentClassList[parentName] = parentObject

    def removeParent(self, parentName):
        self.parentClassList.pop(parentName, None)

    def getParent(self, parentName):
        return self.parentClassList.get(parentName)

    def hasParent(self):
        if self.parentClassList:
            return True
        return False

    def addInterface(self, interfaceName, interfaceObject=None):
        self.interfaceList[interfaceName] = interfaceObject

    def removeInterface(self, interfaceName):
        self.interfaceList.pop(interfaceName, None)

    def getInterface(self, interfaceName):
        return self.interfaceList.get(interfaceName)

    def getNumMethods(self):
        return len(self.methods)

    def hasMethod(self, foreinMethod):
        for method in self.methods:
            if method == foreinMethod:
                return True

        if not self.parentClassList:
            return False
        else:
            for parent in self.parentNameList():
                if self.parentClassList[parent] is None:
                    raise ValueError(f"Parent {parent} of Class {self.className} is not Available")
                else:
                    result = self.parentClassList[parent].hasMethod(foreinMethod)
                    if result:
                        return True
        return False

    def parentNameList(self):
        for parentName in self.parentClassList:
            yield parentName

    def parentObjectList(self):
        for parentName in self.parentClassList:
            yield self.parentClassList[parentName]

    def methodList(self):
        for method in self.methods:
            yield method

    def interfaceNameList(self):
        for interfaceName in self.interfaceList:
            yield interfaceName

    def interfaceObjectList(self):
        for interfaceName in self.interfaceList:
            yield self.interfaceList[interfaceName]
