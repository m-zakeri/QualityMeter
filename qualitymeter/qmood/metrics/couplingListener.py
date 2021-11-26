from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

class CouplingListener(JavaParserLabeledListener):
    def __init__(self):
        self.list = []

    def get_coupling_size(self):
        unique_items = []
        for item in self.list:
            if item not in unique_items:
                unique_items.append(item)
        return len(unique_items)

    def enterLocalTypeDeclaration(self, ctx:JavaParserLabeled.LocalTypeDeclarationContext):
        token = 'IDENTIFIER'
        self.list.append(token)

    def enterClassOrInterfaceType(self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext):
        token ='IDENTIFIER'
        self.list.append(token)