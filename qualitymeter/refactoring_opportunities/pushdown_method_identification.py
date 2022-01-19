"""
This module identifies push-down method refactoring opportunities in Java projects.

"""
import json
from qualitymeter.utils.walker_creator import WalkerCreator


class DetectPushDownMethod(WalkerCreator):

    def __init__(self, path, heuristic, output_name):
        WalkerCreator.__init__(self, path)
        self.__superclasses = []
        self.__methodusages = []
        self.__parents = []
        self.extractSuperClass()
        self.extractAllChildClasses()
        self.extractMethodUsage()
        self.getPushDownOpportunities(heuristic, output_name)

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
                    if par and cl:
                        if sc.identifier.getText() == par.identifier.getText():
                            sc.add_child(cl)

        for inf in self.interfaces:
            # extract child classes from extends keyword and implements keyword (used for interfaces)
            for cl2 in self.classes:
                for par2 in cl2.parents:
                    if inf and par2:
                        if inf.identifier.getText() == par2.identifier.getText():
                            inf.add_child(cl2)
                for imp in cl2.implementations:
                    if imp and inf:
                        if inf.identifier.getText() == imp.identifier.getText():
                            inf.add_child(cl2)

        self.__parents = self.__superclasses + self.interfaces

    def extractMethodUsage(self):
        """Extract all the method usages for each class and store them as method usage
        """
        methodUsages = []
        for parent in self.__parents:
            methodUsage = {"parent": parent, "methods": []}
            if parent:
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

    def getPushDownOpportunities(self, heuristic, output_name):
        """use the heuristic given by the user to extract the push down method opportunities.
        """
        Output = {
            "Method Usages": [],
            "Number Of Opportunities": 0
        }
        counter = 0
        for methodUsage in self.__methodusages:
            for method in methodUsage["methods"]:
                if method and methodUsage["parent"].children:
                    ratio = len(method["method_use"]) / \
                        len(methodUsage["parent"].children)
                    if ratio < heuristic/100 and ratio != 0:
                        ParentObject = {
                            "parent package name": methodUsage["parent"].package_name,
                            "parent name": methodUsage["parent"].identifier.getText(),
                            "original mehtod name": method["method"].identifier.getText(),
                            "opportunities": [],
                            "ratio": None
                        }
                        for usage in method["method_use"]:
                            MethodObject = {
                                "target class package name": usage["target_class"].package_name,
                                "target class name": usage["target_class"].identifier.getText(),
                                "method": [] 
                            }
                            for use in usage["usage"]:
                                params = self.get_parameters(use.parameters)
                                TargetObject = {
                                    "target method name": "{0} - args: {1}".format(
                                    use.identifier.getText(), self.unique(params))
                                }
                                MethodObject["method"].append(TargetObject)
                            counter += 1
                            ParentObject["opportunities"].append(MethodObject)
                        ParentObject["ratio"] = ratio
                        Output["Method Usages"].append(ParentObject)
        
        Output["Number Of Opportunities"] = counter
        json_object = json.dumps(Output, indent = 4)
        with open("output/" + output_name + ".json", "w") as outfile:
                            outfile.write(json_object)

        print("\noutput has been printed to  output/{0}".format(output_name))
