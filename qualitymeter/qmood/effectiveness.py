from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from effectiveness_utils import InfoExtractorListener, get_list_of_files


__searchCache = {}
__userDefined = set()
__allClasses = []
__inheritingClasses = []


def calculate(path):
    global __searchCache
    global __userDefined
    global __allClasses
    global __inheritingClasses
    ANA = 0
    DAM = 0
    MOA = 0
    MFA = 0
    NOP = 0
    files = get_list_of_files(path)
    print(f'Number of files detected: {len(files)}')
    print('Proceeding to parse...')
    _parse_files(files)
    for item in __inheritingClasses:
        _set_ancestors(item)

    for item in __allClasses:
        item['MOA'] = _calc_MOA(item.pop('class_fields'))
        ANA += item['ANA']
        DAM += item['DAM']
        MOA += item['MOA']
        MFA += item['MFA']
        NOP += item['NOP']
    return (ANA + DAM + MOA + MFA + NOP) / (len(__allClasses) * 5)


def _parse_files(file_list):
    global __searchCache
    global __userDefined
    global __allClasses
    global __inheritingClasses

    __searchCache = {}
    __userDefined = set()
    __allClasses = []
    __inheritingClasses = []

    walker = ParseTreeWalker()
    for file in file_list:
        input_stream = FileStream(file, encoding="utf-8")
        lexer = JavaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(stream)
        tree = parser.compilationUnit()
        extractor = InfoExtractorListener()
        walker.walk(extractor, tree)
        __userDefined.update(extractor.return_user_defined())
        for item in extractor.return_indexed_classes():
            if not item['name'] in __searchCache:
                __searchCache[item['name']] = item
            '''else:
                print(f'duplicate class {item["name"]}')'''
            __allClasses.append(item)
            if 'parent' in item:
                __inheritingClasses.append(item)


def _set_ancestors(item):
    tmp = item['parent']
    if type(tmp) != str:
        return
    if tmp.endswith('+'):
        return
    if item['parent'] in __searchCache:
        item['parent'] = __searchCache[tmp]
    else:
        item['parent'] += '+'
        item['MFA'] = 0
        item['ANA'] = 1
        item['NOP'] = len(item['inheritable_methods']) - item['final_method_count']
        return
    if 'parent' in item['parent']:
        _set_ancestors(item['parent'])
    own = item['method_count'] - len(item['inheritable_methods'])
    item['inheritable_methods'].update(item['parent']['inheritable_methods'])
    item['final_method_count'] += item['parent']['final_method_count']
    tmp = len(item['inheritable_methods'])
    item['NOP'] = tmp - item['final_method_count']
    tmp += own
    item['method_count'] = tmp
    if tmp == 0:
        item['MFA'] = 1
    else:
        item['MFA'] = len(item['parent']['inheritable_methods']) / tmp
    item['ANA'] = item['parent']['ANA'] + 1


def _calc_MOA(names):
    count = 0
    for item in names:
        if item in __userDefined:
            count += 1
    return count


if __name__ == '__main__':
    directory = input('Please enter your code base address:\n')
    effectiveness = calculate(directory)
    print(f'Effectiveness: {effectiveness}\nNumber of classes: {len(__allClasses)}')
