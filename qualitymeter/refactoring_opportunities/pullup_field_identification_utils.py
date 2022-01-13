import os
from typing import List, Tuple, Dict

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

T_REPORT = Tuple[str, int, bool, bool, List[Tuple[str, int, bool, int]]]


class InfoExtractorListener(JavaParserLabeledListener):
    """
    A custom listener based on ANTLR generated one, to extract necessary information about classes.
    """

    def __init__(self):
        """
        Create a new InfoExtractorListener to use with ANTLR tree walker.
        """
        self.__is_ignorable = False  # ignores fields while this is true
        self.__class_info = None  # the class which is currently being walked
        self.__class_stack = []  # list of seen classes
        self.__depth = 0  # to keep track of nested classes
        self.__max_depth = 0
        self.__stack_pointers = []  # to keep track of stashed classes
        self.__current_pointer = -1
        self.__package_name = '|UNKNOWN|'

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.__package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__stack_pointers.append(self.__current_pointer)
        self.__current_pointer = len(self.__class_stack)
        self.__class_info = {}
        self.__class_stack.append(self.__class_info)
        self.__depth += 1
        if self.__depth > self.__max_depth:
            self.__max_depth = self.__depth
        self.__class_info['name'] = ctx.IDENTIFIER().getText()
        self.__class_info['package'] = self.__package_name
        self.__class_info['fields'] = {}
        self.__class_info['ignore'] = False
        self.__is_ignorable = False

        if ctx.EXTENDS():
            self.__class_info['parent'] = ctx.typeType().getText()
        else:
            parent_tmp = ctx.parentCtx
            if isinstance(parent_tmp, JavaParserLabeled.TypeDeclarationContext):
                for i in ctx.parentCtx.classOrInterfaceModifier():
                    if i.getText() == 'final':
                        self.__class_info['ignore'] = True
                        self.__is_ignorable = True
                        break
            elif isinstance(parent_tmp, JavaParserLabeled.MemberDeclaration7Context):
                for i in ctx.parentCtx.parentCtx.modifier():
                    if i.getText() == 'final':
                        self.__class_info['ignore'] = True
                        self.__is_ignorable = True
                        break

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth -= 1
        self.__current_pointer = self.__stack_pointers.pop()
        self.__class_info = self.__class_stack[self.__current_pointer]
        self.__is_ignorable = self.__class_info['ignore']

    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        self.__is_ignorable = True

    def exitEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        if self.__class_info:
            self.__is_ignorable = self.__class_info['ignore']
        else:
            self.__is_ignorable = False

    def enterMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        if self.__is_ignorable:
            return

        # access levels: private[0], no modifier[1], protected[2], public[3]
        access_level = 1
        access_flag = False
        final_flag = False

        for modifier in ctx.parentCtx.modifier():
            text = modifier.getText()
            # if it's not determined yet, determine the access level
            if not access_flag:
                if text == 'private':
                    access_level = 0
                    access_flag = True
                    continue
                elif text == 'protected':
                    access_level = 2
                    access_flag = True
                    continue
                elif text == 'public':
                    access_level = 3
                    access_flag = True
                    continue
            # ignore the static fields
            if text == 'static':
                return
            # mark the final ones
            if text == 'final':
                final_flag = True
                continue
        # keep a pointer to field declaration
        current_context = ctx.fieldDeclaration()
        # get field type
        field_type = current_context.typeType().getText()
        # update class fields with each and every declaration
        for i in current_context.variableDeclarators().variableDeclarator():
            field_name = i.variableDeclaratorId().getText()
            self.__class_info['fields'][f'{field_type} {field_name}'] = \
                (i.start.line, final_flag, access_level)

    def return_indexed_classes(self):
        """
        Returns a list of classes indexed by info extractor.

        :return: List of class info dictionaries
        """
        return self.__class_stack


def get_list_of_files(dir_name: str) -> List[str]:
    """
    Lists all of the .java files in the directory and all of the subdirectories.

    :param dir_name: Base directory address
    :return: A list consisting of full-path to the java files
    """
    list_of_files = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        # If entry is a .java file add it to the list
        elif entry.lower().endswith('.java'):
            all_files.append(full_path)
    return all_files


def prettify(result: Dict[str, List[T_REPORT]], logger=None) -> Dict[str, List[Dict]]:
    """
    A function to prettify results, implicitly handling internal translations

    :param result: A dictionary of analysis reports for each parent class
    :param logger: Optional logger for logging purposes
    :return: A structured dictionary of suggestions based on their priorities
    """
    if logger is not None:
        if len(result) == 0:
            logger.warn('No result found.')
            print('No result found.')
            return {}
        logger.info('Prettifying results')
    elif len(result) == 0:
        print('No result found.')
        return {}
    # Suggestion priorities
    priority_hint = []
    priority_low = []
    priority_medium = []
    priority_high = []

    # Create vocabulary for a memory efficient implementation
    ACCESS_VOCAB = ['private', 'no-modifier', 'protected', 'public']

    # Conversion happens here
    for parent in result:
        suggestions = result[parent]
        parent_package = suggestions.pop()
        parent_path = suggestions.pop()
        for suggestion in suggestions:
            pretty = {'parent path': parent_path,
                      'parent package': parent_package,
                      'parent name': parent,
                      'field': suggestion[0],
                      'lowest access level': ACCESS_VOCAB[suggestion[1]],
                      'identical': suggestion[2],
                      'same access level': suggestion[3]}
            # If it has a private variation
            if suggestion[1] == 0:
                # If all of them are private
                if suggestion[3]:
                    pretty['priority'] = 'hint'
                    priority_hint.append(pretty)
                # If some of them are private
                else:
                    pretty['priority'] = 'low'
                    priority_low.append(pretty)
            # If it doesn't have private variation
            else:
                # If all of them are of the same access level
                if suggestion[3]:
                    pretty['priority'] = 'high'
                    priority_high.append(pretty)
                # If they have different modifiers
                else:
                    pretty['priority'] = 'medium'
                    priority_medium.append(pretty)
            child_dicts = []
            for child in suggestion[4]:
                dict_tmp = {'class path': child[4],
                            'class package': child[5],
                            'class name': child[0],
                            'line number': child[1],
                            'is final': child[2],
                            'access level': ACCESS_VOCAB[child[3]]}
                child_dicts.append(dict_tmp)
            pretty['sub classes'] = child_dicts
    return {'high': priority_high,
            'medium': priority_medium,
            'low': priority_low,
            'hint': priority_hint}


def print_prettified(pretty: Dict[str, List[Dict]], min_priority=0, logger=None):
    """
    A function that prints prettified output in a readable format

    :param pretty: Prettified output of the analyzer
    :param logger: Optional logger for logging purposes
    :param min_priority: Minimum level of the suggestions to be printed
    """
    if logger is not None:
        if len(pretty) == 0:
            logger.warn('prettified dictionary was empty')
            print('Prettified dictionary was empty')
            return
        logger.info('Printing prettified results')
    elif len(pretty) == 0:
        print('Prettified dictionary was empty')
        return
    # Check to see if we did suggest anything or not
    flag = True
    if min_priority < 4:
        tmp = pretty['high']
        if len(tmp) > 0:
            flag = False
            print('####    HIGH    ####')
            for item in tmp:
                print(f'Field "{item["field"]}" can be pulled up. '
                      f'Target class: "{item["parent package"]}.{item["parent name"]}" Origin:')
                for child in item['sub classes']:
                    print(f'\tClass: "{child["class name"]}" [Line: {child["line number"]}]'
                          f'\t(Package: {child["class package"]})')
    if min_priority < 3:
        tmp = pretty['medium']
        if len(tmp) > 0:
            flag = False
            print('####    MEDIUM    ####')
            for item in tmp:
                print(f'Field "{item["field"]}" can be pulled up. '
                      f'Target class: "{item["parent package"]}.{item["parent name"]}" Origin:')
                for child in item['sub classes']:
                    print(f'\tClass: "{child["class name"]}" [Line: {child["line number"]}]'
                          f'\t(Package: {child["class package"]})')
    if min_priority < 2:
        tmp = pretty['low']
        if len(tmp) > 0:
            flag = False
            print('####    LOW    ####')
            for item in tmp:
                print(f'Field "{item["field"]}" can be pulled up. '
                      f'Target class: "{item["parent package"]}.{item["parent name"]}" Origin:')
                for child in item['sub classes']:
                    print(f'\tClass: "{child["class name"]}" [Line: {child["line number"]}]'
                          f'\t(Package: {child["class package"]})')
    if min_priority < 1:
        tmp = pretty['hint']
        if len(tmp) > 0:
            flag = False
            print('####    HINTS    ####')
            for item in tmp:
                print(f'Field "{item["field"]}" can be pulled up. '
                      f'Target class: "{item["parent package"]}.{item["parent name"]}" Origin:')
                for child in item['sub classes']:
                    print(f'\tClass: "{child["class name"]}" [Line: {child["line number"]}]'
                          f'\t(Package: {child["class package"]})')

    # Print something in case we haven't suggested anything
    if flag:
        print('Your code is great! There are no refactoring opportunities.')
