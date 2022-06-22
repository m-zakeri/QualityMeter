from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MoveFieldRefactoring(JavaParserLabeledListener):
    def __init__(self):
        self.var = []
        self.allField = {}
        self.className = ''
        self.localParam = []
        self.methodBodyAtt = {}

    @property
    def get_var(self):
        return self.var

    @property
    def get_allField(self):
        return self.allField

    @property
    def get_methodBodyAtt(self):
        return self.methodBodyAtt

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.var = []
        self.className = ctx.IDENTIFIER().getText()

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.var.append((ctx.typeType().getText(), ctx.variableDeclarators().getText()))

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        self.localParam.append(ctx.getText())

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.allField[self.className] = self.var
        self.methodBodyAtt[self.className] = self.localParam
        self.var = []
        self.localParam = []
