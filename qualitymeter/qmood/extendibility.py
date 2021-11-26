"""


"""
from .metrics.polymorphism import Polymorphism
from .metrics.abstraction import Abstraction

class Extendability:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.polymorphismMeter = Polymorphism(self.projectPath)
        self.abstractionMeter = Abstraction(self.projectPath)

        self.polymorphismValue = self.calcPolymorphism()
        self.abstractionValue = self.calcAbstraction()
        self.inheritenceValue = self.calcInheritance()


    def calcAbstraction(self):
        return self.abstractionMeter.calcAbstraction()

    def calcCoupling(self):
        pass

    def calcInheritance(self):
        return self.polymorphismMeter.calcInheritence()

    def calcPolymorphism(self):
        return self.polymorphismMeter.calcPolymorphism()

    def getExtendabilityMeasure(self):
        return 0.5 * (self.abstractionValue + self.inheritenceValue + self.polymorphismValue)
