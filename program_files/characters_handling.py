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
        console.print(f"{self.name} dealt {self.strength} damage to {target.name}.\n")


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
        if self.current_crystal_power >= 1:
            target.current_hp = max(0, target.current_hp - 5)
            console.print(f"{self.name} dealt 5 damage to {target.name}.\n")
            self.current_crystal_power -= 1
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )

    def ability_2(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 2:
            target.current_hp = max(0, target.current_hp - 10)
            console.print(f"{self.name} dealt 10 damage to {target.name}.\n")
            self.current_crystal_power -= 2
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )

    def ability_3(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 3:
            target.current_hp = max(0, target.current_hp - 15)
            console.print(f"{self.name} dealt 15 damage to {target.name}.\n")
            self.current_crystal_power -= 3
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )


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
        if self.current_crystal_power >= 1:
            for character in targets:
                character.current_hp = max(0, character.current_hp - 2)
            console.print(f"{self.name} dealt 2 damage to all enemies.\n")
            self.current_crystal_power -= 1
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )

    def ability_2(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 2:
            target.current_hp = max(0, target.current_hp - 4)
            console.print(f"{self.name} dealt 4 damage to {target.name}.")
            self.current_hp = min(self.max_hp, self.current_hp + 4)
            console.print(f"{self.name} healed herself for 4.\n")
            self.current_crystal_power -= 2
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )

    def ability_3(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 3:
            for character in targets:
                character.current_hp = max(0, character.current_hp - 6)
            console.print(f"{self.name} dealt 6 damage to all enemies.\n")
            self.current_crystal_power -= 3
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )


class Player_Character_Golrik(Character):
    def __init__(self):
        super().__init__("Golrik", 1, 40)
        self.description: str = get_character_description("Golrik")
        self.abilities: list[tuple[str, Callable]] = [
            ("Unstable Strike <1CP>", self.ability_1),
            ("Unpredictable Wave <2CP>", self.ability_2),
            ("Random Bullshit! <3CP>", self.ability_3),
        ]

    def attack(self, target: Character, console):
        super().attack(target, console)

    def ability_1(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 1:
            damage: int = random.randint(1, 5)
            target.current_hp = max(0, target.current_hp - damage)
            console.print(f"{self.name} dealt {damage} damage to {target.name}.")
            health: int = random.randint(1, 5)
            self.current_hp = min(self.max_hp, self.current_hp + health)
            console.print(f"{self.name} healed himself for {health}.\n")
            self.current_crystal_power -= 1
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )

    def ability_2(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 2:
            damage: int = random.randint(2, 4)
            for character in targets:
                character.current_hp = max(0, character.current_hp - damage)
            console.print(f"{self.name} dealt {damage} damage to all enemies.")
            health: int = random.randint(1, 3)
            self.current_hp = min(self.max_hp, self.current_hp + health)
            console.print(f"{self.name} healed himself for {health}.\n")
            self.current_crystal_power -= 2
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )

    def ability_3(self, target: Character, targets: list[Character], console):
        if self.current_crystal_power >= 3:
            damage: int = random.randint(3, 30)
            target.current_hp = max(0, target.current_hp - damage)
            console.print(f"{self.name} dealt {damage} damage to {target.name}.\n")
            self.current_crystal_power -= 3
        else:
            console.print(
                "You tried to use an ability without having enough CP. You lost your turn.\n"
            )


class Enemy_Character_Frus(Character):
    def __init__(self):
        super().__init__("Frus", 1, 5)
        self.description = (
            "Frus - a half-meter-tall, rat-like creature moving on two legs."
        )

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Stone_Anomaly(Character):
    def __init__(self):
        super().__init__("Stone Anomaly", 1, 7)
        self.description = "Stone Anomaly - a small air vortex lifting tiny pebbles."

    def attack(self, target: Character, targets: list[Character], console):
        damage: int = random.randint(1, 2)
        target.current_hp = max(0, target.current_hp - damage)
        console.print(f"{self.name} dealt {damage} damage to {target.name}.\n")


class Enemy_Character_Dark_Goo(Character):
    def __init__(self):
        super().__init__("Dark Goo", 2, 9)
        self.description: str = "Dark Goo - a blob of black slime."

    def attack(self, target: Character, targets: list[Character], console):
        for character in targets:
            character.current_hp = max(0, character.current_hp - 1)
        console.print(f"{self.name} dealt 1 damage to all party members.\n")


class Enemy_Character_Xeres(Character):
    def __init__(self):
        super().__init__("Xeres", 2, 11)
        self.description = "Xeres - a red, spherical spirit floating in the air."

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)
        self.current_hp = min(self.max_hp, self.current_hp + 1)
        console.print(f"{self.name} healed himself for 1.\n")


class Enemy_Character_Treasure_Imp(Character):
    def __init__(self):
        super().__init__("Treasure Imp", 3, 12)
        self.description = "Treasure Imp - a short, hunched creature with an earthy complexion, carrying a sturdy sack on its back."

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)
        target.current_crystal_power = max(0, target.current_crystal_power - 1)
        console.print(f"{self.name} drained 1 CP from {target.name}.\n")


class Enemy_Character_Stone_Elemental(Character):
    def __init__(self):
        super().__init__("Stone Elemental", 3, 13)
        self.description = "Stone Elemental - a small tornado lifting medium-sized rocks, crackling with green energy inside."

    def attack(self, target: Character, targets: list[Character], console):
        damage: int = random.choice([2, 3, 4])
        target.current_hp = max(0, target.current_hp - damage)
        console.print(f"{self.name} dealt {damage} damage to {target.name}.\n")


class Enemy_Character_Blue_Crystal_Spider(Character):
    def __init__(self):
        super().__init__("Blue Crystal Spider", 3, 14)
        self.description = "Blue Crystal Spider - a six-legged creature whose limbs are made of blue crystal blocks with hexagonal bases. At the center of its body rests a transparent crystal fragment, inside of which a small storm can be seen."

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)
        for character in targets:
            character.current_hp = max(0, character.current_hp - 1)
        console.print(f"{self.name} dealt 1 damage to all party members.\n")


class Enemy_Character_Iris(Character):
    def __init__(self):
        super().__init__("Iris", 4, 15)
        self.description = "Iris - a rainbow-colored, spherical spirit hovering in the air, scattering colorful sparks."

    def attack(self, target: Character, targets: list[Character], console):
        random_target_index: int = random.randint(0, len(targets) - 1)
        targets[random_target_index].current_hp = max(
            0, targets[random_target_index].current_hp - 3
        )
        console.print(
            f"{self.name} dealt 3 damage to {targets[random_target_index].name}."
        )
        random_target_index: int = random.randint(0, len(targets) - 1)
        targets[random_target_index].current_hp = max(
            0, targets[random_target_index].current_hp - 2
        )
        console.print(
            f"{self.name} dealt 2 damage to {targets[random_target_index].name}.\n"
        )


class Enemy_Character_Drake(Character):
    def __init__(self):
        super().__init__("Purple-Scaled Drake", 5, 20)
        self.description = "Purple-Scaled Drake - a massive drake with metallic-sheened purple scales, clutching an ornate spear in its claws."

    def attack(self, target: Character, targets: list[Character], console):
        super().attack(target, console)


class Enemy_Character_Skiris(Character):
    def __init__(self):
        super().__init__("Great Skiris, Guardian of the Rykku", 6, 60)
        self.description = "Great Skiris, Guardian of the Rykku - a gigantic snake with golden scales, adorned with pieces of silver armor."

    def attack(self, target: Character, targets: list[Character], console):
        if self.current_hp > 40:
            super().attack(target, console)
        elif self.current_hp > 20:
            for _ in range(3):
                random_target_index: int = random.randint(0, len(targets) - 1)
                targets[random_target_index].current_hp = max(
                    0, targets[random_target_index].current_hp - 3
                )
                console.print(
                    f"{self.name} dealt 3 damage to {targets[random_target_index].name}.\n"
                )
        else:
            target.current_hp = max(0, target.current_hp - 4)
            console.print(f"{self.name} dealt 3 damage to {target.name}.")
            for character in targets:
                character.current_hp = max(0, character.current_hp - 2)
            console.print(f"{self.name} dealt 3 damage to all party members.\n")
