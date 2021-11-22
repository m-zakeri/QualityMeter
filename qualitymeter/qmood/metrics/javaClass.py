class JavaClass:
    def __init__(self, className=""):
        self.className = className
        self.methods = []
        self.parentList = {}

    def setClassName(self, clsName):
        self.className = clsName

    def addMethod(self, method):
        self.methods.append(method)

    def addParent(self, parentName, parentObject=None):
        self.parentList[parentName] = parentObject

    def removeParent(self, parentName):
        self.parentList.pop(parentName, None)

    def getParent(self, parentName):
        return self.parentList.get(parentName)

    def getNumMethods(self):
        return len(self.methods)

    def hasMethod(self, foreinMethod):
        for method in self.methods:
            if method == foreinMethod:
                return True

        if not self.parentList:
            return False
        else:
            for parent in self.parentNameList():
                if self.parentList[parent] is None:
                    raise ValueError(f"Parent {parent} of Class {self.className} is not Available")
                else:
                    result = self.parentList[parent].hasMethod(foreinMethod)
                    if result:
                        return True
        return False

    def parentNameList(self):
        for parentName in self.parentList:
            yield parentName

    def parentObjectList(self):
        for parentName in self.parentList:
            yield self.parentList[parentName]

    def methodList(self):
        for method in self.methods:
            yield method
