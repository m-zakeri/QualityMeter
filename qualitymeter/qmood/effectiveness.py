from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from effectiveness_utils import InfoExtractorListener, get_list_of_files

# A dictionary to speed up class look ups using class name
__searchCache = {}
# A set of user-defined types seen across the code
__userDefined = set()
# A list of parsed classes
__allClasses = []
# A list of classes that extend another one
__inheritingClasses = []


def calculate(path):
    """
    Calculates the effectiveness metric of a java project.

    :param path: Source path of the codebase
    :return: Effectiveness metric
    """
    # Pull globals in
    global __searchCache
    global __userDefined
    global __allClasses
    global __inheritingClasses
    # Initiate necessary metrics
    ANA = 0
    DAM = 0
    MOA = 0
    MFA = 0
    NOP = 0
    # Get a list of .java files
    files = get_list_of_files(path)
    # Logs
    print(f'Number of files detected: {len(files)}')
    print('Proceeding to parse...')
    # Parse the files and update the globals
    _parse_files(files)
    # Handle inheritance
    for item in __inheritingClasses:
        _set_ancestors(item)
    # Calculate project-wise metrics
    for item in __allClasses:
        item['MOA'] = _calc_MOA(item.pop('class_fields'))
        ANA += item['ANA']
        DAM += item['DAM']
        MOA += item['MOA']
        MFA += item['MFA']
        NOP += item['NOP']
    return (ANA + DAM + MOA + MFA + NOP) / (len(__allClasses) * 5)


def _parse_files(file_list):
    """
    Parse all of the .java files in the specified directory and all of its subdirectories
    and updates the global parameters.
    """
    # Pull globals in
    global __searchCache
    global __userDefined
    global __allClasses
    global __inheritingClasses
    # Reset the globals
    __searchCache = {}
    __userDefined = set()
    __allClasses = []
    __inheritingClasses = []
    # Initiate a walker
    walker = ParseTreeWalker()
    # Iterate over all of the indexed .java files and parse them
    for file in file_list:
        # Generic ANTLR stuff
        input_stream = FileStream(file, encoding="utf-8")
        lexer = JavaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(stream)
        tree = parser.compilationUnit()
        # Initiate a custom listener
        extractor = InfoExtractorListener()
        # Walk the tree using listener
        walker.walk(extractor, tree)
        # Update globals
        __userDefined.update(extractor.return_user_defined())
        for item in extractor.return_indexed_classes():
            # Update search cache
            if not item['name'] in __searchCache:
                __searchCache[item['name']] = item
            # Update list of all classes
            __allClasses.append(item)
            # Mark classes with a parent as inheriting
            if 'parent' in item:
                __inheritingClasses.append(item)


def _set_ancestors(item):
    """
    Traces back class parents recursively and updates related metrics.

    :param item: Class info dictionary
    """
    # Cache the parent parameter
    tmp = item['parent']
    # If it's already seen, return
    if type(tmp) != str:
        return
    # If the inherited class is not in the indexed scope, return
    if tmp.endswith('+'):
        return
    # If parent is indexed, update the parent parameter to point at the class
    if item['parent'] in __searchCache:
        item['parent'] = __searchCache[tmp]
    # If it's not indexed mark it with a '+' sign and update the relevant class metrics
    else:
        item['parent'] += '+'
        item['MFA'] = 0
        item['ANA'] = 1
        item['NOP'] = len(item['inheritable_methods']) - item['final_method_count']
        return
    # If the parent itself inherits a class recursively handle that too
    if 'parent' in item['parent']:
        _set_ancestors(item['parent'])  # recursion
    # Calculate the number of un-inheritable methods
    own = item['method_count'] - len(item['inheritable_methods'])
    # Inherit the methods from parent
    item['inheritable_methods'].update(item['parent']['inheritable_methods'])
    # Update the final method counter of current class
    item['final_method_count'] += item['parent']['final_method_count']
    # Cache the number of inheritable methods
    tmp = len(item['inheritable_methods'])
    # Update the polymorphism metric
    # (Note: by default, any inheritable method in java is polymorphic except for the final ones)
    item['NOP'] = tmp - item['final_method_count']
    # Calculate the number of methods using private and inheritable ones
    tmp += own
    # Update the class method counter
    item['method_count'] = tmp
    # Update MFA values
    # Handle division by zero
    if tmp == 0:
        item['MFA'] = 1
    # Divide inherited methods by total method to get MFA
    else:
        item['MFA'] = len(item['parent']['inheritable_methods']) / tmp
    # Update ANA
    # Note: since java doesn't support multiple inheritance we just increment parent's ANA by one
    item['ANA'] = item['parent']['ANA'] + 1


def _calc_MOA(names):
    """
    Calculates MOA metric.

    :param names: A list of non-primitive fields in a class
    :return: Number of user-defined fields
    """
    count = 0
    # Iterate over non primitive data types and check and see if they are user-defined
    for item in names:
        if item in __userDefined:
            count += 1
    return count


if __name__ == '__main__':
    # Get the code base address from user
    directory = input('Please enter your code base address:\n')
    # Calculate effectiveness
    effectiveness = calculate(directory)
    # Print that for user
    print(f'Effectiveness: {effectiveness}\nNumber of classes: {len(__allClasses)}')
