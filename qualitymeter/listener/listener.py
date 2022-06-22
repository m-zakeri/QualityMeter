"""
Class MyListener -> here we extract all the design metrics needed to calculate
    design listener like
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.java_components.java_class import JavaClass
from qualitymeter.java_components.java_interface import JavaInterface
from qualitymeter.java_components.java_method_parameter import JavaMethodParameter


class Listener(JavaParserLabeledListener):

    def __init__(self):
        self.__classes = []
        self.__interfaces = []
        self.__currentPackage = None
        self.__hierarchies = []
        self.__currentClass = None
        self.__currentInterface = None
        self.__currentMethod = None
        self.__currentMethodParametersType = []
        self.__currentMethodParameters = []
        self.__currentMethodModifiers = []
        self.__currentMethodVariables = []
        self.__is_enter_method = False
        self.__currentAttributesModifiers = []

    @property
    def classes(self):
        return self.__classes

    @property
    def hierarchies(self):
        return self.__hierarchies

    @property
    def interfaces(self):
        return self.__interfaces

    def enterCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        package = ""
        for pack in ctx.packageDeclaration().qualifiedName().IDENTIFIER():
            package += "{0}.".format(pack)
        self.__currentPackage = package[:-1]

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """
        enterClassDeclaration.

        :param ctx:
        :return:
        """
        if ctx.EXTENDS() or ctx.IMPLEMENTS():
            self.hierarchies.append(ctx.IDENTIFIER())
        if self.__currentClass is not None:
            temp = JavaClass(ctx.IDENTIFIER(), self.__currentPackage)
            temp.outer_class = self.__currentClass
            self.__currentClass = temp
        else:
            # Create class and store in current class object.
            self.__currentClass = JavaClass(
                ctx.IDENTIFIER(), self.__currentPackage)

        # Here we aim to calculate the Number of Hierarchies or (NoH) metric: mapped to Hierarchy Property.
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                self.__currentClass.add_parent(parent)
        if ctx.IMPLEMENTS():
            for implementations in ctx.typeList().typeType():
                for implementation in implementations.classOrInterfaceType().IDENTIFIER():
                    self.__currentClass.add_implementation(implementation)

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """

        :param ctx:
        :return:
        """
        self.__classes.append(self.__currentClass)
        if self.__currentClass.outer_class:
            self.__currentClass = self.__currentClass.outer_class
        else:
            self.__currentClass = None

    def enterClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        """

        :param ctx:
        :return:
        """
        if self.__currentClass:
            if isinstance(ctx.memberDeclaration(), JavaParserLabeled.MemberDeclaration2Context):
                field_dec = ctx.memberDeclaration().fieldDeclaration()
                for varDec in field_dec.variableDeclarators().variableDeclarator():
                    for i in ctx.modifier():
                        if i.classOrInterfaceModifier():
                            self.__currentAttributesModifiers.append(
                                i.classOrInterfaceModifier().getText())
                    self.__currentClass.add_attribute(field_dec.typeType().getText(),
                                                      varDec.variableDeclaratorId().IDENTIFIER(),
                                                      self.__currentAttributesModifiers)

            elif isinstance(ctx.memberDeclaration(), JavaParserLabeled.MemberDeclaration0Context):
                for i in ctx.modifier():
                    if i.classOrInterfaceModifier():
                        self.__currentMethodModifiers.append(
                            i.classOrInterfaceModifier().getText())
                        if ctx.memberDeclaration().methodDeclaration().formalParameters().formalParameterList():
                            if isinstance(
                                    ctx.memberDeclaration().methodDeclaration(
                                    ).formalParameters().formalParameterList(),
                                    JavaParserLabeled.FormalParameterList0Context):
                                for p in ctx.memberDeclaration().methodDeclaration(). \
                                        formalParameters().formalParameterList().formalParameter():
                                    self.__currentMethodParametersType.append(
                                        p.typeType().getText())
                                    self.__currentMethodParameters.append(JavaMethodParameter(
                                        p.variableDeclaratorId().IDENTIFIER(), p.typeType().getText()))
                            # if isinstance(
                            #         ctx.memberDeclaration().methodDeclaration().formalParameters().formalParameterList(),
                            #         JavaParserLabeled.FormalParameterList1Context):
                            #     # print("FormalParameterList1Context")

                self.__currentMethod = ctx.memberDeclaration().methodDeclaration().IDENTIFIER()

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        """

        :param ctx:
        :return:
        """
        self.__is_enter_method = True

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        """

        :param ctx:
        :return:
        """
        if self.__currentMethod:
            self.__currentClass.add_method(self.__currentMethod,
                                           self.__currentMethodParametersType,
                                           self.__currentMethodParameters,
                                           self.__currentMethodModifiers,
                                           self.__currentMethodVariables)
        self.__currentMethod = None
        self.__currentMethodParametersType = []
        self.__currentMethodParameters = []
        self.__currentMethodModifiers = []
        self.__currentMethodVariables = []
        self.__is_enter_method = False
        self.__currentAttributesModifiers = []

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        """

        :param ctx:
        :return:
        """
        if self.__is_enter_method:
            self.__currentMethodVariables.append(ctx.IDENTIFIER().getText())

    def enterInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceMethodDeclarationContext):
        self.__currentInterface = JavaInterface(
            ctx.IDENTIFIER(), self.__currentPackage)

    def enterInterfaceMethodDeclaration(self, ctx: JavaParserLabeled.InterfaceMethodDeclarationContext):
        if self.__currentInterface:
            self.__currentInterface.add_method(ctx.IDENTIFIER())

    def exitInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceMethodDeclarationContext):
        self.__interfaces.append(self.__currentInterface)
        self.__currentInterface = None

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        self.__currentPackage = None
