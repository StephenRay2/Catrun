import os
import re

def clean_name(filename):
    # Remove file extension
    name = os.path.splitext(filename)[0]

    # Remove trailing numbers (e.g., Sword3 → Sword)
    name = re.sub(r'\d+$', '', name)

    # Split on capital letters: "IronGreatSword" → ["Iron", "Great", "Sword"]
    parts = re.findall(r'[A-Z][a-z0-9]*', name)

    # Join them with spaces
    return " ".join(parts)


def print_items_list():
    folder_path = "assets/sprites/items"
    names = set()

    for picture in os.listdir(folder_path):
        if picture.endswith((".png", ".jpg", ".jpeg")):
            cleaned = clean_name(picture)
            if cleaned:
                names.add(cleaned)

    for i, name in enumerate(sorted(names), start=1):
        print(f"{i}. {name}")


def print_creature_list():
    folder_path = "assets/sprites/mobs"
    names = set()

    for picture in os.listdir(folder_path):
        if picture.endswith((".png", ".jpg", ".jpeg")):
            cleaned = clean_name(picture)
            if cleaned:
                names.add(cleaned)

    for i, name in enumerate(sorted(names), start=1):
        print(f"{i}. {name}")


print_creature_list()
# print_items_list()
