"""
class JavaClass:
- contains the information about a java class. this information include
  class name, the classes it extends, the interfaces it implements and
  the methods it has.
"""


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

    def hasMethod(self, foreignMethod):
        for method in self.methods:
            if method == foreignMethod:
                return True

        for parent in self.parentNameList():
            if self.parentClassList[parent] is None:
                raise ValueError(f"Parent {parent} of Class {self.className} is not Available")
            else:
                result = self.parentClassList[parent].hasMethod(foreignMethod)
                if result:
                    return True

        for interface in self.interfaceNameList():
            if self.interfaceList[interface] is None:
                raise ValueError(f"Parent {interface} of Class {self.className} is not Available")
            else:
                result = self.interfaceList[interface].hasMethod(foreignMethod)
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

    def getAllParents(self):
        allParents = []
        for interfaceName, interfaceObject in self.interfaceList.items():
            if interfaceName not in allParents:
                allParents.append(interfaceName)

            # when interface is a built-in java interface, its object is None
            if not interfaceObject:
                continue

            parentParents = interfaceObject.getAllParents()
            for ancestor in parentParents:
                if ancestor not in allParents:
                    allParents.append(ancestor)

        for className, classObject in self.parentClassList.items():
            if className not in allParents:
                allParents.append(className)

            if not classObject:
                continue

            parentParents = classObject.getAllParents()
            for ancestor in parentParents:
                if ancestor not in allParents:
                    allParents.append(ancestor)
        return allParents
