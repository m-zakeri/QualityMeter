"""
class JavaInterface:
- contains the information about a java interface. this information
  includes the interface name, the interfaces it extends, and the list
  of methods that the interface defines.
"""

class JavaInterface:
    def __init__(self, interfaceName=""):
        self.interfaceName = interfaceName
        self.methods = []
        # in java, an interface can extend another interface
        self.parentList = {}

    def addParent(self, parentName, parentObject=None):
        self.parentList[parentName] = parentObject

    def removeParent(self, parentName):
        self.parentList.pop(parentName, None)

    def addMethod(self, method):
        self.methods.append(method)

    def parentNameList(self):
        for parentName in self.parentList:
            yield parentName

    def hasMethod(self, foreignMethod):
        for method in self.methods:
            if method == foreignMethod:
                return True
        for parent in self.parentNameList():
            if self.parentList[parent] is None:
                raise ValueError(f"Parent {parent} of Class {self.interfaceName} is not Available")
            else:
                result = self.parentList[parent].hasMethod(foreignMethod)
                if result:
                    return True
        return False

    def getAllParents(self):
        allParents = []
        for parentName, parentObject in self.parentList.items():
            if parentName not in allParents:
                allParents.append(parentName)

            if not parentObject:
                continue

            parentParents = parentObject.getAllParents()
            for ancestor in parentParents:
                if ancestor not in allParents:
                    allParents.append(ancestor)

        return allParents
