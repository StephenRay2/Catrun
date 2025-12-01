import pygame
import pygame
import random
import re
import math
import copy
import mob_placement
from debug import font_path, font

HARVEST_TOOL_MULTS = {
    "wood": {"normal": 2, "special": 2},
    "stone": {"normal": 3, "special": 3},
    "metal": {"normal": 4, "special": 4},
    "gold": {"normal": 1, "special": 6},
    "bone": {"normal": 6, "special": 1},
    "obsidian": {"normal": 4, "special": 4},
    "dragon": {"normal": 8, "special": 8},
}
SPECIAL_DROP_MULTS = {
    "metal": 1.5,
    "gold": 4.0,
    "obsidian": 2.0,
    "dragon": 3.0,
}
from mob_placement import player
from buttons import inventory_tab, crafting_tab, level_up_tab, cats_tab, inventory_tab_unused, crafting_tab_unused, level_up_tab_unused, cats_tab_unused
from sounds import sound_manager


hotbar_image = pygame.image.load("assets/sprites/buttons/hotbar.png").convert_alpha()
hotbar_image = pygame.transform.scale(hotbar_image, (514, 55))
player_inventory_image = pygame.image.load("assets/sprites/player/GlenjaminFrontIdle1.png")
player_inventory_image = pygame.transform.scale(player_inventory_image, (500, 500))

image_path = "assets/sprites/items"


def get_weapon_animation_data():
    return {
        "movement_frame_data": {
            "right": [
                {"offset": (15, 21), "rotation": 2},
                {"offset": (21, 18), "rotation": 7},
                {"offset": (17, 3), "rotation": 45},
                {"offset": (21, 18), "rotation": 7},
                {"offset": (15, 21), "rotation": 0},
                {"offset": (11, 21), "rotation": 0},
                {"offset": (7, 21), "rotation": 0},
                {"offset": (11, 21), "rotation": 0},
            ],
            "left": [
                {"offset": (5, 21), "rotation": 0},
                {"offset": (9, 21), "rotation": 2},
                {"offset": (11, 21), "rotation": 4},
                {"offset": (9, 21), "rotation": 2},
                {"offset": (5, 21), "rotation": 0},
                {"offset": (-5, 16), "rotation": -9},
                {"offset": (-13, 2), "rotation": -45},
                {"offset": (-5, 16), "rotation": -9},
            ],
            "up": [
                {"offset": (13, 20), "rotation": 0},
                {"offset": (9, 17), "rotation": 2},
                {"offset": (8, 11), "rotation": 5},
                {"offset": (9, 17), "rotation": 2},
                {"offset": (13, 20), "rotation": 0},
                {"offset": (9, 17), "rotation": 2},
                {"offset": (8, 15), "rotation": 5},
                {"offset": (9, 17), "rotation": 2},
            ],
            "down": [
                {"offset": (0, 20), "rotation": 0},
                {"offset": (1, 18), "rotation": -5},
                {"offset": (3, 16), "rotation": 0},
                {"offset": (1, 18), "rotation": 5},
                {"offset": (0, 20), "rotation": 0},
                {"offset": (1, 18), "rotation": -5},
                {"offset": (3, 16), "rotation": 0},
                {"offset": (1, 18), "rotation": 5},
            ]
        },
        "attack_frame_data": {
            "right": [
                {"offset": (7, 0), "rotation": 45},
                {"offset": (-7, -16), "rotation": 135},
                {"offset": (30, 4), "rotation": 90},
                {"offset": (16, 5), "rotation": 45},
            ],
            "left": [
                {"offset": (0, 0), "rotation": 45},
                {"offset": (14, -16), "rotation": 135},
                {"offset": (-8, 0), "rotation": 90},
                {"offset": (-9, 6), "rotation": 45},
            ],
            "up": [
                {"offset": (8, 11), "rotation": -5},
                {"offset": (5, 3), "rotation": -10},
                {"offset": (9, 17), "rotation": 2},
                {"offset": (13, 20), "rotation": 0},
            ],
            "down": [
                {"offset": (-2, 4), "rotation": -5},
                {"offset": (2, -1), "rotation": -10},
                {"offset": (0, 20), "rotation": 2},
                {"offset": (2, 16), "rotation": 0},
            ]
        }
    }


items_list = [
    # Raw Materials
    {
        "item_name": "Apples",
        "icon": "Apple.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A crisp red apple. Sweet and refreshing.",
        "use_effect": "player.hunger += 5; player.thirst += 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Oranges",
        "icon": "Orange.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A juicy orange. Bursting with citrus flavor.",
        "use_effect": "player.hunger += 4; player.thirst += 5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Coconuts",
        "icon": "Coconut.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "A hard-shelled coconut. Contains sweet milk inside.",
        "use_effect": "player.hunger += 3; player.thirst += 8",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Apple Wood",
        "icon": "AppleWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Sturdy wood from an apple tree. Good for crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Dusk Wood",
        "icon": "DuskWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Dark purple-brown wood. Has a mysterious quality.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Fir Wood",
        "icon": "FirWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Light and flexible fir wood. Easy to work with.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Oak Wood",
        "icon": "OakWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Strong oak wood. Excellent for construction.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Orange Wood",
        "icon": "OrangeWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Aromatic wood from orange trees. Subtle citrus scent.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Willow Wood",
        "icon": "WillowWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Flexible willow wood. Great for light structures.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Olive Wood",
        "icon": "OliveWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Dense olive wood with a smooth grain and sheen.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Palm Wood",
        "icon": "PalmWood.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Sturdy palm wood. Light and salt-kissed.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Blood Berries",
        "icon": "BloodBerries.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Deep red berries. Slightly tart with a hint of sweetness.",
        "use_effect": "player.hunger += .5; player.thirst += .5; player.health += .5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Dawn Berries",
        "icon": "DawnBerries.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Light-colored berries that glow faintly. Taste like crisp morning air.",
        "use_effect": "player.hunger += .5; player.thirst += .5; player.torpidity -= 1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Dusk Berries",
        "icon": "DuskBerries.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Purple berries found at twilight. Mysteriously satisfying. Seriously tiring.",
        "use_effect": "player.hunger += .5; player.thirst += .5; player.torpidity += 1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Sun Berries",
        "icon": "SunBerries.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Bright orange berries. Warm and energizing.",
        "use_effect": "player.hunger += .5; player.thirst += .5; player.warmth += 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Teal Berries",
        "icon": "TealBerries.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Cool blue-green berries. Refreshingly crisp and chill.",
        "use_effect": "player.hunger += .5; player.thirst += .5; player.warmth -= 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Twilight Drupes",
        "icon": "TwilightDrupes.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Plump drupes that share their color with the night sky. Uniquely flavorful.",
        "use_effect": "player.hunger += .5; player.thirst += .5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Vio Berries",
        "icon": "VioBerries.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Deep violet berries. Rich and slightly sweet.",
        "use_effect": "player.hunger += .5; player.thirst += .5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "berry"],
        "output_amount": 1
    },
    {
        "item_name": "Mushroom",
        "icon": "Mushroom.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A common mushroom. Safe to eat and nutritious.",
        "use_effect": "player.hunger += 1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "mushroom"],
        "output_amount": 1
    },
    {
        "item_name": "Dawnshroom",
        "icon": "Dawnshroom.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A luminous mushroom. Has a mild glow.",
        "use_effect": "player.hunger += 1; player.glow_time += 100",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "mushroom"],
        "output_amount": 1
    },
    {
        "item_name": "Duskshroom",
        "icon": "Duskshroom.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A dark mushroom of curious color and qualities. Earthy and savory.",
        "use_effect": "player.hunger += 1; player.temp_weight_increase += .01",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "mushroom"],
        "output_amount": 1
    },
    {
        "item_name": "Raw Beef",
        "icon": "RawBeef.png",
        "stack_size": 100,
        "weight": .2,
        "type": "raw_material",
        "description": "A cut of raw beef. Should be cooked before eating.",
        "use_effect": "player.hunger += 3; player.health -= 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Raw Bear Meat",
        "icon": "RawBearMeat.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "Raw bear meat. Needs cooking to be safe. Unbearable if not cooked properly.",
        "use_effect": "player.hunger += 3; player.health -= 4",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Raw Small Meat",
        "icon": "SmallMeat.png",
        "stack_size": 100,
        "weight": .1,
        "type": "raw_material",
        "description": "Just a wee bit of meat from a wee animal. Needs cooking to be safe.",
        "use_effect": "player.hunger += 2; player.health -= 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Raw Chicken",
        "icon": "RawBirdMeat.png",
        "stack_size": 100,
        "weight": .15,
        "type": "raw_material",
        "description": "Raw chicken meat. Needs cooking to be safe.",
        "use_effect": "player.hunger += 2; player.health -= 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Fish",
        "icon": "Fish.png",
        "stack_size": 100,
        "weight": .3,
        "type": "raw_material",
        "description": "A fresh-caught fish. Best when cooked, but cats love it raw.",
        "use_effect": "player.hunger += 3; player.health -= 1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Raw Venison",
        "icon": "RawVenison.png",
        "stack_size": 100,
        "weight": .2,
        "type": "raw_material",
        "description": "Raw deer meat. Gamey and lean. Best when cooked",
        "use_effect": "player.hunger += 4; player.health -= 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Gila Meat",
        "icon": "RawReptileMeat.png",
        "stack_size": 100,
        "weight": .15,
        "type": "raw_material",
        "description": "Meat from a gila monster. Exotic and tough.",
        "use_effect": "player.hunger += 4; player.health -= 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Stone",
        "icon": "Stone.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "A chunk of solid stone. Useful for building and crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "crafting"],
        "output_amount": 1
    },
    {
        "item_name": "Redrock Stone",
        "icon": "RedrockStone.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "A chunk of redrock stone. Useful for building and crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "crafting"],
        "output_amount": 1
    },
    {
        "item_name": "Clay",
        "icon": "Clay.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Soft clay soil. Can be smelted into ceramic shards.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Clay", "amount": 1}],
        "crafting_medium": None,
        "tags": ["material"],
        "output_amount": 2
    },
    {
        "item_name": "Raw Metal",
        "icon": "RawMetal.png",
        "stack_size": 100,
        "weight": 1,
        "type": "raw_material",
        "description": "Unrefined metal ore. Needs smelting to be useful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Sticks",
        "icon": "Stick.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "Simple wooden sticks. Basic crafting material.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["material", "stick", "fuel"],
        "output_amount": 4
    },
    {
        "item_name": "Raw Gold",
        "icon": "RawGold.png",
        "stack_size": 100,
        "weight": 1,
        "type": "raw_material",
        "description": "Unrefined gold ore. Valuable when smelted.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Poisonous Mushroom",
        "icon": "PoisonousMushroom.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A toxic mushroom. Do not eat! Or do. Could be fun. Or painful. Mess around and find out, I guess. Used in alchemy.",
        "use_effect": "player.poison = True; player.poison_time += 30; player.poison_strength += 1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "mushroom"],
        "output_amount": 1
    },
    {
        "item_name": "Fiber",
        "icon": "Fiber.png",
        "stack_size": 100,
        "weight": .025,
        "type": "raw_material",
        "description": "Plant fibers. Can be woven into twine.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "fiber"],
        "output_amount": 1
    },
    {
        "item_name": "Hide",
        "icon": "Hide.png",
        "stack_size": 100,
        "weight": .1,
        "type": "raw_material",
        "description": "Animal hide. Useful for leather crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Buck Antlers",
        "icon": "BuckAntlers.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Antlers from a buck. Strong and sharp.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Duskwretch Claws",
        "icon": "DuskwretchClaws.png",
        "stack_size": 100,
        "weight": 1.5,
        "type": "raw_material",
        "description": "Sharp, durable claws cut from a duskwretch. Like, super sharp. Razor-sharp.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Pock Eye",
        "icon": "PockEye.png",
        "stack_size": 100,
        "weight": .15,
        "type": "raw_material",
        "description": "A strange eye from a lifeless Pock. Unnerving to look at. May have qualities some might consider to be... unnatural.",
        "use_effect": "player.poison = True; player.poison_time += 100; self.temp_attack_boost += .1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Flint",
        "icon": "Flint.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "Sharp flint stone. Used for fire-starting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Bone",
        "icon": "Bone.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A sturdy bone. Can be carved into tools.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Fur",
        "icon": "Fur.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "Soft animal fur. Warm and comfortable.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Venom Sac",
        "icon": "VenomSac.png",
        "stack_size": 100,
        "weight": .1,
        "type": "raw_material",
        "description": "A small sac filled with venom. Handle with care.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Goat Horns",
        "icon": "GoatHorn.png",
        "stack_size": 100,
        "weight": .4,
        "type": "raw_material",
        "description": "A spiky horn from the crest of a lovely mountain goat's sweet head. You probably didn't get this by asking nicely.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Feathers",
        "icon": "Feather.png",
        "stack_size": 100,
        "weight": .005,
        "type": "raw_material",
        "description": "Light feathers from a bird. Useful for crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Fangs",
        "icon": "Fangs.png",
        "stack_size": 100,
        "weight": .15,
        "type": "raw_material",
        "description": "Sharp front fangs of a giant animal. Useful for crafting and ripping through flesh, if you're into that kind of thing.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Duskacean Claws",
        "icon": "DuskaceanClaw.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "The little tiny baby claw of a creepy crawly purple crustacean. Useful for crafting and clamping things together really tighly, if you'd like.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Amethyst",
        "icon": "Amethyst.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A beautiful purple gemstone. Quite valuable. You feel lighter just lookig at it",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Aquamarine",
        "icon": "Aquamarine.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A clear blue gemstone. Reminds you of the ocean, and yet, you somehow feel a little more quenched.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Garnet",
        "icon": "Garnet.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A shiny reddish gemstone. Is it hot in here? Because I don't mind at all.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Diamond",
        "icon": "Diamond.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A flawless diamond. Extremely rare and valuable. You feel a little tougher just holding it.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Emerald",
        "icon": "Emerald.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A vibrant and energizing green gemstone. Highly prized.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Opal",
        "icon": "Opal.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "An iridescent gemstone. Shimmers with many colors that feed your very soul.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Pearl",
        "icon": "Pearl.png",
        "stack_size": 100,
        "weight": .05,
        "type": "gem",
        "description": "A lustrous pearl. Smooth and elegant. Created in the violent and raging depths of the sea.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Ruby",
        "icon": "Ruby.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A deep red gemstone. Burns with inner fire and ignites your passion for living",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Sapphire",
        "icon": "Sapphire.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A brilliant blue gemstone. Clear as the sky. Must be your lucky day",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Topaz",
        "icon": "Topaz.png",
        "stack_size": 100,
        "weight": .5,
        "type": "gem",
        "description": "A golden yellow gemstone. Warm and radiant. A swift reward for those patient enough to obtain it.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Cage Key",
        "icon": "CageKey.png",
        "stack_size": 10,
        "weight": .15,
        "type": "key",
        "description": "A key for unlocking cages. Single use.",
        "use_effect": "unlock_cage",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["key"],
        "output_amount": 1
    },
    {
        "item_name": "Chest Key",
        "icon": "ChestKey.png",
        "stack_size": 10,
        "weight": .15,
        "type": "key",
        "description": "A key for unlocking chests. Single use.",
        "use_effect": "unlock_chest",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["key"],
        "output_amount": 1
    },
    {
        "item_name": "Pineapple",
        "icon": "Pineapple.png",
        "stack_size": 100,
        "weight": .35,
        "type": "raw_material",
        "description": "A tropical pineapple. Sweet and tangy.",
        "use_effect": "player.hunger += 7; player.thirst += 4; player.thirst += 4",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Watermelon",
        "icon": "Watermelon.png",
        "stack_size": 100,
        "weight": .4,
        "type": "raw_material",
        "description": "A juicy watermelon. Very hydrating.",
        "use_effect": "player.hunger += 6; player.thirst += 8",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Olives",
        "icon": "Olives.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "Fresh olives. Can be pressed for oil.",
        "use_effect": "player.hunger += .5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Fire Fern Leaf",
        "icon": "FireFernLeaf.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A warm leaf that radiates heat. Used in alchemy.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["herb", "potion_ingredient", "Fire Material", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Frost Fern Leaf",
        "icon": "FrostFernLeaf.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A cold leaf that feels icy to touch. Used in alchemy.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["herb", "potion_ingredient", "Arcane Material"],
        "output_amount": 1
    },

    # Cooked Items
    {
        "item_name": "Baked Apples",
        "icon": "BakedApple.png",
        "stack_size": 100,
        "weight": .25,
        "type": "consumable",
        "description": "Apples baked to perfection. Warm and delicious.",
        "use_effect": "player.hunger += 8",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Apples", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "fruit"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Beef",
        "icon": "CookedBeef.png",
        "stack_size": 100,
        "weight": .2,
        "type": "consumable",
        "description": "Perfectly cooked beef. Juicy and savory.",
        "use_effect": "player.hunger += 25",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Raw Beef", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "cooked"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Bear Meat",
        "icon": "CookedBearMeat.png",
        "stack_size": 100,
        "weight": .25,
        "type": "consumable",
        "description": "Perfectly cooked bear meat from a perfectly murdered bear. Tuff but real yummy. Fills you up a lot.",
        "use_effect": "player.hunger += 40",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Raw Bear Meat", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "cooked"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Small Meat",
        "icon": "CookedSmallMeat.png",
        "stack_size": 100,
        "weight": .1,
        "type": "consumable",
        "description": "Toasty lil meat morsel. Juicy and savory.",
        "use_effect": "player.hunger += 12",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Raw Small Meat", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "cooked"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Chicken",
        "icon": "CookedBirdMeat.png",
        "stack_size": 100,
        "weight": .15,
        "type": "consumable",
        "description": "Well-cooked chicken. Tender and flavorful.",
        "use_effect": "player.hunger += 18",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Raw Chicken", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "cooked"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Fish",
        "icon": "CookedFish.png",
        "stack_size": 100,
        "weight": .3,
        "type": "consumable",
        "description": "Grilled fish. Flaky and delicious. Cats prefer fish raw and wriggling.",
        "use_effect": "player.hunger += 16",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Fish", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Venison",
        "icon": "CookedVenison.png",
        "stack_size": 100,
        "weight": .2,
        "type": "consumable",
        "description": "Roasted venison. Gamey and satisfying.",
        "use_effect": "player.hunger += 20",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Raw Venison", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "cooked"],
        "output_amount": 1
    },
    {
        "item_name": "Cooked Gila Meat",
        "icon": "CookedReptileMeat.png",
        "stack_size": 100,
        "weight": .15,
        "type": "consumable",
        "description": "Grilled gila meat. Exotic and hearty.",
        "use_effect": "player.hunger += 14",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Gila Meat", "amount": 1}],
        "crafting_medium": "campfire",
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    

    # Smelted Items
    {
        "item_name": "Metal Ingot",
        "icon": "MetalIngot.png",
        "stack_size": 100,
        "weight": 1,
        "type": "crafted_material",
        "description": "A refined metal ingot. Ready for crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Raw Metal", "amount": 1}],
        "crafting_medium": "smelter",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Gold Ingot",
        "icon": "GoldIngot.png",
        "stack_size": 100,
        "weight": 1,
        "type": "crafted_material",
        "description": "A refined gold ingot. Shiny and valuable.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Raw Gold", "amount": 1}],
        "crafting_medium": "smelter",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Glass",
        "icon": "Glass.png",
        "stack_size": 100,
        "weight": .5,
        "type": "crafted_material",
        "description": "Clear glass. Made from melted sand.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Sand", "amount": 1}],
        "output_amount": 1,
        "crafting_medium": "smelter",
        "tags": ["crafted", "material"]
    },

    # Crafted Items by Hand
    {
        "item_name": "Mushroom Stew",
        "icon": "MushroomStew.png",
        "stack_size": 100,
        "weight": .25,
        "type": "consumable",
        "description": "A hearty mushroom stew. Warm and filling.",
        "use_effect": "player.hunger += 20",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Mushroom", "amount": 3}, {"item": "Small Water", "amount": 1}, {"item": "Wooden Bowl", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["food", "mushroom"],
        "output_amount": 1
    },
    {
        "item_name": "Rope",
        "icon": "Rope.png",
        "stack_size": 100,
        "weight": .5,
        "type": "crafted_material",
        "description": "Strong rope twisted from twine. Very useful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Twine", "amount": 5}],
        "crafting_medium": "hand",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Twine",
        "icon": "Twine.png",
        "stack_size": 100,
        "weight": .1,
        "type": "crafted_material",
        "description": "Simple twine woven from plant fibers.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "Fiber", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Ball Of Twine",
        "icon": "BallOfTwine.png",
        "stack_size": 100,
        "weight": 1,
        "type": "crafted_material",
        "description": "A compact ball of twine. Easy to store. Distracting for cats",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Twine", "amount": 10}],
        "crafting_medium": "hand",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Flint And Steel",
        "icon": "FlintAndSteel.png",
        "stack_size": 100,
        "weight": .75,
        "type": "tool",
        "description": "A fire-starting tool. Strikes sparks reliably.",
        "use_effect": "start_fire",
        "placeable": False,
        "consumable": False,
        "durability": 50,
        "recipe": [{"item": "Flint", "amount": 1}, {"item": "Metal Ingot", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["tool"],
        "output_amount": 1
    },
    {
        "item_name": "Torch",
        "icon": "Torch.png",
        "stack_size": 100,
        "weight": .5,
        "type": "tool",
        "description": "A simple torch. Provides light in darkness.",
        "use_effect": "provide_light; provide_warmth",
        "placeable": True,
        "consumable": False,
        "durability": 300,
        "recipe": [{"item": "Sticks", "amount": 3}, {"item": "Flint", "amount": 1}, {"item": "Stone", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["tool"],
        "output_amount": 1,
        "held_item_frames": {
            "left": ["TorchRightHeld1.png", "TorchRightHeld2.png", "TorchRightHeld3.png", "TorchRightHeld4.png"],
            "right": ["TorchRightHeld1.png", "TorchRightHeld2.png", "TorchRightHeld3.png", "TorchRightHeld4.png"],
            "up": ["TorchUpHeld1.png", "TorchUpHeld2.png", "TorchUpHeld3.png", "TorchUpHeld4.png"],
            "down": ["TorchDownHeld1.png", "TorchDownHeld2.png", "TorchDownHeld3.png", "TorchDownHeld4.png"]
        },
        "held_item_offset": {
            "left": (5, 18),
            "right": (15, 18),
            "up": (13, 10),
            "down": (0, 18)
        },
        "held_item_frame_duration": 0.1,
        **get_weapon_animation_data()
    },
    {
        "item_name": "Small Orange Juice",
        "icon": "SmallOrangeJuice.png",
        "stack_size": 100,
        "weight": .5,
        "type": "consumable",
        "description": "Fresh squeezed orange juice. Refreshing!",
        "use_effect": "player.thirst += 20; player.hunger += 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Oranges", "amount": 2}, {"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Wooden Bowl",
        "icon": "WoodenBowl.png",
        "stack_size": 100,
        "weight": .5,
        "type": "crafted_material",
        "description": "A simple wooden bowl. Holds food and liquids.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["wooden", "material", "container"],
        "output_amount": 1
    },
    {
        "item_name": "Wooden Cup",
        "icon": "WoodenCup.png",
        "stack_size": 100,
        "weight": .25,
        "type": "crafted_material",
        "description": "A carved wooden cup. Perfect for drinking.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["wooden", "material", "container"],
        "output_amount": 1
    },
    {
        "item_name": "Workbench",
        "icon": "Workbench.png",
        "stack_size": 1,
        "weight": 15,
        "type": "structure",
        "description": "A sturdy workbench. Enables advanced crafting.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 25}, {"item": "Stone", "amount": 7}, {"item": "Metal Ingot", "amount": 10}],
        "crafting_medium": "hand",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Arcane Crafter",
        "icon": "ArcaneCrafter.png",
        "stack_size": 1,
        "weight": 20,
        "type": "structure",
        "description": "An advanced arcane crafting station. Enables magical crafting.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "Stone", "amount": 25}, {"item": "Fiber", "amount": 40}, {"item": "Hide", "amount": 10}, {"item": "Metal Ingot", "amount": 10}, {"item": "Gold Ingot", "amount": 10}, {"item_tag": "Arcane Material", "amount": 5}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Campfire",
        "icon": "Campfire.png",
        "stack_size": 100,
        "weight": 1,
        "type": "structure",
        "description": "A simple campfire. Used for cooking, light, and warmth.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 6}, {"item": "Sticks", "amount": 10}, {"item": "Flint", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Oil Lamp",
        "icon": "OilLamp.png",
        "stack_size": 100,
        "weight": .5,
        "type": "tool",
        "description": "An oil lamp burning brightly. Provides steady light.",
        "use_effect": "provide_light; provide_warmth",
        "placeable": True,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Empty Oil Lamp", "amount": 1}, {"item_tag": "oil", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["tool"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "OilLamp1.png",
            "right": "OilLamp1.png",
            "up": "OilLamp1.png",
            "down": "OilLamp1.png"
        },
        "held_item_offset": {
            "left": (5, 18),
            "right": (15, 18),
            "up": (13, 10),
            "down": (0, 18)
        },
        **get_weapon_animation_data()
    },

    # Crafted Items at Mortar and Pestle
    {
        "item_name": "Small Olive Oil",
        "icon": "SmallOliveOil.png",
        "stack_size": 100,
        "weight": .35,
        "type": "crafted_material",
        "description": "Pressed olive oil in a small container.",
        "use_effect": "player.thirst += 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Olives", "amount": 5}, {"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["crafted", "material", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Sealing Paste",
        "icon": "SealingPaste.png",
        "stack_size": 100,
        "weight": .05,
        "type": "crafted_material",
        "description": "A thick and viscous liquid that keeps water out of where it's not wanted, and keeps it in where it's enslaved. I wouldn't it this if I were you.",
        "use_effect": "player.health -= 50; player.poison = True; player.poison_time = 10; player.poison_strength += 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 1}, {"item_tag": "oil", "amount": 1}, {"item_tag": "Fiber", "amount": 1}],
        "output_amount": 10,
        "crafting_medium": "mortar_and_pestle",
        "tags": ["crafted", "material"]
    },
    {
        "item_name": "Small Health Brew",
        "icon": "SmallHealthBrew.png",
        "stack_size": 100,
        "weight": .35,
        "type": "potion",
        "description": "A small healing potion. Restores some health.",
        "use_effect": "player.health += 30",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Blood Berries", "amount": 10}, {"item": "Vio Berries", "amount": 2}, {"item": "Small Water", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Small Stamina Brew",
        "icon": "SmallStaminaBrew.png",
        "stack_size": 100,
        "weight": .35,
        "type": "potion",
        "description": "A small stamina potion. Restores some stamina.",
        "use_effect": "player.stamina += 30",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item_tag": "Fiber", "amount": 10}, {"item": "Twilight Drupes", "amount": 3}, {"item": "Small Water", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Small Bright Brew",
        "icon": "SmallBrightBrew.png",
        "stack_size": 100,
        "weight": .35,
        "type": "potion",
        "description": "A glowing brew. Is your skin... shiny? That's natural, I promise.",
        "use_effect": "player.glow = True; player.glow_time = 300",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Dawn Berries", "amount": 10}, {"item": "Dawnshroom", "amount": 2}, {"item": "Small Water", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Small Chill Brew",
        "icon": "SmallChillBrew.png",
        "stack_size": 100,
        "weight": .35,
        "type": "potion",
        "description": "A cooling brew. Provides resistance to heat.",
        "use_effect": "player.temp_heat_resistance_increase +=.1; player.temp_heat_resistance_timer += 50",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Teal Berries", "amount": 10}, {"item": "Frost Fern Leaf", "amount": 2}, {"item": "Small Water", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Small Heat Brew",
        "icon": "SmallHeatBrew.png",
        "stack_size": 100,
        "weight": .35,
        "type": "potion",
        "description": "A warming brew. Provides resistance to cold.",
        "use_effect": "player.temp_cold_resistance +=.1; player.temp_cold_resistance_timer += 50",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Sun Berries", "amount": 10}, {"item": "Fire Fern Leaf", "amount": 2}, {"item": "Small Water", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },

    # Crafted Items at Workbench
    
    {
        "item_name": "Resurrection Coin",
        "icon": "ResurrectionCoin.png",
        "stack_size": 10,
        "weight": .5,
        "type": "special",
        "description": "A mystical, valuable, and powerful coin. Grants a second chance at life.... or nine",
        "use_effect": "player.resurrect",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 5}, {"item": "Diamond", "amount": 1}, {"item": "Ruby", "amount": 1}, {"item": "Emerald", "amount": 1}, {"item": "Sapphire", "amount": 1}, {"item": "Garnet", "amount": 1}, {"item": "Aquamarine", "amount": 1}, {"item": "Topaz", "amount": 1}, {"item": "Amethyst", "amount": 1}, {"item": "Opal", "amount": 1}, {"item": "Pearl", "amount": 1}, {"item": "Dusk Wood", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Throwing Knife",
        "icon": "ThrowingKnife.png",
        "stack_size": 100,
        "weight": .25,
        "type": "weapon",
        "description": "A balanced throwing knife. Flies true.",
        "use_effect": "ranged_attack",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 1}, {"item": "Hide", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Throwing Star",
        "icon": "ThrowingStar.png",
        "stack_size": 100,
        "weight": .25,
        "type": "weapon",
        "description": "A sharp throwing star. Deadly when thrown.",
        "use_effect": "ranged_attack",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Empty Oil Lamp",
        "icon": "EmptyOilLamp.png",
        "stack_size": 100,
        "weight": .4,
        "type": "crafted_material",
        "description": "An empty oil lamp. Needs oil to function.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 5}, {"item": "Twine", "amount": 1}, {"item": "Flint", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Small Metal Ring",
        "icon": "SmallMetalRing.png",
        "stack_size": 1,
        "weight": .35,
        "type": "equipment",
        "description": "A small metal ring. Simple but functional. Adorn with your favorite gemstone. Or don't. Your choice. Gemstones would be a lot cooler though.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 1}, {"item": "Hide", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Small Gold Ring",
        "icon": "SmallGoldRing.png",
        "stack_size": 1,
        "weight": .3,
        "type": "equipment",
        "description": "A small gold ring. Elegant and valuable. Slap a cool rock in there for varying effects.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 1}, {"item": "Hide", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Ring",
        "icon": "MetalRing.png",
        "stack_size": 1,
        "weight": .5,
        "type": "equipment",
        "description": "A sturdy metal ring. Well-crafted. Much more room for activities. Like 3 times as much room. And gems. But mostly activities.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}, {"item": "Small Metal Ring", "amount": 1}, {"item": "Duskwretch Claws", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Gold Ring",
        "icon": "GoldRing.png",
        "stack_size": 1,
        "weight": .5,
        "type": "equipment",
        "description": "A gold ring with a spot for not one, not two, but three whole gemstones. Quite fancy.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 2}, {"item": "Small Gold Ring", "amount": 1}, {"item": "Goat Horns", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Chain",
        "icon": "MetalChain.png",
        "stack_size": 100,
        "weight": .15,
        "type": "equipment",
        "description": "A small metal chain of tiny metal hoops. Perfect for fine jewelry. Or hula-hopping if you're the size of a cricket.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 1}],
        "output_amount": 5,
        "crafting_medium": "workbench",
        "tags": ["material", "ore"]
    },
    {
        "item_name": "Gold Chain",
        "icon": "GoldChain.png",
        "stack_size": 100,
        "weight": .15,
        "type": "equipment",
        "description": "Ring, ring, ring, ring, ring, ring, ring.... it's a chain made of gold rings.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 1}],
        "output_amount": 5,
        "crafting_medium": "workbench",
        "tags": ["material", "ore"]
    },
    {
        "item_name": "Small Metal Amulet",
        "icon": "SmallMetalAmulet.png",
        "stack_size": 1,
        "weight": .5,
        "type": "equipment",
        "description": "A small metal amulet. May hold power. In the form of gems. That's it. That's the power. Go get yourself some gems. Try looking in some weird-looking rocks or something.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}, {"item": "Metal Chain", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Small Gold Amulet",
        "icon": "SmallGoldAmulet.png",
        "stack_size": 1,
        "weight": .5,
        "type": "equipment",
        "description": "A small gold amulet. Radiates faint energy. Looks super cool though. Trust me, I checked.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 2}, {"item": "Gold Chain", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Metal Amulet",
        "icon": "MediumMetalAmulet.png",
        "stack_size": 1,
        "weight": .75,
        "type": "equipment",
        "description": "A medium metal amulet set with some gems. At least it would be if you set it with some gems.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}, {"item": "Small Metal Amulet", "amount": 1}, {"item": "Bone", "amount": 5}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Gold Amulet",
        "icon": "MediumGoldAmulet.png",
        "stack_size": 1,
        "weight": .75,
        "type": "equipment",
        "description": "A medium gold amulet. Beautifully crafted. Light as a feather. Except for now you have to live with the weight of what you did to those poor avians. You monster.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 2}, {"item": "Small Gold Amulet", "amount": 1}, {"item": "Feathers", "amount": 5}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Amulet",
        "icon": "LargeMetalAmulet.png",
        "stack_size": 1,
        "weight": 1,
        "type": "equipment",
        "description": "A large metal amulet. Feels powerful. Becuase it is. Well, it could be... If you stuck some shiny, pretty, precious little gems inside all those holes you made.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}, {"item": "Medium Metal Amulet", "amount": 1}, {"item": "Fangs", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Gold Amulet",
        "icon": "LargeGoldAmulet.png",
        "stack_size": 1,
        "weight": 1,
        "type": "equipment",
        "description": "A large gold amulet. A masterwork of jewelry. I mean, as masterful as you're able to make. So it's probably decent I guess.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 2}, {"item": "Medium Gold Amulet", "amount": 1}, {"item": "Duskacean Claws", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Cooking Pot",
        "icon": "CookingPot.png",
        "stack_size": 1,
        "weight": 5,
        "type": "structure",
        "description": "A large cooking pot. Used for making massive stews. Like, huge.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 15}, {"item": "Campfire", "amount": 1}, {"item": "Sticks", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Smelter",
        "icon": "Smelter.png",
        "stack_size": 1,
        "weight": 25,
        "type": "structure",
        "description": "A stone smelter. Refines raw materials. ",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 50}, {"item": "Flint", "amount": 5}],
        "crafting_medium": "hand",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Empty Cage",
        "icon": "EmptyCage.png",
        "stack_size": 1,
        "weight": 7.5,
        "type": "structure",
        "description": "An empty cage. Can hold captured animals.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Alchemy Bench",
        "icon": "AlchemyBench.png",
        "stack_size": 1,
        "weight": 15,
        "type": "structure",
        "description": "An alchemy bench. Used for brewing potions.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Dusk Wood", "amount": 15}, {"item": "Oak Wood", "amount": 10}, {"item": "Stone", "amount": 10}, {"item": "Glass Bottle", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Fence",
        "icon": "Fence.png",
        "stack_size": 100,
        "weight": 2.5,
        "type": "structure",
        "description": "A wooden fence section. Marks boundaries. Can keep things in or out. Of what? That's for you to decide.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 15}, {"item": "Sticks", "amount": 10}, {"item": "Rope", "amount": 1}],
        "output_amount": 1,
        "crafting_medium": "workbench",
        "tags": ["item"]
    },
    {
        "item_name": "Chest",
        "icon": "Chest.png",
        "stack_size": 1,
        "weight": 5,
        "type": "structure",
        "description": "A storage chest. Holds many items safely.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 10}, {"item": "Metal Ingot", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Tent",
        "icon": "Tent.png",
        "stack_size": 1,
        "weight": 7.5,
        "type": "structure",
        "description": "A portable tent. Provides shelter anywhere. Except for underwater. Or space. Or in lava. Also enables fast travel to this location.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Hide", "amount": 30}, {"item": "Rope", "amount": 5}, {"item": "Sticks", "amount": 10}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Glass Bottle",
        "icon": "GlassBottle.png",
        "stack_size": 100,
        "weight": .5,
        "type": "crafted_material",
        "description": "An empty glass bottle. Can hold liquids a lot better than your hands.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Glass", "amount": 3}, {"item": "Sealing Paste", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["crafted", "material", "container"],
        "output_amount": 1
    },
    {
        "item_name": "Lantern",
        "icon": "Lantern.png",
        "stack_size": 100,
        "weight": 1.5,
        "type": "tool",
        "description": "A bright lantern. Lights up large areas. Impervious to inclement weather. I think that means it won't go out in the rain. The wicked witch of the west doesn't do that either. I think that means she's impervious to inclement weather. Just kidding, it's becasue she's dead.",
        "use_effect": "provide_light; provide_heat",
        "placeable": True,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Metal Ingot", "amount": 4}, {"item": "Glass", "amount": 4}, {"item": "Torch", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["tool"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "Lantern1.png",
            "right": "Lantern1.png",
            "up": "Lantern1.png",
            "down": "Lantern1.png"
        },
        "held_item_offset": {
            "left": (5, 18),
            "right": (15, 18),
            "up": (13, 10),
            "down": (0, 18)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Mortar And Pestle",
        "icon": "MortarAndPestle.png",
        "stack_size": 1,
        "weight": 10,
        "type": "tool",
        "description": "A mortar and pestle. Grinds ingredients for alchemy. Rock and roll, baby.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 25}, {"item": "Hide", "amount": 10}],
        "crafting_medium": "hand",
        "tags": ["tool"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Bucket",
        "icon": "MetalBucket.png",
        "stack_size": 100,
        "weight": 2.5,
        "type": "tool",
        "description": "A sturdy metal bucket. Carries water and milk and possibly some other things but I've never tried it. Try it out I guess..",
        "use_effect": "collect_liquid",
        "placeable": False,
        "consumable": False,
        "durability": 100,
        "recipe": [{"item": "Rope", "amount": 1}, {"item": "Metal Ingot", "amount": 5}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore", "container", "metal_container"],
        "output_amount": 1
    },
    {
        "item_name": "Fishing Pole",
        "icon": "FishingPole.png",
        "stack_size": 1,
        "weight": .5,
        "type": "tool",
        "description": "A fishing pole. Catch fish from rivers and ponds. Gotta catch 'em... most of 'em, because copyright laws are a thing.",
        "use_effect": "catch_fish",
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Twine", "amount": 15}, {"item": "Sticks", "amount": 5}, {"item": "Metal Ingot", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Rod",
        "icon": "MetalRod.png",
        "stack_size": 100,
        "weight": 1,
        "type": "crafted_material",
        "description": "A sturdy metal rod. Forms the backbone of advanced tools and weapons.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["material", "metal"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Fishing Pole",
        "icon": "FishingPole.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "tool",
        "description": "A fishing pole. Catch fish from rivers and ponds BUT WITH METAL.",
        "use_effect": "catch_fish",
        "placeable": False,
        "consumable": False,
        "durability": 2000,
        "recipe": [{"item": "Twine", "amount": 15}, {"item": "Metal Rod", "amount": 5}, {"item": "Metal Ingot", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["tool"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Axe",
        "icon": "MetalAxe.png",
        "stack_size": 1,
        "weight": 4,
        "type": "tool",
        "description": "A sturdy metal axe. Perfect for chopping wood and solving problems.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 5000,
        "recipe": [{"item": "Metal Ingot", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalAxeRightHeld.png",
            "right": "MetalAxeRightHeld.png",
            "up": "MetalAxeUpHeld.png",
            "down": "MetalAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Bone Weapons
    {
        "item_name": "Bone Axe",
        "icon": "BoneAxe.png",
        "stack_size": 1,
        "weight": 3,
        "type": "tool",
        "description": "An axe crafted from bone. Surprisingly effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Bone", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BoneAxeRightHeld.png",
            "right": "BoneAxeRightHeld.png",
            "up": "BoneAxeUpHeld.png",
            "down": "BoneAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Bone Sword",
        "icon": "BoneSword.png",
        "stack_size": 1,
        "weight": 1,
        "type": "weapon",
        "description": "A sword made from bone. Surprisingly sharp.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Bone", "amount": 12}, {"item": "Sticks", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BoneSwordRightHeld.png",
            "right": "BoneSwordRightHeld.png",
            "up": "BoneSwordUpHeld.png",
            "down": "BoneSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Bone Spear",
        "icon": "BoneSpear.png",
        "stack_size": 1,
        "weight": 1,
        "type": "weapon",
        "description": "A spear tipped with bone. Good for ranged combat.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Bone", "amount": 4}, {"item": "Sticks", "amount": 10}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BoneSpearRightHeld.png",
            "right": "BoneSpearRightHeld.png",
            "up": "BoneSpearUpHeld.png",
            "down": "BoneSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Bone Mace",
        "icon": "BoneMace.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "A mace with a bone head. Useful for crushing.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 700,
        "recipe": [{"item": "Bone", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BoneMaceRightHeld.png",
            "right": "BoneMaceRightHeld.png",
            "up": "BoneMaceUpHeld.png",
            "down": "BoneMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Bone Pickaxe",
        "icon": "BonePickaxe.png",
        "stack_size": 1,
        "weight": 2,
        "type": "tool",
        "description": "A pickaxe with a bone head. Useful for mining.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 700,
        "recipe": [{"item": "Bone", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BonePickaxeRightHeld.png",
            "right": "BonePickaxeRightHeld.png",
            "up": "BonePickaxeUpHeld.png",
            "down": "BonePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Bone Shovel",
        "icon": "BoneShovel.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A shovel with a bone blade. Good for digging.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Bone", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BoneShovelRightHeld.png",
            "right": "BoneShovelRightHeld.png",
            "up": "BoneShovelUpHeld.png",
            "down": "BoneShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Bone Hoe",
        "icon": "BoneHoe.png",
        "stack_size": 1,
        "weight": .75,
        "type": "tool",
        "description": "A hoe with a bone blade. Perfect for tending gardens.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Bone", "amount": 5}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "BoneHoeRightHeld.png",
            "right": "BoneHoeRightHeld.png",
            "up": "BoneHoeUpHeld.png",
            "down": "BoneHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Gold Weapons
    {
        "item_name": "Gold Axe",
        "icon": "GoldAxe.png",
        "stack_size": 1,
        "weight": 3.5,
        "type": "tool",
        "description": "A golden axe. Beautiful and deadly.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Gold Ingot", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldAxeRightHeld.png",
            "right": "GoldAxeRightHeld.png",
            "up": "GoldAxeUpHeld.png",
            "down": "GoldAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Gold Sword",
        "icon": "GoldSword.png",
        "stack_size": 1,
        "weight": 1.25,
        "type": "weapon",
        "description": "A golden sword. Luxurious and effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 700,
        "recipe": [{"item": "Gold Ingot", "amount": 12}, {"item": "Sticks", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldSwordRightHeld.png",
            "right": "GoldSwordRightHeld.png",
            "up": "GoldSwordUpHeld.png",
            "down": "GoldSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Gold Spear",
        "icon": "GoldSpear.png",
        "stack_size": 1,
        "weight": 1.25,
        "type": "weapon",
        "description": "A golden spear. Elegant and deadly.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Gold Ingot", "amount": 4}, {"item": "Sticks", "amount": 10}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldSpearRightHeld.png",
            "right": "GoldSpearRightHeld.png",
            "up": "GoldSpearUpHeld.png",
            "down": "GoldSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Gold Mace",
        "icon": "GoldMace.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A golden mace. Heavy and precious.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Gold Ingot", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldMaceRightHeld.png",
            "right": "GoldMaceRightHeld.png",
            "up": "GoldMaceUpHeld.png",
            "down": "GoldMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Gold Pickaxe",
        "icon": "GoldPickaxe.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "tool",
        "description": "A golden pickaxe. As valuable as it is useful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Gold Ingot", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldPickaxeRightHeld.png",
            "right": "GoldPickaxeRightHeld.png",
            "up": "GoldPickaxeUpHeld.png",
            "down": "GoldPickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Gold Shovel",
        "icon": "GoldShovel.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "tool",
        "description": "A golden shovel. Surprisingly practical.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 700,
        "recipe": [{"item": "Gold Ingot", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldShovelRightHeld.png",
            "right": "GoldShovelRightHeld.png",
            "up": "GoldShovelUpHeld.png",
            "down": "GoldShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Gold Hoe",
        "icon": "GoldHoe.png",
        "stack_size": 1,
        "weight": 1,
        "type": "tool",
        "description": "A golden hoe. Perfect for tending valuable gardens.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Gold Ingot", "amount": 5}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "GoldHoeRightHeld.png",
            "right": "GoldHoeRightHeld.png",
            "up": "GoldHoeUpHeld.png",
            "down": "GoldHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Obsidian Weapons
    {
        "item_name": "Obsidian Axe",
        "icon": "ObsidianAxe.png",
        "stack_size": 1,
        "weight": 3.5,
        "type": "tool",
        "description": "An obsidian axe. Sharp and powerful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1100,
        "recipe": [{"item": "Obsidian Shard", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianAxeRightHeld.png",
            "right": "ObsidianAxeRightHeld.png",
            "up": "ObsidianAxeUpHeld.png",
            "down": "ObsidianAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Obsidian Sword",
        "icon": "ObsidianSword.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "An obsidian sword. Wickedly sharp.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Obsidian Shard", "amount": 12}, {"item": "Sticks", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianSwordRightHeld.png",
            "right": "ObsidianSwordRightHeld.png",
            "up": "ObsidianSwordUpHeld.png",
            "down": "ObsidianSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Obsidian Spear",
        "icon": "ObsidianSpear.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "An obsidian spear. Deadly and elegant.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Obsidian Shard", "amount": 4}, {"item": "Sticks", "amount": 10}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianSpearRightHeld.png",
            "right": "ObsidianSpearRightHeld.png",
            "up": "ObsidianSpearUpHeld.png",
            "down": "ObsidianSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Obsidian Mace",
        "icon": "ObsidianMace.png",
        "stack_size": 1,
        "weight": 2,
        "type": "weapon",
        "description": "An obsidian mace. Devastating.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Obsidian Shard", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianMaceRightHeld.png",
            "right": "ObsidianMaceRightHeld.png",
            "up": "ObsidianMaceUpHeld.png",
            "down": "ObsidianMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Obsidian Pickaxe",
        "icon": "ObsidianPickaxe.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "tool",
        "description": "An obsidian pickaxe. Perfect for mining hard rock.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Obsidian Shard", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianPickaxeRightHeld.png",
            "right": "ObsidianPickaxeRightHeld.png",
            "up": "ObsidianPickaxeUpHeld.png",
            "down": "ObsidianPickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Obsidian Shovel",
        "icon": "ObsidianShovel.png",
        "stack_size": 1,
        "weight": 2,
        "type": "tool",
        "description": "An obsidian shovel. Great for moving dark earth.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Obsidian Shard", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianShovelRightHeld.png",
            "right": "ObsidianShovelRightHeld.png",
            "up": "ObsidianShovelUpHeld.png",
            "down": "ObsidianShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Obsidian Hoe",
        "icon": "ObsidianHoe.png",
        "stack_size": 1,
        "weight": 1.25,
        "type": "tool",
        "description": "An obsidian hoe. Perfect for serious gardening.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Obsidian Shard", "amount": 5}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ObsidianHoeRightHeld.png",
            "right": "ObsidianHoeRightHeld.png",
            "up": "ObsidianHoeUpHeld.png",
            "down": "ObsidianHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Stone Weapons
    {
        "item_name": "Stone Axe",
        "icon": "StoneAxe.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "tool",
        "description": "A stone axe. One of humanity's first tools. Guess your name is humanity now. Sorry, I don't make the rules. Just kidding, I'm the developer, I do make the rules.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 700,
        "recipe": [{"item": "Stone", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StoneAxeRightHeld.png",
            "right": "StoneAxeRightHeld.png",
            "up": "StoneAxeUpHeld.png",
            "down": "StoneAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Sword",
        "icon": "StoneSword.png",
        "stack_size": 1,
        "weight": 1,
        "type": "weapon",
        "description": "A stone sword. Better than sticks, anyway.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Stone", "amount": 12}, {"item": "Sticks", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StoneSwordRightHeld.png",
            "right": "StoneSwordRightHeld.png",
            "up": "StoneSwordUpHeld.png",
            "down": "StoneSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Spear",
        "icon": "StoneSpear.png",
        "stack_size": 1,
        "weight": 1,
        "type": "weapon",
        "description": "A spear tipped with stone. Primitive but effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item": "Stone", "amount": 4}, {"item": "Sticks", "amount": 10}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StoneSpearRightHeld.png",
            "right": "StoneSpearRightHeld.png",
            "up": "StoneSpearUpHeld.png",
            "down": "StoneSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Mace",
        "icon": "StoneMace.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "A stone mace. Heavy and brutal.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Stone", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StoneMaceRightHeld.png",
            "right": "StoneMaceRightHeld.png",
            "up": "StoneMaceUpHeld.png",
            "down": "StoneMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Pickaxe",
        "icon": "StonePickaxe.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "tool",
        "description": "A stone pickaxe. Effective for mining.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Stone", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StonePickaxeRightHeld.png",
            "right": "StonePickaxeRightHeld.png",
            "up": "StonePickaxeUpHeld.png",
            "down": "StonePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Shovel",
        "icon": "StoneShovel.png",
        "stack_size": 1,
        "weight": 1.25,
        "type": "tool",
        "description": "A stone shovel. Good for moving dirt.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Stone", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StoneShovelRightHeld.png",
            "right": "StoneShovelRightHeld.png",
            "up": "StoneShovelUpHeld.png",
            "down": "StoneShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Hoe",
        "icon": "StoneHoe.png",
        "stack_size": 1,
        "weight": .75,
        "type": "tool",
        "description": "A stone hoe. Basic but reliable.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item": "Stone", "amount": 5}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "StoneHoeRightHeld.png",
            "right": "StoneHoeRightHeld.png",
            "up": "StoneHoeUpHeld.png",
            "down": "StoneHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Wooden Weapons
    {
        "item_name": "Wooden Axe",
        "icon": "WoodenAxe.png",
        "stack_size": 1,
        "weight": 2,
        "type": "tool",
        "description": "A wooden axe. Light and easy to swing.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item_tag": "wood", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenAxeRightHeld.png",
            "right": "WoodenAxeRightHeld.png",
            "up": "WoodenAxeUpHeld.png",
            "down": "WoodenAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Sword",
        "icon": "WoodenSword.png",
        "stack_size": 1,
        "weight": .75,
        "type": "weapon",
        "description": "A wooden sword. Good for training.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 300,
        "recipe": [{"item_tag": "wood", "amount": 12}, {"item": "Sticks", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenSwordRightHeld.png",
            "right": "WoodenSwordRightHeld.png",
            "up": "WoodenSwordUpHeld.png",
            "down": "WoodenSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Spear",
        "icon": "WoodenSpear.png",
        "stack_size": 1,
        "weight": .75,
        "type": "weapon",
        "description": "A wooden spear. A basic ranged weapon.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 250,
        "recipe": [{"item_tag": "wood", "amount": 4}, {"item": "Sticks", "amount": 10}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenSpearRightHeld.png",
            "right": "WoodenSpearRightHeld.png",
            "up": "WoodenSpearUpHeld.png",
            "down": "WoodenSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Mace",
        "icon": "WoodenMace.png",
        "stack_size": 1,
        "weight": 1,
        "type": "weapon",
        "description": "A wooden mace. Solid and straightforward.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item_tag": "wood", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenMaceRightHeld.png",
            "right": "WoodenMaceRightHeld.png",
            "up": "WoodenMaceUpHeld.png",
            "down": "WoodenMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Pickaxe",
        "icon": "WoodenPickaxe.png",
        "stack_size": 1,
        "weight": 1.25,
        "type": "tool",
        "description": "A wooden pickaxe. For light mining.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 350,
        "recipe": [{"item_tag": "wood", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenPickaxeRightHeld.png",
            "right": "WoodenPickaxeRightHeld.png",
            "up": "WoodenPickaxeUpHeld.png",
            "down": "WoodenPickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Shovel",
        "icon": "WoodenShovel.png",
        "stack_size": 1,
        "weight": 1,
        "type": "tool",
        "description": "A wooden shovel. Good for digging soft earth.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 300,
        "recipe": [{"item_tag": "wood", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenShovelRightHeld.png",
            "right": "WoodenShovelRightHeld.png",
            "up": "WoodenShovelUpHeld.png",
            "down": "WoodenShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Hoe",
        "icon": "WoodenHoe.png",
        "stack_size": 1,
        "weight": .5,
        "type": "tool",
        "description": "A wooden hoe. Perfect for starting a garden.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 250,
        "recipe": [{"item_tag": "wood", "amount": 5}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenHoeRightHeld.png",
            "right": "WoodenHoeRightHeld.png",
            "up": "WoodenHoeUpHeld.png",
            "down": "WoodenHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Dusk Dragon Scale Weapons
    {
        "item_name": "Dusk Dragon Scale Axe",
        "icon": "DuskDragonScaleAxe.png",
        "stack_size": 1,
        "weight": 4,
        "type": "tool",
        "description": "An axe crafted from dusk dragon scales. Deadly and mystical.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1400,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScaleAxeRightHeld.png",
            "right": "DuskDragonScaleAxeRightHeld.png",
            "up": "DuskDragonScaleAxeUpHeld.png",
            "down": "DuskDragonScaleAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Dusk Dragon Scale Sword",
        "icon": "DuskDragonScaleSword.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A sword forged from dusk dragon scales. Elegant and powerful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 6}, {"item": "Metal Rod", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScaleSwordRightHeld.png",
            "right": "DuskDragonScaleSwordRightHeld.png",
            "up": "DuskDragonScaleSwordUpHeld.png",
            "down": "DuskDragonScaleSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Dusk Dragon Scale Spear",
        "icon": "DuskDragonScaleSpear.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A spear tipped with dusk dragon scales. Fearsome.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScaleSpearRightHeld.png",
            "right": "DuskDragonScaleSpearRightHeld.png",
            "up": "DuskDragonScaleSpearUpHeld.png",
            "down": "DuskDragonScaleSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Dusk Dragon Scale Mace",
        "icon": "DuskDragonScaleMace.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "weapon",
        "description": "A mace forged from dusk dragon scales. Crushingly effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1100,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScaleMaceRightHeld.png",
            "right": "DuskDragonScaleMaceRightHeld.png",
            "up": "DuskDragonScaleMaceUpHeld.png",
            "down": "DuskDragonScaleMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Dusk Dragon Scale Pickaxe",
        "icon": "DuskDragonScalePickaxe.png",
        "stack_size": 1,
        "weight": 2.75,
        "type": "tool",
        "description": "A pickaxe forged from dusk dragon scales. Unbreakable.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1200,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScalePickaxeRightHeld.png",
            "right": "DuskDragonScalePickaxeRightHeld.png",
            "up": "DuskDragonScalePickaxeUpHeld.png",
            "down": "DuskDragonScalePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Dusk Dragon Scale Shovel",
        "icon": "DuskDragonScaleShovel.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "tool",
        "description": "A shovel forged from dusk dragon scales. Perfect for dark tasks.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScaleShovelRightHeld.png",
            "right": "DuskDragonScaleShovelRightHeld.png",
            "up": "DuskDragonScaleShovelUpHeld.png",
            "down": "DuskDragonScaleShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Dusk Dragon Scale Hoe",
        "icon": "DuskDragonScaleHoe.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A hoe forged from dusk dragon scales. For twilight gardens.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Dusk Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "DuskDragonScaleHoeRightHeld.png",
            "right": "DuskDragonScaleHoeRightHeld.png",
            "up": "DuskDragonScaleHoeUpHeld.png",
            "down": "DuskDragonScaleHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Electric Dragon Scale Weapons
    {
        "item_name": "Electric Dragon Scale Axe",
        "icon": "ElectricDragonScaleAxe.png",
        "stack_size": 1,
        "weight": 4,
        "type": "tool",
        "description": "An axe forged from electric dragon scales. Crackling with power.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1400,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScaleAxeRightHeld.png",
            "right": "ElectricDragonScaleAxeRightHeld.png",
            "up": "ElectricDragonScaleAxeUpHeld.png",
            "down": "ElectricDragonScaleAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Electric Dragon Scale Sword",
        "icon": "ElectricDragonScaleSword.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A sword forged from electric dragon scales. Shocks enemies.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 6}, {"item": "Metal Rod", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScaleSwordRightHeld.png",
            "right": "ElectricDragonScaleSwordRightHeld.png",
            "up": "ElectricDragonScaleSwordUpHeld.png",
            "down": "ElectricDragonScaleSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Electric Dragon Scale Spear",
        "icon": "ElectricDragonScaleSpear.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A spear tipped with electric dragon scales. Electrifying.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScaleSpearRightHeld.png",
            "right": "ElectricDragonScaleSpearRightHeld.png",
            "up": "ElectricDragonScaleSpearUpHeld.png",
            "down": "ElectricDragonScaleSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Electric Dragon Scale Mace",
        "icon": "ElectricDragonScaleMace.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "weapon",
        "description": "A mace forged from electric dragon scales. Powerful and shocking.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1100,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScaleMaceRightHeld.png",
            "right": "ElectricDragonScaleMaceRightHeld.png",
            "up": "ElectricDragonScaleMaceUpHeld.png",
            "down": "ElectricDragonScaleMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Electric Dragon Scale Pickaxe",
        "icon": "ElectricDragonScalePickaxe.png",
        "stack_size": 1,
        "weight": 2.75,
        "type": "tool",
        "description": "A pickaxe forged from electric dragon scales. Breaks anything.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1200,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScalePickaxeRightHeld.png",
            "right": "ElectricDragonScalePickaxeRightHeld.png",
            "up": "ElectricDragonScalePickaxeUpHeld.png",
            "down": "ElectricDragonScalePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Electric Dragon Scale Shovel",
        "icon": "ElectricDragonScaleShovel.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "tool",
        "description": "A shovel forged from electric dragon scales. For energetic digging.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScaleShovelRightHeld.png",
            "right": "ElectricDragonScaleShovelRightHeld.png",
            "up": "ElectricDragonScaleShovelUpHeld.png",
            "down": "ElectricDragonScaleShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Electric Dragon Scale Hoe",
        "icon": "ElectricDragonScaleHoe.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A hoe forged from electric dragon scales. For shocking gardens.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Electric Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "ElectricDragonScaleHoeRightHeld.png",
            "right": "ElectricDragonScaleHoeRightHeld.png",
            "up": "ElectricDragonScaleHoeUpHeld.png",
            "down": "ElectricDragonScaleHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Fire Dragon Scale Weapons
    {
        "item_name": "Fire Dragon Scale Axe",
        "icon": "FireDragonScaleAxe.png",
        "stack_size": 1,
        "weight": 4,
        "type": "tool",
        "description": "An axe forged from fire dragon scales. Burning with power.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1400,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScaleAxeRightHeld.png",
            "right": "FireDragonScaleAxeRightHeld.png",
            "up": "FireDragonScaleAxeUpHeld.png",
            "down": "FireDragonScaleAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Fire Dragon Scale Sword",
        "icon": "FireDragonScaleSword.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A sword forged from fire dragon scales. Sets enemies ablaze.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 6}, {"item": "Metal Rod", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScaleSwordRightHeld.png",
            "right": "FireDragonScaleSwordRightHeld.png",
            "up": "FireDragonScaleSwordUpHeld.png",
            "down": "FireDragonScaleSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Fire Dragon Scale Spear",
        "icon": "FireDragonScaleSpear.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A spear tipped with fire dragon scales. Fiery and deadly.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScaleSpearRightHeld.png",
            "right": "FireDragonScaleSpearRightHeld.png",
            "up": "FireDragonScaleSpearUpHeld.png",
            "down": "FireDragonScaleSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Fire Dragon Scale Mace",
        "icon": "FireDragonScaleMace.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "weapon",
        "description": "A mace forged from fire dragon scales. Inferno in your hands.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1100,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScaleMaceRightHeld.png",
            "right": "FireDragonScaleMaceRightHeld.png",
            "up": "FireDragonScaleMaceUpHeld.png",
            "down": "FireDragonScaleMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Fire Dragon Scale Pickaxe",
        "icon": "FireDragonScalePickaxe.png",
        "stack_size": 1,
        "weight": 2.75,
        "type": "tool",
        "description": "A pickaxe forged from fire dragon scales. Hot mining.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1200,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScalePickaxeRightHeld.png",
            "right": "FireDragonScalePickaxeRightHeld.png",
            "up": "FireDragonScalePickaxeUpHeld.png",
            "down": "FireDragonScalePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Fire Dragon Scale Shovel",
        "icon": "FireDragonScaleShovel.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "tool",
        "description": "A shovel forged from fire dragon scales. For lava gardens.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScaleShovelRightHeld.png",
            "right": "FireDragonScaleShovelRightHeld.png",
            "up": "FireDragonScaleShovelUpHeld.png",
            "down": "FireDragonScaleShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Fire Dragon Scale Hoe",
        "icon": "FireDragonScaleHoe.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A hoe forged from fire dragon scales. For volcanic soil.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Fire Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "FireDragonScaleHoeRightHeld.png",
            "right": "FireDragonScaleHoeRightHeld.png",
            "up": "FireDragonScaleHoeUpHeld.png",
            "down": "FireDragonScaleHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Ice Dragon Scale Weapons
    {
        "item_name": "Ice Dragon Scale Axe",
        "icon": "IceDragonScaleAxe.png",
        "stack_size": 1,
        "weight": 4,
        "type": "tool",
        "description": "An axe forged from ice dragon scales. Freezing enemies in their tracks.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1400,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScaleAxeRightHeld.png",
            "right": "IceDragonScaleAxeRightHeld.png",
            "up": "IceDragonScaleAxeUpHeld.png",
            "down": "IceDragonScaleAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Ice Dragon Scale Sword",
        "icon": "IceDragonScaleSword.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A sword forged from ice dragon scales. Chills the blood.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 6}, {"item": "Metal Rod", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScaleSwordRightHeld.png",
            "right": "IceDragonScaleSwordRightHeld.png",
            "up": "IceDragonScaleSwordUpHeld.png",
            "down": "IceDragonScaleSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Ice Dragon Scale Spear",
        "icon": "IceDragonScaleSpear.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A spear tipped with ice dragon scales. Deadly and cold.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScaleSpearRightHeld.png",
            "right": "IceDragonScaleSpearRightHeld.png",
            "up": "IceDragonScaleSpearUpHeld.png",
            "down": "IceDragonScaleSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Ice Dragon Scale Mace",
        "icon": "IceDragonScaleMace.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "weapon",
        "description": "A mace forged from ice dragon scales. Smash and freeze.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1100,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScaleMaceRightHeld.png",
            "right": "IceDragonScaleMaceRightHeld.png",
            "up": "IceDragonScaleMaceUpHeld.png",
            "down": "IceDragonScaleMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Ice Dragon Scale Pickaxe",
        "icon": "IceDragonScalePickaxe.png",
        "stack_size": 1,
        "weight": 2.75,
        "type": "tool",
        "description": "A pickaxe forged from ice dragon scales. Cool mining.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1200,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScalePickaxeRightHeld.png",
            "right": "IceDragonScalePickaxeRightHeld.png",
            "up": "IceDragonScalePickaxeUpHeld.png",
            "down": "IceDragonScalePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Ice Dragon Scale Shovel",
        "icon": "IceDragonScaleShovel.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "tool",
        "description": "A shovel forged from ice dragon scales. For frozen earth.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScaleShovelRightHeld.png",
            "right": "IceDragonScaleShovelRightHeld.png",
            "up": "IceDragonScaleShovelUpHeld.png",
            "down": "IceDragonScaleShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Ice Dragon Scale Hoe",
        "icon": "IceDragonScaleHoe.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A hoe forged from ice dragon scales. For winter crops.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Ice Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "IceDragonScaleHoeRightHeld.png",
            "right": "IceDragonScaleHoeRightHeld.png",
            "up": "IceDragonScaleHoeUpHeld.png",
            "down": "IceDragonScaleHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Poison Dragon Scale Weapons
    {
        "item_name": "Poison Dragon Scale Axe",
        "icon": "PoisonDragonScaleAxe.png",
        "stack_size": 1,
        "weight": 4,
        "type": "tool",
        "description": "An axe forged from poison dragon scales. Venomous.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1400,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "weapon"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScaleAxeRightHeld.png",
            "right": "PoisonDragonScaleAxeRightHeld.png",
            "up": "PoisonDragonScaleAxeUpHeld.png",
            "down": "PoisonDragonScaleAxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Poison Dragon Scale Sword",
        "icon": "PoisonDragonScaleSword.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A sword forged from poison dragon scales. Toxic blade.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 6}, {"item": "Metal Rod", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScaleSwordRightHeld.png",
            "right": "PoisonDragonScaleSwordRightHeld.png",
            "up": "PoisonDragonScaleSwordUpHeld.png",
            "down": "PoisonDragonScaleSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Poison Dragon Scale Spear",
        "icon": "PoisonDragonScaleSpear.png",
        "stack_size": 1,
        "weight": 1.75,
        "type": "weapon",
        "description": "A spear tipped with poison dragon scales. Poisonous.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScaleSpearRightHeld.png",
            "right": "PoisonDragonScaleSpearRightHeld.png",
            "up": "PoisonDragonScaleSpearUpHeld.png",
            "down": "PoisonDragonScaleSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Poison Dragon Scale Mace",
        "icon": "PoisonDragonScaleMace.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "weapon",
        "description": "A mace forged from poison dragon scales. Causes severe poison.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1100,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScaleMaceRightHeld.png",
            "right": "PoisonDragonScaleMaceRightHeld.png",
            "up": "PoisonDragonScaleMaceUpHeld.png",
            "down": "PoisonDragonScaleMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Poison Dragon Scale Pickaxe",
        "icon": "PoisonDragonScalePickaxe.png",
        "stack_size": 1,
        "weight": 2.75,
        "type": "tool",
        "description": "A pickaxe forged from poison dragon scales. Toxic mining.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1200,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 4}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScalePickaxeRightHeld.png",
            "right": "PoisonDragonScalePickaxeRightHeld.png",
            "up": "PoisonDragonScalePickaxeUpHeld.png",
            "down": "PoisonDragonScalePickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Poison Dragon Scale Shovel",
        "icon": "PoisonDragonScaleShovel.png",
        "stack_size": 1,
        "weight": 2.25,
        "type": "tool",
        "description": "A shovel forged from poison dragon scales. For toxic digging.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 3}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScaleShovelRightHeld.png",
            "right": "PoisonDragonScaleShovelRightHeld.png",
            "up": "PoisonDragonScaleShovelUpHeld.png",
            "down": "PoisonDragonScaleShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Poison Dragon Scale Hoe",
        "icon": "PoisonDragonScaleHoe.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A hoe forged from poison dragon scales. For venomous plants.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 900,
        "recipe": [{"item": "Poison Dragon Scale", "amount": 2}, {"item": "Metal Rod", "amount": 4}],
        "crafting_medium": "arcane_crafter",
        "tags": ["tool", "gardening"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "PoisonDragonScaleHoeRightHeld.png",
            "right": "PoisonDragonScaleHoeRightHeld.png",
            "up": "PoisonDragonScaleHoeUpHeld.png",
            "down": "PoisonDragonScaleHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    # Crafted through Gameplay
    {
    
        "item_name": "Sand",
        "icon": "Sand.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "It's a pile... it's sand... It's a lil pile of sand.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Small Water",
        "icon": "SmallWater.png",
        "stack_size": 100,
        "weight": .35,
        "type": "consumable",
        "description": "Fresh water in a small cup. Quenches thirst.",
        "use_effect": "player.thirst += 25",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1,
        "recipe_alternatives": [
            {
                "recipe": [{"item": "Large Metal Water", "amount": 1}, {"item": "Wooden Cup", "amount": 4}],
                "output_amount": 4,
                "crafting_medium": "hand"
            },
            {
                "recipe": [{"item": "Medium Glass Water", "amount": 1}, {"item": "Wooden Cup", "amount": 2}],
                "output_amount": 2,
                "crafting_medium": "hand"
            }
        ]
    },
    {
        "item_name": "Small Milk",
        "icon": "SmallMilk.png",
        "stack_size": 100,
        "weight": .35,
        "type": "consumable",
        "description": "Fresh milk in a small cup. Unless you're the size of a pea. Then it's a ginormous cup. Way too big for one little pea-sized guy or gal to drink. Creamy and nutritious.",
        "use_effect": "player.thirst += 12; player.hunger += 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1,
        "recipe_alternatives": [
            {
                "recipe": [{"item": "Coconut", "amount": 1}, {"item": "Wooden Cup", "amount": 1}],
                "output_amount": 1,
                "crafting_medium": "hand"
            }
        ]
    },
    {
        "item_name": "Medium Glass Water",
        "icon": "MediumGlassWater.png",
        "stack_size": 100,
        "weight": .7,
        "type": "consumable",
        "description": "Water in a medium glass bottle. Very refreshing. So refreshing. You'll feel so refreshed.",
        "use_effect": "player.thirst += 50",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1,
        "recipe_alternatives": [
            {
                "recipe": [{"item": "Large Metal Water", "amount": 1}, {"item": "Glass Bottle", "amount": 2}],
                "output_amount": 2,
                "crafting_medium": "hand"
            },
            {
                "recipe": [{"item": "Small Water", "amount": 2}, {"item": "Glass Bottle", "amount": 1}],
                "output_amount": 1,
                "crafting_medium": "hand"
            }
        ]
    },
    {
        "item_name": "Medium Glass Milk",
        "icon": "MediumGlassMilk.png",
        "stack_size": 100,
        "weight": .7,
        "type": "consumable",
        "description": "Milk in a medium glass bottle. Rich and filling. Whether cow or coconut, you'll be craving the goods.",
        "use_effect": "player.thirst += 40; player.hunger += 10",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1,
        "recipe_alternatives": [
            {
                "recipe": [{"item": "Coconut", "amount": 2}, {"item": "Glass Bottle", "amount": 1}],
                "output_amount": 1,
                "crafting_medium": "hand"
            }
        ]
    },
    {
        "item_name": "Medium Glass Orange Juice",
        "icon": "MediumGlassOrangeJuice.png",
        "stack_size": 100,
        "weight": .7,
        "type": "consumable",
        "description": "Orange juice in a medium bottle. Tangy and sweet.",
        "use_effect": "player.thirst += 35; player.hunger += 10; player.stamina += 20",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Oranges", "amount": 4}, {"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Water",
        "icon": "LargeMetalWater.png",
        "stack_size": 100,
        "weight": 1,
        "type": "consumable",
        "description": "Anti-thirst in a large metal canteen. Lasts a long time.",
        "use_effect": "player.thirst += 100",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["material", "ore"],
        "output_amount": 1,
        "recipe_alternatives": [
            {
                "recipe": [{"item": "Small Water", "amount": 4}, {"item": "Large Metal Canteen", "amount": 1}],
                "output_amount": 1,
                "crafting_medium": "hand"
            },
            {
                "recipe": [{"item": "Medium Glass Water", "amount": 2}, {"item": "Large Metal Canteen", "amount": 1}],
                "output_amount": 1,
                "crafting_medium": "hand"
            }
        ]
    },
    {
        "item_name": "Large Metal Milk",
        "icon": "LargeMetalMilk.png",
        "stack_size": 100,
        "weight": 1,
        "type": "consumable",
        "description": "Cow sauce in a large metal canteen. Very satisfying.",
        "use_effect": "player.thirst += 80; player.hunger += 20",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["material", "ore"],
        "output_amount": 1,
        "recipe_alternatives": [
            {
                "recipe": [{"item": "Coconut", "amount": 4}, {"item": "Large Metal Canteen", "amount": 1}],
                "output_amount": 1,
                "crafting_medium": "hand"
            }
        ]
    },
    {
        "item_name": "Large Metal Orange Juice",
        "icon": "LargeMetalOrangeJuice.png",
        "stack_size": 100,
        "weight": 1,
        "type": "consumable",
        "description": "Orange juice in a large canteen. Packed with flavor.",
        "use_effect": "player.thirst += 60; player.hunger += 15; player.stamina += 40",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Oranges", "amount": 8}, {"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Olive Oil",
        "icon": "MediumGlassOliveOil.png",
        "stack_size": 100,
        "weight": .7,
        "type": "crafted_material",
        "description": "Olive oil in a medium glass bottle. Perfect for fuel refills.",
        "use_effect": "player.thirst += 5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Olives", "amount": 15}, {"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["crafted", "oil", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Olive Oil",
        "icon": "LargeMetalOliveOil.png",
        "stack_size": 100,
        "weight": 1,
        "type": "crafted_material",
        "description": "Olive oil in a large metal canteen. All of the oil's in a large metal canteen. I love oil straight from the canteen made of metal. I'll live better knowing I have my metal canteen of oil pressed from all of the olives of all of the olive trees.",
        "use_effect": "player.thirst += 10",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Olives", "amount": 20}, {"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "oil", "fuel"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Health Brew",
        "icon": "MediumGlassHealthBrew.png",
        "stack_size": 100,
        "weight": .7,
        "type": "potion",
        "description": "A medium healing potion. Restores substantial health.",
        "use_effect": "player.health += 80",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Blood Berries", "amount": 15}, {"item": "Vio Berries", "amount": 4}, {"item": "Medium Glass Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Stamina Brew",
        "icon": "MediumGlassStaminaBrew.png",
        "stack_size": 100,
        "weight": .7,
        "type": "potion",
        "description": "A medium stamina potion. Restores substantial stamina.",
        "use_effect": "player.stamina += 80",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item_tag": "Fiber", "amount": 15}, {"item": "Twilight Drupes", "amount": 4}, {"item": "Medium Glass Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Bright Brew",
        "icon": "MediumGlassBrightBrew.png",
        "stack_size": 100,
        "weight": .7,
        "type": "potion",
        "description": "A glowing brew. Provides extended glowy-glowyness.",
        "use_effect": "player.glow = True; player.glow_time = 1000",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Dawn Berries", "amount": 15}, {"item": "Dawnshroom", "amount": 4}, {"item": "Medium Glass Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Chill Brew",
        "icon": "MediumGlassChillBrew.png",
        "stack_size": 100,
        "weight": .7,
        "type": "potion",
        "description": "A cooling brew. Provides exxtteeeended heat resistance.",
        "use_effect": "player.temp_heat_resistance_increase +=.3; player.temp_heat_resistance_timer += 200",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Teal Berries", "amount": 15}, {"item": "Frost Fern Leaf", "amount": 4}, {"item": "Medium Glass Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Heat Brew",
        "icon": "MediumGlassHeatBrew.png",
        "stack_size": 100,
        "weight": .7,
        "type": "potion",
        "description": "A warming tasty bev. Provides extended cold resistance.",
        "use_effect": "player.temp_cold_resistance_increase +=.3; player.temp_cold_resistance_timer += 200",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Sun Berries", "amount": 15}, {"item": "Fire Fern Leaf", "amount": 4}, {"item": "Medium Glass Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Canteen",
        "icon": "LargeMetalCanteen.png",
        "stack_size": 100,
        "weight": .7,
        "type": "crafted_material",
        "description": "A large empty metal canteen. Holds lots of liquid. This baby can hold a LOT of liquids. Not as much as a cooking pot, but like, a lot.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 10}, {"item": "Sealing Paste", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore", "container"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Health Brew",
        "icon": "LargeMetalHealthBrew.png",
        "stack_size": 100,
        "weight": .5,
        "type": "potion",
        "description": "A large healing potion. Restores to full health.",
        "use_effect": "player.health = player.max_health",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Blood Berries", "amount": 30}, {"item": "Vio Berries", "amount": 10}, {"item": "Duskshroom", "amount": 2}, {"item": "Large Metal Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Stamina Brew",
        "icon": "LargeMetalStaminaBrew.png",
        "stack_size": 100,
        "weight": .5,
        "type": "potion",
        "description": "A large stamina potion. Restores to full stamina.",
        "use_effect": "player.stamina = player.max_stamina",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Sun Berries", "amount": 30}, {"item": "Twilight Drupes", "amount": 10}, {"item": "Dawn Berries", "amount": 5}, {"item": "Large Metal Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Bright Brew",
        "icon": "LargeMetalBrightBrew.png",
        "stack_size": 100,
        "weight": .5,
        "type": "potion",
        "description": "A glowing brew. It's a glow up for you. Or maybe this drink just gives everyone else bad eyesight...",
        "use_effect": "player.glow = True; player.glow_time = 3000",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Dawn Berries", "amount": 30}, {"item": "Dawnshroom", "amount": 10}, {"item": "Sun Berries", "amount": 5}, {"item": "Large Metal Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Chill Brew",
        "icon": "LargeMetalChillBrew.png",
        "stack_size": 100,
        "weight": .5,
        "type": "potion",
        "description": "A suuuuuper chill cooling brew. Provides long-lasting heat resistance.",
        "use_effect": "player.temp_heat_resistance_increase +=.6; player.temp_heat_resistance_timer += 500",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Teal Berries", "amount": 30}, {"item": "Frost Fern Leaf", "amount": 10}, {"item": "Duskshroom", "amount": 5}, {"item": "Large Metal Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Heat Brew",
        "icon": "LargeMetalHeatBrew.png",
        "stack_size": 100,
        "weight": .5,
        "type": "potion",
        "description": "An exceedingly warming brew. Provides long-lasting cold resistance.",
        "use_effect": "player.temp_cold_resistance_increase +=.6; player.temp_cold_resistance_timer += 500",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Sun Berries", "amount": 30}, {"item": "Fire Fern Leaf", "amount": 10}, {"item": "Dusk Berries", "amount": 5}, {"item": "Large Metal Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    # Raw Liquids
    {
        "item_name": "Waterbucket",
        "icon": "Waterbucket.png",
        "stack_size": 100,
        "weight": 5,
        "type": "raw_material",
        "description": "Fresh water collected from a pond or lake or stream. Can be used for drinking or cooking.",
        "use_effect": "player.thirst += 100",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": "gameplay",
        "tags": ["liquid", "water", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Lavabucket",
        "icon": "Lavabucket.png",
        "stack_size": 100,
        "weight": 5,
        "type": "raw_material",
        "description": "Molten lava collected from a lava pond or stream or river or lake. Extremely hot and dangerous. Used for something, probably.",
        "use_effect": "player.is_alive = False; player.health = 0",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": "gameplay",
        "tags": ["liquid", "lava", "material"],
        "output_amount": 1
    },
    # Tamed Cats - one item for each cat type
    {
        "item_name": "Tamed Black Cat",
        "icon": "assets/sprites/mobs/BlackCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed black cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "black"
    },
    {
        "item_name": "Tamed Salt and Pepper Cat",
        "icon": "assets/sprites/mobs/SandPCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed salt and pepper cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "salt_and_pepper"
    },
    {
        "item_name": "Tamed White Cat",
        "icon": "assets/sprites/mobs/WhiteCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed white cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "white"
    },
    {
        "item_name": "Tamed Black and White Cat",
        "icon": "assets/sprites/mobs/WandBCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed black and white cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "white_and_black"
    },
    {
        "item_name": "Tamed Sandy Cat",
        "icon": "assets/sprites/mobs/SandyCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed sandy cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "sandy"
    },
    {
        "item_name": "Tamed Orange Cat",
        "icon": "assets/sprites/mobs/OrangeCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed orange cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "orange"
    },
    {
        "item_name": "Tamed Calico Cat",
        "icon": "assets/sprites/mobs/CalicoCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed calico cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "calico"
    },
    {
        "item_name": "Tamed Gray Cat",
        "icon": "assets/sprites/mobs/GrayCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed gray cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "gray"
    },
    {
        "item_name": "Tamed Orange and White Cat",
        "icon": "assets/sprites/mobs/WandOCatRightStanding.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "pet",
        "description": "A tamed orange and white cat companion. Loyal and ready to fight.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["pet", "tamed_cat"],
        "output_amount": 1,
        "cat_object": None,
        "cat_type": "white_and_orange"
    },
    {
        "item_name": "Metal Nail",
        "icon": "MetalNail.png",
        "stack_size": 100,
        "weight": .005,
        "type": "building_material",
        "description": "Nailed it. A sturdy metal nail. Used in various building recipes.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["building", "material", "metal"],
        "output_amount": 15
    },
    {
        "item_name": "Arrow",
        "icon": "Arrow.png",
        "stack_size": 100,
        "weight": .05,
        "type": "weapon",
        "description": "A pointy, pointy arrow. Perfect for poking people super hard from really far away.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Flint", "amount": 1}, {"item": "Sticks", "amount": 1}, {"item": "Feathers", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["weapon", "projectile"],
        "output_amount": 1
    },
    {
        "item_name": "Ash Lotus",
        "icon": "AshLotus.png",
        "stack_size": 100,
        "weight": .1,
        "type": "raw_material",
        "description": "A rare lotus flower with ashy petals. Prized for crafting. Craft for a prize.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["plant", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Bird Egg",
        "icon": "BirdEgg.png",
        "stack_size": 100,
        "weight": .15,
        "type": "raw_material",
        "description": "A bird's egg. Either the period or the offspring of one of our fine feathered friends. Can be cooked or used in crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["egg", "food"],
        "output_amount": 1
    },
    {
        "item_name": "Bola",
        "icon": "Bola.png",
        "stack_size": 100,
        "weight": .4,
        "type": "weapon",
        "description": "A throwing weapon made of rope and weights. Effective for controlling enemies. Kinky.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Rope", "amount": 3}, {"item": "Stone", "amount": 3}],
        "crafting_medium": "hand",
        "tags": ["weapon", "throwing"],
        "output_amount": 1
    },
    {
        "item_name": "Bone Powder",
        "icon": "BonePowder.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "Ground bone powder. Not from the ground. It has been ground. Not as in it used to be ground, but like... it's bone that has been all ground up. Useful for various crafting recipes, probably.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Bone", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["material", "powder"],
        "output_amount": 2
    },
    {
        "item_name": "Chain Bola",
        "icon": "ChainBola.png",
        "stack_size": 100,
        "weight": .6,
        "type": "weapon",
        "description": "An upgraded bola with metal chains. More effective and durable and freakishly heavy. Good luck throwing one of these.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 3}, {"item": "Metal Chain", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "throwing"],
        "output_amount": 1
    },
    {
        "item_name": "Chitin",
        "icon": "Chitin.png",
        "stack_size": 100,
        "weight": .2,
        "type": "raw_material",
        "description": "Hard shelly chitin. Used in advanced crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "insect"],
        "output_amount": 1
    },
    {
        "item_name": "Dusk Dragon Scale",
        "icon": "DuskDragonScale.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A scale from a dusk dragon. Mystical and powerful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["dragon", "material", "scale"],
        "output_amount": 1
    },
    {
        "item_name": "Dusk Egg",
        "icon": "DuskEgg.png",
        "stack_size": 100,
        "weight": .5,
        "type": "raw_material",
        "description": "An egg from a mysterious dusk creature. Possibly Nutritious?",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["egg"],
        "output_amount": 1
    },
    {
        "item_name": "Electric Dragon Scale",
        "icon": "ElectricDragonScale.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A scale from an electric dragon. Crackles with energy.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["dragon", "material", "scale"],
        "output_amount": 1
    },
    {
        "item_name": "Waterskin",
        "icon": "Waterskin.png",
        "stack_size": 1,
        "weight": .1,
        "type": "container",
        "description": "An empty waterskin. Can be filled with water. It's called a WATERskin, not a milkskin or a potionskin. Don't even try it.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Hide", "amount": 4}, {"item_tag": "Fiber", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["container"],
        "output_amount": 1
    },
    {
        "item_name": "Ceramic Shard",
        "icon": "CeramicShard.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A piece of fired ceramic. Used in pottery crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Clay", "amount": 1}],
        "crafting_medium": "smelter",
        "tags": ["material", "ceramic"],
        "output_amount": 4
    },
    {
        "item_name": "Ceramic Pot",
        "icon": "CeramicPot.png",
        "stack_size": 100,
        "weight": .3,
        "type": "weapon",
        "description": "A sturdy ceramic pot. Can be used to make explosive bombs. Or flower containers. The bold and the beautiful.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Ceramic Shard", "amount": 8}],
        "crafting_medium": "workbench",
        "tags": ["decoration", "clay"],
        "output_amount": 1
    },
    {
        "item_name": "Fire Bomb",
        "icon": "FireBomb.png",
        "stack_size": 100,
        "weight": .3,
        "type": "weapon",
        "description": "An explosive bomb filled with fire. Dangerous and effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "Fire Material", "amount": 2}, {"item": "Sealing Paste", "amount": 2}, {"item": "Twine", "amount": 1}, {"item": "Ceramic Pot", "amount": 1}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "explosive"],
        "output_amount": 1
    },
    {
        "item_name": "Ice Bomb",
        "icon": "IceBomb.png",
        "stack_size": 100,
        "weight": .3,
        "type": "weapon",
        "description": "An explosive bomb filled with Ice. Dangerous and effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "Ice Material", "amount": 2}, {"item": "Sealing Paste", "amount": 2}, {"item": "Twine", "amount": 1}, {"item": "Ceramic Pot", "amount": 1}],
        "crafting_medium": "arcane_crafter",
        "tags": ["weapon", "explosive"],
        "output_amount": 1
    },
    {
        "item_name": "Fire Dragon Egg",
        "icon": "FireDragonEgg.png",
        "stack_size": 100,
        "weight": 1,
        "type": "raw_material",
        "description": "An egg from a fire dragon. Radiates intense heat.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["egg", "dragon", "Arcane Material", "Fire Material"],
        "output_amount": 1
    },
    {
        "item_name": "Fire Dragon Scale",
        "icon": "FireDragonScale.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A scale from a fire dragon. Hot to the touch.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["dragon", "material", "scale", "Fire Material", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Flute",
        "icon": "Flute.png",
        "stack_size": 1,
        "weight": .15,
        "type": "tool",
        "description": "A wooden flute. Can be played to produce soothing sounds and gather your peeps. Very intricate, requires great skill and tools when crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 300,
        "recipe": [{"item_tag": "wood", "amount": 1}, {"item": "Marsh Reed", "amount" : 1}],
        "crafting_medium": "workbench",
        "tags": ["tool", "instrument"],
        "output_amount": 1
    },
    {
        "item_name": "Ice Dragon Scale",
        "icon": "IceDragonScale.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A scale from an ice dragon. Cold to the touch.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["dragon", "material", "scale", "Ice Material", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Inferno Horn",
        "icon": "InfernoHorn.png",
        "stack_size": 100,
        "weight": .3,
        "type": "raw_material",
        "description": "A horn from an inferno beast. Burns with inner fire.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "horn", "Fire Material", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Leather Boots",
        "icon": "LeatherBoots.png",
        "stack_size": 1,
        "weight": 1,
        "type": "armor",
        "description": "Protective leather boots. Provides moderate defense.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Hide", "amount": 15}, {"item": "Twine", "amount": 10}],
        "crafting_medium": "workbench",
        "tags": ["armor", "leather"],
        "output_amount": 1
    },
    {
        "item_name": "Leather Chestplate",
        "icon": "LeatherChestplate.png",
        "stack_size": 1,
        "weight": 2,
        "type": "armor",
        "description": "Protective leather chestplate. Provides moderate defense.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Hide", "amount": 25}, {"item": "Twine", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["armor", "leather"],
        "output_amount": 1
    },
    {
        "item_name": "Leather Gloves",
        "icon": "LeatherGloves.png",
        "stack_size": 1,
        "weight": .5,
        "type": "armor",
        "description": "Protective leather gloves. Provides light defense.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item": "Hide", "amount": 12}, {"item": "Twine", "amount": 6}],
        "crafting_medium": "workbench",
        "tags": ["armor", "leather"],
        "output_amount": 1
    },
    {
        "item_name": "Leather Helmet",
        "icon": "LeatherHelmet.png",
        "stack_size": 1,
        "weight": .75,
        "type": "armor",
        "description": "Protective leather helmet. Provides light to moderate defense.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 450,
        "recipe": [{"item": "Hide", "amount": 10}, {"item": "Twine", "amount": 6}],
        "crafting_medium": "workbench",
        "tags": ["armor", "leather"],
        "output_amount": 1
    },
    {
        "item_name": "Leather Leggings",
        "icon": "LeatherLeggings.png",
        "stack_size": 1,
        "weight": 1.25,
        "type": "armor",
        "description": "Protective leather leggings. Provides moderate defense.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 550,
        "recipe": [{"item": "Hide", "amount": 18}, {"item": "Twine", "amount": 12}],
        "crafting_medium": "workbench",
        "tags": ["armor", "leather"],
        "output_amount": 1
    },
    {
        "item_name": "Lizard Egg",
        "icon": "LizardEgg.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "An egg from a lizard. Warm and white.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["egg"],
        "output_amount": 1
    },
    {
        "item_name": "Marsh Reed",
        "icon": "MarshReed.png",
        "stack_size": 100,
        "weight": .075,
        "type": "raw_material",
        "description": "A reed from a marsh. Who'd've thunk?.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["plant", "material", "fiber"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Floor",
        "icon": "MetalFloor.png",
        "stack_size": 100,
        "weight": 2.5,
        "type": "building_material",
        "description": "A metal floor tile. Used for building and construction.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["building", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Hoe",
        "icon": "MetalHoe.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "tool",
        "description": "A metal hoe. Perfect for tilling soil.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Metal Ingot", "amount": 5}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "farming"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalHoeRightHeld.png",
            "right": "MetalHoeRightHeld.png",
            "up": "MetalHoeUpHeld.png",
            "down": "MetalHoeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Metal Ladder",
        "icon": "MetalLadder.png",
        "stack_size": 100,
        "weight": 2,
        "type": "building_material",
        "description": "A metal ladder. Used for climbing and construction.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 12}],
        "crafting_medium": "workbench",
        "tags": ["building", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Mace",
        "icon": "MetalMace.png",
        "stack_size": 1,
        "weight": 3,
        "type": "weapon",
        "description": "A heavy metal mace. Excellent for crushing enemies.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Metal Ingot", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalMaceRightHeld.png",
            "right": "MetalMaceRightHeld.png",
            "up": "MetalMaceUpHeld.png",
            "down": "MetalMaceDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Metal Pickaxe",
        "icon": "MetalPickaxe.png",
        "stack_size": 1,
        "weight": 2.5,
        "type": "tool",
        "description": "A metal pickaxe. Essential for mining ore and stone.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1200,
        "recipe": [{"item": "Metal Ingot", "amount": 8}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "mining"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalPickaxeRightHeld.png",
            "right": "MetalPickaxeRightHeld.png",
            "up": "MetalPickaxeUpHeld.png",
            "down": "MetalPickaxeDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Metal Shovel",
        "icon": "MetalShovel.png",
        "stack_size": 1,
        "weight": 2,
        "type": "tool",
        "description": "A metal shovel. Great for digging.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Metal Ingot", "amount": 6}, {"item": "Sticks", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["tool", "digging"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalShovelRightHeld.png",
            "right": "MetalShovelRightHeld.png",
            "up": "MetalShovelUpHeld.png",
            "down": "MetalShovelDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Metal Spear",
        "icon": "MetalSpear.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "A metal spear. Effective for ranged melee combat.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 700,
        "recipe": [{"item": "Metal Ingot", "amount": 4}, {"item": "Sticks", "amount": 10}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalSpearRightHeld.png",
            "right": "MetalSpearRightHeld.png",
            "up": "MetalSpearUpHeld.png",
            "down": "MetalSpearDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 20),
            "right": (15, 20),
            "up": (13, 19),
            "down": (0, 19)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Metal Stairs",
        "icon": "MetalStairs.png",
        "stack_size": 100,
        "weight": 15,
        "type": "building_material",
        "description": "Metal stairs. Used for building and construction.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 25}, {"item": "Metal Nail", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["building", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Sword",
        "icon": "MetalSword.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "A metal sword. A classic melee weapon.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 800,
        "recipe": [{"item": "Metal Ingot", "amount": 12}, {"item": "Sticks", "amount": 2}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "MetalSwordRightHeld.png",
            "right": "MetalSwordRightHeld.png",
            "up": "MetalSwordUpHeld.png",
            "down": "MetalSwordDownHeld.png"
        },
        "held_item_offset": {
            "left": (3, 22),
            "right": (17, 22),
            "up": (12, 21),
            "down": (1, 21)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Milk Bucket",
        "icon": "MilkBucket.png",
        "stack_size": 10,
        "weight": .5,
        "type": "container",
        "description": "A bucket of fresh milk. Nutritious and useful.",
        "use_effect": "player.hunger += 20; player.thirst += 70",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": "gameplay",
        "tags": ["food", "container"],
        "output_amount": 1
    },
    {
        "item_name": "Monster Meat",
        "icon": "MonsterMeat.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "Meat from a monster. Is probably fine to eat.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Oak Wood Stairs",
        "icon": "OakWoodStairs.png",
        "stack_size": 100,
        "weight": 12.5,
        "type": "building_material",
        "description": "Oak wood stairs. Strong and reliable for building.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Oak Wood", "amount": 25}, {"item": "Metal Nail", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["building", "material", "wood"],
        "output_amount": 1
    },
    {
        "item_name": "Obsidian Shard",
        "icon": "ObsidianShard.png",
        "stack_size": 100,
        "weight": .15,
        "type": "raw_material",
        "description": "A shard of obsidian. Sharp and useful for crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material"],
        "output_amount": 1
    },
    {
        "item_name": "Phoenix Feather",
        "icon": "PhoenixFeather.png",
        "stack_size": 100,
        "weight": .05,
        "type": "raw_material",
        "description": "A feather from a phoenix. Glows with inner flame.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "feather", "Fire Material", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Poison Dragon Scale",
        "icon": "PoisonDragonScale.png",
        "stack_size": 100,
        "weight": .25,
        "type": "raw_material",
        "description": "A scale from a poison dragon. Toxic and powerful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["dragon", "material", "scale", "Arcane Material"],
        "output_amount": 1
    },
    {
        "item_name": "Rope Ladder",
        "icon": "RopeLadder.png",
        "stack_size": 100,
        "weight": .5,
        "type": "building_material",
        "description": "A rope ladder. Portable and useful for climbing.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Twine", "amount": 10}, {"item": "Rope", "amount": 12}],
        "crafting_medium": "hand",
        "tags": ["building", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Salt",
        "icon": "Salt.png",
        "stack_size": 100,
        "weight": .1,
        "type": "raw_material",
        "description": "Salt. Contains: Salt. Used for preservation and cooking.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": "gameplay",
        "tags": ["material", "food"],
        "output_amount": 1
    },
    {
        "item_name": "Sea Meat",
        "icon": "SeaMeat.png",
        "stack_size": 100,
        "weight": .3,
        "type": "raw_material",
        "description": "Meat from a sea creature. Exotic and flavorful.",
        "use_effect": "player.hunger -= 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Snowball",
        "icon": "Snowball.png",
        "stack_size": 100,
        "weight": .1,
        "type": "weapon",
        "description": "A packed ball of snow. Can be thrown for damage or just for funsies.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["weapon", "throwing"],
        "output_amount": 1
    },
    {
        "item_name": "Spiked Wooden Club",
        "icon": "SpikedWoodenClub.png",
        "stack_size": 1,
        "weight": 2,
        "type": "weapon",
        "description": "A wooden club with spikes. More effective than a regular club.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Wooden Club", "amount": 1}, {"item": "Metal Nail", "amount": 10}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "SpikedWoodenClubRightHeld.png",
            "right": "SpikedWoodenClubRightHeld.png",
            "up": "SpikedWoodenClubUpHeld.png",
            "down": "SpikedWoodenClubDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Stone Floor",
        "icon": "StoneFloor.png",
        "stack_size": 100,
        "weight": 2,
        "type": "building_material",
        "description": "A stone floor tile. Durable and looks solid.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 15}, {"item": "Clay", "amount": 4}],
        "crafting_medium": "workbench",
        "tags": ["building", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Stone Stairs",
        "icon": "StoneStairs.png",
        "stack_size": 100,
        "weight": 2.5,
        "type": "building_material",
        "description": "Stone stairs. Sturdy and reliable.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 25}, {"item": "Metal Nail", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["building", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Travelers Cloak",
        "icon": "TravelersCloak.png",
        "stack_size": 1,
        "weight": 1,
        "type": "clothing",
        "description": "A sturdy cloak for travelers. Provides protection from the elements.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item": "Hide", "amount": 25}, {"item": "Rope", "amount": 2}, {"item": "Twine", "amount": 5}],
        "crafting_medium": "hand",
        "tags": ["clothing", "armor"],
        "output_amount": 1
    },
    {
        "item_name": "Tusk",
        "icon": "Tusk.png",
        "stack_size": 100,
        "weight": .2,
        "type": "raw_material",
        "description": "A large tusk from a beast. Valuable and useful.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "bone"],
        "output_amount": 1
    },
    {
        "item_name": "Water Well",
        "icon": "WaterWell.png",
        "stack_size": 1,
        "weight": 10,
        "type": "placeable",
        "description": "A well for drawing water. Can be placed pretty much anywhere to get some of that moist, dank water your body so desperately craves.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 25}, {"item": "Metal Ingot", "amount": 2}, {"item": "Metal Bucket", "amount": 1}, {"item_tag": "wood", "amount": 10}, {"item": "Rope", "amount": 5}],
        "crafting_medium": "workbench",
        "tags": ["building", "water"],
        "output_amount": 1
    },
    {
        "item_name": "Filled Waterskin",
        "icon": "FilledWaterskin.png",
        "stack_size": 10,
        "weight": .25,
        "type": "container",
        "description": "A waterskin filled with water. Quenches a bit of thirst.",
        "use_effect": "player.thirst += 15",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": "gameplay",
        "tags": ["food", "container"],
        "return_item": "Waterskin",
        "output_amount": 1
    },
    {
        "item_name": "Wood Boat",
        "icon": "WoodBoat.png",
        "stack_size": 1,
        "weight": 10,
        "type": "tool",
        "description": "A wooden boat. Useful for traveling across water.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item_tag": "wood", "amount": 20}, {"item_tag": "Metal Nail", "amount": 15}, {"item": "Sealing Paste", "amount": 6}],
        "crafting_medium": "workbench",
        "tags": ["tool", "transport"],
        "output_amount": 1
    },
    {
        "item_name": "Wood Bow",
        "icon": "WoodBow.png",
        "stack_size": 1,
        "weight": .5,
        "type": "weapon",
        "description": "A wooden bow. Classic ranged weapon.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item_tag": "wood", "amount": 5}, {"item": "Twine", "amount": 5}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "ranged"],
        "output_amount": 1
    },
    {
        "item_name": "Wood Floor",
        "icon": "WoodFloor.png",
        "stack_size": 100,
        "weight": 1,
        "type": "building_material",
        "description": "A wooden floor tile. Warm and natural.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 15}, {"item": "Metal Nail", "amount": 12}],
        "crafting_medium": "workbench",
        "tags": ["building", "material", "wood"],
        "output_amount": 1
    },
    {
        "item_name": "Wood Ladder",
        "icon": "WoodLadder.png",
        "stack_size": 100,
        "weight": 1,
        "type": "building_material",
        "description": "A wooden ladder. Simple and effective.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 15}, {"item": "Sticks", "amount": 5}, {"item": "Metal Nail", "amount": 15}],
        "crafting_medium": "workbench",
        "tags": ["building", "material", "wood"],
        "output_amount": 1
    },
    {
        "item_name": "Wooden Club",
        "icon": "WoodenClub.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "A wooden club. Simple but effective.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 400,
        "recipe": [{"item_tag": "wood", "amount": 12}],
        "crafting_medium": "hand",
        "tags": ["weapon", "melee"],
        "output_amount": 1,
        "held_item_frames": {
            "left": "WoodenClubRightHeld.png",
            "right": "WoodenClubRightHeld.png",
            "up": "WoodenClubUpHeld.png",
            "down": "WoodenClubDownHeld.png"
        },
        "held_item_offset": {
            "left": (5, 21),
            "right": (15, 21),
            "up": (13, 20),
            "down": (0, 20)
        },
        **get_weapon_animation_data()
    },
    {
        "item_name": "Wooden Crossbow",
        "icon": "WoodenCrossbow.png",
        "stack_size": 1,
        "weight": 1.5,
        "type": "weapon",
        "description": "A wooden crossbow. Powerful ranged weapon.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item_tag": "wood", "amount": 6}, {"item": "Metal Ingot", "amount": 2}, {"item": "Twine", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["weapon", "ranged"],
        "output_amount": 1
    }

]
_item_weight_lookup = {item["item_name"]: item.get("weight", 0) for item in items_list if "item_name" in item}

def _get_tier(name_lower):
    if "dragon scale" in name_lower:
        return "dragon"
    if "obsidian" in name_lower:
        return "obsidian"
    if "gold" in name_lower:
        return "gold"
    if "metal" in name_lower:
        return "metal"
    if "bone" in name_lower:
        return "bone"
    if "stone" in name_lower:
        return "stone"
    if "wood" in name_lower:
        return "wood"
    return None

_tier_durabilities = {
    "wood": 300,
    "stone": 800,
    "metal": 1800,
    "bone": 1000,
    "gold": 1400,
    "obsidian": 2200,
    "dragon": 5000,
}

_weaponish_keywords = ("axe", "sword", "spear", "mace", "pickaxe", "shovel", "hoe", "club", "bow", "crossbow")
_explicit_dur_overrides = {
    "Torch": 800,
    "Oil Lamp": 1500,
    "Leather Boots": 500,
    "Leather Chestplate": 500,
    "Leather Gloves": 500,
    "Leather Helmet": 500,
    "Leather Leggings": 500,
    "Wooden Crossbow": 1200,
}

for item in items_list:
    name = item.get("item_name", "")
    if name in _explicit_dur_overrides:
        item["durability"] = _explicit_dur_overrides[name]
        continue
    name_lower = name.lower()
    if not any(k in name_lower for k in _weaponish_keywords):
        continue
    tier = _get_tier(name_lower)
    if tier:
        item["durability"] = _tier_durabilities.get(tier, item.get("durability"))

for item in items_list:
    # Handle tamed cat icons from mobs folder
    if "cat_type" in item:
        # Load hotbar version (45x45)
        item["image_hotbar"] = pygame.transform.scale(
            pygame.image.load(item['icon']).convert_alpha(),
            (45, 45)
        )
        # Load inventory version (60x60)
        item["image"] = pygame.transform.scale(
            pygame.image.load(item['icon']).convert_alpha(),
            (60, 60)
        )
    else:
        # Load hotbar version (45x45)
        item["image_hotbar"] = pygame.transform.scale(
            pygame.image.load(f"{image_path}/{item['icon']}").convert_alpha(),
            (45, 45)
        )
        # Load inventory version (60x60)
        item["image"] = pygame.transform.scale(
            pygame.image.load(f"{image_path}/{item['icon']}").convert_alpha(),
            (60, 60)
        )
    
    if "held_item_frames" in item:
        item["held_item_images"] = {}
        itemframes_path = "assets/sprites/itemFrames"
        for direction, frame_names in item["held_item_frames"].items():
            names = frame_names if isinstance(frame_names, (list, tuple)) else [frame_names]
            loaded_frames = []
            for frame_name in names:
                try:
                    img = pygame.image.load(f"{itemframes_path}/{frame_name}").convert_alpha()
                    loaded_frames.append(img)
                except:
                    loaded_frames.append(None)
            if len(loaded_frames) == 1:
                item["held_item_images"][direction] = loaded_frames[0]
            else:
                item["held_item_images"][direction] = loaded_frames

class Inventory():
    def __init__(self, capacity):
        self.capacity = capacity
        self.inventory_list = [None] * capacity
        self.slot_size = 64
        self.rows = 8
        self.columns = 8
        self.gap_size = 4
        self.padding_size = 5
        self.total_inventory_weight = 0
        self.state = "inventory"
        self.hotbar_size = 10
        self.hotbar_slots = [None] * self.hotbar_size
        self.selected_hotbar_slot = 0
        self.selected_inventory_slot = None
        self.selection_mode = "hotbar"
        self.ui_open = False
        self.inventory_full_message_timer = 0
        self.hotbar_name_display_until = 0
        self.hotbar_name_display_text = ""
        self.hotbar_name_font = pygame.font.Font(font_path, 10)
        self.tooltip_title_font = pygame.font.Font(font_path, 18)
        self.tooltip_body_font = pygame.font.Font(font_path, 14)
        self.tooltip_small_font = pygame.font.Font(font_path, 12)
        self.tooltip_delay_ms = 1000
        self.tooltip_mode_active = False
        self._hover_candidate = None
        self._hover_active_id = None
        self._hover_start_time = 0
        self._hover_display_data = None
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        self.drop_menu_active = False
        self.drop_menu_slot = None
        self.drop_menu_is_hotbar = False
        self.drop_menu_position = (0, 0)
        self.drop_menu_rect = None
        self.drop_menu_context = None
        self.drop_option_rects = {}
        self.drop_amount_input = ""
        self.awaiting_drop_amount = False
        self.amount_action = None
        self.inventory_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/inventory_screen.png").convert_alpha(), (1100, 600))
        self.crafting_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/crafting_screen.png").convert_alpha(), (1100, 600))
        self.level_up_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/level_up_screen.png").convert_alpha(), (1100, 600))
        self.cat_screen_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/cats_screen.png").convert_alpha(), (1100, 600))
        self.cat_card_image = pygame.image.load("assets/sprites/buttons/CatCard.png").convert_alpha()
        self.cat_card_portrait_sources = {}
        self.cat_card_portrait_cache = {}
        self.cat_card_scroll = 0
        self.cat_card_max_scroll = 0
        self.cat_card_columns = 3
        self.cat_card_column_padding = 14
        self.cat_card_row_padding = 30
        self.cat_card_title_font = pygame.font.Font(font_path, 16)
        self.cat_card_stat_font = pygame.font.Font(font_path, 10)
        self.level_up_skill_image = pygame.image.load("assets/sprites/buttons/level_up_skill_button.png").convert_alpha()
        self.level_up_skill_flash_image = pygame.image.load("assets/sprites/buttons/level_up_skill_button_flash.png").convert_alpha()
        self.level_up_button_rects = []
        self.level_up_font = pygame.font.Font(font_path, 22)
        self.level_up_value_font = pygame.font.Font(font_path, 18)
        self.last_level_up_click_time = 0
        
        self.selected_crafting_item = None
        self.crafting_slot_positions = {}
        self.last_click_time = 0
        self.last_click_slot = None
        self.crafting_completion_flash = False
        self.crafting_completion_slot = None
        self.crafting_completion_time = 0
        self.crafting_flash_duration = 0.3
        
        self.selected_cat_id = None
        self.cat_card_rects = []
        self.cat_hover_scale = {}
        self.cat_card_entries = []
        self.last_cat_click_time = 0
        self.cat_upgrade_button_rects = []

    def recalc_weight(self):
        """Recompute total carried weight and sync it to the player immediately."""
        total = 0
        for slot in (self.hotbar_slots + self.inventory_list):
            if not slot:
                continue
            weight = _item_weight_lookup.get(slot["item_name"], 0)
            total += round(slot.get("quantity", 0) * weight, 1)
        self.total_inventory_weight = round(total, 1)
        player.weight = self.total_inventory_weight
        return self.total_inventory_weight

    def draw_inventory(self, screen):
        
        width = screen.get_width()
        height = screen.get_height()
        x_pos = screen.get_width() / 2 - self.inventory_image.get_width() / 2
        y_pos = screen.get_height() / 2 - self.inventory_image.get_height() / 2
        if self.state == "inventory":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.inventory_image, (x_pos, y_pos - 20))
            screen.blit(player_inventory_image, (700, 90))

            screen.blit(inventory_tab, (width // 2 - 533, height // 2 - 303))
            crafting_tab_unused.draw(screen)
            level_up_tab_unused.draw(screen)
            cats_tab_unused.draw(screen)

        elif self.state == "crafting":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.crafting_image, (x_pos, y_pos - 20))

            inventory_tab_unused.draw(screen)
            screen.blit(crafting_tab, (width // 2 - 397, height // 2 - 303))
            level_up_tab_unused.draw(screen)
            cats_tab_unused.draw(screen)
            
            self.draw_crafting(screen)
    
        elif self.state == "level_up":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.level_up_image, (x_pos, y_pos - 20))
            screen.blit(player_inventory_image, (700, 90))
            self.draw_level_up(screen)

            inventory_tab_unused.draw(screen)
            crafting_tab_unused.draw(screen)
            screen.blit(level_up_tab, (width // 2 - 261, height // 2 - 303))
            cats_tab_unused.draw(screen)

        elif self.state == "cats":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.cat_screen_image, (x_pos, y_pos - 20))
            self.draw_cats_tab(screen, x_pos, y_pos - 20)
            if self.selected_cat_id:
                self.draw_selected_cat_info(screen, x_pos, y_pos - 20)

            inventory_tab_unused.draw(screen)
            crafting_tab_unused.draw(screen)
            level_up_tab_unused.draw(screen)
            screen.blit(cats_tab, (width // 2 - 125, height // 2 - 303))

        # Common player info (level / weight / temp)
        self.draw_player_info(screen)

    def draw_player_info(self, screen):
        """Render basic player info shared across inventory tabs."""
        font = pygame.font.Font(font_path, 14)
        self.recalc_weight()
        player.weight = self.total_inventory_weight
        total_weight_pos_x = screen.get_width()/2 + 15
        info_y = 70

        level_text = font.render(f"Level: {player.level}", True, (200, 220, 255))
        screen.blit(level_text, (total_weight_pos_x, info_y))
        info_y += 22

        weight_label = font.render("Weight:", True, (200, 200, 50))
        weight_value = font.render(f"{round(self.total_inventory_weight, 1)} / {player.max_weight}", True, (200, 200, 50))
        screen.blit(weight_label, (total_weight_pos_x, info_y))
        screen.blit(weight_value, (total_weight_pos_x, info_y + 16))
        info_y += 36

        temp_display = int(player.current_temperature) if hasattr(player, "current_temperature") else "N/A"
        temp_text = font.render(f"Temp: {temp_display}", True, (255, 200, 120))
        screen.blit(temp_text, (total_weight_pos_x, info_y + 6))

    def draw_cats_tab(self, screen, x_pos, y_pos):
        """Draw cat cards for every tamed cat the player owns."""
        panel_padding_x = 60
        panel_padding_y = 55
        tab_left = inventory_tab_unused.rect.left if inventory_tab_unused else screen.get_width() // 2 - 533
        tab_bottom = inventory_tab_unused.rect.bottom if inventory_tab_unused else (screen.get_height() // 2 - 303) + 44
        area_left_bound = x_pos + panel_padding_x
        area_right_bound = x_pos + self.cat_screen_image.get_width() - panel_padding_x
        shifted_left = 30
        area_x = max(area_left_bound - shifted_left, tab_left - shifted_left)
        area_y = max(y_pos + panel_padding_y, tab_bottom + 8)
        area_width = max(0, area_right_bound - area_x)
        area_height = self.cat_screen_image.get_height() - ((area_y - (y_pos - 20)) + 25)
        if area_width <= 0 or area_height <= 0:
            return

        cat_surface = pygame.Surface((area_width, area_height), pygame.SRCALPHA)
        entries = self._gather_tamed_cat_entries()
        self.cat_card_entries = entries
        card_width = self.cat_card_image.get_width()
        card_height = self.cat_card_image.get_height()
        columns = max(1, self.cat_card_columns)
        horizontal_gap = self.cat_card_column_padding
        row_offset_x = 0
        portrait_height = int(card_height)
        portrait_side = max(10, min(int(card_width * 4.5), portrait_height))
        portrait_size = (portrait_side, portrait_side)

        if entries:
            total_rows = math.ceil(len(entries) / columns)
            total_height = max(0, total_rows * (card_height + self.cat_card_row_padding) - self.cat_card_row_padding)
            self.cat_card_max_scroll = max(0, total_height - area_height)
            self.cat_card_scroll = max(0, min(self.cat_card_scroll, self.cat_card_max_scroll))
        else:
            self.cat_card_max_scroll = 0
            self.cat_card_scroll = 0

        y_offset = -self.cat_card_scroll
        mouse_pos = pygame.mouse.get_pos()
        self.cat_card_rects = []

        if not entries:
            info_font = pygame.font.Font(font_path, 20)
            info_text = info_font.render("No tamed cats yet. Feed a cat to tame one!", True, (230, 220, 200))
            info_rect = info_text.get_rect(center=(area_width // 4, area_height // 3))
            cat_surface.blit(info_text, info_rect)
        else:
            for idx, entry in enumerate(entries):
                col = idx % columns
                row = idx // columns
                draw_x = row_offset_x + col * (card_width + horizontal_gap)
                draw_y = y_offset + row * (card_height + self.cat_card_row_padding)
                if draw_y > area_height or draw_y + card_height < -card_height:
                    continue

                card_rect_local = pygame.Rect(draw_x, draw_y, card_width, card_height)
                card_rect_screen = pygame.Rect(draw_x + area_x, draw_y + area_y, card_width, card_height)
                self.cat_card_rects.append((card_rect_screen, entry["id"], idx))

                is_hovered = card_rect_screen.collidepoint(mouse_pos)
                is_selected = entry["id"] == self.selected_cat_id

                scale = self.cat_hover_scale.get(entry["id"], 1.0)
                if is_hovered and scale < 1.02:
                    scale = min(1.02, scale + 0.002)
                elif not is_hovered and scale > 1.0:
                    scale = max(1.0, scale - 0.002)
                self.cat_hover_scale[entry["id"]] = scale

                card_surface = self.cat_card_image.copy()

                if is_hovered:
                    shadow_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
                    pygame.draw.rect(shadow_surface, (0, 0, 0, 30), shadow_surface.get_rect(), border_radius=5)
                    card_surface.blit(shadow_surface, (0, 0))

                portrait = self._load_cat_portrait(entry.get("icon"), portrait_size)
                portrait_target = pygame.Rect(0, 0, portrait_size[0], portrait_size[1])
                portrait_target.centerx = card_width // 2
                portrait_target.centery = portrait_height // 2 - 58
                if portrait:
                    card_surface.blit(portrait, portrait_target)
                else:
                    fallback_rect = pygame.Rect(0, 0, portrait_size[0], portrait_size[1])
                    fallback_rect.center = portrait_target.center
                    pygame.draw.rect(card_surface, (60, 60, 90), fallback_rect, border_radius=6)

                text_color = (0, 0, 0)
                text_x = 8
                text_y = 5

                self._draw_text(
                    card_surface,
                    self.cat_card_title_font,
                    entry['name'],
                    (text_x, text_y),
                    text_color
                )

                bar_width = card_width - 16
                bar_height = 10
                bar_x = 8
                bar_y = card_height - 40

                health_current, health_max = entry['health']
                hunger_current, hunger_max = entry['hunger']

                pygame.draw.rect(card_surface, (60, 60, 60), pygame.Rect(bar_x, bar_y, bar_width, bar_height), border_radius=3)
                health_ratio = max(0, min(1, health_current / health_max)) if health_max > 0 else 0
                health_width = int(bar_width * health_ratio)
                health_color = (100, 200, 100) if health_ratio > 0.5 else (255, 200, 100) if health_ratio > 0.25 else (255, 100, 100)
                pygame.draw.rect(card_surface, health_color, pygame.Rect(bar_x, bar_y, health_width, bar_height), border_radius=3)
                pygame.draw.rect(card_surface, (200, 200, 200), pygame.Rect(bar_x, bar_y, bar_width, bar_height), width=1, border_radius=3)

                health_text = self.cat_card_stat_font.render(f"HP: {health_current}/{health_max}", True, (0, 0, 0))
                card_surface.blit(health_text, (bar_x, bar_y - 10))

                bar_y += 20
                pygame.draw.rect(card_surface, (60, 60, 60), pygame.Rect(bar_x, bar_y, bar_width, bar_height), border_radius=3)
                hunger_ratio = max(0, min(1, hunger_current / hunger_max)) if hunger_max > 0 else 0
                hunger_width = int(bar_width * hunger_ratio)
                hunger_color = (150, 100, 200)
                pygame.draw.rect(card_surface, hunger_color, pygame.Rect(bar_x, bar_y, hunger_width, bar_height), border_radius=3)
                pygame.draw.rect(card_surface, (200, 200, 200), pygame.Rect(bar_x, bar_y, bar_width, bar_height), width=1, border_radius=3)

                hunger_text = self.cat_card_stat_font.render(f"Hunger: {hunger_current}/{hunger_max}", True, (0, 0, 0))
                card_surface.blit(hunger_text, (bar_x, bar_y - 10))

                if scale != 1.0:
                    new_size = (int(card_width * scale), int(card_height * scale))
                    card_surface = pygame.transform.scale(card_surface, new_size)
                    offset_x = int((card_width - new_size[0]) / 2)
                    offset_y = int((card_height - new_size[1]) / 2)
                    temp_rect = pygame.Rect(draw_x + offset_x, draw_y + offset_y, new_size[0], new_size[1])
                    cat_surface.blit(card_surface, temp_rect)
                else:
                    cat_surface.blit(card_surface, card_rect_local)

                if is_selected:
                    border_width = 3
                    pygame.draw.rect(cat_surface, (255, 255, 0), pygame.Rect(draw_x, draw_y, card_width, card_height), width=border_width, border_radius=5)

        screen.blit(cat_surface, (area_x, area_y))

    def draw_selected_cat_info(self, screen, x_pos, y_pos):
        """Draw the selected cat's information in the upper right and stats in bottom right."""
        cat_obj = self._get_cat_by_id(self.selected_cat_id)
        if not cat_obj:
            return

        panel_width = 380
        panel_height = 380
        panel_x = screen.get_width() - panel_width - 170
        panel_y = 0

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)

        image_size = 300
        cat_image = None
        if hasattr(cat_obj, 'stand_right_image'):
            try:
                cat_image = pygame.transform.scale(cat_obj.stand_right_image, (image_size, image_size))
            except:
                pass

        image_y = 20
        if cat_image:
            image_x = (panel_width - image_size) // 2
            panel_surface.blit(cat_image, (image_x, image_y))

        text_x = 10
        text_y = 75
        name_font = pygame.font.Font(font_path, 22)
        stat_font = pygame.font.Font(font_path, 16)

        cat_name = getattr(cat_obj, 'cat_name', 'Unnamed Cat') or 'Unnamed Cat'
        name_text = name_font.render(str(cat_name), True, (255, 200, 100))
        panel_surface.blit(name_text, (text_x, text_y))
        text_y += 30

        level = int(getattr(cat_obj, 'level', 1))
        experience = int(getattr(cat_obj, 'experience', 0))
        next_level_exp = int(getattr(cat_obj, 'next_level_exp', 100))
        unspent_points = int(getattr(cat_obj, 'unspent_stat_points', 0))

        level_text = stat_font.render(f"Level: {level}", True, (200, 220, 255))
        panel_surface.blit(level_text, (text_x, text_y))
        text_y += 25

        exp_text = stat_font.render(f"EXP: {experience}/{next_level_exp}", True, (200, 220, 200))
        panel_surface.blit(exp_text, (text_x, text_y))
        text_y += 25

        if unspent_points > 0:
            points_text = stat_font.render(f"Points: {unspent_points}", True, (255, 220, 80))
            panel_surface.blit(points_text, (text_x, text_y))

        screen.blit(panel_surface, (panel_x, panel_y))

        stats_panel_x = screen.get_width() - panel_width - 170
        stats_panel_y = screen.get_height() - 380
        stats_panel_width = 380
        stats_panel_height = 360

        stats_surface = pygame.Surface((stats_panel_width, stats_panel_height), pygame.SRCALPHA)

        stats_text_x = 10
        stats_text_y = 10
        title_font = pygame.font.Font(font_path, 16)

        title = title_font.render("Stats", True, (0, 0, 0))
        stats_surface.blit(title, (stats_text_x, stats_text_y))
        stats_text_y += 25

        health = int(getattr(cat_obj, 'health', 100))
        max_health = int(getattr(cat_obj, 'max_health', 100))
        hunger = int(getattr(cat_obj, 'hunger', 100))
        max_hunger = int(getattr(cat_obj, 'max_hunger', 100))
        attack = int(getattr(cat_obj, 'attack', 10))
        # Speed is displayed as a percentage-like stat (100 = default).
        raw_speed = float(getattr(cat_obj, 'speed', 1))
        speed = int(getattr(cat_obj, 'speed_stat', raw_speed * 100))
        defense = int(getattr(cat_obj, 'defense', 5))

        # Bottom stats: larger font and more spacing than the top-right text.
        bottom_stat_font = pygame.font.Font(font_path, 18)
        stat_line_height = 35
        self.cat_upgrade_button_rects = []

        # Match player level-up button behavior (flash + hover) for cats.
        flash_cycle = unspent_points > 0 and (pygame.time.get_ticks() // 400) % 2 == 0
        mouse_pos = pygame.mouse.get_pos()

        # Layout order: Health, Hunger, Attack, Defense (speed is no longer an upgradeable stat)
        stats_list = [
            ("Health", health, max_health, "health"),
            ("Hunger", hunger, max_hunger, "hunger"),
            ("Attack", attack, None, "attack"),
            ("Defense", defense, None, "defense"),
        ]

        for label, value, max_val, key in stats_list:
            if max_val:
                stat_text = bottom_stat_font.render(f"{label}: {value}/{max_val}", True, (0, 0, 0))
            else:
                stat_text = bottom_stat_font.render(f"{label}: {value}", True, (0, 0, 0))

            stats_surface.blit(stat_text, (stats_text_x, stats_text_y))

            # Use the same level-up button sprites as the player.
            button_x = stats_panel_width - self.level_up_skill_image.get_width() - 20
            button_y = stats_text_y - 5

            # Local rect (panel space) for drawing.
            button_local_rect = self.level_up_skill_image.get_rect(topleft=(button_x, button_y))
            # Screen-space rect for hover/click detection.
            button_screen_rect = button_local_rect.move(stats_panel_x, stats_panel_y)

            hover = button_screen_rect.collidepoint(mouse_pos)
            button_image = self.level_up_skill_flash_image if (hover or flash_cycle) else self.level_up_skill_image
            stats_surface.blit(button_image, button_local_rect)

            self.cat_upgrade_button_rects.append((button_screen_rect, self.selected_cat_id, key))

            stats_text_y += stat_line_height

        screen.blit(stats_surface, (stats_panel_x, stats_panel_y))

    def _gather_tamed_cat_entries(self):
        entries = []
        seen_ids = set()

        world_cats = getattr(mob_placement, "cats", [])
        for cat in world_cats:
            entry = self._build_cat_entry_from_object(cat)
            if entry and entry["id"] not in seen_ids:
                entries.append(entry)
                seen_ids.add(entry["id"])

        for slot in (self.hotbar_slots + self.inventory_list):
            entry = self._build_cat_entry_from_slot(slot)
            if entry and entry["id"] not in seen_ids:
                entries.append(entry)
                seen_ids.add(entry["id"])

        if self.dragged_item:
            entry = self._build_cat_entry_from_slot(self.dragged_item)
            if entry and entry["id"] not in seen_ids:
                entries.append(entry)
                seen_ids.add(entry["id"])

        if self.drop_menu_slot:
            entry = self._build_cat_entry_from_slot(self.drop_menu_slot)
            if entry and entry["id"] not in seen_ids:
                entries.append(entry)
                seen_ids.add(entry["id"])

        return entries

    def _build_cat_entry_from_object(self, cat_obj, icon_override=None):
        if not cat_obj or not getattr(cat_obj, "tamed", False):
            return None
        if not getattr(cat_obj, "is_alive", True):
            return None

        icon_path = icon_override
        if not icon_path and getattr(cat_obj, "cat_type", None):
            icon_path = cat_obj.cat_type.get("stand_right_image")

        level = int(getattr(cat_obj, "level", 1))
        max_health = int(getattr(cat_obj, "max_health", getattr(cat_obj, "full_health", 100)))
        health = int(min(max_health, getattr(cat_obj, "health", max_health)))
        hunger_max = int(getattr(cat_obj, "max_hunger", 100))
        hunger = int(min(hunger_max, getattr(cat_obj, "hunger", hunger_max)))
        experience = int(getattr(cat_obj, "experience", getattr(cat_obj, "tame", 0)))
        experience_max = int(getattr(cat_obj, "next_level_exp", getattr(cat_obj, "tame_max", 100)) or 100)
        attack_value = int(getattr(cat_obj, "attack", getattr(cat_obj, "attack_damage", max(5, level * 4))))
        speed_value = int(getattr(cat_obj, "base_speed", 0) * getattr(cat_obj, "speed", 1))
        defense_value = int(getattr(cat_obj, "defense", max(5, level * 5)))

        entry = {
            "id": getattr(cat_obj, "unique_id", id(cat_obj)),
            "name": cat_obj.cat_name or self._format_cat_type(cat_obj.cat_type.get("type") if getattr(cat_obj, "cat_type", None) else "Cat"),
            "level": level,
            "health": (health, max_health),
            "hunger": (hunger, hunger_max),
            "experience": (experience, max(experience_max, 1)),
            "attack": attack_value,
            "speed": max(0, speed_value),
            "defense": defense_value,
            "icon": icon_path,
            "cat_object": cat_obj,
        }
        return entry

    def _build_cat_entry_from_slot(self, slot):
        if not slot or "cat_type" not in slot:
            return None
        cat_obj = slot.get("cat_object")
        if cat_obj:
            return self._build_cat_entry_from_object(cat_obj, icon_override=slot.get("icon"))

        level = int(slot.get("cat_level", 1))
        health = int(slot.get("cat_health", 100))
        max_health = max(health, 100)
        hunger = int(slot.get("cat_hunger", 100))
        hunger_max = int(slot.get("cat_hunger_max", 100))
        experience = int(slot.get("cat_experience", slot.get("cat_tame", 0)))
        experience_max = int(slot.get("cat_experience_max", slot.get("cat_tame_max", 100)))
        name = slot.get("cat_name") or self._format_cat_type(slot.get("cat_type"))
        attack_value = int(slot.get("cat_attack", max(5, level * 4)))
        speed_value = int(slot.get("cat_speed", 160))
        defense_value = int(slot.get("cat_defense", max(5, level * 3)))

        return {
            "id": ("slot", id(slot)),
            "name": name,
            "level": level,
            "health": (health, max_health),
            "hunger": (hunger, hunger_max),
            "experience": (experience, max(1, experience_max)),
            "attack": attack_value,
            "speed": speed_value,
            "defense": defense_value,
            "icon": slot.get("icon"),
        }

    def _format_cat_type(self, cat_type_key):
        if not cat_type_key:
            return "Cat"
        return cat_type_key.replace("_", " ").title()

    def _load_cat_portrait(self, icon_path, portrait_size):
        if not icon_path:
            return None
        cache_key = (icon_path, portrait_size)
        if cache_key in self.cat_card_portrait_cache:
            return self.cat_card_portrait_cache[cache_key]

        base_surface = self.cat_card_portrait_sources.get(icon_path)
        if base_surface is None:
            try:
                base_surface = pygame.image.load(icon_path).convert_alpha()
                self.cat_card_portrait_sources[icon_path] = base_surface
            except Exception:
                return None

        portrait = pygame.transform.scale(base_surface, portrait_size)
        self.cat_card_portrait_cache[cache_key] = portrait
        return portrait

    def _draw_text(self, surface, font_obj, text, position, color):
        if not text:
            return
        text_surface = font_obj.render(text, True, color)
        surface.blit(text_surface, position)

    def handle_cat_scroll(self, direction):
        """Scroll cat cards vertically. Direction > 0 scrolls down."""
        if self.state != "cats":
            return
        if direction == 0 or self.cat_card_max_scroll <= 0:
            return
        scroll_step = 40
        self.cat_card_scroll = max(0, min(self.cat_card_scroll + direction * scroll_step, self.cat_card_max_scroll))

    def draw_level_up(self, screen):
        # Draw the stat list on the left of the level-up screen along with upgrade buttons.
        start_x = (screen.get_width() / 2 - self.level_up_image.get_width() / 2) + 50
        base_y = (screen.get_height() / 2 - self.level_up_image.get_height() / 2) + 90
        start_y = base_y + 40
        line_height = 45
        button_x = start_x + 360
        flash_cycle = player.unspent_stat_points > 0 and (pygame.time.get_ticks() // 400) % 2 == 0
        mouse_pos = pygame.mouse.get_pos()

        self.level_up_button_rects = []
        
        # Top text with Level, EXP, and Weight
        top_text = self.level_up_font.render(
            f"Level {player.level}  |  EXP: {int(player.experience)}/{int(player.next_level_exp)}  |  Weight: {round(player.weight, 1)}/{int(player.max_weight)}",
            True,
            (0, 0, 0)
        )
        points_text = self.level_up_font.render(f"Unspent Points: {player.unspent_stat_points}", True, (255, 220, 80))
        screen.blit(top_text, (start_x, base_y - 20))
        screen.blit(points_text, (start_x, base_y + 5))

        preview_color = (20, 110, 20)

        stats = [
            {
                "key": "health",
                "label": "Max Health",
                "base": int(player.max_health),
                "preview": int(round((player.health_leveler + 0.1) * 100))
            },
            {
                "key": "stamina",
                "label": "Max Stamina",
                "base": int(player.max_stamina),
                "preview": int(round((player.stamina_leveler + 0.1) * 100))
            },
            {
                "key": "hunger",
                "label": "Max Hunger",
                "base": int(player.max_hunger),
                "preview": int(round((player.hunger_leveler + 0.1) * 100))
            },
            {
                "key": "thirst",
                "label": "Max Thirst",
                "base": int(player.max_thirst),
                "preview": int(round((player.thirst_leveler + 0.1) * 100))
            },
            {
                "key": "temperature_resistance",
                "label": "Temp Resist",
                "base": int(player.temperature_resistance_leveler * 2),
                "preview": int((player.temperature_resistance_leveler + 1) * 2)
            },
            {
                "key": "weight",
                "label": "Max Weight",
                "base": int(player.max_weight),
                "preview": int(round((player.weight_leveler + 0.1) * 100 * player.temp_weight_increase))
            },
            {
                "key": "strength",
                "label": "Strength",
                "base": int(player.attack),
                "preview": int(player.damage + (player.strength_leveler) * player.strength_level_gain)
            },
            {
                "key": "speed",
                "label": "Speed",
                "base": int(player.speed),
                "preview": int(round((player.speed_leveler + 0.05) * 100))
            },
            {
                "key": "defense",
                "label": "Defense",
                "base": int(player.defense),
                "preview": int(round((player.defense_leveler + 0.1) * 100))
            },
            {
                "key": "resilience",
                "label": "Resilience",
                "base": int(player.resilience),
                "preview": int(round((player.resilience_leveler + 0.1) * 100))
            },
        ]

        for idx, stat in enumerate(stats):
            y = start_y + idx * line_height
            label_text = self.level_up_font.render(stat["label"], True, (0, 0, 0))
            value_str = f"{stat['base']}"
            if player.unspent_stat_points > 0:
                value_str = f"{stat['base']} -> {stat['preview']}"
            value_text = self.level_up_value_font.render(value_str, True, preview_color if player.unspent_stat_points > 0 else (0, 0, 0))
            screen.blit(label_text, (start_x, y))
            screen.blit(value_text, (start_x + 160, y + 6))

            button_rect = self.level_up_skill_image.get_rect(topleft=(button_x, y - 10))
            hover = button_rect.collidepoint(mouse_pos)
            button_image = self.level_up_skill_flash_image if (hover or flash_cycle) else self.level_up_skill_image
            screen.blit(button_image, button_rect)
            self.level_up_button_rects.append((button_rect, stat["key"]))

    def handle_level_up_event(self, event):
        if self.state != "level_up":
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        now = pygame.time.get_ticks()
        if now - self.last_level_up_click_time < 200:
            return
        for button_rect, stat_key in self.level_up_button_rects:
            if button_rect.collidepoint(event.pos):
                if player.apply_stat_upgrade(stat_key):
                    self.last_level_up_click_time = now
                break

    def handle_cats_event(self, event):
        if self.state != "cats":
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        now = pygame.time.get_ticks()
        if now - self.last_cat_click_time < 200:
            return

        for button_rect, cat_id, stat_key in self.cat_upgrade_button_rects:
            if button_rect.collidepoint(event.pos):
                cat_obj = self._get_cat_by_id(cat_id)
                if cat_obj and hasattr(cat_obj, 'apply_stat_upgrade'):
                    if cat_obj.apply_stat_upgrade(stat_key):
                        self.last_cat_click_time = now
                return

        for card_rect, cat_id, idx in self.cat_card_rects:
            if card_rect.collidepoint(event.pos):
                if self.selected_cat_id == cat_id:
                    self.selected_cat_id = None
                else:
                    self.selected_cat_id = cat_id
                self.last_cat_click_time = now
                break

    def _get_cat_by_id(self, cat_id):
        if not self.cat_card_entries:
            return None
        for entry in self.cat_card_entries:
            if entry.get("id") == cat_id:
                cat_obj = entry.get("cat_object")
                if cat_obj:
                    return cat_obj
        return None

    def begin_hover_pass(self):
        self.tooltip_mode_active = True
        self._hover_candidate = None

    def clear_hover_state(self):
        self.tooltip_mode_active = False
        self._hover_candidate = None
        self._hover_active_id = None
        self._hover_display_data = None
        self._hover_start_time = 0

    def _get_item_def(self, item_name):
        for item in items_list:
            if item["item_name"] == item_name:
                return item
        return None

    def _is_pickaxe_item(self, item_def):
        if not item_def:
            return False
        name = item_def.get("item_name", "").lower()
        tags = item_def.get("tags", [])
        return "pickaxe" in name or ("mining" in tags)

    def _is_axe_item(self, item_def):
        if not item_def:
            return False
        name = item_def.get("item_name", "").lower()
        return "axe" in name and "pickaxe" not in name

    def _get_tool_tier(self, item_def):
        if not item_def:
            return None
        name = item_def.get("item_name", "").lower()
        tags = item_def.get("tags", [])
        if "dragon scale" in name:
            return "dragon"
        if "obsidian" in name:
            return "obsidian"
        if "gold" in name:
            return "gold"
        if "metal" in name:
            return "metal"
        if "stone" in name:
            return "stone"
        if "bone" in name:
            return "bone"
        if "wood" in name:
            return "wood"
        if "mining" in tags:
            return "metal"
        return None

    def register_hover_candidate(self, candidate_id, item_name, rect, recipe=None, slot_data=None):
        if not self.tooltip_mode_active:
            return

        item_def = self._get_item_def(item_name)
        if not item_def:
            return

        durability = item_def.get("durability")
        if slot_data is not None and slot_data.get("durability") is not None:
            durability = slot_data.get("durability")

        status_effects = None
        if slot_data is not None:
            status_effects = slot_data.get("status_effects")
        if status_effects is None:
            status_effects = item_def.get("status_effects")
        if status_effects is None:
            status_effects = item_def.get("use_effect")

        self._hover_candidate = {
            "id": candidate_id,
            "item_def": item_def,
            "rect": rect,
            "durability": durability,
            "status": status_effects,
            "recipe": recipe,
        }

    def _finalize_hover_candidate(self):
        now = pygame.time.get_ticks()

        if not self.tooltip_mode_active or self._hover_candidate is None:
            self._hover_active_id = None
            self._hover_display_data = None
            self._hover_start_time = 0
            return

        if self._hover_candidate["id"] != self._hover_active_id:
            self._hover_active_id = self._hover_candidate["id"]
            self._hover_start_time = now

        self._hover_display_data = self._hover_candidate

    def _wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test_line = word if current == "" else current + " " + word
            if font.size(test_line)[0] <= max_width:
                current = test_line
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if not lines:
            lines = [""]
        return lines

    def create_item_instance(self, item_def, quantity=1):
        new_item = item_def.copy()
        new_item["quantity"] = quantity
        if item_def.get("durability") is not None:
            new_item["durability"] = item_def["durability"]
            new_item["max_durability"] = item_def["durability"]
        return new_item

    def decrement_durability(self, slot_index, is_hotbar=True, amount=1):
        slot_list = self.hotbar_slots if is_hotbar else self.inventory_list
        if slot_index is None or slot_index < 0 or slot_index >= len(slot_list):
            return
        slot = slot_list[slot_index]
        if slot is None:
            return
        if slot.get("durability") is None:
            return
        slot["durability"] -= amount
        if slot["durability"] <= 0:
            slot_list[slot_index] = None

    def _format_status_effects(self, status):
        effects = []
        if isinstance(status, list):
            raw_effects = status
        else:
            raw_effects = [status]

        for raw in raw_effects:
            if raw is None:
                continue
            parts = [p.strip() for p in str(raw).split(";") if p.strip()]
            for part in parts:
                match = re.match(r"player\.(\w+)\s*([+-]=)\s*([+-]?\d*\.?\d+)", part)
                if match:
                    stat_name, op, val = match.groups()
                    label = stat_name.replace("_", " ").title()
                    sign = "+" if op == "+=" and not val.startswith("-") else ""
                    effects.append(f"{label} {sign}{val}")
                    continue
                effects.append(part)
        return effects

    def draw_hover_tooltip(self, screen):
        self._finalize_hover_candidate()

        if not self.tooltip_mode_active or self._hover_display_data is None:
            return

        now = pygame.time.get_ticks()
        if now - self._hover_start_time < self.tooltip_delay_ms:
            return

        data = self._hover_display_data
        item_def = data["item_def"]
        rect_x, rect_y, rect_w, rect_h = data["rect"]
        max_text_width = 280

        lines = []
        lines.append((self.tooltip_title_font, item_def.get("item_name", "Unknown"), (255, 255, 255)))

        description = item_def.get("description", "")
        for line in self._wrap_text(description, self.tooltip_body_font, max_text_width):
            lines.append((self.tooltip_body_font, line, (230, 230, 230)))

        durability_label = "Durability" if data.get("recipe") is None else "Max Durability"
        durability_value = data.get("durability")
        dur_text = f"{durability_label}: {durability_value}" if durability_value is not None else f"{durability_label}: N/A"
        lines.append((self.tooltip_small_font, dur_text, (210, 210, 210)))

        is_pickaxe = self._is_pickaxe_item(item_def)
        is_axe = self._is_axe_item(item_def)
        tier = self._get_tool_tier(item_def)
        if tier and (is_pickaxe or is_axe):
            mults = HARVEST_TOOL_MULTS.get(tier, {"normal": 1, "special": 1})
            if is_axe:
                lines.append((self.tooltip_small_font, f"Harvest Yield (wood): x{mults.get('normal',1)}", (200, 230, 255)))
            if is_pickaxe:
                lines.append((self.tooltip_small_font, f"Harvest Yield (mining): x{mults.get('special',1)}", (200, 230, 255)))

        status = data.get("status")
        formatted_status = self._format_status_effects(status) if status else []
        if formatted_status:
            lines.append((self.tooltip_small_font, "Status Effects:", (200, 255, 200)))
            for effect in formatted_status:
                for line in self._wrap_text(effect, self.tooltip_small_font, max_text_width):
                    lines.append((self.tooltip_small_font, f"- {line}", (200, 230, 200)))
        else:
            lines.append((self.tooltip_small_font, "Status Effects: None", (180, 180, 180)))

        recipe = data.get("recipe")
        if recipe:
            lines.append((self.tooltip_small_font, "Recipe:", (255, 220, 160)))
            for req in recipe:
                if "item" in req:
                    label = f"{req['item']} x{req.get('amount', 1)}"
                elif "item_tag" in req:
                    pretty = req["item_tag"].replace("_", " ").title()
                    label = f"{pretty} x{req.get('amount', 1)}"
                else:
                    label = "Unknown ingredient"
                for line in self._wrap_text(label, self.tooltip_small_font, max_text_width):
                    lines.append((self.tooltip_small_font, f"- {line}", (230, 230, 200)))

        line_height = 4
        rendered = []
        max_width = 0
        for font, text, color in lines:
            surface = font.render(text, True, color)
            rendered.append(surface)
            max_width = max(max_width, surface.get_width())
            line_height += surface.get_height() + 4

        padding = 10
        box_width = max_width + padding * 2
        box_height = line_height + padding

        tooltip_x = rect_x + rect_w + 12
        tooltip_y = rect_y

        if tooltip_x + box_width > screen.get_width() - 10:
            tooltip_x = rect_x - box_width - 12
        if tooltip_y + box_height > screen.get_height() - 10:
            tooltip_y = max(10, screen.get_height() - box_height - 10)

        bg_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 230))
        pygame.draw.rect(bg_surface, (255, 255, 255, 200), (0, 0, box_width, box_height), 1, border_radius=6)

        current_y = padding // 2
        for surf in rendered:
            bg_surface.blit(surf, (padding, current_y))
            current_y += surf.get_height() + 4

        screen.blit(bg_surface, (tooltip_x, tooltip_y))

    def show_selected_hotbar_name(self, duration_ms=1200):
        slot = None
        if 0 <= self.selected_hotbar_slot < len(self.hotbar_slots):
            slot = self.hotbar_slots[self.selected_hotbar_slot]

        if slot is None or "item_name" not in slot:
            self.hotbar_name_display_text = ""
            self.hotbar_name_display_until = 0
            return

        self.hotbar_name_display_text = slot["item_name"]
        self.hotbar_name_display_until = pygame.time.get_ticks() + duration_ms

    def draw_hotbar(self, screen):
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        screen.blit(hotbar_image, (hotbar_x, hotbar_y))
        slot_size = self.slot_size * .75
        hotbar_font = pygame.font.Font(font_path, 10)
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        mouse_pos = pygame.mouse.get_pos()

        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y

            if i == self.selected_hotbar_slot and self.selection_mode == "hotbar":
                highlight_surface = pygame.Surface((slot_size + 6, slot_size + 6), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (255, 255, 255, 200), (0, 0, slot_size + 6, slot_size + 6), 3)
                screen.blit(highlight_surface, (x - 4.5, y - 4.5))
                
            
            slot = self.hotbar_slots[i]
            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image_hotbar"], (x, y))  # Use hotbar version

                        stack_weight = round(quantity * item["weight"], 1)
                        weight_text = hotbar_font.render(str(stack_weight), True, (250, 250, 20))
                        weight_x_pos = x + 29
                        if stack_weight == int(stack_weight) and stack_weight < 10:
                            weight_x_pos += 4
                        screen.blit(weight_text, (weight_x_pos, y + 3))

                        if quantity > 1:
                            stack_text = hotbar_font.render(str(quantity), True, (255, 255, 255))
                            if quantity >= 100:
                                screen.blit(stack_text, (x + 28, y + 33))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 29, y + 33))
                            else:
                                screen.blit(stack_text, (x + 30, y + 33))

                        if slot.get("durability") is not None and slot.get("durability") < item.get("durability", slot.get("durability")):
                            max_dur = item.get("durability", slot["durability"])
                            cur_dur = max(0, min(slot["durability"], max_dur))
                            ratio = cur_dur / max_dur if max_dur else 0
                            bar_width = int(slot_size * ratio)
                            bar_height = 3
                            bar_x = x
                            bar_y = y + slot_size - bar_height - 1
                            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, slot_size, bar_height))
                            pygame.draw.rect(screen, (50, 200, 50), (bar_x, bar_y, bar_width, bar_height))

                        if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                            self.register_hover_candidate(
                                ("hotbar", i),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot
                            )

                        break

        if self.hotbar_name_display_text and pygame.time.get_ticks() < self.hotbar_name_display_until:
            selected_x = first_slot_x + self.selected_hotbar_slot * slot_spacing
            selected_y = slot_y
            name_surface = self.hotbar_name_font.render(self.hotbar_name_display_text, True, (255, 255, 255))
            bg_width = name_surface.get_width() + 8
            bg_height = name_surface.get_height() + 4
            bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 160))
            bg_x = int(selected_x + (slot_size - bg_width) / 2)
            bg_y = int(selected_y + slot_size + 2)
            screen.blit(bg_surface, (bg_x, bg_y))
            screen.blit(name_surface, (bg_x + 4, bg_y + 2))

    def draw_drop_menu(self, screen):
        if not self.drop_menu_active:
            return

        is_special_menu = hasattr(self, 'drop_menu_context') and self.drop_menu_context is not None
        
        if is_special_menu:
            slot = self.drop_menu_slot if isinstance(self.drop_menu_slot, dict) else None
        else:
            slot = self._get_slot_from_context(self.drop_menu_slot, self.drop_menu_is_hotbar)
        
        if slot is None:
            if is_special_menu:
                self.close_special_menu_drop()
            else:
                self.close_drop_menu()
            return

        menu_width = 240
        option_height = 26
        title_height = 18
        padding = 10
        options = [
            ("drop_one", "Drop one (R)"),
            ("drop_amount", "Drop amount..."),
            ("drop_all", "Drop all"),
            ("split_one", "Split one to new stack"),
            ("split_half", "Split half"),
            ("split_amount", "Split amount..."),
            ("split_singles", "Split into singles"),
        ]
        menu_height = padding * 2 + title_height + (option_height + 4) * len(options)
        if self.awaiting_drop_amount:
            menu_height += option_height + 4

        menu_x, menu_y = self.drop_menu_position
        if menu_x + menu_width > screen.get_width() - 10:
            menu_x = screen.get_width() - menu_width - 10
        if menu_y + menu_height > screen.get_height() - 10:
            menu_y = screen.get_height() - menu_height - 10

        self.drop_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

        bg_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 190))
        pygame.draw.rect(bg_surface, (220, 220, 220), bg_surface.get_rect(), 2, border_radius=8)
        screen.blit(bg_surface, (menu_x, menu_y))

        option_font = pygame.font.Font(font_path, 16)
        title_font = pygame.font.Font(font_path, 14)

        title_text = title_font.render(slot.get("item_name", "Item"), True, (255, 255, 255))
        screen.blit(title_text, (menu_x + padding, menu_y + padding))

        self.drop_option_rects = {}
        start_y = menu_y + padding + title_height + 4
        for idx, (key, label) in enumerate(options):
            rect = pygame.Rect(menu_x + padding, start_y + idx * (option_height + 4), menu_width - padding * 2, option_height)
            self.drop_option_rects[key] = rect
            pygame.draw.rect(screen, (40, 40, 40, 180), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1, border_radius=4)
            text_surface = option_font.render(label, True, (255, 255, 255))
            screen.blit(text_surface, (rect.x + 8, rect.y + 5))

        if self.awaiting_drop_amount:
            input_rect = pygame.Rect(menu_x + padding, start_y + len(options) * (option_height + 4), menu_width - padding * 2, option_height)
            pygame.draw.rect(screen, (30, 30, 30, 200), input_rect)
            pygame.draw.rect(screen, (180, 180, 180), input_rect, 1, border_radius=4)
            prompt_label = "Split amount" if self.amount_action == "split" else "Drop amount"
            prompt = f"{prompt_label}: {self.drop_amount_input or '_'}"
            prompt_surface = option_font.render(prompt, True, (255, 255, 255))
            screen.blit(prompt_surface, (input_rect.x + 8, input_rect.y + 5))

    def draw_items(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 18
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
        font = pygame.font.Font(font_path, 14)
        self.recalc_weight()
        mouse_pos = pygame.mouse.get_pos()

        for hotbar_slot in self.hotbar_slots:
            if hotbar_slot is not None:
                item_name = hotbar_slot["item_name"]
                quantity = hotbar_slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        stack_weight = round(quantity * item["weight"], 1)
                        break

        for slot_index in range(self.capacity):
            slot = self.inventory_list[slot_index]

            row = slot_index // self.columns
            col = slot_index % self.columns
            x = start_x + col * (self.slot_size + self.gap_size)
            y = start_y + row * (self.slot_size + self.gap_size - 3)

            if self.selection_mode == "inventory" and self.selected_inventory_slot == slot_index:
                highlight_surface = pygame.Surface((self.slot_size + 8, self.slot_size + 8), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (255, 255, 255, 200), (0, 0, self.slot_size + 8, self.slot_size + 8), 4)
                screen.blit(highlight_surface, (x - 4, y - 4))

            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]

                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))  # Use inventory version (already 60x60)
                        if pygame.Rect(x, y, self.slot_size, self.slot_size).collidepoint(mouse_pos):
                            self.register_hover_candidate(
                                ("inventory", slot_index),
                                item_name,
                                (x, y, self.slot_size, self.slot_size),
                                slot_data=slot
                            )

                        stack_weight = round(quantity * item["weight"], 1)
                        weight_text = font.render(str(stack_weight), True, (250, 250, 20))
                        weight_x_pos = x + 39
                        if stack_weight == int(stack_weight) and stack_weight < 10:
                            weight_x_pos += 7
                        screen.blit(weight_text, (weight_x_pos, y + 4))
                        
                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))

                        if slot.get("durability") is not None and slot.get("durability") < item.get("durability", slot.get("durability")):
                            max_dur = item.get("durability", slot["durability"])
                            cur_dur = max(0, min(slot["durability"], max_dur))
                            ratio = cur_dur / max_dur if max_dur else 0
                            bar_width = int(self.slot_size * ratio)
                            bar_height = 4
                            bar_x = x
                            bar_y = y + self.slot_size - bar_height - 2
                            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, self.slot_size, bar_height))
                            pygame.draw.rect(screen, (50, 200, 50), (bar_x, bar_y, bar_width, bar_height))

                        break
        
    def get_craftable_items(self):
        """Get all items that have recipes and crafting_medium is 'hand', sorted alphabetically."""
        craftable = []
        for item in items_list:
            if item["recipe"] is not None and item.get("crafting_medium") == "hand":
                craftable.append(item)
        craftable.sort(key=lambda x: x["item_name"])
        return craftable

    def has_materials_for_recipe(self, recipe):
        if recipe is None:
            return False
        
        for requirement in recipe:
            if "item" in requirement:
                item_name = requirement["item"]
                amount_needed = requirement["amount"]
                amount_have = self.get_item_count(item_name)
                if amount_have < amount_needed:
                    return False
            elif "item_tag" in requirement:
                tag = requirement["item_tag"]
                amount_needed = requirement["amount"]
                amount_have = self.get_items_by_tag_count(tag)
                if amount_have < amount_needed:
                    return False
        return True

    def get_item_count(self, item_name):
        count = 0
        for slot in self.inventory_list + self.hotbar_slots:
            if slot and slot["item_name"] == item_name:
                count += slot["quantity"]
        return count

    def get_items_by_tag_count(self, tag):
        count = 0
        for slot in self.inventory_list + self.hotbar_slots:
            if slot:
                item_name = slot["item_name"]
                for item in items_list:
                    if item["item_name"] == item_name and tag in item["tags"]:
                        count += slot["quantity"]
                        break
        return count

    def remove_materials_from_inventory(self, recipe):
        if recipe is None:
            return False
        for requirement in recipe:
            if "item" in requirement:
                item_name = requirement["item"]
                amount_to_remove = requirement["amount"]
                self.remove_item(item_name, amount_to_remove)
            elif "item_tag" in requirement:
                tag = requirement["item_tag"]
                amount_to_remove = requirement["amount"]
                self.remove_items_by_tag(tag, amount_to_remove)
        return True

    def remove_item(self, item_name, amount):
        remaining = amount
        
        for slot in self.inventory_list:
            if slot and slot["item_name"] == item_name:
                if slot["quantity"] <= remaining:
                    remaining -= slot["quantity"]
                    slot["quantity"] = 0
                else:
                    slot["quantity"] -= remaining
                    remaining = 0
                    break
            if remaining == 0:
                break
        
        if remaining > 0:
            for slot in self.hotbar_slots:
                if slot and slot["item_name"] == item_name:
                    if slot["quantity"] <= remaining:
                        remaining -= slot["quantity"]
                        slot["quantity"] = 0
                    else:
                        slot["quantity"] -= remaining
                        remaining = 0
                        break
                if remaining == 0:
                    break
        
        for i in range(len(self.inventory_list)):
            if self.inventory_list[i] and self.inventory_list[i]["quantity"] <= 0:
                self.inventory_list[i] = None
        
        for i in range(len(self.hotbar_slots)):
            if self.hotbar_slots[i] and self.hotbar_slots[i]["quantity"] <= 0:
                self.hotbar_slots[i] = None

        self.recalc_weight()

    def remove_items_by_tag(self, tag, amount):
        remaining = amount
        
        for slot in self.inventory_list:
            if slot:
                item_name = slot["item_name"]
                for item in items_list:
                    if item["item_name"] == item_name and tag in item["tags"]:
                        if slot["quantity"] <= remaining:
                            remaining -= slot["quantity"]
                            slot["quantity"] = 0
                        else:
                            slot["quantity"] -= remaining
                            remaining = 0
                        break
            if remaining == 0:
                break
        
        if remaining > 0:
            for slot in self.hotbar_slots:
                if slot:
                    item_name = slot["item_name"]
                    for item in items_list:
                        if item["item_name"] == item_name and tag in item["tags"]:
                            if slot["quantity"] <= remaining:
                                remaining -= slot["quantity"]
                                slot["quantity"] = 0
                            else:
                                slot["quantity"] -= remaining
                                remaining = 0
                            break
                if remaining == 0:
                    break
        
        for i in range(len(self.inventory_list)):
            if self.inventory_list[i] and self.inventory_list[i]["quantity"] <= 0:
                self.inventory_list[i] = None
        
        for i in range(len(self.hotbar_slots)):
            if self.hotbar_slots[i] and self.hotbar_slots[i]["quantity"] <= 0:
                self.hotbar_slots[i] = None

        self.recalc_weight()
    def draw_crafting(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 18
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44

        font_small = pygame.font.Font(font_path, 14)
        font_medium = pygame.font.Font(font_path, 18)
        font_large = pygame.font.Font(font_path, 22)
        mouse_pos = pygame.mouse.get_pos()

        self.crafting_slot_positions = {}

        craftable_items = self.get_craftable_items()
        
        for idx, item in enumerate(craftable_items):
            if idx >= self.capacity:
                break
            
            row = idx // self.columns
            col = idx % self.columns
            x = start_x + col * (self.slot_size + self.gap_size)
            y = start_y + row * (self.slot_size + self.gap_size - 3)
            
            has_materials = self.has_materials_for_recipe(item["recipe"])
            
            if has_materials:
                highlight_surface = pygame.Surface((self.slot_size, self.slot_size), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (100, 255, 100, 100), (0, 0, self.slot_size, self.slot_size))
                screen.blit(highlight_surface, (x, y))
            else:
                highlight_surface = pygame.Surface((self.slot_size, self.slot_size), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (100, 100, 100, 150), (0, 0, self.slot_size, self.slot_size))
                screen.blit(highlight_surface, (x, y))
            
            screen.blit(item["image"], (x, y))

            self.crafting_slot_positions[idx] = (x, y, item)

            if pygame.Rect(x, y, self.slot_size, self.slot_size).collidepoint(mouse_pos):
                self.register_hover_candidate(
                    ("crafting_recipe", idx),
                    item["item_name"],
                    (x, y, self.slot_size, self.slot_size),
                    recipe=item.get("recipe")
                )

        # Draw crafting completion flash
        if self.crafting_completion_flash and self.crafting_completion_slot:
            x, y = self.crafting_completion_slot
            flash_surface = pygame.Surface((self.slot_size, self.slot_size), pygame.SRCALPHA)
            pygame.draw.rect(flash_surface, (255, 255, 255, 150), (0, 0, self.slot_size, self.slot_size))
            screen.blit(flash_surface, (x, y))

        if hasattr(self, 'selected_crafting_item') and self.selected_crafting_item is not None:
            item = self.selected_crafting_item
            
            preview_x = screen.get_width() - 400
            preview_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 60
            
            for item_data in items_list:
                if item_data["item_name"] == item["item_name"]:
                    preview_image = item_data["image"]
                    preview_scaled = pygame.transform.scale(preview_image, (250, 250))
                    preview_rect = preview_scaled.get_rect(center=(preview_x + 60, preview_y + 60))
                    screen.blit(preview_scaled, preview_rect)
                    break
            
            recipe_x = screen.get_width() - 550
            recipe_y = screen.get_height() / 2 - self.inventory_image.get_height() / 2 + 290
            
            name_text = font_large.render(item["item_name"], True, (20, 20, 50))
            screen.blit(name_text, (recipe_x, recipe_y))
            
            recipe_y += 40
            max_width = 400
            words = item["description"].split()
            line = ""
            for word in words:
                test_line = line + word + " "
                test_width = font_small.size(test_line)[0]
                if test_width > max_width:
                    if line:
                        desc_text = font_small.render(line, True, (0, 0, 0))
                        screen.blit(desc_text, (recipe_x, recipe_y))
                        recipe_y += 20
                    line = word + " "
                else:
                    line = test_line
            if line:
                desc_text = font_small.render(line, True, (0, 0, 0))
                screen.blit(desc_text, (recipe_x, recipe_y))
                recipe_y += 20
            
            recipe_y += 20
            recipe_label = font_medium.render("Recipe:", True, (20, 20, 50))
            screen.blit(recipe_label, (recipe_x, recipe_y))
            
            recipe_y += 40
            if item["recipe"]:
                for requirement in item["recipe"]:
                    if "item" in requirement:
                        item_name = requirement["item"]
                        amount = requirement["amount"]
                        have = self.get_item_count(item_name)
                    elif "item_tag" in requirement:
                        item_name = requirement["item_tag"].replace("_", " ").title()
                        amount = requirement["amount"]
                        have = self.get_items_by_tag_count(requirement["item_tag"])
                    
                    color = (50, 255, 50) if have >= amount else (255, 50, 50)
                    req_text = font_small.render(f"{item_name}: {have}/{amount}", True, color)
                    temp_surface = pygame.Surface((req_text.get_width() + 10, req_text.get_height() + 10), pygame.SRCALPHA)
                    temp_surface.fill((0, 0, 0, 100))
                    screen.blit(temp_surface, (recipe_x - 5, recipe_y -5))
                    screen.blit(req_text, (recipe_x, recipe_y))
                    recipe_y += 30

    def craft_item(self, item):
        if not self.has_materials_for_recipe(item["recipe"]):
            return False
        
        self.remove_materials_from_inventory(item["recipe"])
        
        self.add({item["item_name"]: item["output_amount"]})
        
        # Play random hammer_wood sound
        sound_manager.play_sound(random.choice([f"hammer_wood{i}" for i in range(1, 4)]))
        
        return True

    def add(self, resource):
        all_added = True
        
        for entry in resource:
            if isinstance(entry, dict) and "__full_item__" in entry:
                added = self._add_full_item_instance(entry["__full_item__"])
                if not added:
                    all_added = False
                    if self.inventory_full_message_timer <= 0:
                        self.inventory_full_message_timer = 2.0
                continue

            item_name = entry
            stacked = False
            
            for item_data in items_list:
                if item_data["item_name"] == item_name:
                    max_stack = item_data["stack_size"]
                    
                    for i in range(self.hotbar_size):
                        slot = self.hotbar_slots[i]
                        if slot and slot["item_name"] == item_name:
                            if slot["quantity"] < max_stack:
                                slot["quantity"] += 1
                                stacked = True
                                break
                    
                    if not stacked:
                        for i in range(self.capacity):
                            slot = self.inventory_list[i]
                            if slot and slot["item_name"] == item_name:
                                if slot["quantity"] < max_stack:
                                    slot["quantity"] += 1
                                    stacked = True
                                    break
                    
                    if not stacked:
                        for i in range(self.hotbar_size):
                            if self.hotbar_slots[i] is None:
                                self.hotbar_slots[i] = self.create_item_instance(item_data, 1)
                                stacked = True
                                break
                    
                    if not stacked:
                        for i in range(self.capacity):
                            if self.inventory_list[i] is None:
                                self.inventory_list[i] = self.create_item_instance(item_data, 1)
                                stacked = True
                                break
                    
                    break
            
            if not stacked:
                all_added = False
                if self.inventory_full_message_timer <= 0:
                    self.inventory_full_message_timer = 2.0
        
        self.recalc_weight()
        return all_added
    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        first_slot_x = hotbar_x + 4.5  # Changed from 3 to match draw_hotbar
        slot_y = hotbar_y + 4.5  # Changed from 3 to match draw_hotbar
        slot_spacing = 51  # Changed from 34 to match draw_hotbar
        slot_size = self.slot_size * 0.75  # Changed from /2 to *0.75 to match draw_hotbar
        
        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y

            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:  # Changed from /2 to use slot_size variable
                return (i, True)
        
        if self.ui_open:
            start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 17
            start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
            
            for slot_index in range(self.capacity):
                row = slot_index // self.columns
                col = slot_index % self.columns
                x = start_x + col * (self.slot_size + self.gap_size)
                y = start_y + row * (self.slot_size + self.gap_size - 3)
                
                if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                    return (slot_index, False)
        
        return (None, None)
    
    def handle_crafting_click(self, mouse_pos, current_time):
        import time
        
        for idx, (x, y, item) in self.crafting_slot_positions.items():
            if x <= mouse_pos[0] <= x + self.slot_size and y <= mouse_pos[1] <= y + self.slot_size:
                if self.last_click_slot == idx and (current_time - self.last_click_time) < 0.3:
                    if self.has_materials_for_recipe(item["recipe"]):
                        # Craft immediately and trigger flash
                        self.craft_item(item)
                        # Trigger completion flash
                        self.crafting_completion_flash = True
                        self.crafting_completion_time = pygame.time.get_ticks() / 1000.0
                        self.crafting_completion_slot = (x, y)
                        self.last_click_slot = None
                        self.last_click_time = 0
                        return True
                else:
                    self.selected_crafting_item = item
                    self.last_click_slot = idx
                    self.last_click_time = current_time
                    return False
        
        return False

    def update_flash(self, dt):
        """Update completion flash timer"""
        if self.crafting_completion_flash:
            current_time = pygame.time.get_ticks() / 1000.0
            if current_time - self.crafting_completion_time >= self.crafting_flash_duration:
                self.crafting_completion_flash = False
                self.crafting_completion_slot = None
                self.crafting_completion_time = 0

    def start_drag(self, slot_index, is_hotbar):
        if slot_index is None:
            return False
        if (not is_hotbar) and self.state != "inventory":
            return False

        self.close_drop_menu()
        slots = self.hotbar_slots if is_hotbar else self.inventory_list
        slot = slots[slot_index]
        if slot is None:
            return False

        self.dragging = True
        self.dragged_item = slot.copy()
        self.dragged_from_slot = slot_index
        self.dragged_from_hotbar = is_hotbar
        slots[slot_index] = None
        self.recalc_weight()
        return True

    def update_drag(self, mouse_pos):
        pass

    def end_drag(self, slot_index, is_hotbar, screen):
        if not self.dragging:
            return
        
        if is_hotbar:
            target_slot = self.hotbar_slots[slot_index]
        else:
            target_slot = self.inventory_list[slot_index]
        
        new_selection_hotbar = None
        new_selection_inventory = None

        if target_slot is None:
            if is_hotbar:
                self.hotbar_slots[slot_index] = self.dragged_item
                new_selection_hotbar = slot_index
            else:
                self.inventory_list[slot_index] = self.dragged_item
                new_selection_inventory = slot_index
        
        elif target_slot["item_name"] == self.dragged_item["item_name"]:
            max_stack = 100
            for item in items_list:
                if item["item_name"] == self.dragged_item["item_name"]:
                    max_stack = item["stack_size"]
                    break

            space_available = max_stack - target_slot["quantity"]
            amount_to_add = min(space_available, self.dragged_item["quantity"])
            
            target_slot["quantity"] += amount_to_add
            self.dragged_item["quantity"] -= amount_to_add
            
            if self.dragged_item["quantity"] > 0:
                if self.dragged_from_hotbar:
                    self.hotbar_slots[self.dragged_from_slot] = self.dragged_item
                else:
                    self.inventory_list[self.dragged_from_slot] = self.dragged_item
            # Stacking keeps selection on the target slot
            if is_hotbar:
                new_selection_hotbar = slot_index
            else:
                new_selection_inventory = slot_index
        
        else:
            if is_hotbar:
                self.hotbar_slots[slot_index] = self.dragged_item
                new_selection_hotbar = slot_index
            else:
                self.inventory_list[slot_index] = self.dragged_item
                new_selection_inventory = slot_index
            
            if self.dragged_from_hotbar:
                self.hotbar_slots[self.dragged_from_slot] = target_slot
            else:
                self.inventory_list[self.dragged_from_slot] = target_slot
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        if new_selection_hotbar is not None:
            self.selected_hotbar_slot = new_selection_hotbar
            self.selection_mode = "hotbar"
            self.selected_inventory_slot = None
        elif new_selection_inventory is not None:
            self.selected_inventory_slot = new_selection_inventory
            self.selection_mode = "inventory"
            self.selected_hotbar_slot = self.selected_hotbar_slot if 0 <= self.selected_hotbar_slot < self.hotbar_size else 0
        self.recalc_weight()

    def cancel_drag(self):
        if not self.dragging:
            return
        
        if self.dragged_from_hotbar:
            self.hotbar_slots[self.dragged_from_slot] = self.dragged_item
        else:
            self.inventory_list[self.dragged_from_slot] = self.dragged_item
        
        # Restore selection to the slot we canceled from
        if self.dragged_from_hotbar:
            self.selected_hotbar_slot = self.dragged_from_slot
            self.selection_mode = "hotbar"
            self.selected_inventory_slot = None
        else:
            self.selected_inventory_slot = self.dragged_from_slot
            self.selection_mode = "inventory"
        # Ensure hotbar index stays in range
        if self.selected_hotbar_slot >= self.hotbar_size:
            self.selected_hotbar_slot = 0
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        self.recalc_weight()

    def draw_dragged_item(self, screen):
        if not self.dragging or self.dragged_item is None:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for item in items_list:
            if item["item_name"] == self.dragged_item["item_name"]:
                temp_surface = item["image"].copy()
                temp_surface.set_alpha(180)
                screen.blit(temp_surface, (mouse_x - self.slot_size // 2, mouse_y - self.slot_size // 2))
                
                if self.dragged_item["quantity"] > 1:
                    font = pygame.font.Font(font_path, 16)
                    quantity = self.dragged_item["quantity"]
                    stack_text = font.render(str(quantity), True, (255, 255, 255))
                    
                    x = mouse_x - self.slot_size // 2
                    y = mouse_y - self.slot_size // 2
                    
                    if quantity >= 100:
                        screen.blit(stack_text, (x + 38, y + 44))
                    elif quantity > 9:
                        screen.blit(stack_text, (x + 42, y + 44))
                    else:
                        screen.blit(stack_text, (x + 47, y + 44))
                
                break
    def select_hotbar_slot(self, index, do_use=False, screen=None):
        if index is None or index < 0 or index >= self.hotbar_size:
            return

        self.selected_hotbar_slot = index

        if do_use:
            self.use_hotbar_slot(index, screen)

    def use_hotbar_slot(self, index, screen=None):
        slot = self.hotbar_slots[index]
        if slot is None:
            return

        item_name = slot["item_name"]
        quantity = slot["quantity"]

        consumables = {"Apples", "Baked Apples", "Small thirst", "Small Health Brew"}  # expand as needed
        if item_name in consumables:
            slot["quantity"] -= 1
            if slot["quantity"] <= 0:
                self.hotbar_slots[index] = None

        else:
            print(f"Used hotbar slot {index}: {item_name} x{quantity}")

    def handle_keydown_hotbar(self, event, screen=None, use_on_press=False):
        key_to_index = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
            pygame.K_6: 5,
            pygame.K_7: 6,
            pygame.K_8: 7,
            pygame.K_9: 8,
            pygame.K_0: 9,
            # numeric keypad
            pygame.K_KP1: 0,
            pygame.K_KP2: 1,
            pygame.K_KP3: 2,
            pygame.K_KP4: 3,
            pygame.K_KP5: 4,
            pygame.K_KP6: 5,
            pygame.K_KP7: 6,
            pygame.K_KP8: 7,
            pygame.K_KP9: 8,
            pygame.K_KP0: 9,
        }

        if hasattr(event, 'key') and event.key in key_to_index:
            idx = key_to_index[event.key]
            self.select_hotbar_slot(idx, do_use=use_on_press, screen=screen)
        elif hasattr(event, 'key'):
            pass

    def handle_selection_click(self, mouse_pos, screen):
        slot_index, is_hotbar = self.get_slot_at_mouse(mouse_pos, screen)
    
        if slot_index is not None:
            if is_hotbar:
                self.selected_hotbar_slot = slot_index
                self.selection_mode = "hotbar"
                self.selected_inventory_slot = None
            else:
                self.selected_inventory_slot = slot_index
                self.selection_mode = "inventory"
            
            self.close_drop_menu()
            return (slot_index, is_hotbar)
        
        self.close_drop_menu()
        return (None, None)

    def close_drop_menu(self):
        self.drop_menu_active = False
        self.drop_menu_slot = None
        self.drop_menu_is_hotbar = False
        self.drop_menu_context = None
        self.drop_option_rects = {}
        self.drop_menu_rect = None
        self.drop_amount_input = ""
        self.awaiting_drop_amount = False
        self.amount_action = None

    def open_drop_menu(self, slot_index, is_hotbar, mouse_pos):
        if slot_index is None:
            self.close_drop_menu()
            return False
        slots = self.hotbar_slots if is_hotbar else self.inventory_list
        if slot_index < 0 or slot_index >= len(slots):
            self.close_drop_menu()
            return False
        if slots[slot_index] is None:
            self.close_drop_menu()
            return False

        self.drop_menu_active = True
        self.drop_menu_slot = slot_index
        self.drop_menu_is_hotbar = is_hotbar
        self.drop_menu_position = mouse_pos
        self.awaiting_drop_amount = False
        self.drop_amount_input = ""
        self.amount_action = None
        return True

    def handle_drop_right_click(self, mouse_pos, screen):
        slot_index, is_hotbar = self.get_slot_at_mouse(mouse_pos, screen)
        if slot_index is None:
            self.close_drop_menu()
            return False

        slots = self.hotbar_slots if is_hotbar else self.inventory_list
        if slots[slot_index] is None:
            self.close_drop_menu()
            return False

        self.handle_selection_click(mouse_pos, screen)
        return self.open_drop_menu(slot_index, is_hotbar, mouse_pos)

    def _get_slot_from_context(self, slot_index, is_hotbar):
        slots = self.hotbar_slots if is_hotbar else self.inventory_list
        if slot_index is None or slot_index < 0 or slot_index >= len(slots):
            return None
        return slots[slot_index]

    def remove_quantity_from_slot(self, slot_index, is_hotbar, amount):
        if amount is None or amount <= 0:
            return None
        slot = self._get_slot_from_context(slot_index, is_hotbar)
        if slot is None:
            return None

        drop_amount = min(amount, slot.get("quantity", 0))
        if drop_amount <= 0:
            return None

        item_name = slot.get("item_name")
        item_data = next((item for item in items_list if item["item_name"] == item_name), None)

        slot["quantity"] -= drop_amount
        if slot["quantity"] <= 0:
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None

        self.recalc_weight()
        return {"item_data": item_data, "item_name": item_name, "amount": drop_amount}

    def remove_selected_quantity(self, amount):
        if self.selection_mode == "hotbar":
            slot_index = self.selected_hotbar_slot
            is_hotbar = True
        elif self.selection_mode == "inventory":
            if self.selected_inventory_slot is None:
                return None
            slot_index = self.selected_inventory_slot
            is_hotbar = False
        else:
            return None

        return self.remove_quantity_from_slot(slot_index, is_hotbar, amount)

    def _first_empty_inventory_slot(self):
        for idx, slot in enumerate(self.inventory_list):
            if slot is None:
                return ("inventory", idx)
        for idx, slot in enumerate(self.hotbar_slots):
            if slot is None:
                return ("hotbar", idx)
        return (None, None)

    def _count_empty_slots(self, exclude_hotbar_index=None, exclude_inventory_index=None):
        count = 0
        for idx, slot in enumerate(self.inventory_list):
            if idx == exclude_inventory_index:
                continue
            if slot is None:
                count += 1
        for idx, slot in enumerate(self.hotbar_slots):
            if idx == exclude_hotbar_index:
                continue
            if slot is None:
                count += 1
        return count

    def _place_new_stack(self, item_data, quantity, exclude_hotbar_index=None, exclude_inventory_index=None):
        if quantity is None or quantity <= 0 or not item_data:
            return False
        new_stack = self.create_item_instance(item_data, quantity)
        for idx, slot in enumerate(self.inventory_list):
            if idx == exclude_inventory_index:
                continue
            if slot is None:
                self.inventory_list[idx] = new_stack
                return True
        for idx, slot in enumerate(self.hotbar_slots):
            if idx == exclude_hotbar_index:
                continue
            if slot is None:
                self.hotbar_slots[idx] = new_stack
                return True
        return False

    def _place_full_stack(self, stack_item):
        """Place a fully defined item stack into the first available slot."""
        stack_copy = copy.deepcopy(stack_item)
        for i in range(self.hotbar_size):
            if self.hotbar_slots[i] is None:
                self.hotbar_slots[i] = copy.deepcopy(stack_copy)
                return True
        for i in range(self.capacity):
            if self.inventory_list[i] is None:
                self.inventory_list[i] = copy.deepcopy(stack_copy)
                return True
        return False

    def _add_full_item_instance(self, item_instance):
        """Add a fully defined inventory item (preserving durability/metadata)."""
        if not item_instance:
            return False
        instance_copy = copy.deepcopy(item_instance)
        item_name = instance_copy.get("item_name")
        if not item_name:
            return False
        quantity = int(instance_copy.get("quantity", 1)) or 1
        max_stack = instance_copy.get("stack_size", 1) or 1

        if max_stack > 1:
            for slot_list in (self.hotbar_slots, self.inventory_list):
                for slot in slot_list:
                    if not slot:
                        continue
                    if slot.get("item_name") != item_name:
                        continue
                    if slot.get("durability") != instance_copy.get("durability"):
                        continue
                    if slot.get("max_durability") != instance_copy.get("max_durability"):
                        continue
                    available = max_stack - slot.get("quantity", 0)
                    if available <= 0:
                        continue
                    add_amount = min(available, quantity)
                    slot["quantity"] += add_amount
                    quantity -= add_amount
                    if quantity <= 0:
                        return True

        while quantity > 0:
            stack_amount = min(max_stack, quantity)
            stack_copy = copy.deepcopy(instance_copy)
            stack_copy["quantity"] = stack_amount
            placed = self._place_full_stack(stack_copy)
            if not placed:
                return False
            quantity -= stack_amount
        return True

    def _perform_drop_from_menu(self, amount):
        if self.drop_menu_slot is None:
            return None
        result = self.remove_quantity_from_slot(self.drop_menu_slot, self.drop_menu_is_hotbar, amount)
        self.close_drop_menu()
        return result

    def _split_stack(self, amount=None, mode=None):
        """Split items from the drop menu slot into a new stack."""
        if self.drop_menu_slot is None:
            return False

        slot = self._get_slot_from_context(self.drop_menu_slot, self.drop_menu_is_hotbar)
        if slot is None:
            return False

        item_name = slot.get("item_name")
        item_data = next((item for item in items_list if item["item_name"] == item_name), None)
        if not item_data:
            return False

        current_qty = slot.get("quantity", 0)
        if current_qty <= 1:
            return False

        # Determine split amount
        split_amount = None
        if mode == "half":
            split_amount = max(1, current_qty // 2)
        elif mode == "all_singles":
            # Attempt to peel items off into single stacks where space allows
            movable = min(current_qty - 1, self._count_empty_slots(
                exclude_hotbar_index=self.drop_menu_slot if self.drop_menu_is_hotbar else None,
                exclude_inventory_index=self.drop_menu_slot if not self.drop_menu_is_hotbar else None
            ))
            if movable <= 0:
                return False
            moved = 0
            for _ in range(movable):
                if self._place_new_stack(
                    item_data,
                    1,
                    exclude_hotbar_index=self.drop_menu_slot if self.drop_menu_is_hotbar else None,
                    exclude_inventory_index=self.drop_menu_slot if not self.drop_menu_is_hotbar else None
                ):
                    moved += 1
                else:
                    break
            if moved <= 0:
                return False
            slot["quantity"] -= moved
            if slot["quantity"] <= 0:
                if self.drop_menu_is_hotbar:
                    self.hotbar_slots[self.drop_menu_slot] = None
                else:
                    self.inventory_list[self.drop_menu_slot] = None
            self.recalc_weight()
            return True
        else:
            # Explicit amount (one or custom)
            split_amount = amount if amount is not None else 1

        if split_amount is None or split_amount <= 0:
            return False
        if split_amount >= current_qty:
            split_amount = current_qty - 1
        if split_amount <= 0:
            return False

        placed = self._place_new_stack(
            item_data,
            split_amount,
            exclude_hotbar_index=self.drop_menu_slot if self.drop_menu_is_hotbar else None,
            exclude_inventory_index=self.drop_menu_slot if not self.drop_menu_is_hotbar else None
        )
        if not placed:
            return False

        slot["quantity"] -= split_amount
        if slot["quantity"] <= 0:
            if self.drop_menu_is_hotbar:
                self.hotbar_slots[self.drop_menu_slot] = None
            else:
                self.inventory_list[self.drop_menu_slot] = None
        self.recalc_weight()
        return True

    def handle_drop_menu_click(self, mouse_pos):
        if not self.drop_menu_active:
            return None

        if self.drop_menu_rect and not self.drop_menu_rect.collidepoint(mouse_pos):
            self.close_drop_menu()
            return None

        for key, rect in self.drop_option_rects.items():
            if rect.collidepoint(mouse_pos):
                is_special_menu = hasattr(self, 'drop_menu_context') and self.drop_menu_context is not None
                
                if key == "drop_one":
                    if is_special_menu:
                        return self.handle_special_menu_drop(1)
                    else:
                        return self._perform_drop_from_menu(1)
                if key == "drop_all":
                    if is_special_menu:
                        slot = self.drop_menu_slot
                        amount = slot.get("quantity", 0) if slot else 0
                        return self.handle_special_menu_drop(amount)
                    else:
                        slot = self._get_slot_from_context(self.drop_menu_slot, self.drop_menu_is_hotbar)
                        amount = slot.get("quantity", 0) if slot else 0
                        return self._perform_drop_from_menu(amount)
                if key == "drop_amount":
                    self.awaiting_drop_amount = True
                    self.drop_amount_input = ""
                    self.amount_action = "drop"
                if key == "split_one":
                    if is_special_menu:
                        if self.handle_special_menu_split(amount=1):
                            self.close_special_menu_drop()
                    else:
                        if self._split_stack(amount=1):
                            self.close_drop_menu()
                if key == "split_half":
                    if is_special_menu:
                        if self.handle_special_menu_split(mode="half"):
                            self.close_special_menu_drop()
                    else:
                        if self._split_stack(mode="half"):
                            self.close_drop_menu()
                if key == "split_amount":
                    self.awaiting_drop_amount = True
                    self.drop_amount_input = ""
                    self.amount_action = "split"
                if key == "split_singles":
                    if is_special_menu:
                        if self.handle_special_menu_split(mode="all_singles"):
                            self.close_special_menu_drop()
                    else:
                        if self._split_stack(mode="all_singles"):
                            self.close_drop_menu()
                return None

        return None

    def handle_drop_amount_key(self, event):
        if not (self.drop_menu_active and self.awaiting_drop_amount):
            return None

        is_special_menu = hasattr(self, 'drop_menu_context') and self.drop_menu_context is not None

        if event.key == pygame.K_RETURN:
            self.awaiting_drop_amount = False
            try:
                amount = int(self.drop_amount_input) if self.drop_amount_input else 0
            except ValueError:
                amount = 0
            if amount <= 0:
                if is_special_menu:
                    self.close_special_menu_drop()
                else:
                    self.close_drop_menu()
                return None
            if self.amount_action == "split":
                if is_special_menu:
                    self.handle_special_menu_split(amount=amount)
                    self.close_special_menu_drop()
                else:
                    self._split_stack(amount=amount)
                    self.close_drop_menu()
                return None
            else:
                if is_special_menu:
                    return self.handle_special_menu_drop(amount)
                else:
                    return self._perform_drop_from_menu(amount)
        elif event.key == pygame.K_BACKSPACE:
            self.drop_amount_input = self.drop_amount_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            if is_special_menu:
                self.close_special_menu_drop()
            else:
                self.close_drop_menu()
        else:
            if hasattr(event, "unicode") and event.unicode.isdigit():
                if len(self.drop_amount_input) < 3:
                    self.drop_amount_input += event.unicode
        return None
    
    def get_selected_item(self):
        """
        Get the item data for the currently selected item (from hotbar or inventory).
        Returns: item data dict or None if no valid item selected
        """
        # Determine which slot is selected based on selection mode
        if self.selection_mode == "hotbar":
            slot = self.hotbar_slots[self.selected_hotbar_slot]
        elif self.selection_mode == "inventory":
            if self.selected_inventory_slot is None:
                return None
            slot = self.inventory_list[self.selected_inventory_slot]
        else:
            return None
        
        # Check if slot has an item
        if slot is None:
            return None
        
        item_name = slot["item_name"]
        
        # Find the item data in items_list
        for item in items_list:
            if item["item_name"] == item_name:
                return item
        
        return None

    def throw_item(self):
        """
        Remove the currently selected item from inventory for throwing.
        Does NOT apply the use_effect (unlike consume_item).
        Returns: (success: bool, tags: list, thrown_instance: dict|None)
        """
        # Determine which slot to throw from based on selection mode
        if self.selection_mode == "hotbar":
            slot_index = self.selected_hotbar_slot
            slot = self.hotbar_slots[slot_index]
            is_hotbar = True
        elif self.selection_mode == "inventory":
            if self.selected_inventory_slot is None:
                return (False, [], None)
            slot_index = self.selected_inventory_slot
            slot = self.inventory_list[slot_index]
            is_hotbar = False
        else:
            return (False, [], None)
        
        # Check if slot has an item
        if slot is None:
            return (False, [], None)
        
        item_name = slot["item_name"]
        
        # Find the item data in items_list
        item_data = None
        for item in items_list:
            if item["item_name"] == item_name:
                item_data = item
                break
        
        if item_data is None:
            return (False, [], None)

        thrown_instance = copy.deepcopy(slot)
        thrown_instance["quantity"] = 1
        # Cat objects should never reach here, but guard against it
        thrown_instance.pop("cat_object", None)
        
        # Reduce quantity by 1
        slot["quantity"] -= 1
        
        # Remove item from slot if quantity reaches 0
        if slot["quantity"] <= 0:
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None

        # Return empty container if defined
        if item_data.get("return_item"):
            self.add([item_data["return_item"]])

        self.recalc_weight()
        return (True, item_data.get("tags", []), thrown_instance)

    def consume_item(self):
        """
        Consume the currently selected item (from hotbar or inventory).
        Returns: (success: bool, tags: list) - True if consumed, and the item's tags
        """
        # Determine which slot to consume from based on selection mode
        if self.selection_mode == "hotbar":
            slot_index = self.selected_hotbar_slot
            slot = self.hotbar_slots[slot_index]
            is_hotbar = True
        elif self.selection_mode == "inventory":
            if self.selected_inventory_slot is None:
                return (False, [])  # No inventory slot selected
            slot_index = self.selected_inventory_slot
            slot = self.inventory_list[slot_index]
            is_hotbar = False
        else:
            return (False, [])  # Invalid selection mode
        
        # Check if slot has an item
        if slot is None:
            return (False, [])
        
        item_name = slot["item_name"]
        
        # Find the item data in items_list
        item_data = None
        for item in items_list:
            if item["item_name"] == item_name:
                item_data = item
                break
        
        if item_data is None:
            return (False, [])  # Item not found in items_list
        
        # Check if item is consumable
        if not item_data.get("consumable", False):
            return (False, [])
        
        # Apply the use_effect to the player
        use_effect = item_data.get("use_effect")
        if use_effect:
            self.apply_use_effect(use_effect)
        
        # Reduce quantity by 1
        slot["quantity"] -= 1
        
        # Remove item from slot if quantity reaches 0
        if slot["quantity"] <= 0:
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None
        
        # Return an empty container if defined via return_item field
        if item_data.get("return_item"):
            self.add([item_data["return_item"]])
        else:
            # Return an empty container only if the recipe actually uses a container item
            recipe = item_data.get("recipe")
            if recipe and isinstance(recipe, list):
                for recipe_item in recipe:
                    if not (isinstance(recipe_item, dict) and "item" in recipe_item):
                        continue
                    container_name = recipe_item["item"]
                    # Check whether this recipe item is a container (by tag or type)
                    container_data = next((itm for itm in items_list if itm["item_name"] == container_name), None)
                    if container_data and ("container" in container_data.get("tags", []) or container_data.get("type") == "container"):
                        self.add([container_name])
                        break  # only add one container back
        
        return (True, item_data.get("tags", []))  # Return success and tags
        
    def apply_use_effect(self, use_effect):
        
        if use_effect is None:
            return
        
        from mob_placement import player
        
        effects = use_effect.split(";")
        
        for effect in effects:
            effect = effect.strip()
            
            if not effect:
                continue
            
            try:
                exec(effect)
            except Exception as e:
                print(f"Error applying effect '{effect}': {e}")
        
        if player.health > player.max_health:
            player.health = player.max_health
        if player.hunger > player.max_hunger:
            player.hunger = player.max_hunger
        if player.stamina > player.max_stamina:
            player.stamina = player.max_stamina
        if player.thirst > player.max_thirst:
            player.thirst = player.max_thirst
    
    def place_cat(self, cam_x=0):
        """Place a tamed cat from inventory into the world at player position."""
        # Determine which slot to use
        if self.selection_mode == "hotbar":
            slot_index = self.selected_hotbar_slot
            slot = self.hotbar_slots[slot_index]
            is_hotbar = True
        elif self.selection_mode == "inventory":
            if self.selected_inventory_slot is None:
                return None
            slot_index = self.selected_inventory_slot
            slot = self.inventory_list[slot_index]
            is_hotbar = False
        else:
            return None
        
        # Check if slot has a tamed cat (check for cat_type field which all tamed cat items have)
        if slot is None or "cat_type" not in slot:
            return None
        
        # Get the cat object
        cat = slot.get("cat_object")
        if cat is None:
            return None
        
        # Place the cat near the player (using world coordinates)
        # player.rect is in screen coordinates, so we add cam_x to get world coordinates
        from mob_placement import player
        if player.last_direction == "right":
            cat.rect.centerx = player.rect.centerx + cam_x + 50
            cat.rect.centery = player.rect.centery
        if player.last_direction == "left":
            cat.rect.centerx = player.rect.centerx + cam_x - 50
            cat.rect.centery = player.rect.centery
        if player.last_direction == "up":
            cat.rect.centerx = player.rect.centerx + cam_x
            cat.rect.centery = player.rect.centery - 50
        if player.last_direction == "down":
            cat.rect.centerx = player.rect.centerx + cam_x
            cat.rect.centery = player.rect.centery + 50

        # Restore cat data from inventory
        if "cat_name" in slot:
            cat.cat_name = slot["cat_name"]
        if "cat_health" in slot:
            cat.health = slot["cat_health"]
        if "cat_tame" in slot:
            cat.tame = slot["cat_tame"]
        if "cat_level" in slot:
            cat.level = slot["cat_level"]
        
        # Remove the item from inventory
        slot["quantity"] -= 1
        if slot["quantity"] <= 0:
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None
        
        return cat

    def open_special_menu_drop(self, slot_data, menu_context, mouse_pos=(0, 0)):
        self.drop_menu_active = True
        self.drop_menu_slot = slot_data
        self.drop_menu_is_hotbar = False
        self.drop_menu_position = mouse_pos
        self.drop_menu_context = menu_context
        self.awaiting_drop_amount = False
        self.drop_amount_input = ""
        self.amount_action = None
        return True

    def handle_special_menu_drop(self, amount):
        if not self.drop_menu_active:
            return None
        
        slot_data = self.drop_menu_slot
        if not isinstance(slot_data, dict) or "item_name" not in slot_data:
            return None
        
        drop_amount = min(amount, slot_data.get("quantity", 0))
        if drop_amount <= 0:
            return None
        
        item_name = slot_data.get("item_name")
        item_data = next((item for item in items_list if item["item_name"] == item_name), None)
        
        slot_data["quantity"] -= drop_amount
        if slot_data["quantity"] <= 0:
            slot_data["quantity"] = 0
        
        self.recalc_weight()
        return {"item_data": item_data, "item_name": item_name, "amount": drop_amount}

    def handle_special_menu_split(self, amount=None, mode=None):
        if not self.drop_menu_active:
            return False
        
        slot_data = self.drop_menu_slot
        if not isinstance(slot_data, dict) or "item_name" not in slot_data:
            return False
        
        item_name = slot_data.get("item_name")
        item_data = next((item for item in items_list if item["item_name"] == item_name), None)
        if not item_data:
            return False
        
        current_qty = slot_data.get("quantity", 0)
        if current_qty <= 1:
            return False
        
        split_amount = None
        if mode == "half":
            split_amount = max(1, current_qty // 2)
        elif mode == "all_singles":
            movable = min(current_qty - 1, self._count_empty_slots())
            if movable <= 0:
                return False
            moved = 0
            for _ in range(movable):
                if self._place_new_stack(item_data, 1):
                    moved += 1
                else:
                    break
            if moved <= 0:
                return False
            slot_data["quantity"] -= moved
            if slot_data["quantity"] <= 0:
                slot_data["quantity"] = 0
            self.recalc_weight()
            return True
        else:
            split_amount = amount if amount is not None else 1
        
        if split_amount is None or split_amount <= 0:
            return False
        if split_amount >= current_qty:
            split_amount = current_qty - 1
        if split_amount <= 0:
            return False
        
        placed = self._place_new_stack(item_data, split_amount)
        if not placed:
            return False
        
        slot_data["quantity"] -= split_amount
        if slot_data["quantity"] <= 0:
            slot_data["quantity"] = 0
        self.recalc_weight()
        return True

    def close_special_menu_drop(self):
        self.drop_menu_active = False
        self.drop_menu_slot = None
        self.drop_menu_context = None
        self.drop_menu_rect = None

inventory = Inventory(64)
