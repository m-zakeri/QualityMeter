"""
implement the functionality module
functionality = 0.12 * Cohesion + 0.22 * Polymorphism + 0.22 * Messaging +
                0.22 * Design Size + 0.22 * Hierarchies

"""

from qualitymeter.java_components.walker import WalkerCreator


class Functionality(WalkerCreator):
    def __init__(self, streams):
        WalkerCreator.__init__(self, streams)

    def calc_cohesion(self):
        """
        calculating cohesion.

        This class calculates cohesion among methods of class.
        Cohesion Among Methods of Class (CAM) : computes the relatedness among methods of a class
        based upon the parameter list of the methods.

        :return: average cc
        """

        cc = 0
        for cls in self.classes:
            attributes_len = len(cls.attribute)
            methods_len = len(cls.methods)
            if attributes_len == 0 or methods_len == 0:
                continue
            invoked = {}
            for attr in cls.attribute:
                invoked[attr.identifier] = 0
            for method in cls.methods:
                counted_once = []
                for variable in method.variables:
                    for attr in cls.attribute:
                        if variable in str(attr.identifier) and variable not in counted_once:
                            invoked[attr.identifier] += 1
                            counted_once.append(str(attr.identifier))
            r = 0
            for item in invoked:
                r += invoked.get(item) / methods_len
            cc += r / attributes_len

        return cc / len(self.classes)

    def calc_design_size(self):
        """
        calculating design size.

        This class calculates design size in classes.
        Design Size of Classes (DSC) : a count of the total number of classes in the design.

        :return: count of all the classes
        """

        result = 0
        for _ in self.classes:
            result += 1

        return result

    def calc_polymorphism(self):
        """
        calculating polymorphism.

        This class calculates number of polymorphic methods.
        Number of Polymorphic Methods (NOP) : a count of the methods that can
        exhibit polymorphic behavior.

        :return: results
        """

        polymorphic_methods = []
        for cls in self.classes:
            polymorphic = 0
            if cls:
                for clmt in cls.methods:
                    if "public" in clmt.modifiers:
                        polymorphic += 1
                polymorphic_methods.append(polymorphic)

        for inf in self.interfaces:
            polymorphic = 0
            if inf:
                for _ in inf.methods:
                    polymorphic += 1
                polymorphic_methods.append(polymorphic)

        if len(polymorphic_methods) != 0:
            result = sum(polymorphic_methods) / len(polymorphic_methods)
        else:
            result = 0

        return result

    def calc_classInterfaceSize(self):
        """
        calculating class interface size.

        This class calculates class interface size.
        Class Interface Size (CIS) : a count of the number of public methods in a class.

        :return: result
        """
        public_methods = []
        for cls in self.classes:
            public = 0
            if cls:
                for clmt in cls.methods:
                    if "public" in clmt.modifiers:
                        public += 1
                    public_methods.append(public)
        result = sum(public_methods) / len(self.classes)
        return result

    def calc_hierarchies(self):
        """
        calculating number of hierarchies.

        This class calculates number of hierarchies.
        Number of Hierarchies (NOH) : a count of the number of class hierarchies in the design.
        """

        hierarchies = 0
        for _ in self.hierarchies:
            hierarchies += 1
        return hierarchies

    def get_value(self):
        """
        returning the final results along the Design Property metrics.

        :return: functionality
        """

        cohesion = self.calc_cohesion()
        design_size = self.calc_design_size()
        polymorphism = self.calc_polymorphism()
        messaging = self.calc_classInterfaceSize()
        hierarchies = self.calc_hierarchies()
        functionality = 0.12 * cohesion + 0.22 * polymorphism + 0.22 * design_size + \
                        0.22 * messaging + 0.22 * hierarchies

        return functionality
