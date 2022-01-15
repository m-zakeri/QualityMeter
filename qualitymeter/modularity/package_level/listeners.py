import networkx as nx
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


def get_node_key(class_name, package_name):
    return package_name + class_name


class Node:
    """
    Each node object is a unique class (a package-class pair)
    """
    def __init__(self, class_name: str, package_name: str):
        self.class_name = class_name
        self.package_name = package_name

    def __str__(self):
        return get_node_key(self.class_name, self.package_name)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.class_name == other.class_name and self.package_name == other.package_name

    def __hash__(self):
        return hash(str(self))


class NodeGeneratorListener(JavaParserLabeledListener):
    """A listener for adding nodes (package-class pairs) to an undirected graph"""
    def __init__(self, graph: nx.Graph):
        self.__current_package = None
        self.graph = graph

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.__current_package = ctx.getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        node = Node(ctx.IDENTIFIER().getText(), self.__current_package)
        self.graph.add_node(node, key=str(node))

    def enterInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceDeclarationContext):
        node = Node(ctx.IDENTIFIER().getText(), self.__current_package)
        self.graph.add_node(node, key=str(node))


class OutputListener(JavaParserLabeledListener):
    """
    A listener for adding edges (associations) between nodes (classes of the project)
    """
    def __init__(self, graph: nx.Graph):
        self.__current_package = None
        self.__current_class = None
        self.__imported_packages = {}  # Packages imported in the current file (current package)
        self.__graph = graph

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.__current_package = ctx.getText()
        self.__imported_packages[self.__current_package] = {self.__current_package}

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        identifier = ctx.qualifiedName().getText()
        if "." in identifier:
            identifier = identifier[:identifier.rfind(".")]

        self.__imported_packages[self.__current_package].add(f"package{identifier};")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__current_class = ctx.IDENTIFIER().getText()

        if ctx.typeType():  # extends
            self.add_edge(ctx.typeType())
        if ctx.typeList():  # implements
            for t in ctx.typeList().typeType():
                self.add_edge(t)

    def enterInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceDeclarationContext):
        self.__current_class = ctx.IDENTIFIER().getText()

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        self.add_edge(ctx.typeType())

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        self.add_edge(ctx.typeType())

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        """
        Capture instance variable declaration and add edge only if initialization is also done
         (otherwise it will be initialized in a method where we capture it using the enterFormalParameter method)
        """
        initializer = ctx.variableDeclarators().variableDeclarator()[0].variableInitializer()
        if initializer:
            self.add_edge(ctx.typeType())

    def add_edge(self, type_obj):
        class_or_interface = type_obj.classOrInterfaceType()
        if not class_or_interface:
            return
        associated_class = class_or_interface.IDENTIFIER(0).getText()
        if associated_class:
            node1 = self.find_node(self.__current_class, [self.__current_package])
            node2 = self.find_node(associated_class, self.__imported_packages[self.__current_package])
            if self.__graph.has_edge(node1, node2):
                prev_weight = self.__graph.edges.get((node1, node2)).get("weight")
            else:
                prev_weight = 0
            self.__graph.add_weighted_edges_from(
                [(node1, node2, prev_weight + 1)]
            )

    def find_node(self, class_name, package_list: list):
        for pkg in package_list:
            for node, key in self.__graph.nodes(data="key"):
                if key == get_node_key(class_name, pkg):
                    return node
        return Node(class_name, "Unknown")
