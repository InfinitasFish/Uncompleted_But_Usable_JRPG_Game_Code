class Item:
    def __init__(self, name, typ, desc, prop):
        self.name = name
        self.typ = typ
        self.desc = desc
        self.prop = prop

    def get_name(self):
        return self.name

    def get_description(self):
        return self.desc

    def get_type(self):
        return self.typ

    def get_property(self):
        return self.prop