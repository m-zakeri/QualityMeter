class JavaModifier:
    def __init__(self):
        self.PRIVATE = False
        self.FINAL = False
        self.STATIC = False

    def set_final_flag(self, flag):
        self.FINAL = flag

    def set_private_flag(self, flag):
        self.FINAL = flag

    def set_static_flag(self, flag):
        self.STATIC = flag

    def is_final(self):
        return self.FINAL

    def is_private(self):
        return self.PRIVATE

    def is_static(self):
        return self.STATIC
