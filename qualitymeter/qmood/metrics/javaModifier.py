class JavaModifier:
    def __init__(self):
        self.PRIVATE = False
        self.FINAL = False
        self.STATIC = False

    def setFinalFlag(self, flag):
        self.FINAL = flag

    def setPrivateFlag(self, flag):
        self.FINAL = flag

    def setStaticFlag(self, flag):
        self.STATIC = flag

    def isFinal(self):
        return self.FINAL

    def isPrivate(self):
        return self.PRIVATE

    def isStatic(self):
        return self.STATIC
