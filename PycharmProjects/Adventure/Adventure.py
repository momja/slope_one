__author__ = 'maxomdal'

import random


class Map(object):  # Creates a map that the player can navigate through in order to comlete the game
    pass


class Enemy(object):    # Creates a class of the enemy that will be used repeatedly to produce multiple enemies. Later,
    # more enemies can be created from subclasses of Enemy class
    def __init__(self, health):
        self.health = health

    def enemy_move(self, total_defense):
        if random.randint(0, 1) == 0:  # The enemy hits you based on a random chance
            print "your enemy tried to attack but missed!"
        else:
            print "your enemy attacked"

            def find_damage(enemy_attack):
                total_damage = enemy_attack - total_defense
                if total_damage < 0:
                    total_damage = 0
                return total_damage
            character.health -= find_damage(random.randint(5, 15))
        if self.health <= 0:
            character.battle_won()


enemy = Enemy(50)


def play_again():
        print "You are now faced with a new enemy!"
        enemy.health = 50
        character.player_fight(True)


class Player(object):

    # All of the attacks are broken down into specific groups based on you level.
    # Dict 1 contains all of the attacks for level one players, and so on
    # The first number in the tuple is the limit to how many times an attack can be used
    all_attacks_combat = [{"Punch": [20, 20, 12], "Kick": [30, 30, 8], "Headbutt": [30, 30, 6]},
                   {"Slide": [30, 30, 10],  "Side Kick": [15, 15, 15], "Uppercut": [20, 20, 10]},
                   {"Karate Chop": [20, 20, 15], "Throw Enemy": [10, 10, 20], "Double Slap": [10, 10, 15, 15]},
                   {"Triple Kick": [10, 10, 20, 15, 10], "Side Kick To Heart": [5, 5, 80], "Triple Side Kick": [5, 5, 10, 14, 50]}]
    all_attacks_sword = [{}, {}, {}]
    all_attacks_gun = [{}, {}, {}]
    # All of the defenses are broken down into specific groups based on your level.
    # Dict 1 contains all of the defenses for level one players, and so on
    # The first number in the tuple shows you the damage it will protect you from, and the second is a float that
    # gives probability of the attack working
    all_defenses = [{"Block": [5, 1], "Recover": [7, 0.75]},
                    {"Retreat": [8, 0.75], "Shield": [9, 0.6]},
                    {"Duck": [10, 0.70], "Cover": [15, 0.5]}]

    def __init__(self, name):
        self.name = name
        self.health = 100
        self.wallet = 0
        self.potions = {"Elixir": 1, "Stats Boost": 0, "Attack Boost": 0, "Defense Boost": 0}
        self.experience = 0
        self.level = 1
        self.run = False
        self.total_defense = 0
        self.information = {"Wallet": self.wallet, "Potions": self.potions,
                            "XP": self.experience, "Level": self.level,
                            "Attack Set": self.all_attacks_combat[self.level - 1],
                            "Defense Set": self.all_defenses[self.level - 1]}
        print "It is nice to meet you %s, I am your guardian. I will watch as you battle your way through this game." \
              "To get started, press the number associated with the given object, then hit enter. If you wish to visit the store, or check your inventory, just enter 'store', or 'inventory'" % self.name
        print

    def list_options(self, attacks, defenses):
        print "what would you like to do next?"
        print "1 " + attacks.keys()[0], "%i/%i" % (attacks.values()[0][0], attacks.values()[0][1])
        print "2 " + attacks.keys()[1], "%i/%i" % (attacks.values()[1][0], attacks.values()[1][1])
        print "3 " + attacks.keys()[2], "%i/%i" % (attacks.values()[2][0], attacks.values()[2][1])
        print "4 " + defenses.keys()[0]
        print "5 " + defenses.keys()[1]
        print "6 " + "Run"
        answer = raw_input()
        if answer == "inventory":
            print "Items in inventory: " + str(self.information.items())
            return False
        elif answer == "store":
            print "Items in store: "
            self.list_store()
            return  False
        elif answer == "elixir":
            if self.potions["Elixir"] > 0:
                self.health += 30
                print "you used an elixir to heal yourself."
                self.potions["Elixir"] -= 1
            else:
                print "you are out of elixir"
            return False
        else:
            if answer == "1" or answer == "2" or answer == "3" or answer == "4" or answer == "5" or answer == "6":
                return int(answer)
            else:
                self.list_options(attacks, defenses)

    def battle_over(self):
        self.wallet = 0
        self.potions["Elixir"] = 0

    def battle_won(self):
        money_earned = random.randint(5, 2000)
        print "You beat your foe! Congratulations, you earned %i Gold" % money_earned
        character.wallet += money_earned
        character.experience += 10
        if character.experience >= 50:
            character.level += 1
            self.new_attack_set()
            print "You have leveled up!"
        print
        print "You won the battle"
        play_again()

    def player_fight(self, move):
        def use_attack(attack_choice):
            print
            if attack_choice < 3 and attacks.values()[attack_choice][0] != 0:
                print "you %s him" % attacks.keys()[attack_choice]
                enemy.health -= attacks.values()[attack_choice][-1]
                print "Enemy Health: %i" % enemy.health
                attacks.values()[attack_choice][0] -= 1
            elif attack_choice < 5:
                if random.random() < defenses.values()[attack_choice - 3][1]:
                    print "you defended yourself with %s" % defenses.keys()[attack_choice - 3]
                    self.total_defense = defenses.values()[attack_choice - 3][0]
                else:
                    print "your defense failed to work!"
            elif attack_choice == 5:
                print "you attempt to run away"
                if random.randint(0, 2) == 0:
                    print "you got away"
                    self.run = True
                else:
                    print "you can't get away, keep fighting"
            else:
                print "you did not move"
        print
        if self.health > 0:
            if move is not False:
                enemy.enemy_move(self.total_defense)
            self.total_defense = 0
            print "Your Health: %i" % self.health
            attacks = self.information["Attack Set"]
            defenses = self.information["Defense Set"]
            move = self.list_options(attacks, defenses)
            if move is not False:
                use_attack(move - 1)
        else:
            print "You died in the epic battle. Better luck next time..."
            self.battle_over()
        if enemy.health <= 0:
            self.battle_won()
        elif self.run is True:
            pass
        else:
            self.player_fight(move)

    def new_attack_set(self):
        self.information["Attack Set"] = self.all_attacks_combat[self.level - 1]

    def list_store(self):
        elixir_price = 10
        sword_price = 100
        print "Money:" + str(self.wallet)
        print
        print "1 Elixir: " + str(elixir_price)
        print "2 Sword: " + str(sword_price)
        answer = raw_input("Choose Item, or type exit: ")
        if answer == "1":
            if self.wallet >= elixir_price:
                print "You bought Elixir for 10 Gold"
                print
                print "Type 'elixir' to heal yourself and consume your elixir"
                self.wallet -= elixir_price
                self.potions["Elixir"] += 1
            else:
                print "you do not have enough money to buy this item. Sorry. Come back later!"
                self.list_store()
        elif answer == "2":
            if self.wallet >= sword_price:
                print "You purchased a sword! The sword will give you a whole new set of powerful attacks."
                self.wallet -= sword_price
            else:
                print "you do not have enough money to buy this item. Sorry. Come back later!"
        else:
            print "you leave the store"



character = Player(raw_input("What is your name? "))


def begin_game():
        print "You have ran into an enemy! He wants to fight you and take your possesions!" \
              "Do not lose or you will have to start over."
        character.player_fight(0)

begin_game()
