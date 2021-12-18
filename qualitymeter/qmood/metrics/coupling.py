from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .coupling_listener import CouplingListener

class Coupling:
    def __init__(self, project_path):
        self.project_path = project_path

    def get_listener(self, stream):
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        listener = CouplingListener()
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=listener)
        return listener

    def calc_coupling(self):
        count_coupling = 0
        total_num_classes_and_interfaces = 0
        for stream in FileReader.get_file_streams(self.project_path):
            listener = self.get_listener(stream)
            count_coupling += listener.get_coupling_size()
            total_num_classes_and_interfaces += listener.get_num_classes()
            total_num_classes_and_interfaces += listener.get_num_interfaces()

        if total_num_classes_and_interfaces == 0:
            return 0
        return count_coupling / total_num_classes_and_interfaces
