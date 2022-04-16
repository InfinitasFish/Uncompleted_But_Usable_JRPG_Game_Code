import random
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.poisoned = [0, 0]
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def get_name(self):
        return self.name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, heal_amount):
        self.hp += heal_amount
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def is_poisoned(self):
        return self.poisoned[1] > 0

    def get_poisoned(self, dmg, turns):
        self.poisoned = [dmg, turns]

    def take_poison_damage(self):
        self.take_damage(self.poisoned[0])
        self.poisoned[1] -= 1

    def get_poison_prop(self):
        return self.poisoned

    def restore_mp(self, mp_amount):
        self.mp += mp_amount
        if self.mp > self.maxmp:
            self.mp = self.maxmp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(bcolors.BOLD + bcolors.OKBLUE + "\n    ACTIONS:", bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\n    MAGIC:", bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ":", spell.get_name(), "(cost:", str(spell.get_cost()) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.OKGREEN + bcolors.BOLD + "\n    ITEMS:", bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ":",
                  item["item"].get_name() + ":",
                  item["item"].get_description(),
                  "(" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print(bcolors.FAIL + bcolors.BOLD + "    TARGET:", bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)

            i += 1
        return int(input("    Choose target:")) - 1

    def get_stats(self):
        if self.hp == 0:
            return
        hp_mp_display_strings = self.generate_hp_mp_strings(20, 10, 9, 9)

        print(bcolors.BOLD + self.name + "    " +
              hp_mp_display_strings[2] + "|" + bcolors.OKGREEN + hp_mp_display_strings[0] + bcolors.ENDC + "|    " +
              bcolors.BOLD +
              hp_mp_display_strings[3] + "|" + bcolors.OKBLUE + hp_mp_display_strings[1] + bcolors.ENDC + "|\n")

    def get_enemy_stats(self):
        if self.hp == 0:
            return
        hp_mp_display_strings = self.generate_hp_mp_strings(10, 5, 7, 3)

        print(bcolors.BOLD + self.name + "    " +
              hp_mp_display_strings[2] + "|" + bcolors.FAIL + hp_mp_display_strings[0] + bcolors.ENDC + "|    " +
              bcolors.BOLD +
              hp_mp_display_strings[3] + "|" + bcolors.OKBLUE + hp_mp_display_strings[1] + bcolors.ENDC + "|\n")

    def generate_hp_mp_strings(self, hp_per_tick, mp_per_tick, hp_str_len, mp_str_len):
        hp_bar = ""
        mp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * hp_per_tick
        mp_bar_ticks = (self.mp / self.maxmp) * mp_per_tick

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(hp_bar) < hp_per_tick:
            hp_bar += " "

        while len(mp_bar) < mp_per_tick:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        mp_string = str(self.mp) + "/" + str(self.maxmp)

        while len(hp_string) < hp_str_len:
            hp_string = " " + hp_string

        while len(mp_string) < mp_str_len:
            mp_string = " " + mp_string

        return [hp_bar, mp_bar, hp_string, mp_string]

