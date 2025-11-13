import os

def print_items_list():
    folder_path = "assets/sprites/items"
    i = 0
    for picture in os.listdir(folder_path):
        i += 1
        if picture.endswith((".png", ".jpg", ".jpeg")):
            print(f"{i}. {picture}")


def print_creature_list():
    folder_path = "assets/sprites/mobs"
    i = 0
    for picture in os.listdir(folder_path):
        i += 1
        if picture.endswith((".png", ".jpg", ".jpeg")):
            print(f"{i}. {picture}")


print_creature_list()