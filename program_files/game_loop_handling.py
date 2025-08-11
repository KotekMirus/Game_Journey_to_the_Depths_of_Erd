from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
import questionary
import battle_loop_handling as battle
import characters_handling as characters

game_ended: bool = False
console: Console = Console()
game_start: bool = True


def initialize_party() -> list[characters.Character]:
    character_1: characters.Character = characters.Player_Character_Arson()
    character_2: characters.Character = characters.Player_Character_Histri()
    return [character_1, character_2]


def main_game_loop():
    player_characters: list[characters.Character] = initialize_party()
    inventory: dict[str:str] = {}
    inventory_usable: dict[str:int] = {
        "Healing potion (+10HP)": 0,
        "Great healing potion (+20HP)": 0,
        "Power crystal (+2CP)": 0,
        "Great power crystal (+4CP)": 0,
    }
    while not game_ended:
        if game_start:
            console.print("Początek")
            game_start = False
        choice: str = questionary.select(
            "Choose your action:",
            choices=[
                "Check party",
                "Check layer description",
                "Check inventory",
                "Use item",
                "Explore layer",
            ],
        ).ask()
        if choice == "Check party":
            battle.show_status(console, player_characters, None)
            # tutaj wyświetlenie opisów ability i opisów postaci
        elif choice == "Check layer description":
            pass
        elif choice == "Check inventory":
            console.print(inventory_usable + inventory)
        elif choice == "Use item":
            item_choices: list[questionary.Choice] = [
                questionary.Choice(
                    title=item + ": " + str(inventory_usable[item]), value=item
                )
                for item in inventory_usable
            ]
            item_key: str = questionary.select(
                "Choose item to use:", choices=item_choices
            ).ask()
            character_choices: list[questionary.Choice] = [
                questionary.Choice(title=c.name, value=i)
                for i, c in enumerate(player_characters)
            ]
            character_index: int = questionary.select(
                "Choose character:", choices=character_choices
            ).ask()
            if inventory_usable[item_key] > 0:
                if item_key == "Healing potion (+10HP)":
                    player_characters[character_index].current_hp = min(
                        player_characters[character_index].max_hp,
                        player_characters[character_index].current_hp + 10,
                    )
                elif item_key == "Great healing potion (+20HP)":
                    player_characters[character_index].current_hp = min(
                        player_characters[character_index].max_hp,
                        player_characters[character_index].current_hp + 20,
                    )
                elif item_key == "Power crystal (+2CP)":
                    player_characters[character_index].current_crystal_power = min(
                        player_characters[character_index].max_crystal_power,
                        player_characters[character_index].current_crystal_power + 2,
                    )
                elif item_key == "Great power crystal (+4CP)":
                    player_characters[character_index].current_crystal_power = min(
                        player_characters[character_index].max_crystal_power,
                        player_characters[character_index].current_crystal_power + 4,
                    )
                else:
                    console.print("This item can't be used.")
            else:
                console.print("You don't have enough X of this item.")
        elif choice == "Explore layer":
            pass
