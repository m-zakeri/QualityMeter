"""
class JavaMethod:
- keeps the information about a method defined in java. the information contains
  method name and a list that includes the type of parameters in the order that
  they appear in the method.
- it also overloads the == operator. two methods are equal when they have the
  same method names and an equal number of parameters. when the number of
  parameters is equal, the parameter types should also match. if all of these
  cases happened, then the methods are considered equal.
"""

from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class JavaMethod:
    def __init__(self, methodName=""):
        self.methodName = methodName
        self.parameterList = []

    def getNumOfParameters(self):
        return len(self.parameterList)

    def setParameterList(self, parameterList):
        if not parameterList:
            return

        try:
            formalParameters = parameterList.formalParameter()
            for parameter in formalParameters:
                self.parameterList.append(self.getTypeOfParameter(parameter))
        except AttributeError:
            parameter = parameterList.lastFormalParameter()
            self.parameterList.append(self.getTypeOfParameter(parameter))

    def getTypeOfParameter(self, parameter):
        if parameter.typeType().classOrInterfaceType():
            for classOrInterface in parameter.typeType().classOrInterfaceType().IDENTIFIER():
                return classOrInterface.getText()
        if parameter.typeType().primitiveType():
            primitive = parameter.typeType().primitiveType()
            return self.getPrimitiveType(primitive)

    def getPrimitiveType(self, primitive):
        if primitive.BOOLEAN():
            return primitive.BOOLEAN().getText()
        if primitive.CHAR():
            return primitive.CHAR().getText()
        if primitive.BYTE():
            return primitive.BYTE().getText()
        if primitive.SHORT():
            return primitive.SHORT().getText()
        if primitive.INT():
            return primitive.INT().getText()
        if primitive.LONG():
            return primitive.LONG().getText()
        if primitive.FLOAT():
            return primitive.FLOAT().getText()
        if primitive.DOUBLE():
            return primitive.DOUBLE().getText()

    # if two function signatures are equal, __eq__ returns true
    def __eq__(self, other):
        if other.methodName != self.methodName:
            return False
        if other.getNumOfParameters() != other.getNumOfParameters():
            return False

        for parameter in zip(self.parameterList, other.parameterList):
            if parameter[0] != parameter[1]:
                return False
        return True

    def setModifier(self, modifier):
        self.modifier = modifier
