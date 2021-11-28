import os
from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class InfoExtractorListener(JavaParserLabeledListener):
    def __init__(self):
        self.__user_defined = set()
        self.__class_info = None
        self.__class_stack = []
        self.__depth = 0
        self.__max_depth = 0
        self.__stack_pointers = []
        self.__current_pointer = -1
        self.__uninheritable_tags = ('static', 'private')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__user_defined.add(ctx.IDENTIFIER().getText())
        self.__stack_pointers.append(self.__current_pointer)
        self.__current_pointer = len(self.__class_stack)
        self.__class_info = {}
        self.__class_stack.append(self.__class_info)
        self.__depth += 1
        if self.__depth > self.__max_depth:
            self.__max_depth = self.__depth
        self.__class_info['name'] = ctx.IDENTIFIER().getText()
        self.__class_info['inheritable_methods'] = set()
        self.__class_info['method_count'] = 0
        self.__class_info['final_method_count'] = 0
        self.__class_info['private_field'] = 0
        self.__class_info['total_field'] = 0
        self.__class_info['class_fields'] = []
        if ctx.EXTENDS():
            self.__class_info['parent'] = ctx.typeType().getText()
        else:
            self.__class_info['MFA'] = 0
            self.__class_info['ANA'] = 0

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.__class_info['total_field'] == 0:
            self.__class_info['DAM'] = 1
        else:
            self.__class_info['DAM'] = self.__class_info['private_field'] / self.__class_info['total_field']
        if not ctx.EXTENDS():
            self.__class_info['NOP'] = len(self.__class_info['inheritable_methods']) - self.__class_info[
                'final_method_count']
        self.__depth -= 1
        self.__current_pointer = self.__stack_pointers.pop()
        self.__class_info = self.__class_stack[self.__current_pointer]

    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        self.__user_defined.add(ctx.IDENTIFIER().getText())

    def enterMemberDeclaration0(self, ctx: JavaParserLabeled.MemberDeclaration0Context):
        self.__class_info['method_count'] += 1
        inheritablef = True
        finalf = False
        for i in ctx.parentCtx.modifier():
            text = i.getText()
            if text in self.__uninheritable_tags:
                inheritablef = False
            elif text == 'final':
                finalf = True
        if inheritablef:
            self.__class_info['inheritable_methods'].add(ctx.methodDeclaration().IDENTIFIER().getText())
            if finalf:
                self.__class_info['final_method_count'] += 1

    def enterMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        self.__class_info['total_field'] += 1
        for i in ctx.parentCtx.modifier():
            text = i.getText()
            if text == 'private' or text == 'protected':
                self.__class_info['private_field'] += 1
        tmp = ctx.fieldDeclaration().typeType().classOrInterfaceType()
        if tmp:
            text = tmp.getText()
            if text != 'String' or text != 'Random':
                self.__class_info['class_fields'].append(text)

    def return_indexed_classes(self):
        return self.__class_stack

    def return_user_defined(self):
        return self.__user_defined


def get_list_of_files(dir_name):
    # create a list of file and sub directories
    # names in the given directory
    list_of_files = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        elif entry.lower().endswith('.java'):
            all_files.append(full_path)
    return all_files
