from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import questionary
import battle_loop_handling as battle
import characters_handling as characters
import exploration_handling as exploration
import json

console: Console = Console()


def initialize_party() -> list[characters.Character]:
    character_1: characters.Character = characters.Player_Character_Arson()
    character_2: characters.Character = characters.Player_Character_Histri()
    character_3: characters.Character = characters.Player_Character_Golrik()
    return [character_1, character_2, character_3]


def initialize_descriptions() -> tuple[str, str, str, dict[str:str], dict[str:str]]:
    descriptions: dict[str : dict[str:str]] = None
    with open("descriptions.json", "r", encoding="utf-8") as file:
        descriptions = json.load(file)
    return (
        descriptions["introduction"],
        descriptions["boss_introduction"],
        descriptions["ending"],
        descriptions["layers"],
        descriptions["notes"],
    )


def main_game_loop():
    player_characters: list[characters.Character] = initialize_party()
    introduction, boss_introduction, ending, layers_descriptions, notes = (
        initialize_descriptions()
    )
    discovered_locations: list[list[str]] = [["?"] * 10 for _ in range(5)]
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
    console.print(
        Panel(introduction, title="Introduction", border_style="#a4f5ea"),
        highlight=False,
    )
    while True:
        if current_layer_index == 5:
            battle_result: bool = battle.battle(
                console, player_characters, all_layers_contents[current_layer_index][0]
            )
            if battle_result:
                console.print(ending)
            else:
                console.print(
                    "Unfortunately, the Great Skiris, Guardian of the Rykku, proved far too powerful for the brave adventurers. They fell beneath the weight of his relentless attacks. [bold red]GAME OVER[/bold red]"
                )
            console.print(
                "[bold]THANK YOU FOR PLAYING <3[/bold]",
                style="#f551f2",
                highlight=False,
            )
            input("Press 'Enter' to end game.")
            break
        choice: str = questionary.select(
            "Choose your action:",
            choices=[
                "Check party",
                "Check layer description",
                "Check the discovered locations",
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
        elif choice == "Check the discovered locations":
            console.print(
                "You are currently on layer " + str(current_layer_index + 1) + "."
            )
            table: Table = Table(title="Discovered locations", show_lines=True)
            table.add_column("Layer")
            for i in range(10):
                table.add_column("Place " + str(i + 1))
            for i in range(len(discovered_locations)):
                table.add_row(str(i + 1), *discovered_locations[i])
            console.print(table)
            console.print(
                "EU - exit to upper layer\nEL - exit to lower layer\ni  - useful information\nF  - fountain\nN  - nothing\n"
            )
        elif choice == "Check inventory":
            inventory_combined = inventory_usable | inventory
            table: Table = Table(title="Inventory", show_lines=True)
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
            item_choices.append(questionary.Choice(title="Back", value="Back"))
            item_key: str = questionary.select(
                "Choose item to use:", choices=item_choices
            ).ask()
            if item_key == "Back":
                continue
            character_choices: list[questionary.Choice] = [
                questionary.Choice(title=c.name, value=i)
                for i, c in enumerate(player_characters)
            ]
            character_choices.append(questionary.Choice(title="Back", value="Back"))
            character_index: int = questionary.select(
                "Choose character:", choices=character_choices
            ).ask()
            if character_index == "Back":
                continue
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
            console.print(
                "You are currently on layer " + str(current_layer_index + 1) + "."
            )
            place_choices: list[questionary.Choice] = [
                questionary.Choice(title="Place " + str(i + 1), value=i)
                for i in range(len(all_layers_contents[current_layer_index]))
            ]
            place_index: int = questionary.select(
                "Choose place to explore:", choices=place_choices
            ).ask()
            if isinstance(all_layers_contents[current_layer_index][place_index], str):
                if all_layers_contents[current_layer_index][place_index] == "S":
                    discovered_locations[current_layer_index][place_index] = "EU"
                    console.print("This is the gateway to the upper layer.")
                    choice: str = questionary.select(
                        "Do you want to go to upper layer?",
                        choices=[
                            "Yes",
                            "No",
                        ],
                    ).ask()
                    if choice == "Yes":
                        current_layer_index -= 1
                elif all_layers_contents[current_layer_index][place_index] == "E":
                    discovered_locations[current_layer_index][place_index] = "EL"
                    console.print("This is the gateway to the lower layer.")
                    choice: str = questionary.select(
                        "Do you want to go to lower layer?",
                        choices=[
                            "Yes",
                            "No",
                        ],
                    ).ask()
                    if choice == "Yes":
                        current_layer_index += 1
                elif all_layers_contents[current_layer_index][place_index] == "EE":
                    discovered_locations[current_layer_index][place_index] = "EL"
                    console.print(
                        'Before you stands a massive slab of cream-colored material. Countless swirling patterns are carved into the pale stone. At about the height of your head, five precisely cut holes are set into the slab, each surrounded by a gilded frame shaped like the fangs of an open maw. Above them, an inscription in the Dekti language reads: "Heart of the Rykku."',
                        highlight=False,
                    )
                    if crystal_counter == 5:
                        choice: str = questionary.select(
                            "Do you want to put the collected crystals into the holes?",
                            choices=[
                                "Yes",
                                "No",
                            ],
                        ).ask()
                        if choice == "Yes":
                            console.print(
                                "Write the word you want to create from the runes."
                            )
                            word: str = input("Word: ")
                            word = word.replace(" ", "")
                            if word.lower() == "sfjpx":
                                console.print(
                                    "When you placed the strange crystals into the openings in the slab, the gate slowly slid into the ground with a distinctive grinding sound, leaving a wide and even taller passage leading into a dark chamber."
                                )
                                current_layer_index += 1
                            else:
                                console.print("Nothing happens.")
                elif all_layers_contents[current_layer_index][place_index] == "F":
                    discovered_locations[current_layer_index][place_index] = "F"
                    console.print(
                        "Amid the tunnels rich with precious deposits, you find a small fountain crafted from silver metal. Water slowly trickles from its tip, flowing along its ornate carvings into the basin below. The liquid shimmers with all the colors of the rainbow."
                    )
                    choice: str = questionary.select(
                        "Do you want your party to drink from the fountain?",
                        choices=[
                            "Yes",
                            "No",
                        ],
                    ).ask()
                    if choice == "Yes":
                        discovered_locations[current_layer_index][place_index] = "N"
                        all_layers_contents[current_layer_index][place_index] = " "
                        for character in player_characters:
                            character.current_hp = character.max_hp
                            character.current_crystal_power = (
                                character.max_crystal_power
                            )
                        console.print(
                            "The water tasted like tomato juice. Your party members have been fully restored (HP and CP). The mysterious fountain crumbled, its liquid instantly sinking into the ground, while the once-silver fragments turned into ordinary stone."
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
                    discovered_locations[current_layer_index][place_index] = "N"
                    all_layers_contents[current_layer_index][place_index] = " "
                    console.print(
                        "You found a [#bb3efa]strange crystal[/#bb3efa] with a rune. Is the rune important? Probably not."
                    )
                elif all_layers_contents[current_layer_index][place_index][0] == "N":
                    discovered_locations[current_layer_index][place_index] = "i"
                    console.print(
                        notes[all_layers_contents[current_layer_index][place_index]],
                        style="black on yellow",
                        highlight=False,
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
                    console.print("You found useful items.")
                    console.print(
                        *all_layers_contents[current_layer_index][place_index],
                        style="#60fc65"
                    )
                    discovered_locations[current_layer_index][place_index] = "N"
                    all_layers_contents[current_layer_index][place_index] = " "
                else:
                    battle_result: bool = battle.battle(
                        console,
                        player_characters,
                        all_layers_contents[current_layer_index][place_index],
                    )
                    if battle_result:
                        console.print("The enemies have been defeated by your party!")
                        discovered_locations[current_layer_index][place_index] = "N"
                        all_layers_contents[current_layer_index][place_index] = " "
                    else:
                        console.print(
                            "Unfortunately, the enemies have overwhelmed you. Your party has fallen. [bold red]GAME OVER[/bold red]"
                        )
                        input("Press 'Enter' to end game.")
                        break
