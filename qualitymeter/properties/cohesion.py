"""


"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Cohesion(JavaParserLabeledListener):
    def __init__(self, classes):
        self.__classes = classes
        self.__skip = False
        self.__invoked = {}
        self.__counter = 0
        self.__counted = []
        self.__result = []

    @property
    def result(self):
        return self.__result

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if len(self.__classes[self.__counter][1]) == 0 or len(self.__classes[self.__counter][2]) == 0:
            self.__result.append(0.0)
            self.__skip = True
            return

        for text in self.__classes[self.__counter][1]:
            self.__invoked[text] = 0

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.__skip:
            self.__skip = False
            return

        r = 0
        for item in self.__invoked:
            r += self.__invoked.get(item) / len(self.__classes[self.__counter][2])

        cc = r / len(self.__classes[self.__counter][1])
        self.__result.append(cc)

        self.__counter += 1
        self.__invoked = {}

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.__skip:
            return

        self.__counted = []

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        if self.__skip:
            return

        text = ctx.IDENTIFIER().getText()
        if text in self.__classes[self.__counter][1] and text not in self.__counted:
            self.__counted.append(text)
            self.__invoked[text] += 1
