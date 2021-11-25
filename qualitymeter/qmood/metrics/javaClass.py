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

    def getInheritedMethodList(self):
        def isDuplicateMethod(method, methodList):
            for m in methodList:
                if m == method:
                    return True
            return False

        if not self.parentClassList and not self.interfaceList:
            return []

        result = []
        for interfaceName, interfaceObject in self.interfaceList.items():
            if not interfaceObject:
                continue

            for iMethod in interfaceObject.methodList():
                if not isDuplicateMethod(iMethod, result):
                    result.append(iMethod)

            inheritedMethods = interfaceObject.getInheritedMethodList()
            for method in inheritedMethods:
                if not isDuplicateMethod(method, result):
                    result.append(method)

        for className, classObject in self.parentClassList.items():
            if not classObject:
                continue

            for method in classObject.methodList():
                if not isDuplicateMethod(method, result):
                    result.append(method)

            inheritedMethods = classObject.getInheritedMethodList()
            for method in inheritedMethods:
                if not isDuplicateMethod(method, result):
                    result.append(method)

        return result
