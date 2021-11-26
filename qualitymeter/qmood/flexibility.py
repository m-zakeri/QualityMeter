from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener



class myListener(JavaParserLabeledListener):

    def __init__(self):
        self.__number_of_coupling = 0

    @property
    def get_number_of_coupling(self):
        return self.__number_of_coupling


    def enterVariableDeclarator(self, ctx:JavaParserLabeled.VariableDeclaratorContext):

        if ctx.variableInitializer().expression().NEW() is not None:
            self.__number_of_coupling += 1
            
 if __name__ == '__main__':
 
    stream = FileStream(A.java, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parse_tree = parser.compilationUnit()
    my_listener = myListener()
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)
    print(f'DCC={my_listener.get_number_of_coupling}')
