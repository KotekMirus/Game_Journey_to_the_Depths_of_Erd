from characters_handling import Character
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
import questionary
import random
from collections.abc import Callable


def show_status(
    console: Console, player_characters: list[Character], enemies: list[Character]
):
    player_characters_panels: list[Panel] = [
        Panel(
            f"STR: {character.strength}\nHP: {character.current_hp}/{character.max_hp}\nCP: {character.current_crystal_power}/{character.max_crystal_power}",
            title=character.name,
            border_style="#b3feff",
        )
        for character in player_characters
    ]
    player_group: Panel = Panel(
        Columns(player_characters_panels, expand=True, equal=True),
        title="Party",
        border_style="green",
    )
    console.print(player_group)
    if enemies:
        enemies_panels: list[Panel] = [
            Panel(
                f"HP: {enemy.current_hp}/{enemy.max_hp}",
                title=enemy.name,
                border_style="#b3feff",
            )
            for enemy in enemies
        ]
        enemies_group: Panel = Panel(
            Columns(enemies_panels, expand=True, equal=True),
            title="Enemies",
            border_style="red",
        )
        console.print(enemies_group)


def introduce_enemies(console: Console, enemies: list[Character]):
    console.print("[bold red]Enemies[/bold red]")
    for enemy in enemies:
        console.print(enemy.description, style="#73fafa")


def battle(
    console: Console, player_characters: list[Character], enemies: list[Character]
) -> bool:
    console.rule(f"[bold #bb3efa]Battle[/bold #bb3efa]", style="#bb3efa")
    battle_ended: bool = False
    introduce_enemies(console, enemies)
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
                player_character.attack(enemies[target_index], console)
            elif choice == "Use ability":
                abilities_choices: list[questionary.Choice] = [
                    questionary.Choice(title=a[0], value=a[1])
                    for a in player_character.abilities
                ]
                ability: Callable = questionary.select(
                    "Choose your ability:",
                    choices=abilities_choices,
                ).ask()
                target_index: int = questionary.select(
                    "Choose your target:", choices=target_choices
                ).ask()
                ability(enemies[target_index], enemies, console)
            elif choice == "End turn":
                pass
            enemies: list[Character] = [
                enemy for enemy in enemies if enemy.current_hp > 0
            ]
            if not enemies:
                return True
        for enemy in enemies:
            console.rule(f"[bold red]{enemy.name}'s turn[/bold red]", style="red")
            random_target_index = random.randint(0, len(player_characters) - 1)
            enemy.attack(
                player_characters[random_target_index], player_characters, console
            )
            player_characters_are_dead: bool = all(
                character.current_hp <= 0 for character in player_characters
            )
            if player_characters_are_dead:
                return False
