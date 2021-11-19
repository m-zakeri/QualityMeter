"""


"""
from .metrics.polymorphism import Polymorphism

class Extendability:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.calcPolymorphism()

    def calcAbstraction(self):
        pass

    def calcCoupling(self):
        pass

    def calcInheritance(self):
        pass

    def calcPolymorphism(self):
        polymorphismMeter = Polymorphism(self.projectPath)
        return polymorphismMeter.calcPolymorphism()
        # get value from polymorphismMeter and return it.
