"""


"""

from qualitymeter.properties.coupling import Coupling
from qualitymeter.properties.cohesion import Cohesion
from .quality_attribute import QualityAttribute


class Understandability(QualityAttribute):
    def __init__(self, stream):
        QualityAttribute.__init__(self, stream)

    def calc_coupling(self):
        listener = Coupling(self.common_listener.classes_name)
        self.walker.walk(listener, self.parse_tree)
        return sum(listener.result) / len(listener.result)

    def calc_cohesion(self):
        listener = Cohesion(self.common_listener.classes)
        self.walker.walk(listener, self.parse_tree)
        return sum(listener.result) / len(listener.result)

    def get_value(self):
        coupling = self.calc_coupling()
        cohesion = self.calc_cohesion()

        print('Coupling: ' + str(coupling))
        print('Cohesion: ' + str(cohesion))

        # raise NotImplementedError()    # TODO: Calculate Understandability Formula
