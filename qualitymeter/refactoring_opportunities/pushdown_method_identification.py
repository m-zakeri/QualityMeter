"""
This module identifies push-down method refactoring opportunities in Java projects.

"""
from qualitymeter.utils.walker_creator import WalkerCreator


class DetectPushDownMethod(WalkerCreator):

    def __init__(self, path, heuristic):
        WalkerCreator.__init__(self, path)
        self.__superclasses = []
        self.__methodusages = []
        self.__parents = []
        self.extractSuperClass()
        self.extractAllChildClasses()
        self.extractMethodUsage()
        self.getPushDownOpportunities(heuristic)

    def get_parameters(self, params):
        """get parameters with better format

        Args:
            params (JaavaMethodParameter): raw parameters 

        Returns:
            result: list of string formated parameters 
        """
        result = []
        for param in params:
            p = "({0}) {1}".format(
                param.parameter_type, param.identifier.getText())
            result.append(p)
        return result

    def unique(self, list):
        """return unique list

        Args:
            list (array): array to be unique

        Returns:
            unique_list: list of unique values
        """

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return unique_list

    def findClass(self, class_name):
        """find one class by identifier

        Args:
            class_name (string): name of the searched class

        Returns:
            JavaClass: returns class if found
        """
        for cl in self.classes:
            if cl.identifier.getText() == class_name:
                return cl

        return None

    def extractSuperClass(self):
        """extract classes that are used as parent for another class

        """
        for cl in self.classes:
            if cl:
                for pr in cl.parents:
                    if pr:
                        parent = self.findClass(pr.identifier.getText())
                        if parent:
                            self.__superclasses.append(parent)

        self.__superclasses = self.unique(self.__superclasses)

    def extractAllChildClasses(self):
        """extract all children classes for each parent and add them to the parent as children
        """

        for sc in self.__superclasses:
            # extract child classes from extends keyword (used for classes)
            for cl in self.classes:
                for par in cl.parents:
                    if sc.identifier.getText() == par.identifier.getText():
                        sc.add_child(cl)

        for inf in self.interfaces:
            # extract child classes from extends keyword and implements keyword (used for interfaces)
            for cl2 in self.classes:
                for par2 in cl2.parents:
                    if inf.identifier.getText() == par2.identifier.getText():
                        inf.add_child(cl2)
                for imp in cl2.implementations:
                    if inf.identifier.getText() == imp.identifier.getText():
                        inf.add_child(cl2)

        self.__parents = self.__superclasses + self.interfaces

    def extractMethodUsage(self):
        """Extract all the method usages for each class and store them as method usage
        """
        methodUsages = []
        for parent in self.__parents:
            methodUsage = {"parent": parent, "methods": []}
            for method in parent.methods:
                temp_method = {"method": method, "method_use": []}
                for child in parent.children:
                    target = {"target_class": child, "usage": []}
                    for child_method in child.methods:
                        if method.identifier.getText() == child_method.identifier.getText():
                            target["usage"].append(child_method)
                    if target["usage"]:
                        temp_method["method_use"].append(target)
                methodUsage["methods"].append(temp_method)

            methodUsages.append(methodUsage)

        self.__methodusages += methodUsages

    def getPushDownOpportunities(self, heuristic):
        """use the heuristic given by the user to extract the push down method opportunities.
        """

        counter = 0
        for methodUsage in self.__methodusages:
            for method in methodUsage["methods"]:
                ratio = len(method["method_use"]) / \
                    len(methodUsage["parent"].children)
                if ratio < heuristic/100 and ratio != 0:
                    print(
                        "___________________________________________________________________")
                    print("\nparent package name: {0}".format(
                        methodUsage["parent"].package_name))
                    print("parent: {0}".format(
                        methodUsage["parent"].identifier.getText()))
                    print("method name: {0}\n".format(
                        method["method"].identifier.getText()))
                    print("\topportunities:")
                    print("\t- - - - -")
                    for usage in method["method_use"]:
                        print("\tpackage of target class: {0}".format(
                            usage["target_class"].package_name))
                        print("\ttarget class: {0}".format(
                            usage["target_class"].identifier.getText()))
                        print("\ttargets:")
                        for use in usage["usage"]:
                            params = self.get_parameters(use.parameters)
                            print("\t\ttarget method name: {0} - args: {1}".format(
                                use.identifier.getText(), self.unique(params)))
                        print("\t- - - - -")
                        counter += 1
                    print("ratio: {0}".format(ratio))

        print("\nopportunities detected ({0})".format(counter))
