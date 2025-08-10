from characters_handling import Character
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
import questionary


def show_status(
    console: Console, player_characters: list[Character], enemies: list[Character]
):
    player_characters_panels: list[Panel] = [
        Panel(
            f"HP: {character.current_hp}/{character.max_hp}\nCP: {character.current_crystal_power}/{character.max_crystal_power}",
            title=character.name,
        )
        for character in player_characters
    ]
    enemies_panels: list[Panel] = [
        Panel(
            f"HP: {enemy.current_hp}/{enemy.max_hp}",
            title=enemy.name,
        )
        for enemy in enemies
    ]
    player_group: Panel = Panel(
        Columns(player_characters_panels, expand=True, equal=True),
        title="Party",
        border_style="yellow",
    )
    enemies_group: Panel = Panel(
        Columns(enemies_panels, expand=True, equal=True),
        title="Enemies",
        border_style="yellow",
    )
    console.print(player_group)
    console.print(enemies_group)


def battle(
    console: Console, player_characters: list[Character], enemies: list[Character]
):
    console.rule(f"[bold green]Battle[/bold green]")
    battle_ended: bool = False
    while not battle_ended:
        for player_character in player_characters:
            show_status(console, player_characters, enemies)
            console.rule(f"[bold green]{player_character.name}'s turn[/bold green]")
            choice: str = questionary.select(
                "Choose your action:", choices=["Attack", "Use ability", "End turn"]
            ).ask()
            target_choices: list[questionary.Choice] = [
                questionary.Choice(title=e.name, value=i) for i, e in enumerate(enemies)
            ]
            if choice == "Attack":
                target_index: int = questionary.select(
                    "Choose your target:", choices=target_choices
                ).ask()
                player_character.attack(enemies[target_index])
            elif choice == "Use ability":
                abilities_choices: list[questionary.Choice] = [
                    questionary.Choice(title=e.name, value=i)
                    for i, e in enumerate(player_character.abilities)
                ]
                ability_index: int = questionary.select(
                    "Choose your ability:",
                    choices=abilities_choices,
                ).ask()
                target_index: int = questionary.select(
                    "Choose your target:", choices=target_choices
                ).ask()
                # użycie umiejętności
            elif choice == "End turn":
                pass
        for enemy in enemies:
            console.rule(f"[bold green]{enemy.name}'s turn[/bold green]")
            # tu atakują przeciwnicy


# warunek zakończenia battle (deaths)
