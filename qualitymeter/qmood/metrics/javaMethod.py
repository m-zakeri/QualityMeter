from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

class JavaMethod:
    def __init__(self, methodName=""):
        self.methodName = methodName
        self.parameterList = []


    def setParameterList(self, parameterList):
        if not parameterList:
            return

        formalParameters = parameterList.formalParameter()
        for parameter in formalParameters:
            if parameter.typeType().classOrInterfaceType():
                # TODO: parse class Parameters
                for classOrInterface in parameter.typeType().classOrInterfaceType().IDENTIFIER():
                    self.parameterList.append(classOrInterface.getText())
            if parameter.typeType().primitiveType():
                primitive = parameter.typeType().primitiveType()
                self.parameterList.append(self.getPrimitiveType(primitive))


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
