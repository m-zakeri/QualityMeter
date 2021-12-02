import argparse
import os
import sys
import glob

import matplotlib.pyplot as plt
import networkx as nx
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.modularity.package_level.listeners import OutputListener, NodeGeneratorListener


def process_file(file_name: str, listener: JavaParserLabeledListener):
    """
    Walk the parse tree of the given java file, listen to all declarations using the given listener
    """
    stream = FileStream(file_name, encoding="utf-8")
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parse_tree = parser.compilationUnit()

    walker = ParseTreeWalker()
    walker.walk(listener, parse_tree)


def main(args):
    directory = args.directory
    graph = nx.Graph()
    if directory[-1] != "/":
        directory = directory + "/"
    node_generator_listener = NodeGeneratorListener(graph)
    output_listener = OutputListener(graph)

    if not os.path.isdir(directory):
        sys.exit(-1)

    for listener in [node_generator_listener, output_listener]:
        for filename in glob.iglob(directory + '**/*.java', recursive=True):
            process_file(filename, listener)

    edges = []
    for edge in list(graph.edges):
        node1, node2 = edge
        weight = graph.edges.get(edge).get("weight")
        edges.append((node1, node2, weight))

    q_value = calculate_q(edges)
    # plt.title(f"Q value = {q_value}")
    # labels = nx.get_edge_attributes(graph, 'weight')
    # pos = nx.spring_layout(graph)
    # nx.draw_networkx(graph, pos)
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    # plt.show()
    print("Q of this project equals to: ", q_value)


def calculate_q(edges):
    m = 0
    lst = []
    for edge in edges:
        node1, node2, weight = edge
        node1.k = getattr(node1, "k", 0) + weight
        node2.k = getattr(node2, "k", 0) + weight
        m += weight

    tmp = 0
    for edge in edges:
        node1, node2, weight = edge
        if node1.package_name == node2.package_name:
            tmp += (weight - (node1.k * node2.k) / (2 * m))

    return round((1 / (2 * m)) * tmp, 4)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-d", "--directory", help="Project directory")
    args = arg_parser.parse_args()
    main(args)
