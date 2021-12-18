"""


"""
from .metrics.polymorphism import Polymorphism
from .metrics.abstraction import Abstraction
from .metrics.coupling import Coupling

class Extendability:
    def __init__(self, project_path):
        self.project_path = project_path
        self.polymorphism_meter = Polymorphism(self.project_path)
        self.abstraction_meter = Abstraction(self.project_path)

        self.polymorphism_value = self.calc_polymorphism()
        self.abstraction_value = self.calc_abstraction()
        self.inheritance_value = self.calc_inheritance()
        self.coupling_value = self.calc_coupling()

        print("Polymorphism = ", self.polymorphism_value)
        print("Abstraction = ", self.abstraction_value)
        print("Inheritance = ", self.inheritance_value)
        print("Coupling = ", self.coupling_value)

    def calc_abstraction(self):
        return self.abstraction_meter.calc_abstraction()

    def calc_coupling(self):
        coupling_meter = Coupling(self.project_path)
        return coupling_meter.calc_coupling()

    def calc_inheritance(self):
        return self.polymorphism_meter.calc_inheritence()

    def calc_polymorphism(self):
        return self.polymorphism_meter.calc_polymorphism()

    def get_extendability_measure(self):
        return 0.5 * (self.abstraction_value - self.coupling_value
                + self.inheritance_value + self.polymorphism_value)
