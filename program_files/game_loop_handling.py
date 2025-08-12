from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
import questionary
import battle_loop_handling as battle
import characters_handling as characters
import exploration_handling as exploration
import json

game_ended: bool = False
console: Console = Console()


def initialize_party() -> list[characters.Character]:
    character_1: characters.Character = characters.Player_Character_Arson()
    character_2: characters.Character = characters.Player_Character_Histri()
    character_3: characters.Character = characters.Player_Character_Golrik()
    return [character_1, character_2, character_3]


def initialize_descriptions() -> tuple[dict[str:str], dict[str:str]]:
    descriptions: dict[str : dict[str:str]] = None
    with open("descriptions.json", "r") as file:
        descriptions = json.load(file)
    return descriptions["layers"], descriptions["notes"]


def main_game_loop():
    player_characters: list[characters.Character] = initialize_party()
    layers_descriptions, notes = initialize_descriptions()
    inventory: dict[str:str] = {}
    inventory_usable: dict[str:int] = {
        "Healing potion (+10HP)": 0,
        "Great healing potion (+20HP)": 0,
        "Power crystal (+2CP)": 0,
        "Great power crystal (+4CP)": 0,
    }
    crystal_counter: int = 0
    current_layer_index: int = 0
    all_layers_contents: list[list[str, list[characters.Character]]] = (
        exploration.generate_all_layers_contents()
    )
    console.print("Początek")
    while not game_ended:
        if current_layer_index == 5:
            console.print("Final battle!")
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
            for character in player_characters:
                console.print("\n")
                console.print(character.description)
            console.print("\n")
        elif choice == "Check layer description":
            console.print(layers_descriptions[str(current_layer_index)])
        elif choice == "Check inventory":
            inventory_combined = inventory_usable | inventory
            table = Table(title="Inventory", show_lines=True)
            table.add_column("Item")
            table.add_column("Quantity/Description")
            for item, description in inventory_combined.items():
                table.add_row(item, str(description))
            console.print(table)
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
                inventory_usable[item_key] -= 1
            else:
                console.print("You don't have enough copies of this item.")
        elif choice == "Explore layer":
            place_choices: list[questionary.Choice] = [
                questionary.Choice(title="Miejsce " + str(i + 1), value=i)
                for i in range(len(all_layers_contents[current_layer_index]))
            ]
            place_index: int = questionary.select(
                "Choose place to explore:", choices=place_choices
            ).ask()
            if isinstance(all_layers_contents[current_layer_index][place_index], str):
                if all_layers_contents[current_layer_index][place_index] == "S":
                    console.print("This is gateway to upper layer.")
                    choice: str = questionary.select(
                        "Do you want to go to upper layer?:",
                        choices=[
                            "Yes",
                            "No",
                        ],
                    ).ask()
                    if choice == "Yes":
                        current_layer_index -= 1
                elif all_layers_contents[current_layer_index][place_index] == "E":
                    console.print("This is gateway to lower layer.")
                    choice: str = questionary.select(
                        "Do you want to go to lower layer?:",
                        choices=[
                            "Yes",
                            "No",
                        ],
                    ).ask()
                    if choice == "Yes":
                        current_layer_index += 1
                elif all_layers_contents[current_layer_index][place_index] == "EE":
                    console.print("You see fancy gateway with five holes.")
                    if crystal_counter == 5:
                        choice: str = questionary.select(
                            "Do you want to put collected crystals into holes?:",
                            choices=[
                                "Yes",
                                "No",
                            ],
                        ).ask()
                        if choice == "Yes":
                            console.print("Write word you want to create from runes.")
                            word: str = input("Word: ")
                            word = word.replace(" ", "")
                            if word.lower() == "sfjpx":
                                console.print("Gateway opens!")
                                current_layer_index += 1
                            else:
                                console.print("Nothing happens.")
                elif all_layers_contents[current_layer_index][place_index] == "F":
                    console.print("You found strange fountain.")
                    choice: str = questionary.select(
                        "Do you want to drink water from fountain?:",
                        choices=[
                            "Yes",
                            "No",
                        ],
                    ).ask()
                    if choice == "Yes":
                        all_layers_contents[current_layer_index][place_index] = " "
                        for character in player_characters:
                            character.current_hp = character.max_hp
                            character.current_crystal_power = (
                                character.max_crystal_power
                            )
                        console.print(
                            "Members of your party were fully regenerated (HP and CP). Strange fountain felt apart."
                        )
                elif all_layers_contents[current_layer_index][place_index][0] == "C":
                    inventory[
                        "Crystal "
                        + all_layers_contents[current_layer_index][place_index][1]
                    ] = (
                        "Strange crystal with rune '"
                        + all_layers_contents[current_layer_index][place_index][1]
                        + "'."
                    )
                    crystal_counter += 1
                    all_layers_contents[current_layer_index][place_index] = " "
                    console.print(
                        "You found strange crystal with rune. Is rune important? Probably not."
                    )
                elif all_layers_contents[current_layer_index][place_index][0] == "N":
                    console.print(
                        notes[all_layers_contents[current_layer_index][place_index]],
                        style="black on yellow",
                    )
                elif all_layers_contents[current_layer_index][place_index] == " ":
                    console.print("Nothing interesting here.")
            elif isinstance(
                all_layers_contents[current_layer_index][place_index], list
            ):
                if isinstance(
                    all_layers_contents[current_layer_index][place_index][0], str
                ):
                    for item in all_layers_contents[current_layer_index][place_index]:
                        inventory_usable[item] += 1
                    console.print("You found usefull items.")
                    console.print(
                        *all_layers_contents[current_layer_index][place_index],
                        style="#60fc65"
                    )
                    all_layers_contents[current_layer_index][place_index] = " "
                else:
                    console.print("Battle!")
