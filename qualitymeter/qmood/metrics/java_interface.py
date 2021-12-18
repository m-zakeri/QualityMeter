"""
class JavaInterface:
- contains the information about a java interface. this information
  includes the interface name, the interfaces it extends, and the list
  of methods that the interface defines.
"""

class JavaInterface:
    def __init__(self, interface_name=""):
        self.interface_name = interface_name
        self.methods = []
        # in java, an interface can extend another interface
        self.parent_list = {}

    def add_parent(self, parent_name, parent_object=None):
        self.parent_list[parent_name] = parent_object

    def remove_parent(self, parent_name):
        self.parent_list.pop(parent_name, None)

    def add_method(self, method):
        self.methods.append(method)

    def parent_name_list(self):
        for parent_name in self.parent_list:
            yield parent_name

    def method_list(self):
        for method in self.methods:
            yield method

    def has_method(self, foreign_method):
        for method in self.methods:
            if method == foreign_method:
                return True
        for parent in self.parent_name_list():
            if self.parent_list[parent] is None:
                raise ValueError(f"Parent {parent} of Class {self.interface_name} is not Available")
            else:
                result = self.parent_list[parent].has_method(foreign_method)
                if result:
                    return True
        return False

    def get_all_parents(self):
        all_parents = []
        for parent_name, parent_object in self.parent_list.items():
            if parent_name not in all_parents:
                all_parents.append(parent_name)

            if not parent_object:
                continue

            parent_parents = parent_object.get_all_parents()
            for ancestor in parent_parents:
                if ancestor not in all_parents:
                    all_parents.append(ancestor)

        return all_parents

    def get_inherited_method_list(self):
        def is_duplicate_method(method, method_list):
            for m in method_list:
                if m == method:
                    return True
            return False

        if not self.parent_list:
            return []

        result = []
        for parent_name, parent_object in self.parent_list.items():
            if not parent_object:
                continue

            for pMethod in parent_object.method_list():
                if not is_duplicate_method(pMethod, result):
                    result.append(pMethod)

            parent_methods = parent_object.get_inherited_method_list()
            for pMethod in parent_methods:
                if not is_duplicate_method(pMethod, result):
                    result.append(pMethod)
        return result
