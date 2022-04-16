import random
from Classes.Game import Person, bcolors
from Classes.Magic import Spell
from Classes.Inventory import Item


# Create Magic Spells
fire = Spell("Fire", 10, 80, "black")
thunder = Spell("Thunder", 20, 100, "black")
blizzard = Spell("Blizzard", 15, 90, "black")
meteor = Spell("Meteor", 30, 150, "black")
quake = Spell("Quake", 100, 400, "black")
on_menya_vanshotnul = Spell("VANSHOT??!", 500, 10000, "black")

heal = Spell("Heal", 15, 100, "white")
cura = Spell("Cura", 25, 150, "white")


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_pot = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 1)
hi_elixer = Item("Mega-Elixer", "elixer", "Fully restores party's HP/MP", 1)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)
dung_pie = Item("Dung Pie", "poison", "Poison Enemy For 10 Turns With 100 Dmg", [100, 10])


# Instantiate People
player_spells = [fire, thunder, meteor, blizzard, quake, heal, cura]
player1_items = [{"item": potion, "quantity": 5},
                 {"item": hi_potion, "quantity": 2},
                 {"item": grenade, "quantity": 1}]

player2_items = [{"item": grenade, "quantity": 1}]

player3_items = [{"item": hi_elixer, "quantity": 3}]

player1 = Person("SlavaInf", 400, 200, 50, 20, player_spells, player1_items + [{"item": dung_pie, "quantity": 3}])
player2 = Person("SonZai", 800, 100, 80, 40, player_spells, player2_items)
player3 = Person("InfinitasFish", 300, 500, 20, 10, player_spells + [on_menya_vanshotnul], player3_items)

players = [player1, player2, player3]

enemy1 = Person("Babadzaki", 10000, 100, 80, 50, [fire, meteor], [{"item": potion, "quantity": 2}])
enemy2 = Person("Weeb", 500, 1, 20, 5, [], [{"item": dung_pie, "quantity": 10}])
enemy3 = Person("Lol", 200, 1, 500, 10, [quake], [{}])

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==================\n\n")
    print("NAME    /   HP    /    MP:\n")
    for player in players:
        player.get_stats()

    for e in enemies:
        e.get_enemy_stats()

    for player in players:
        if player.get_hp() == 0:
            continue

        print("\n    " + bcolors.BOLD + player.get_name(), bcolors.ENDC)
        target_enemy = enemies[player.choose_target(enemies)]
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            target_enemy.take_damage(dmg)
            print(bcolors.OKBLUE + player.get_name(), "attacked",
                  target_enemy.get_name(), "for", dmg, "points of DMG.", bcolors.ENDC)

            if target_enemy.get_hp() == 0:
                print(bcolors.FAIL + target_enemy.get_name() + bcolors.ENDC, "has died!")

        elif index == 1:
            player.choose_magic()
            current_mp = player.get_mp()
            magic_choice = int(input("    Choose Magic Spell:")) - 1

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            spell_cost = spell.get_cost()
            spell_name = spell.get_name()

            if current_mp < spell_cost:
                print(bcolors.FAIL + player.get_name(), "don't have enough MP!", bcolors.ENDC)
            else:
                player.reduce_mp(spell_cost)
                if spell.get_type() == "white":
                    player.heal(magic_dmg)
                    print(bcolors.OKGREEN + spell_name, "heals", player.get_name(),
                          "for", magic_dmg, "HP.", bcolors.ENDC)
                elif spell.get_type() == "black":
                    target_enemy.take_damage(magic_dmg)
                    print(bcolors.OKBLUE + spell_name, "deals", magic_dmg, "magic DMG to",
                          target_enemy.get_name() + ".", bcolors.ENDC)

                    if target_enemy.get_hp() == 0:
                        print(bcolors.FAIL + target_enemy.get_name() + bcolors.ENDC, "has died!")

        elif index == 2:
            player.choose_item()
            item_choose = int(input("    Choose Item:")) - 1
            item = player.items[item_choose]["item"]
            item_quantity = player.items[item_choose]["quantity"]
            item_name = item.get_name()
            item_type = item.get_type()
            item_prop = item.get_property()

            if item_quantity == 0:
                print(bcolors.WARNING + player.get_name(), "don't have that item!", bcolors.ENDC)
            elif item_type == "potion":
                player.heal(item_prop)
                player.items[item_choose]["quantity"] -= 1
                print(bcolors.OKGREEN + item_name, "heals", player.get_name(), "for", item_prop, "HP.", bcolors.ENDC)
            elif item_type == "elixer":
                player.heal(player.get_max_hp())
                player.restore_mp(player.get_max_mp())
                player.items[item_choose]["quantity"] -= 1
                print(bcolors.OKGREEN + item_name, "fully restores", player.get_name(), "HP and MP.", bcolors.ENDC)
            elif item_type == "attack":
                target_enemy.take_damage(item_prop)
                player.items[item_choose]["quantity"] -= 1
                print(bcolors.OKBLUE + player.get_name(), "attacked for", item_prop, "points of DMG.", bcolors.ENDC)

                if target_enemy.get_hp() == 0:
                    print(bcolors.FAIL + target_enemy.get_name() + bcolors.ENDC, "has died!")

            elif item_type == "poison":
                target_enemy.get_poisoned(item_prop[0], item_prop[1])
                player.items[item_choose]["quantity"] -= 1
                print(player.get_name() + "'ve", bcolors.OKGREEN + "poisoned", target_enemy.get_name() +
                      bcolors.ENDC, "for", item_prop[1], "with", item_prop[0], "dmg")

    defeated_enemies = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + "You have won!" + bcolors.ENDC)
        running = False

    for enemy in enemies:
        if enemy.get_hp() == 0:
            continue

        target_index = random.randrange(0, len(players))
        target_player = players[target_index]
        e_dmg = enemy.generate_damage()

        target_player.take_damage(e_dmg)
        print(bcolors.FAIL + enemy.get_name(), "attacks", target_player.get_name(),
              "for", e_dmg, "damage.", bcolors.ENDC)

        if target_player.get_hp() == 0:
            print(bcolors.FAIL + target_player.get_name(), "has died!" + bcolors.ENDC)

        if enemy.is_poisoned():
            enemy.take_poison_damage()
            print(enemy.get_name(), "took", enemy.get_poison_prop()[0], bcolors.OKGREEN + "poison DMG.", bcolors.ENDC)

            if target_enemy.get_hp() == 0:
                print(bcolors.FAIL + target_enemy.get_name() + bcolors.ENDC, "has died!")

    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players == len(players):
        print(bcolors.FAIL + "You have lost!.." + bcolors.ENDC)
        running = False
