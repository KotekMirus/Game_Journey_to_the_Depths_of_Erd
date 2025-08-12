import characters_handling as characters
import random

layers_data: list[dict[str:any]] = [
    {
        "battles_number": 3,
        "enemies_number_per_battle": [1, 1, 2, 2, 2, 3],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["E", "N1", "N2", "CS", "T", "T", "T"],
    },
    {
        "battles_number": 4,
        "enemies_number_per_battle": [1, 2, 2, 2, 3, 3],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "CF", "T", "T", "T"],
    },
    {
        "battles_number": 4,
        "enemies_number_per_battle": [2, 2, 3, 3, 3, 4],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "CJ", "N3", "F", "T"],
    },
    {
        "battles_number": 5,
        "enemies_number_per_battle": [2, 3, 3, 3, 4, 4],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "CP", "CX", "T"],
    },
    {
        "battles_number": 6,
        "enemies_number_per_battle": [3, 3, 4, 4, 4, 5],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "N4", "T"],
    },
    {
        "battles_number": 1,
        "enemies_number_per_battle": [1],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": [],
    },
]


def generate_layer_content(layer_index: int) -> list[str, list[characters.Character]]:
    layer_content: list[str, list[characters.Character]] = []
    for _ in range(layers_data[layer_index]["battles_number"]):
        enemies_number: int = random.choice(
            layers_data[layer_index]["enemies_number_per_battle"]
        )
        battle: list[characters.Character] = []
        for _ in range(enemies_number):
            enemy_type: characters.Character = random.choice(
                layers_data[layer_index]["enemies_types"]
            )
            battle.append(enemy_type())
        layer_content.append(battle)
    places_contents: list[str, list[str]] = []
    for content in layers_data[layer_index]["places_contents"]:
        if content == "T":
            treasures: list[str] = []
            items_number_chances: list[int] = [1, 1, 1, 1, 1, 2, 2, 2, 3]
            items_number: int = random.choice(items_number_chances)
            items_type_chances: list[str] = [
                "H1",
                "H1",
                "H1",
                "H1",
                "H2",
                "H2",
                "C1",
                "C1",
                "C1",
                "C2",
            ]
            for _ in range(items_number):
                item_type: str = random.choice(items_type_chances)
                if item_type == "H1":
                    treasures.append("Healing potion (+10HP)")
                elif item_type == "H2":
                    treasures.append("Great healing potion (+20HP)")
                elif item_type == "C1":
                    treasures.append("Power crystal (+2CP)")
                elif item_type == "C2":
                    treasures.append("Great power crystal (+4CP)")
            places_contents.append(treasures)
        else:
            places_contents.append(content)
    layer_content = layer_content + places_contents
    random.shuffle(layer_content)
    return layer_content


def generate_all_layers_contents() -> list[list[str, list[characters.Character]]]:
    all_layers_contents: list[list[str, list[characters.Character]]] = []
    for i in range(len(layers_data)):
        all_layers_contents.append(generate_layer_content(i))
    return all_layers_contents
