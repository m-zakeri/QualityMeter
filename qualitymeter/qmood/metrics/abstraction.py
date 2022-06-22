"""
class Abstraction
- this class calculates the meter of abstraction by finding the number of parent
  classes for each class. it then returns the average number of parents for each
  class as the metric for Abstraction.
"""


from antlr4 import *
from qualitymeter.utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .abstraction_listener import AbstractionListener
from .java_container import JavaCLassContainer, JavaInterfaceContaienr

class Abstraction:
    def __init__(self, project_path):
        self.project_path = project_path
        self.class_container = JavaCLassContainer()
        self.interface_container = JavaInterfaceContaienr()

    def get_listener(self, stream):
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        listener = AbstractionListener()
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=listener)
        return listener

    def extract_java_classes(self, listener):
        java_classes = listener.get_java_class_list()
        for java_class in java_classes:
            self.class_container.add_java_class(java_class)

    def extract_java_interfaces(self, listener):
        java_interfaces = listener.get_java_interface_list()
        for java_interface in java_interfaces:
            self.interface_container.add_java_interface(java_interface)

    def set_class_parents(self):
        for java_class in self.class_container.java_class_list():
            for parent_name in java_class.parent_name_list():
                if self.class_container.get_java_class(parent_name):
                    java_class.add_parent(parent_name, self.class_container.get_java_class(parent_name))

        for java_class in self.class_container.java_class_list():
            for interface_name in java_class.interface_name_list():
                if self.interface_container.get_java_interface(interface_name):
                    java_class.addInterface(
                        interface_name, self.interface_container.get_java_interface(interface_name))

    def set_interface_parents(self):
        for java_interface in self.interface_container.java_interface_list():
            for parent_name in java_interface.parent_name_list():
                if self.interface_container.get_java_interface(parent_name):
                    java_interface.add_parent(
                        parent_name, self.interface_container.get_java_interface(parent_name))

    def calc_abstraction(self):
        for stream in FileReader.get_file_streams(self.project_path):
            listener = self.get_listener(stream)
            self.extract_java_classes(listener)
            self.extract_java_interfaces(listener)
        self.set_class_parents()
        self.set_interface_parents()

        total_number_of_ancestors = 0
        for java_class in self.class_container.java_class_list():
            ancestors = java_class.get_all_parents()
            total_number_of_ancestors += len(ancestors)

        for java_interface in self.interface_container.java_interface_list():
            ancestors = java_interface.get_all_parents()
            total_number_of_ancestors += len(ancestors)

        if self.class_container.get_size() == 0 and self.interface_container.get_size() == 0:
            return 0
        return (total_number_of_ancestors /
                (self.class_container.get_size() + self.interface_container.get_size()))
