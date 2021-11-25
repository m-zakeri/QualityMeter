"""


"""
from .metrics.polymorphism import Polymorphism
from .metrics.abstraction import Abstraction

class Extendability:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.polymorphismMeter = Polymorphism(self.projectPath)
        self.abstractionMeter = Abstraction(self.projectPath)

        polymorphismValue = self.calcPolymorphism()
        abstractionValue = self.calcAbstraction()
        inheritenceValue = self.calcInheritance()

    def calcAbstraction(self):
        return self.abstractionMeter.calcAbstraction()

    def calcCoupling(self):
        pass

    def calcInheritance(self):
        return self.polymorphismMeter.calcInheritence()

    def calcPolymorphism(self):
        return self.polymorphismMeter.calcPolymorphism()
