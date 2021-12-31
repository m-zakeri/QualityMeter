import os

from antlr4 import *
import networkx as nx
import networkx.algorithms.community as nx_comm
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
import re


java_dataTypes_list = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'String']


class realationListener(JavaParserLabeledListener):
    def __init__(self):
        self.__currentClass = "None"
        self.__currentMethod = "None"
        self.__everyObjectAndItsClass = {}
        self.__classStack = [0]
        self.__nodes = []
        self.__edges = {}

    def getNodes(self):
        return self.__nodes

    def getEdges(self):
        return self.__edges

    # To Get the nodes (better to say Methods)---------------------------------------------------------------
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
       self.__currentClass = ctx.IDENTIFIER().getText()
       self.__classStack.append(self.__currentClass)
       #print('entered class is:', self.__currentClass)

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        x = self.__classStack.pop()
        lastItem = len(self.__classStack) - 1
        if  lastItem is not 0:
            self.__currentClass = self.__classStack[lastItem]
        #print('exited class is:', x)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.__currentMethod = ctx.IDENTIFIER().getText()
        self.__nodes.append(ctx.IDENTIFIER().getText()+':'+self.__currentClass)
        # print(self.__currentMethod)

    # To Get the edges (better to say relation between Methods)----------------------------------------------
    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        objectAddress = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().getText()
        objectClassAdress = ctx.typeType().getText()
        if objectClassAdress not in java_dataTypes_list:
            self.__everyObjectAndItsClass[objectAddress] = objectClassAdress
            # print(self.__everyObjectAndItsClass)

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.qualifiedName().IDENTIFIER(0).getText() == 'java':
            i = len(ctx.qualifiedName().IDENTIFIER())
            java_dataTypes_list.append(ctx.qualifiedName().IDENTIFIER(i - 1).getText())
            # print(ctx.qualifiedName().IDENTIFIER(i-1).getText())

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        self.VariableDeclarator = ctx.variableDeclaratorId().getText()

    # def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
    #     self.VariableDeclarator = 'none'

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        className = self.__currentClass
        if '.' in ctx.expression().getText():
            return
        if '(' in ctx.expression().getText():
            return
        if '[' in ctx.expression().getText():
            return
        # print(ctx.expression().getText())
        # print(self.__currentMethod)
        if ctx.expression().primary().getText() == 'this':
            #if hasattr(ctx, 'methodCall' )
            if isinstance(ctx.methodCall(), type(None)):
                return
            else:
                className = self.__currentClass
        elif ctx.expression().primary().getText() not in self.__everyObjectAndItsClass.keys():
            return
        else:
            className = self.__everyObjectAndItsClass[ctx.expression().primary().getText()]

        if isinstance(ctx.methodCall(), type(None)):
            return
        else:
            methodName = ctx.methodCall().IDENTIFIER().getText()

        if self.__currentMethod+":"+self.__currentClass in self.__edges.keys():
            self.__edges[self.__currentMethod + ":" + self.__currentClass][1] += 1
        else:
            self.__edges[self.__currentMethod+":"+self.__currentClass] = [methodName+":"+className, 1]
        # print(self.__edges)

    def exitExpression3(self, ctx: JavaParserLabeled.Expression3Context):
        if 'super' in ctx.methodCall().getText():
            return
        if 'this' in ctx.methodCall().getText():
            return
        # print(ctx.methodCall().getText())
        # print(self.__currentMethod)
        if isinstance(ctx.methodCall(), type(None)):
            return
        else:
            methodName = ctx.methodCall().IDENTIFIER().getText()

        if self.__currentMethod + ":" + self.__currentClass in self.__edges.keys():
            self.__edges[self.__currentMethod + ":" + self.__currentClass][1] += 1
        else:
            self.__edges[self.__currentMethod + ":" + self.__currentClass] = [methodName + ":" + self.__currentClass, 1]
        # print(self.__edges)


def add_nodes(graph, nodeList):
    for i in nodeList:
        graph.add_node(i)
        # print(i)


def add_edges(graph, edgeDictionary):
    startNodes = list(edgeDictionary.keys())
    for i in range(len(startNodes)):
        graph.add_edge(startNodes[i], edgeDictionary[startNodes[i]][0], weight=edgeDictionary[startNodes[i]][1])
        # Ex: graph[startNode][endNode]['weight']
        # print(startNodes[i], edgeDictionary[startNodes[i]])



def compile_j(arg, graph):

    # Stage 1 --------------------------------------------------------------------------------------------------------
    stream = FileStream(arg, encoding='utf8')  # Step 1.1: Load input source into stream
    lexer = JavaLexer(stream)  # Step 1.2: Create an instance of AssignmentStLexer
    token_stream = CommonTokenStream(lexer)  # Step 1.3: Convert the input source into a list of tokens
    parser = JavaParserLabeled(token_stream)  # Step 1.4: Create an instance of the AssignmentStParser

    # Stage 2 --------------------------------------------------------------------------------------------------------
    parse_tree = parser.compilationUnit()  # Step 2.1: Create parse tree
    my_listener = realationListener()  # Step 2.2: Create an instance of AssignmentStListener
    walker = ParseTreeWalker()  # Step 2.3: Create a walker to traverse the parse tree
    walker.walk(t=parse_tree, listener=my_listener)  # Step 2.4: Traverse the parse tree using Listener
    # print('nodes are :', my_listener.getNodes())
    # print('edges are :', my_listener.getEdges())

    # Stage 3 --------------------------------------------------------------------------------------------------------
    add_nodes(graph, my_listener.getNodes())
    add_edges(graph, my_listener.getEdges())
    # print('Graph nodes are :', graph.nodes)
    # print('Graph edges are :', graph.edges)

def main():
    graph = nx.Graph()
    pattern = re.compile(r".+\.java$")
    for root, subdirs, files in os.walk('.'):
        java_file_names = list(filter(lambda f: pattern.match(f), files))
        for el in java_file_names:
            compile_j(os.path.join(root, el), graph)

    # Measure modularity
    q = nx_comm.modularity(graph, nx_comm.label_propagation_communities(graph))
    print(q)

if __name__ == '__main__':
    main()