"""


"""
from .metrics.polymorphism import Polymorphism
from .metrics.abstraction import Abstraction

class Extendability:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        # polymorphismValue = self.calcPolymorphism()
        abstractionValue = self.calcAbstraction()

    def calcAbstraction(self):
        abstractionMeter = Abstraction(self.projectPath)
        return abstractionMeter.calcAbstraction()

    def calcCoupling(self):
        pass

    def calcInheritance(self):
        pass

    def calcPolymorphism(self):
        polymorphismMeter = Polymorphism(self.projectPath)
        return polymorphismMeter.calcPolymorphism()
