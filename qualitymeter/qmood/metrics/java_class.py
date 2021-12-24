"""
class JavaClass:
- contains the information about a java class. this information include
  class name, the classes it extends, the interfaces it implements and
  the methods it has.
"""


class JavaClass:
    def __init__(self, class_name=""):
        self.class_name = class_name
        self.methods = []
        self.parent_class_list = {}
        self.interface_list = {}

    def set_class_name(self, cls_name):
        self.class_name = cls_name

    def add_method(self, method):
        self.methods.append(method)

    def add_parent(self, parent_name, parent_object=None):
        self.parent_class_list[parent_name] = parent_object

    def remove_parent(self, parent_name):
        self.parent_class_list.pop(parent_name, None)

    def get_parent(self, parent_name):
        return self.parent_class_list.get(parent_name)

    def has_parent(self):
        if self.parent_class_list:
            return True
        return False

    def addInterface(self, interfaceName, interfaceObject=None):
        self.interface_list[interfaceName] = interfaceObject

    def remove_interface(self, interface_name):
        self.interface_list.pop(interface_name, None)

    def get_interface(self, interface_name):
        return self.interface_list.get(interface_name)

    def has_method(self, foreign_method):
        for method in self.methods:
            if method == foreign_method:
                return True

        for parent in self.parent_name_list():
            if self.parent_class_list[parent] is None:
                raise ValueError(f"Parent {parent} of Class {self.class_name} is not Available")
            else:
                result = self.parent_class_list[parent].has_method(foreign_method)
                if result:
                    return True

        for interface in self.interface_name_list():
            if self.interface_list[interface] is None:
                raise ValueError(f"Parent {interface} of Class {self.class_name} is not Available")
            else:
                result = self.interface_list[interface].has_method(foreign_method)
                if result:
                    return True
        return False

    def parent_name_list(self):
        for parent_name in self.parent_class_list:
            yield parent_name

    def parent_object_list(self):
        for parent_name in self.parent_class_list:
            yield self.parent_class_list[parent_name]

    def method_list(self):
        for method in self.methods:
            yield method

    def interface_name_list(self):
        for interface_name in self.interface_list:
            yield interface_name

    def interface_object_list(self):
        for interface_name in self.interface_list:
            yield self.interface_list[interface_name]

    def get_all_parents(self):
        all_parents = []
        for interface_name, interface_object in self.interface_list.items():
            if interface_name not in all_parents:
                all_parents.append(interface_name)

            # when interface is a built-in java interface, its object is None
            if not interface_object:
                continue

            parent_parents = interface_object.get_all_parents()
            for ancestor in parent_parents:
                if ancestor not in all_parents:
                    all_parents.append(ancestor)

        for class_name, class_object in self.parent_class_list.items():
            if class_name not in all_parents:
                all_parents.append(class_name)

            if not class_object:
                continue

            parent_parents = class_object.get_all_parents()
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

        if not self.parent_class_list and not self.interface_list:
            return []

        result = []
        for interface_name, interface_object in self.interface_list.items():
            if not interface_object:
                continue

            for iMethod in interface_object.method_list():
                if not is_duplicate_method(iMethod, result):
                    result.append(iMethod)

            inherited_methods = interface_object.get_inherited_method_list()
            for method in inherited_methods:
                if not is_duplicate_method(method, result):
                    result.append(method)

        for class_name, class_object in self.parent_class_list.items():
            if not class_object:
                continue

            for method in class_object.method_list():
                if not is_duplicate_method(method, result):
                    result.append(method)

            inherited_methods = class_object.get_inherited_method_list()
            for method in inherited_methods:
                if not is_duplicate_method(method, result):
                    result.append(method)

        return result
