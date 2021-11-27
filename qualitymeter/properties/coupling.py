"""
A listener class to calculate coupling value.

"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Coupling(JavaParserLabeledListener):
    """
    Coupling Listener Class.

    ...

    Attributes
    ----------
    self.__classes : list
        input classes
    self.__current_cls : str
        current class
    self.__dcc : int
        direct class coupling
    self.__counted : list
        hold counted classes
    self.__result : list
        classes coupling value

    Methods
    -------
    result():
        Get classes coupling value.
    __calc_dcc(ctx):
        Get classes coupling value.
    enterClassDeclaration(ctx: JavaParserLabeled.ClassDeclarationContext):
        Enter class declaration listener.
    exitClassDeclaration(ctx: JavaParserLabeled.ClassDeclarationContext):
        Exit class declaration listener.
    enterFieldDeclaration(ctx: JavaParserLabeled.FieldDeclarationContext):
        Enter field listener.
    enterMethodDeclaration(ctx: JavaParserLabeled.MethodDeclarationContext):
        Enter method declaration listener.
    """

    def __init__(self, classes_name):
        """
        Constructs all the necessary variables for the coupling object.

        Parameters
        ----------
            self.__classes : list
                input classes
            self.__current_cls : str
                current class
            self.__dcc : int
                direct class coupling
            self.__counted : list
                hold counted classes
            self.__result : list
                classes coupling value
        """

        self.__classes_name = classes_name
        self.__current_cls = ''
        self.__dcc = 0
        self.__counted = []
        self.__result = []

    @property
    def result(self):
        """
        Get classes coupling value.

        Returns
        -------
        Classes coupling value
        """

        return self.__result

    def __calc_dcc(self, ctx):
        """
        Calculate dcc.

        Returns
        -------
        Classes dcc value
        """

        # Get class or interface type context.
        ctx = ctx.typeType().classOrInterfaceType()

        # Check if the context is none or not.
        if ctx is None:
            return

        # Get the context text.
        text = ctx.IDENTIFIER(0).getText()

        # Check if the class is not the current class and has not counted before and it is one the project classes.
        if text != self.__current_cls and text not in self.__counted and text in self.__classes_name:
            # Increment the dcc variable.
            self.__dcc += 1
            # Mark the class as counted.
            self.__counted.append(text)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """
        Enter class declaration listener.

        Parameters
        ----------
        ctx : object
            Class declaration context

        Returns
        -------
        None
        """

        # Update the current class variable.
        self.__current_cls = ctx.IDENTIFIER().getText()
        # Reset the dcc variable.
        self.__dcc = 0
        # Reset the counted list.
        self.__counted = []

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """
        Exit class declaration listener.

        Parameters
        ----------
        ctx : object
            Class declaration context

        Returns
        -------
        None
        """

        # Append calculated dcc to the result.
        self.__result.append(self.__dcc)

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        """
        Enter field declaration listener.

        Parameters
        ----------
        ctx : object
            Field declaration context

        Returns
        -------
        None
        """

        # Calculate the field dcc.
        self.__calc_dcc(ctx)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        """
        Enter method declaration listener.

        Parameters
        ----------
        ctx : object
            Method declaration context

        Returns
        -------
        None
        """

        # Get formal parameter list context.
        ctx = ctx.formalParameters().formalParameterList()

        # Check if the context exist.
        if ctx:
            # Calculate dcc for the method parameters.
            for item in ctx.formalParameter():
                self.__calc_dcc(item)
