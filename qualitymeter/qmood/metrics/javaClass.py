class JavaClass:
    def __init__(self, className=""):
        self.className = className
        self.methodList = []
        self.parentList = []


    def setClassName(self, clsName):
        self.className = clsName


    def addMethod(self, methodName):
        self.methodList.append(methodName)


    def addParent(self, parent):
        self.parentList.append(parent)
