"""
The module identify pull-up method refactoring opportunities in Java projects

"""

import itertools
import json
import os

from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class pullUpListener(JavaParserLabeledListener):
    
    """
    This class investigate the situations for PullUp refactoring between 
    prent classes and inherited ones.
    """

    def __init__(self):
        self.__classes = []
        self.__class_interface = {}
        self.__parent_and_child_classes = {}
        self.__methods_of_classes = {}
        self.__current_class_or_interface = None

    @property
    def get_methods_and_classes(self):
        """
        This method is the getter of __methods_of_classes.
        :param:
        :return: a dictionary of methods belong to each class
        """
        
        return self.__methods_of_classes

    @property
    def get_parents_and_children(self):
        """
        This method is the getter of __parent_and_child_classes.
        :param:
        :return: a dictionary of parent of each class
        """
        
        return self.__parent_and_child_classes

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        """
        This method add the current class, its parent to the proper dictionary.
        :param: context of ClassDeclarationContext
        :return: None
        """

        self.__current_class_or_interface = ctx.IDENTIFIER().getText()
        self.__classes.append(ctx.IDENTIFIER().getText())
        self.__methods_of_classes[self.__current_class_or_interface] = []
        self.__class_interface[ctx.IDENTIFIER().getText()] = False

        if ctx.EXTENDS() is not None and ctx.typeType().getText() in self.__classes:
            self.__parent_and_child_classes[ctx.IDENTIFIER().getText()] = ctx.typeType().getText()

        elif ctx.IMPLEMENTS() is not None and ctx.typeList().getText() in self.__classes:
            self.__parent_and_child_classes[ctx.IDENTIFIER().getText()] = ctx.typeList().getText()

    def enterInterfaceDeclaration(self, ctx:JavaParserLabeled.InterfaceDeclarationContext):
        """
        This method add the current class, its parent to the proper dictionary.
        :param: context of InterfaceDeclarationContext
        :return: None
        """
        
        self.__current_class_or_interface = ctx.IDENTIFIER().getText()
        self.__classes.append(ctx.IDENTIFIER().getText())
        self.__methods_of_classes[self.__current_class_or_interface] = []
        self.__class_interface[ctx.IDENTIFIER().getText()] = True

        if ctx.EXTENDS() is not None and ctx.typeList().getText() in self.__classes:
            self.__parent_and_child_classes[ctx.IDENTIFIER().getText()] = ctx.typeList().getText()

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        """
        This method add the methods of the current class to the proper dictionary.
        :param: context of MethodDeclarationContext
        :return: None
        """
        
        if self.__current_class_or_interface is None:
            return

        method_signature = f"{ctx.IDENTIFIER().getText()} {ctx.formalParameters().getText()}" # signature without considering return value
        # method_signature = f"{ctx.typeTypeOrVoid().getText()} {ctx.IDENTIFIER().getText()} {ctx.formalParameters().getText()}" # signature considering return value
        
        self.__methods_of_classes[self.__current_class_or_interface].append(method_signature)

    def get_pullups(self, file_name):
        """
        This method collects the situations of pullups and return them as a dictionary,
        where keys represent the class and values represent a list of methods that must be pulled up.
        :param: None
        :return: a dictionary of class-methods
        """

        if self.__current_class_or_interface is None:
            return []
        
        # Collecting a dictionary of classes and their children.
        parent_children = {}
        for classname in set(self.get_parents_and_children.values()):
            children = parent_children.get(classname, [])
            for key, value in self.get_parents_and_children.items():
                if value == classname:
                    children.append(key)

            parent_children[classname] = children
            
        class_methods_to_refactor = []
        for key, value in parent_children.items():
            for classes_tuple in list(itertools.combinations(value, 2)):
                methods1 = set(self.get_methods_and_classes[classes_tuple[0]])
                methods2 = set(self.get_methods_and_classes[classes_tuple[1]])
                parents_methods = set(self.get_methods_and_classes[key])
                methods_to_refactor_ = list(methods1.intersection(methods2) - parents_methods)

                if len(methods_to_refactor_) != 0:
                    parent_class = {"name": key, "is_interface": self.__class_interface[key]}
                    children_classes = [{"name": classes_tuple[0], "is_interface": self.__class_interface[classes_tuple[0]]}, {"name": classes_tuple[1], "is_interface": self.__class_interface[classes_tuple[1]]}]
                    
                    merged_opportunity = False
                    for item in class_methods_to_refactor:
                        if item["filename"] == file_name and item["parent_class"] == parent_class and item["pullup_methods"] == methods_to_refactor_:
                            for x in children_classes:
                                if x not in item["children_classes"]:
                                    item["children_classes"].append(x)

                            merged_opportunity = True
                            break

                    if not merged_opportunity:
                        class_methods_to_refactor.append(
                            {
                                "filename": file_name, 
                                "parent_class": parent_class, 
                                "children_classes": children_classes, 
                                "pullup_methods": methods_to_refactor_}
                            )

        return class_methods_to_refactor


def get_all_filenames(walk_dir, valid_extensions):
    """get all files of a directory
    Args:
        walk_dir ([type]): [description]
        valid_extensions ([type]): [description]
    Yields:
        [type]: [description]
    """
    
    for root, sub_dirs, files in os.walk(walk_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if any([file_name.endswith(extension) for extension in valid_extensions]) and "test" not in file_path:
                yield file_path
                

if __name__ == '__main__':
    walk_dir = "./SF110-20130704-src/23_jwbf/src"
    valid_extensions = ['.java']
    
    for file_name in get_all_filenames(walk_dir, valid_extensions):
        stream = FileStream(file_name, encoding='utf-8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parse_tree = parser.compilationUnit()
        walker = ParseTreeWalker()
        pu_listener = pullUpListener()
        walker.walk(t=parse_tree, listener=pu_listener)

        pullups = pu_listener.get_pullups(file_name)
        jsonified_pullups = json.dumps(pullups, indent=4)
        
        print(jsonified_pullups)
