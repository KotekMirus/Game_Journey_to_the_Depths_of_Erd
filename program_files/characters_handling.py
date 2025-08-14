import random
from collections.abc import Callable
import json


def get_character_description(character_name: str) -> str:
    descriptions: dict[str : dict[str:str]] = None
    with open("descriptions.json", "r", encoding="utf-8") as file:
        descriptions = json.load(file)
    return descriptions["characters"][character_name]


class Character:
    def __init__(self, name: str, strength: int, max_hp: int):
        self.name: str = name
        self.max_hp: int = max_hp
        self.current_hp: int = self.max_hp
        self.max_crystal_power: int = 6
        self.current_crystal_power: int = self.max_crystal_power
        self.strength: int = strength

    def attack(self, target, console):
        target.current_hp = max(0, target.current_hp - self.strength)
        console.print(f"{self.name} dealt {self.strength} damage to {target.name}.")


class Player_Character_Arson(Character):
    def __init__(self):
        super().__init__("Arson", 2, 40)
        self.description: str = get_character_description("Arson")
        self.abilities: list[tuple[str, Callable]] = [
            ("Power Attack 1 <1CP>", self.ability_1),
            ("Power Attack 2 <2CP>", self.ability_2),
            ("Power Attack 3 <3CP>", self.ability_3),
        ]

    def attack(self, target: Character, console):
        super().attack(target, console)

    def ability_1(self, target: Character, targets: list[Character], console):
        pass

    def ability_2(self, target: Character, targets: list[Character], console):
        pass

    def ability_3(self, target: Character, targets: list[Character], console):
        pass


class Player_Character_Histri(Character):
    def __init__(self):
        super().__init__("Histri", 1, 45)
        self.description: str = get_character_description("Histri")
        self.abilities: list[tuple[str, Callable]] = [
            ("Shockwave <1CP>", self.ability_1),
            ("Life Drain <2CP>", self.ability_2),
            ("Mighty Storm <3CP>", self.ability_3),
        ]

    def attack(self, target: Character, console):
        super().attack(target, console)

    def ability_1(self, target: Character, targets: list[Character], console):
        pass

    def ability_2(self, target: Character, targets: list[Character], console):
        pass

    def ability_3(self, target: Character, targets: list[Character], console):
        pass


class Player_Character_Golrik(Character):
    def __init__(self):
        super().__init__("Golrik", 1, 40)
        self.description: str = get_character_description("Golrik")
        self.abilities: list[tuple[str, Callable]] = [
            ("Unstable Strike <1CP>", self.ability_1),
            ("Healing Circle <2CP>", self.ability_2),
            ("Random Bullshit! <3CP>", self.ability_3),
        ]

    def attack(self, target: Character, console):
        super().attack(target, console)

    def ability_1(self, target: Character, targets: list[Character], console):
        pass

    def ability_2(self, target: Character, targets: list[Character], console):
        pass

    def ability_3(self, target: Character, targets: list[Character], console):
        pass


class Enemy_Character_Frus(Character):
    def __init__(self):
        super().__init__("Frus", 1, 5)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Stone_Anomaly(Character):
    def __init__(self):
        super().__init__("Stone Anomaly", 1, 7)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        target.current_hp = max(0, target.current_hp - random.randint(1, 2))


class Enemy_Character_Dark_Goo(Character):
    def __init__(self):
        super().__init__("Dark Goo", 2, 9)
        self.description: str = "description"

    def attack(self, target: Character, targets: list[Character], console):
        for character in targets:
            character.current_hp = max(0, target.current_hp - 1)


class Enemy_Character_Xeres(Character):
    def __init__(self):
        super().__init__("Xeres", 2, 11)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Treasure_Imp(Character):
    def __init__(self):
        super().__init__("Treasure Imp", 3, 12)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Stone_Elemental(Character):
    def __init__(self):
        super().__init__("Stone Elemental", 3, 13)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        target.current_hp = max(0, target.current_hp - random.choice([2, 3, 4]))


class Enemy_Character_Blue_Crystal_Spider(Character):
    def __init__(self):
        super().__init__("Blue Crystal Spider", 4, 14)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Iris(Character):
    def __init__(self):
        super().__init__("Iris", 4, 15)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Drake(Character):
    def __init__(self):
        super().__init__("Purple-Scaled Drake", 5, 20)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Skiris(Character):
    def __init__(self):
        super().__init__("Great Skiris, Guardian of the Rykku", 5, 50)
        self.description = "description"

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)
