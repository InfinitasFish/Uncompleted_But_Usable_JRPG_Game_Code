import random


class Spell:
    def __init__(self, name, cost, dmg, typ):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = typ

    def generate_damage(self):
        dmg_l = self.dmg - 15
        dmg_h = self.dmg + 15
        return random.randrange(dmg_l, dmg_h)

    def get_cost(self):
        return self.cost

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

