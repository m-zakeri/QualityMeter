"""
A listener class to calculate abstraction value.

"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Abstraction(JavaParserLabeledListener):
    def __init__(self):
        self.__result = 0
        self.__abstracts = []

    # creating property for result.
    @property
    def result(self):
        return self.__result

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # extracting classes with parents
        if ctx.EXTENDS():
            for id in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                # store classes with parents.
                self.__abstracts.append({
                    "class": ctx.IDENTIFIER().getText(),
                    "extends": id.getText(),
                    "count": 1
                })
        else:
            # adding classes without parent with count zero
            self.__abstracts.append({
                "class": ctx.IDENTIFIER().getText(),
                "extends": "",
                "count": 0
            })

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        # iterating abstracts.
        for abstract in self.__abstracts:
            cls = abstract
            # while there is a class that extends the
            while any(ab["class"] == cls["extends"] and ab["count"] != 0 for ab in self.__abstracts):
                for x in self.__abstracts:
                    if x["class"] == cls["extends"]:
                        abstract["count"] += 1
                        cls = x
                        break

        # storing the counts of abstracts in one array to calculate mean of abstractions in all classes.
        counts = []
        for a in self.__abstracts:
            counts.append(a["count"])
        if len(counts) != 0:
            self.__result = sum(counts) / len(counts)
        else:
            return 0
