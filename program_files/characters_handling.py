import random


class Character:
    def __init__(self, name: str, strength: int, max_hp: int):
        self.name: str = name
        self.max_hp: int = max_hp
        self.current_hp: int = self.max_hp
        self.max_crystal_power: int = 6
        self.current_crystal_power: int = self.max_crystal_power
        self.strength: int = strength

    def attack(self, target):
        target.current_hp = max(0, target.current_hp - self.strength)


class Player_Character_Arson(Character):
    def __init__(self):
        super().__init__("Arson", 2, 40)
        self.abilities = ["Power Attack 1", "Power Attack 2", "Power Attack 3"]

    def attack(self, target: Character):
        super().attack(target)

    def ability_1(self):
        pass

    def ability_2(self):
        pass

    def ability_3(self):
        pass


class Player_Character_Histri(Character):
    def __init__(self):
        super().__init__("Histri", 1, 45)
        self.abilities = ["Shockwave", "Life Drain", "Mighty Storm"]

    def attack(self, target: Character):
        super().attack(target)

    def ability_1(self):
        pass

    def ability_2(self):
        pass

    def ability_3(self):
        pass


class Enemy_Character_Frus(Character):
    def __init__(self):
        super().__init__("Frus", 1, 10)
        self.description = "description"

    def attack(self, target: Character):
        super().attack(target)


class Enemy_Character_Frus(Character):
    def __init__(self):
        super().__init__("Dark Goo", 1, 15)
        self.description: str = "description"

    def attack(self, target: Character):
        target.current_hp = max(0, target.current_hp - random.randint(1, 2))
