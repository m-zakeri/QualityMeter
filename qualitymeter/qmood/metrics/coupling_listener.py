from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

class CouplingListener(JavaParserLabeledListener):
    def __init__(self):
        self.list = []
        self.num_classes = 0
        self.num_interfaces = 0

    def get_coupling_size(self):
        unique_items = []
        for item in self.list:
            if item not in unique_items:
                unique_items.append(item)
        return len(unique_items)

    def get_num_classes(self):
        return self.num_classes

    def get_num_interfaces(self):
        return self.num_interfaces

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.num_classes += 1

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        self.num_interfaces += 1

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
