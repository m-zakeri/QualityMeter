from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from move_field_refactoring import MoveFieldRefactoring


def listener(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # Step 2: Create an instance of lexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of parser
    parser = JavaParserLabeled(token_stream)
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()

    # Step 6: Create an instance of listener
    my_listener1 = MoveFieldRefactoring()

    # Step 7: Create an instance of walker
    walker = ParseTreeWalker()
    # Step 8: Traverse parse tree
    walker.walk(t=parse_tree, listener=my_listener1)

    allField = my_listener1.get_allField
    allLocalParam = my_listener1.get_methodBodyAtt
    print('MoveFieldRefactoring : ')
    values = []
    for v in allField.values():
        values.append(v)

    commonField = list(set.intersection(*map(set, values)))

    classs = {}
    for item in commonField:
        classs[item[1]] = []
        for k in allField.keys():
            for t in allField[k]:
                if t == item:
                    classs[item[1]].append(k)

    countInClass = {}
    for k in classs:
        for item in classs[k]:
            countInClass[item] = (k, allLocalParam[item].count(k))
    if len(countInClass) > 1:
        print(f'countInClass = {countInClass}')
    else:
        print('No refactoring found')
    return countInClass
