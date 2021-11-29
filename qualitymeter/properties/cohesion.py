"""
A listener class to calculate cohesion value.

"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Cohesion(JavaParserLabeledListener):
    """
    Cohesion Listener Class.

    ...

    Attributes
    ----------
    self.__classes : list
        input classes
    self.__skip : bool
        whether to skip a class or not
    self.__invoked : dict
        whether a method invoke a global variable or not
    self.__counter : int
        show current class index
    self.__counted : list
        hold counted variable for a method
    self.__result : list
        classes cohesion value

    Methods
    -------
    result():
        Get classes cohesion value.
    enterClassDeclaration(ctx: JavaParserLabeled.ClassDeclarationContext):
        Enter class declaration listener.
    exitClassDeclaration(ctx: JavaParserLabeled.ClassDeclarationContext):
        Exit class declaration listener.
    enterMethodDeclaration(ctx: JavaParserLabeled.MethodDeclarationContext):
        Enter method declaration listener.
    enterPrimary4(ctx: JavaParserLabeled.Primary4Context):
        Enter primary 4 listener.
    """

    def __init__(self, classes):
        """
        Constructs all the necessary variables for the cohesion object.

        Parameters
        ----------
            self.__classes : list
                input classes
            self.__skip : bool
                whether to skip a class or not
            self.__invoked : dict
                whether a method invoke a global variable or not
            self.__counter : int
                show current class index
            self.__counted : list
                hold counted variable for a method
            self.__result : list
                classes cohesion value
        """

        self.__classes = classes
        self.__skip = False
        self.__invoked = {}
        self.__counter = 0
        self.__counted = []
        self.__result = []

    @property
    def result(self):
        """
        Get classes cohesion value.

        Returns
        -------
        Classes cohesion value
        """

        return self.__result

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

        # Check if the number of methods or global variable of a class is zero or not.
        if len(self.__classes[self.__counter][1]) == 0 or len(self.__classes[self.__counter][2]) == 0:
            # If zero then cc is zero.
            self.__result.append(0.0)
            # Skip next steps for the class.
            self.__skip = True
            return

        # Initialize global variables with zero which represents they are not invoked by a method yet.
        for text in self.__classes[self.__counter][1]:
            self.__invoked[text] = 0

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

        # Check whether to skip the class or not.
        if self.__skip:
            # Set skip variable to false for the next class.
            self.__skip = False
            return

        # Define r variable which is ratio of number of functions share the global variable i of a class / total
        # number of function of the class.
        r = 0
        # Calculate r value.
        for item in self.__invoked:
            r += self.__invoked.get(item) / len(self.__classes[self.__counter][2])

        # Define and calculate cc value which is the mean r cohesion count of a class of number of global variable
        # for a class.
        cc = r / len(self.__classes[self.__counter][1])
        # Append cc value to result variable.
        self.__result.append(cc)

        # Move to next class.
        self.__counter += 1
        # Reset invoked variable for the next class.
        self.__invoked = {}

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

        # Check whether to skip the class or not.
        if self.__skip:
            return

        # Reset counted variable for the new method.
        self.__counted = []

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        """
        Enter primary 4 listener.

        Parameters
        ----------
        ctx : object
            Primary 4 context

        Returns
        -------
        None
        """

        # Check whether to skip the class or not.
        if self.__skip:
            return

        # Get variable text.
        text = ctx.IDENTIFIER().getText()
        # Check if the variable is global and has not counted before.
        if text in self.__classes[self.__counter][1] and text not in self.__counted:
            # Mark the variable as counted.
            self.__counted.append(text)
            # The method uses the global variable.
            self.__invoked[text] += 1
