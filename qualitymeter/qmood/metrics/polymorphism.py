"""
class Polymorphism:
- measures the value of polymorphism using the structure of classes and interfaces.
  it uses class polymorphismListener to obtain the information needed for classes
  and interfaces.
- when structures became available, for each method in a class, it recursively checks
  for the existence of the method in the parent class itself, or in interfaces that
  the parent class implements.
  it also checks for the existence of the method in interfaces the class itself implements.
  if any of the two cases happened, the method has been overridden, otherwise, it has not.
"""

from antlr4 import *
from utils.file_reader import FileReader
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .polymorphism_listener import PolymorphismListener
from .java_container import JavaCLassContainer, JavaInterfaceContaienr


class Polymorphism:
    def __init__(self, project_path):
        self.project_path = project_path
        self.java_class_container = JavaCLassContainer()
        self.java_interface_container = JavaInterfaceContaienr()

        for stream in FileReader.get_file_streams(self.project_path):
            listener = self.get_listener(stream)
            self.extract_stream_classes(listener)
            self.extract_stream_interfaces(listener)
        self.set_interface_parents()
        self.set_class_parents()

    def get_listener(self, stream):
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        listener = PolymorphismListener()
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=listener)
        return listener

    def extract_stream_classes(self, listener):
        java_class_list = listener.get_class_list()
        for java_class in java_class_list:
            self.java_class_container.add_java_class(java_class)

    def extract_stream_interfaces(self, listener):
        java_interface_list = listener.get_interface_list()
        for java_interface in java_interface_list:
            self.java_interface_container.add_java_interface(java_interface)

    def set_class_parents(self):
        for java_class in self.java_class_container.java_class_list():
            java_builtin_parents = []
            for parent_name in java_class.parent_name_list():
                if self.java_class_container.get_java_class(parent_name):
                    java_class.add_parent(parent_name, self.java_class_container.get_java_class(parent_name))
                else:
                    java_builtin_parents.append(parent_name)

            for builtin_parent in java_builtin_parents:
                # We exclude inheriting Java built-in classes.
                java_class.remove_parent(builtin_parent)

        for java_class in self.java_class_container.java_class_list():
            java_builtin_interfaces = []
            for interface_name in java_class.interface_name_list():
                if self.java_interface_container.get_java_interface(interface_name):
                    java_class.addInterface(
                        interface_name, self.java_interface_container.get_java_interface(interface_name))
                else:
                    java_builtin_interfaces.append(interface_name)

            for java_builtin_interface in java_builtin_interfaces:
                java_class.remove_interface(java_builtin_interface)

    def set_interface_parents(self):
        for java_interface in self.java_interface_container.java_interface_list():
            java_builtin_interfaces = []
            for parent_name in java_interface.parent_name_list():
                if self.java_interface_container.get_java_interface(parent_name):
                    java_interface.add_parent(
                        parent_name, self.java_interface_container.get_java_interface(parent_name))
                else:
                    java_builtin_interfaces.append(parent_name)

            for builtin_parent in java_builtin_interfaces:
                java_interface.remove_parent(builtin_parent)


    def calc_polymorphism(self):
        total_methods_can_be_overriden = 0
        for java_class in self.java_class_container.java_class_list():
            inherited_methods = java_class.get_inherited_method_list()
            for method in java_class.method_list():
                is_inherited = False
                for iMethod in inherited_methods:
                    if iMethod == method:
                        is_inherited = True
                        break
                if not is_inherited and not(
                    method.get_modifier().is_private()
                    or method.get_modifier().is_final()
                    or method.get_modifier().is_static()
                ):
                    total_methods_can_be_overriden += 1

        for java_interface in self.java_interface_container.java_interface_list():
            inherited_methods = java_interface.get_inherited_method_list()
            for method in java_interface.method_list():
                is_inherited = False
                for iMethod in inherited_methods:
                    if iMethod == method:
                        is_inherited = True
                        break
                if not is_inherited and not(
                    method.get_modifier().is_private()
                    or method.get_modifier().is_final()
                    or method.get_modifier().is_static()
                ):
                    total_methods_can_be_overriden += 1

        if self.java_class_container.get_size() == 0 and self.java_interface_container.get_size():
            return 0
        return (total_methods_can_be_overriden /
                (self.java_class_container.get_size() + self.java_interface_container.get_size()))

    def calc_inheritence(self):
        sum_metric_for_class_and_interface = 0
        for java_class in self.java_class_container.java_class_list():
            inherited_methods = java_class.get_inherited_method_list()
            count_inherited = len(inherited_methods)
            count_methods = count_inherited

            for method in java_class.method_list():
                is_overriden = False
                for iMethod in inherited_methods:
                    if iMethod == method:
                        is_overriden = True
                        break
                if not is_overriden:
                    count_methods += 1

            if count_methods != 0:
                sum_metric_for_class_and_interface += count_inherited / count_methods

        for java_interface in self.java_interface_container.java_interface_list():
            inherited_methods = java_interface.get_inherited_method_list()
            count_inherited = len(inherited_methods)
            count_methods = count_inherited

            for method in java_interface.method_list():
                is_overriden = False
                for iMethod in inherited_methods:
                    if iMethod == method:
                        is_overriden = True
                        break
                if not is_overriden:
                    count_methods += 1

            if count_methods != 0:
                sum_metric_for_class_and_interface += count_inherited / count_methods

        if self.java_class_container.get_size() == 0 and self.java_interface_container.get_size() == 0:
            return 0
        return (sum_metric_for_class_and_interface /
                (self.java_class_container.get_size() + self.java_interface_container.get_size()))
