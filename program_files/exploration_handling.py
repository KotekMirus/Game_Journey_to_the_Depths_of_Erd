import characters_handling as characters
import random

layers_data = [
    {
        "battles_number": 3,
        "enemies_number_per_battle": [1, 1, 2, 2, 2, 3],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "N1", "N2", "T", "T", "T"],
    },
    {
        "battles_number": 4,
        "enemies_number_per_battle": [1, 2, 2, 2, 3, 3],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "C1", "T", "T", "T"],
    },
    {
        "battles_number": 4,
        "enemies_number_per_battle": [2, 2, 3, 3, 3, 4],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "C2", "N3", "F", "T"],
    },
    {
        "battles_number": 5,
        "enemies_number_per_battle": [2, 3, 3, 3, 4, 4],
        "enemies_types": [
            characters.Enemy_Character_Frus,
            characters.Enemy_Character_Dark_Goo,
        ],
        "places_contents": ["S", "E", "C3", "T", "T"],
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
    layer_content = layer_content + layers_data[layer_index]["places_contents"]
    random.shuffle(layer_content)
    return layer_content


def generate_all_layers_contents() -> list[list[str, list[characters.Character]]]:
    all_layers_contents: list[list[str, list[characters.Character]]] = []
    for i in range(len(layers_data)):
        all_layers_contents.append(generate_layer_content(i))
    return all_layers_contents
