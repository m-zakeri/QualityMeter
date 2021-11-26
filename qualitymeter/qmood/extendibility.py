"""


"""
from .metrics.polymorphism import Polymorphism
from .metrics.coupling import Coupling

class Extendability:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        polymorphismValue = self.calcPolymorphism()
        couplingValue = self.calcCoupling()

    def calcAbstraction(self):
        pass

    def calcCoupling(self):
        couplingMeter = Coupling(self.projectPath)
        return couplingMeter.calcCoupling()

    def calcInheritance(self):
        pass

    def calcPolymorphism(self):
        polymorphismMeter = Polymorphism(self.projectPath)
        return polymorphismMeter.calcPolymorphism()
