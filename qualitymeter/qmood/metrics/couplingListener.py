from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

class CouplingListener(JavaParserLabeledListener):
    def __init__(self):
        self.list = []
        self.numClasses = 0
        self.numInterfaces = 0

    def get_coupling_size(self):
        unique_items = []
        for item in self.list:
            if item not in unique_items:
                unique_items.append(item)
        return len(unique_items)

    def getNumClasses(self):
        return self.numClasses

    def getNumInterfaces(self):
        return self.numInterfaces

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.numClasses += 1

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.numInterfaces += 1

    # covering local variable declaration
    def enterLocalVariableDeclaration(self, ctx:JavaParserLabeled.LocalVariableDeclarationContext):
        if ctx.typeType().classOrInterfaceType():
            for token in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.list.append(token.getText())

    # covering new expressions
    def enterExpression4(self, ctx:JavaParserLabeled.Expression4Context):
        # we only count non-primitive new expressions
        if ctx.NEW() and isinstance(ctx.creator().createdName(), JavaParserLabeled.CreatedName0Context):
            for token in ctx.creator().createdName().IDENTIFIER():
                self.list.append(token.getText())

    # covering parameters
    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        if ctx.typeType().classOrInterfaceType():
            for token in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.list.append(token.getText())
