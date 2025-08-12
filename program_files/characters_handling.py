import random
from collections.abc import Callable
import json


def get_character_description(character_name: str) -> str:
    descriptions: dict[str : dict[str:str]] = None
    with open("descriptions.json", "r") as file:
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

    def attack(self, target):
        target.current_hp = max(0, target.current_hp - self.strength)


class Player_Character_Arson(Character):
    def __init__(self):
        super().__init__("Arson", 2, 40)
        self.description: str = get_character_description("Arson")
        self.abilities: list[tuple[str, Callable]] = [
            ("Power Attack 1 <1CP>", self.ability_1),
            ("Power Attack 2 <2CP>", self.ability_2),
            ("Power Attack 3 <3CP>", self.ability_3),
        ]

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
        self.description: str = get_character_description("Histri")
        self.abilities: list[tuple[str, Callable]] = [
            ("Shockwave <1CP>", self.ability_1),
            ("Life Drain <2CP>", self.ability_2),
            ("Mighty Storm <3CP>", self.ability_3),
        ]

    def attack(self, target: Character):
        super().attack(target)

    def ability_1(self):
        pass

    def ability_2(self):
        pass

    def ability_3(self):
        pass


class Player_Character_Golrik(Character):
    def __init__(self):
        super().__init__("Golrik", 1, 40)
        self.description: str = get_character_description("Golrik")
        self.abilities: list[tuple[str, Callable]] = [
            ("Dual strike <1CP>", self.ability_1),
            ("Healing circle <2CP>", self.ability_2),
            ("Random bullshit! <3CP>", self.ability_3),
        ]

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


class Enemy_Character_Dark_Goo(Character):
    def __init__(self):
        super().__init__("Dark Goo", 1, 15)
        self.description: str = "description"

    def attack(self, target: Character):
        target.current_hp = max(0, target.current_hp - random.randint(1, 2))
