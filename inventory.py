import pygame
import random
from mob_placement import player
from buttons import inventory_tab, crafting_tab, level_up_tab, cats_tab, inventory_tab_unused, crafting_tab_unused, level_up_tab_unused, cats_tab_unused
from sounds import sound_manager


hotbar_image = pygame.image.load("assets/sprites/buttons/hotbar.png").convert_alpha()
hotbar_image = pygame.transform.scale(hotbar_image, (514, 55))
player_inventory_image = pygame.image.load("assets/sprites/player/GlenjaminFrontIdle1.png")
player_inventory_image = pygame.transform.scale(player_inventory_image, (500, 500))

image_path = "assets/sprites/items"

items_list = [
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A crisp red apple. Sweet and refreshing.',
        "durability": None,
        "icon": 'Apple.png',
        "item_name": 'Apples',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 5; player.thirst += 3',
        "weight": 0.5
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A juicy orange. Bursting with citrus flavor.',
        "durability": None,
        "icon": 'Orange.png',
        "item_name": 'Oranges',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 4; player.thirst += 5',
        "weight": 0.5
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A hard-shelled coconut. Contains sweet milk inside.',
        "durability": None,
        "icon": 'Coconut.png',
        "item_name": 'Coconuts',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 3; player.thirst += 8',
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Sturdy wood from an apple tree. Good for crafting.',
        "durability": None,
        "icon": 'AppleWood.png',
        "item_name": 'Apple Wood',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['wood', 'material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Dark purple-brown wood. Has a mysterious quality.',
        "durability": None,
        "icon": 'DuskWood.png',
        "item_name": 'Dusk Wood',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['wood', 'material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Light and flexible fir wood. Easy to work with.',
        "durability": None,
        "icon": 'FirWood.png',
        "item_name": 'Fir Wood',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['wood', 'material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Strong oak wood. Excellent for construction.',
        "durability": None,
        "icon": 'OakWood.png',
        "item_name": 'Oak Wood',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['wood', 'material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Deep red berries. Slightly tart with a hint of sweetness.',
        "durability": None,
        "icon": 'BloodBerries.png',
        "item_name": 'Blood Berries',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5; player.health += .5',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Light-colored berries that glow faintly. Taste like crisp morning air.',
        "durability": None,
        "icon": 'DawnBerries.png',
        "item_name": 'Dawn Berries',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5; player.torpidity -= 1',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Purple berries found at twilight. Mysteriously satisfying. Seriously tiring.',
        "durability": None,
        "icon": 'DuskBerries.png',
        "item_name": 'Dusk Berries',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5; player.torpidity += 1',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Bright orange berries. Warm and energizing.',
        "durability": None,
        "icon": 'SunBerries.png',
        "item_name": 'Sun Berries',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5; player.warmth += 2',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Cool blue-green berries. Refreshingly crisp and chill.',
        "durability": None,
        "icon": 'TealBerries.png',
        "item_name": 'Teal Berries',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5; player.warmth -= 2',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Plump drupes that share their color with the night sky. Uniquely flavorful.',
        "durability": None,
        "icon": 'TwilightDrupes.png',
        "item_name": 'Twilight Drupes',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Deep violet berries. Rich and slightly sweet.',
        "durability": None,
        "icon": 'VioBerries.png',
        "item_name": 'Vio Berries',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'berry'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5; player.thirst += .5',
        "weight": 0.05
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A common mushroom. Safe to eat and nutritious.',
        "durability": None,
        "icon": 'Mushroom.png',
        "item_name": 'Mushroom',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'mushroom'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 1',
        "weight": 0.1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A luminous mushroom. Has a mild glow.',
        "durability": None,
        "icon": 'Dawnshroom.png',
        "item_name": 'Dawnshroom',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'mushroom'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 1; player.glow_time += 100',
        "weight": 0.1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A dark mushroom of curious color and qualities. Earthy and savory.',
        "durability": None,
        "icon": 'Duskshroom.png',
        "item_name": 'Duskshroom',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'mushroom'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 1; player.temp_weight_increase += .01',
        "weight": 0.1
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'A cut of raw beef. Should be cooked before eating.',
        "durability": None,
        "icon": 'RawBeef.png',
        "item_name": 'Raw Beef',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 3; player.health -= 3',
        "weight": 0.4
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Raw bear meat. Needs cooking to be safe. Unbearable if not cooked properly.',
        "durability": None,
        "icon": 'RawBearMeat.png',
        "item_name": 'Raw Bear Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 3; player.health -= 4',
        "weight": 0.5
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Just a wee bit of meat from a wee animal. Needs cooking to be safe.',
        "durability": None,
        "icon": 'SmallMeat.png',
        "item_name": 'Small Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 2; player.health -= 3',
        "weight": 0.2
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Raw chicken meat. Needs cooking to be safe.',
        "durability": None,
        "icon": 'RawBirdMeat.png',
        "item_name": 'Raw Chicken',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 2; player.health -= 3',
        "weight": 0.3
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'A fresh-caught fish. Best when cooked, but cats love it raw.',
        "durability": None,
        "icon": 'Fish.png',
        "item_name": 'Fish',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 3; player.health -= 1',
        "weight": 0.6
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Raw deer meat. Gamey and lean. Best when cooked',
        "durability": None,
        "icon": 'RawVenison.png',
        "item_name": 'Raw Venison',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 4; player.health -= 2',
        "weight": 0.4
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Meat from a gila monster. Exotic and tough.',
        "durability": None,
        "icon": 'RawReptileMeat.png',
        "item_name": 'Gila Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 4; player.health -= 2',
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A chunk of solid stone. Useful for building and crafting.',
        "durability": None,
        "icon": 'Stone.png',
        "item_name": 'Stone',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'crafting'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Unrefined metal ore. Needs smelting to be useful.',
        "durability": None,
        "icon": 'RawMetal.png',
        "item_name": 'Raw Metal',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": True,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Simple wooden sticks. Basic crafting material.',
        "durability": None,
        "icon": 'Stick.png',
        "item_name": 'Sticks',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'stick'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Unrefined gold ore. Valuable when smelted.',
        "durability": None,
        "icon": 'RawGold.png',
        "item_name": 'Raw Gold',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": True,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A toxic mushroom. Do not eat! Or do. Could be fun. Or painful. Mess around and find out, I guess. Used in alchemy.',
        "durability": None,
        "icon": 'PoisonousMushroom.png',
        "item_name": 'Poisonous Mushroom',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'mushroom'],
        "type": 'raw_material',
        "use_effect": 'player.poison = True; player.poison_time += 30; player.poison_strength += 1',
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Plant fibers. Can be woven into twine.',
        "durability": None,
        "icon": 'Fiber.png',
        "item_name": 'Fiber',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'fiber'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.05
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Animal hide. Useful for leather crafting.',
        "durability": None,
        "icon": 'Hide.png',
        "item_name": 'Hide',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Antlers from a buck. Strong and sharp.',
        "durability": None,
        "icon": 'BuckAntlers.png',
        "item_name": 'Buck Antlers',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Sharp, durable claws cut from a duskwretch. Like, super sharp. Razor-sharp.',
        "durability": None,
        "icon": 'DuskwretchClaws.png',
        "item_name": 'Duskwretch Claws',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 3
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A strange eye from a lifeless Pock. Unnerving to look at. May have qualities some might consider to be... unnatural.',
        "durability": None,
        "icon": 'PockEye.png',
        "item_name": 'Pock Eye',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": 'player.poison = True; player.poison_time += 100; self.temp_attack_boost += .1',
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Sharp flint stone. Used for fire-starting.',
        "durability": None,
        "icon": 'Flint.png',
        "item_name": 'Flint',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['item'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A sturdy bone. Can be carved into tools.',
        "durability": None,
        "icon": 'Bone.png',
        "item_name": 'Bone',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Soft animal fur. Warm and comfortable.',
        "durability": None,
        "icon": 'Fur.png',
        "item_name": 'Fur',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A small sac filled with venom. Handle with care.',
        "durability": None,
        "icon": 'VenomSac.png',
        "item_name": 'Venom Sac',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": "A spiky horn from the crest of a lovely mountain goat's sweet head. You probably didn't get this by asking nicely.",
        "durability": None,
        "icon": 'GoatHorn.png',
        "item_name": 'Goat Horns',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.8
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Light feathers from a bird. Useful for crafting.',
        "durability": None,
        "icon": 'Feather.png',
        "item_name": 'Feathers',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.01
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": "Sharp front fangs of a giant animal. Useful for crafting and ripping through flesh, if you're into that kind of thing.",
        "durability": None,
        "icon": 'Fangs.png',
        "item_name": 'Fangs',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": "The little tiny baby claw of a creepy crawly purple crustacean. Useful for crafting and clamping things together really tighly, if you'd like.",
        "durability": None,
        "icon": 'DuskaceanClaw.png',
        "item_name": 'Duskacean Claws',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'animal_parts'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A beautiful purple gemstone. Quite valuable. You feel lighter just lookig at it',
        "durability": None,
        "icon": 'Amethyst.png',
        "item_name": 'Amethyst',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A clear blue gemstone. Reminds you of the ocean, and yet, you somehow feel a little more quenched.',
        "durability": None,
        "icon": 'Aquamarine.png',
        "item_name": 'Aquamarine',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": "A shiny reddish gemstone. Is it hot in here? Because I don't mind at all.",
        "durability": None,
        "icon": 'Garnet.png',
        "item_name": 'Garnet',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A flawless diamond. Extremely rare and valuable. You feel a little tougher just holding it.',
        "durability": None,
        "icon": 'Diamond.png',
        "item_name": 'Diamond',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A vibrant and energizing green gemstone. Highly prized.',
        "durability": None,
        "icon": 'Emerald.png',
        "item_name": 'Emerald',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'An iridescent gemstone. Shimmers with many colors that feed your very soul.',
        "durability": None,
        "icon": 'Opal.png',
        "item_name": 'Opal',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A lustrous pearl. Smooth and elegant. Created in the violent and raging depths of the sea.',
        "durability": None,
        "icon": 'Pearl.png',
        "item_name": 'Pearl',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A deep red gemstone. Burns with inner fire and ignites your passion for living',
        "durability": None,
        "icon": 'Ruby.png',
        "item_name": 'Ruby',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A brilliant blue gemstone. Clear as the sky. Must be your lucky day',
        "durability": None,
        "icon": 'Sapphire.png',
        "item_name": 'Sapphire',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A golden yellow gemstone. Warm and radiant. A swift reward for those patient enough to obtain it.',
        "durability": None,
        "icon": 'Topaz.png',
        "item_name": 'Topaz',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['gemstone'],
        "type": 'gem',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A key for unlocking cages. Single use.',
        "durability": None,
        "icon": 'CageKey.png',
        "item_name": 'Cage Key',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 10,
        "tags": ['key'],
        "type": 'key',
        "use_effect": 'unlock_cage',
        "weight": 0.3
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A key for unlocking chests. Single use.',
        "durability": None,
        "icon": 'ChestKey.png',
        "item_name": 'Chest Key',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 10,
        "tags": ['key'],
        "type": 'key',
        "use_effect": 'unlock_chest',
        "weight": 0.3
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tropical pineapple. Sweet and tangy.',
        "durability": None,
        "icon": 'Pineapple.png',
        "item_name": 'Pineapple',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 7; player.thirst += 4; player.thirst += 4',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A juicy watermelon. Very hydrating.',
        "durability": None,
        "icon": 'Watermelon.png',
        "item_name": 'Watermelon',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += 6; player.thirst += 8',
        "weight": 0.8
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Fresh olives. Can be pressed for oil.',
        "durability": None,
        "icon": 'Olives.png',
        "item_name": 'Olives',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'raw_material',
        "use_effect": 'player.hunger += .5',
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A warm leaf that radiates heat. Used in alchemy.',
        "durability": None,
        "icon": 'FireFernLeaf.png',
        "item_name": 'Fire Fern Leaf',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['herb', 'potion_ingredient', 'Fire Material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A cold leaf that feels icy to touch. Used in alchemy.',
        "durability": None,
        "icon": 'FrostFernLeaf.png',
        "item_name": 'Frost Fern Leaf',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['herb', 'potion_ingredient'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Apples baked to perfection. Warm and delicious.',
        "durability": None,
        "icon": 'BakedApple.png',
        "item_name": 'Baked Apples',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Apples', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'fruit'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 8',
        "weight": 0.5
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Perfectly cooked beef. Juicy and savory.',
        "durability": None,
        "icon": 'CookedBeef.png',
        "item_name": 'Cooked Beef',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Beef', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'cooked'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 25',
        "weight": 0.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Perfectly cooked bear meat from a perfectly murdered bear. Tuff but real yummy. Fills you up a lot.',
        "durability": None,
        "icon": 'CookedBearMeat.png',
        "item_name": 'Cooked Bear Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Bear Meat', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'cooked'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 40',
        "weight": 0.5
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Toasty lil meat morsel. Juicy and savory.',
        "durability": None,
        "icon": 'CookedSmallMeat.png',
        "item_name": 'Cooked Small Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Small Meat', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'cooked'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 12',
        "weight": 0.2
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Well-cooked chicken. Tender and flavorful.',
        "durability": None,
        "icon": 'CookedBirdMeat.png',
        "item_name": 'Cooked Chicken',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Chicken', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'cooked'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 18',
        "weight": 0.3
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Grilled fish. Flaky and delicious. Cats prefer fish raw and wriggling.',
        "durability": None,
        "icon": 'CookedFish.png',
        "item_name": 'Cooked Fish',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Fish', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 16',
        "weight": 0.6
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Roasted venison. Gamey and satisfying.',
        "durability": None,
        "icon": 'CookedVenison.png',
        "item_name": 'Cooked Venison',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Venison', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'cooked'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 20',
        "weight": 0.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'campfire',
        "description": 'Grilled gila meat. Exotic and hearty.',
        "durability": None,
        "icon": 'CookedReptileMeat.png',
        "item_name": 'Cooked Gila Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gila Meat', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 14',
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "description": 'A refined metal ingot. Ready for crafting.',
        "durability": None,
        "icon": 'MetalIngot.png',
        "item_name": 'Metal Ingot',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Metal', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "description": 'A refined gold ingot. Shiny and valuable.',
        "durability": None,
        "icon": 'GoldIngot.png',
        "item_name": 'Gold Ingot',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Raw Gold', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "description": 'Clear glass. Made from melted sand.',
        "durability": None,
        "icon": 'Glass.png',
        "item_name": 'Glass',
        "output_amount": 5,
        "placeable": False,
        "recipe": [{'item': 'Bucket of Sand', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A hearty mushroom stew. Warm and filling.',
        "durability": None,
        "icon": 'MushroomStew.png',
        "item_name": 'Mushroom Stew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Mushroom', 'amount': 3}, {'item': 'Small Water', 'amount': 1}, {'item': 'Wooden Bowl', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'mushroom'],
        "type": 'consumable',
        "use_effect": 'player.hunger += 20',
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'Strong rope twisted from twine. Very useful.',
        "durability": None,
        "icon": 'Rope.png',
        "item_name": 'Rope',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Twine', 'amount': 5}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'Simple twine woven from plant fibers.',
        "durability": None,
        "icon": 'Twine.png',
        "item_name": 'Twine',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Fiber', 'amount': 4}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A compact ball of twine. Easy to store. Distracting for cats',
        "durability": None,
        "icon": 'BallOfTwine.png',
        "item_name": 'Ball Of Twine',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Twine', 'amount': 10}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A fire-starting tool. Strikes sparks reliably.',
        "durability": 50,
        "icon": 'FlintAndSteel.png',
        "item_name": 'Flint And Steel',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Flint', 'amount': 1}, {'item': 'Metal Ingot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['tool'],
        "type": 'tool',
        "use_effect": 'start_fire',
        "weight": 1.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A simple torch. Provides light in darkness.',
        "durability": 300,
        "held_item_frames": {'left': 'Torch1.png', 'right': 'Torch1.png', 'up': 'Torch1.png', 'down': 'Torch1.png'},
        "held_item_offset": {'left': (5, 18), 'right': (15, 18), 'up': (13, 10), 'down': (0, 18)},
        "icon": 'Torch.png',
        "item_name": 'Torch',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Sticks', 'amount': 5}, {'item': 'Flint', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['tool'],
        "type": 'tool',
        "use_effect": 'provide_light; provide_warmth',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'Fresh squeezed orange juice. Refreshing!',
        "durability": None,
        "icon": 'SmallOrangeJuice.png',
        "item_name": 'Small Orange Juice',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Oranges', 'amount': 3}, {'item': 'Wooden Cup', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'consumable'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 20; player.hunger += 2',
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A simple wooden bowl. Holds food and liquids.',
        "durability": None,
        "icon": 'WoodenBowl.png',
        "item_name": 'Wooden Bowl',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'wood', 'amount': 2}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['wooden', 'material'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A carved wooden cup. Perfect for drinking.',
        "durability": None,
        "icon": 'WoodenCup.png',
        "item_name": 'Wooden Cup',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'wood', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['wooden', 'material', 'container'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A sturdy workbench. Enables advanced crafting.',
        "durability": None,
        "icon": 'Workbench.png',
        "item_name": 'Workbench',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item_tag': 'wood', 'amount': 25}, {'item': 'Stone', 'amount': 7}, {'item': 'Metal Ingot', 'amount': 10}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 30
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A simple campfire. Used for cooking, light, and warmth.',
        "durability": None,
        "icon": 'Campfire.png',
        "item_name": 'Campfire',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Stone', 'amount': 6}, {'item': 'Sticks', 'amount': 10}, {'item': 'Flint', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'An oil lamp burning brightly. Provides steady light.',
        "durability": 600,
        "icon": 'OilLamp.png',
        "item_name": 'Oil Lamp',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Empty Oil Lamp', 'amount': 1}, {'item_tag': 'oil', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['tool'],
        "type": 'tool',
        "use_effect": 'provide_light; provide_warmth',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": 'Pressed olive oil in a small container.',
        "durability": None,
        "icon": 'SmallOliveOil.png',
        "item_name": 'Small Olive Oil',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Olives', 'amount': 5}, {'item': 'Wooden Cup', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": 'player.thirst += 2',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": "A thick and viscous liquid that keeps water out of where it's not wanted, and keeps it in where it's enslaved. I wouldn't it this if I were you.",
        "durability": None,
        "icon": 'SealingPaste.png',
        "item_name": 'Sealing Paste',
        "output_amount": 20,
        "placeable": False,
        "recipe": [{'item': 'Stone', 'amount': 1}, {'item_tag': 'oil', 'amount': 1}, {'item': 'Fiber', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": 'player.health -= 50; player.poison = True; player.poison_time = 10; player.poison_strength += 3',
        "weight": 0.1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": 'A small healing potion. Restores some health.',
        "durability": None,
        "icon": 'SmallHealthBrew.png',
        "item_name": 'Small Health Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Blood Berries', 'amount': 10}, {'item': 'Vio Berries', 'amount': 2}, {'item': 'Small Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.health += 30',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": 'A small stamina potion. Restores some stamina.',
        "durability": None,
        "icon": 'SmallStaminaBrew.png',
        "item_name": 'Small Stamina Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Fiber', 'amount': 10}, {'item': 'Twilight Drupes', 'amount': 3}, {'item': 'Small Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.stamina += 30',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": "A glowing brew. Is your skin... shiny? That's natural, I promise.",
        "durability": None,
        "icon": 'SmallBrightBrew.png',
        "item_name": 'Small Bright Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Dawn Berries', 'amount': 10}, {'item': 'Dawnshroom', 'amount': 2}, {'item': 'Small Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.glow = True; player.glow_time = 300',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": 'A cooling brew. Provides resistance to heat.',
        "durability": None,
        "icon": 'SmallChillBrew.png',
        "item_name": 'Small Chill Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Teal Berries', 'amount': 10}, {'item': 'Frost Fern Leaf', 'amount': 2}, {'item': 'Small Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.temp_heat_resistance_increase +=.1; player.temp_heat_resistance_timer += 50',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'mortar_and_pestle',
        "description": 'A warming brew. Provides resistance to cold.',
        "durability": None,
        "icon": 'SmallHeatBrew.png',
        "item_name": 'Small Heat Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Sun Berries', 'amount': 10}, {'item': 'Fire Fern Leaf', 'amount': 2}, {'item': 'Small Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.temp_cold_resistance +=.1; player.temp_cold_resistance_timer += 50',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A mystical, valuable, and powerful coin. Grants a second chance at life.... or nine',
        "durability": None,
        "icon": 'ResurrectionCoin.png',
        "item_name": 'Resurrection Coin',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 5}, {'item': 'Diamond', 'amount': 1}, {'item': 'Ruby', 'amount': 1}, {'item': 'Emerald', 'amount': 1}, {'item': 'Sapphire', 'amount': 1}, {'item': 'Garnet', 'amount': 1}, {'item': 'Aquamarine', 'amount': 1}, {'item': 'Topaz', 'amount': 1}, {'item': 'Amethyst', 'amount': 1}, {'item': 'Opal', 'amount': 1}, {'item': 'Pearl', 'amount': 1}, {'item': 'Duskwood', 'amount': 1}],
        "smeltable": False,
        "stack_size": 10,
        "tags": ['item'],
        "type": 'special',
        "use_effect": 'player.resurrect',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A balanced throwing knife. Flies true.',
        "durability": None,
        "icon": 'ThrowingKnife.png',
        "item_name": 'Throwing Knife',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 1}, {'item': 'Hide', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['item'],
        "type": 'weapon',
        "use_effect": 'ranged_attack',
        "weight": 0.5
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A sharp throwing star. Deadly when thrown.',
        "durability": None,
        "icon": 'ThrowingStar.png',
        "item_name": 'Throwing Star',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 2}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['item'],
        "type": 'weapon',
        "use_effect": 'ranged_attack',
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An empty oil lamp. Needs oil to function.',
        "durability": None,
        "icon": 'EmptyOilLamp.png',
        "item_name": 'Empty Oil Lamp',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Stone', 'amount': 5}, {'item': 'Fiber', 'amount': 1}, {'item': 'Flint', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 0.8
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A small metal ring. Simple but functional. Adorn with your favorite gemstone. Or don't. Your choice. Gemstones would be a lot cooler though.",
        "durability": None,
        "icon": 'SmallMetalRing.png',
        "item_name": 'Small Metal Ring',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 1}, {'item': 'Hide', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 0.7
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A small gold ring. Elegant and valuable. Slap a cool rock in there for varying effects.',
        "durability": None,
        "icon": 'SmallGoldRing.png',
        "item_name": 'Small Gold Ring',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 1}, {'item': 'Hide', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 0.6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A sturdy metal ring. Well-crafted. Much more room for activities. Like 3 times as much room. And gems. But mostly activities.',
        "durability": None,
        "icon": 'MetalRing.png',
        "item_name": 'Metal Ring',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 2}, {'item': 'Small Metal Ring', 'amount': 1}, {'item': 'Duskwretch Claws', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A gold ring with a spot for not one, not two, but three whole gemstones. Quite fancy.',
        "durability": None,
        "icon": 'GoldRing.png',
        "item_name": 'Gold Ring',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 2}, {'item': 'Small Gold Ring', 'amount': 1}, {'item': 'Goat Horns', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A small metal chain of tiny metal hoops. Perfect for fine jewelry. Or hula-hopping if you're the size of a cricket.",
        "durability": None,
        "icon": 'MetalChain.png',
        "item_name": 'Metal Chain',
        "output_amount": 5,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "Ring, ring, ring, ring, ring, ring, ring.... it's a chain made of gold rings.",
        "durability": None,
        "icon": 'GoldChain.png',
        "item_name": 'Gold Chain',
        "output_amount": 5,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A small metal amulet. May hold power. In the form of gems. That's it. That's the power. Go get yourself some gems. Try looking in some weird-looking rocks or something.",
        "durability": None,
        "icon": 'SmallMetalAmulet.png',
        "item_name": 'Small Metal Amulet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 2}, {'item': 'Metal Chain', 'amount': 3}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A small gold amulet. Radiates faint energy. Looks super cool though. Trust me, I checked.',
        "durability": None,
        "icon": 'SmallGoldAmulet.png',
        "item_name": 'Small Gold Amulet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 2}, {'item': 'Gold Chain', 'amount': 3}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A medium metal amulet set with some gems. At least it would be if you set it with some gems.',
        "durability": None,
        "icon": 'MediumMetalAmulet.png',
        "item_name": 'Medium Metal Amulet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 2}, {'item': 'Small Metal Amulet', 'amount': 1}, {'item': 'Bone', 'amount': 5}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 1.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A medium gold amulet. Beautifully crafted. Light as a feather. Except for now you have to live with the weight of what you did to those poor avians. You monster.',
        "durability": None,
        "icon": 'MediumGoldAmulet.png',
        "item_name": 'Medium Gold Amulet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 2}, {'item': 'Small Gold Amulet', 'amount': 1}, {'item': 'Feathers', 'amount': 5}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 1.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A large metal amulet. Feels powerful. Becuase it is. Well, it could be... If you stuck some shiny, pretty, precious little gems inside all those holes you made.',
        "durability": None,
        "icon": 'LargeMetalAmulet.png',
        "item_name": 'Large Metal Amulet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 2}, {'item': 'Medium Metal Amulet', 'amount': 1}, {'item': 'Fangs', 'amount': 3}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A large gold amulet. A masterwork of jewelry. I mean, as masterful as you're able to make. So it's probably decent I guess.",
        "durability": None,
        "icon": 'LargeGoldAmulet.png',
        "item_name": 'Large Gold Amulet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Gold Ingot', 'amount': 2}, {'item': 'Medium Gold Amulet', 'amount': 1}, {'item': 'Duskacean Claws', 'amount': 3}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['material', 'ore'],
        "type": 'equipment',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A large cooking pot. Used for making massive stews. Like, huge.',
        "durability": None,
        "icon": 'CookingPot.png',
        "item_name": 'Cooking Pot',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 10}, {'item': 'Campfire', 'amount': 1}, {'item': 'Sticks', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 10
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A stone smelter. Refines raw materials. ',
        "durability": None,
        "icon": 'Smelter.png',
        "item_name": 'Smelter',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Stone', 'amount': 50}, {'item': 'Flint', 'amount': 5}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 50
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An empty cage. Can hold captured animals.',
        "durability": None,
        "icon": 'EmptyCage.png',
        "item_name": 'Empty Cage',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 10}, {'item': 'Metal Chain', 'amount': 3}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 15
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An alchemy bench. Used for brewing potions.',
        "durability": None,
        "icon": 'AlchemyBench.png',
        "item_name": 'Alchemy Bench',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Dusk Wood', 'amount': 15}, {'item': 'Oak Wood', 'amount': 10}, {'item': 'Stone', 'amount': 10}, {'item': 'Glass Bottle', 'amount': 3}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 30
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A wooden fence section. Marks boundaries. Can keep things in or out. Of what? That's for you to decide.",
        "durability": None,
        "icon": 'Fence.png',
        "item_name": 'Fence',
        "output_amount": 2,
        "placeable": True,
        "recipe": [{'item_tag': 'wood', 'amount': 5}, {'item': 'Sticks', 'amount': 10}, {'item': 'Rope', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A storage chest. Holds many items safely.',
        "durability": None,
        "icon": 'Chest.png',
        "item_name": 'Chest',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item_tag': 'wood', 'amount': 8}, {'item': 'Metal Ingot', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 10
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A portable tent. Provides shelter anywhere. Except for underwater. Or space. Or in lava.',
        "durability": None,
        "icon": 'Tent.png',
        "item_name": 'Tent',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Hide', 'amount': 30}, {'item': 'Rope', 'amount': 5}, {'item': 'Sticks', 'amount': 10}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['item'],
        "type": 'structure',
        "use_effect": None,
        "weight": 15
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An empty glass bottle. Can hold liquids a lot better than your hands.',
        "durability": None,
        "icon": 'GlassBottle.png',
        "item_name": 'Glass Bottle',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Glass', 'amount': 2}, {'item': 'Sealing Paste', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material', 'container'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A bright lantern. Lights up large areas. Impervious to inclement weather. I think that means it won't go out in the rain. The wicked witch of the west doesn't do that either. I think that means she's impervious to inclement weather. Just kidding, it's becasue she's dead.",
        "durability": 1000,
        "icon": 'Lantern.png',
        "item_name": 'Lantern',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 4}, {'item': 'Glass', 'amount': 4}, {'item': 'Torch', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['tool'],
        "type": 'tool',
        "use_effect": 'provide_light; provide_heat',
        "weight": 3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A mortar and pestle. Grinds ingredients for alchemy. Rock and roll, baby.',
        "durability": None,
        "icon": 'MortarAndPestle.png',
        "item_name": 'Mortar And Pestle',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Stone', 'amount': 25}, {'item': 'Hide', 'amount': 10}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool'],
        "type": 'tool',
        "use_effect": None,
        "weight": 20
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A sturdy metal bucket. Carries water and milk and possibly some other things but I've never tried it. Try it out I guess..",
        "durability": 100,
        "icon": 'MetalBucket.png',
        "item_name": 'Metal Bucket',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Rope', 'amount': 1}, {'item': 'Metal Ingot', 'amount': 5}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore', 'container', 'metal_container'],
        "type": 'tool',
        "use_effect": 'collect_liquid',
        "weight": 5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": "A fishing pole. Catch fish from rivers and ponds. Gotta catch 'em... most of 'em, because copyright laws are a thing.",
        "durability": 500,
        "icon": 'FishingPole.png',
        "item_name": 'Fishing Pole',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Twine', 'amount': 5}, {'item': 'Sticks', 'amount': 5}, {'item': 'Metal Ingot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['food', 'meat'],
        "type": 'tool',
        "use_effect": 'catch_fish',
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A fishing pole. Catch fish from rivers and ponds BUT WITH METAL.',
        "durability": 2000,
        "icon": 'FishingPole.png',
        "item_name": 'Metal Fishing Pole',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Twine', 'amount': 5}, {'item': 'Metal Ingot', 'amount': 6}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['food', 'meat'],
        "type": 'tool',
        "use_effect": 'catch_fish',
        "weight": 5
    },
    {
        "attack_frame_data": {'right': [{'offset': (7, 0), 'rotation': 45}, {'offset': (-7, -16), 'rotation': 135}, {'offset': (30, 4), 'rotation': 90}, {'offset': (16, 5), 'rotation': 45}], 'left': [{'offset': (0, 0), 'rotation': 45}, {'offset': (14, -16), 'rotation': 135}, {'offset': (-8, 0), 'rotation': 90}, {'offset': (-9, 6), 'rotation': 45}], 'up': [{'offset': (8, 11), 'rotation': -5}, {'offset': (5, 3), 'rotation': -10}, {'offset': (9, 17), 'rotation': 2}, {'offset': (13, 20), 'rotation': 0}], 'down': [{'offset': (-2, 4), 'rotation': -5}, {'offset': (2, -1), 'rotation': -10}, {'offset': (0, 20), 'rotation': 2}, {'offset': (2, 16), 'rotation': 0}]},
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A sturdy metal axe. Perfect for chopping wood and solving problems.',
        "durability": 5000,
        "held_item_frames": {'left': 'MetalAxeRightHeld.png', 'right': 'MetalAxeRightHeld.png', 'up': 'MetalAxeUpHeld.png', 'down': 'MetalAxeDownHeld.png'},
        "held_item_offset": {'left': (5, 21), 'right': (15, 21), 'up': (13, 20), 'down': (0, 20)},
        "icon": 'MetalAxe.png',
        "item_name": 'Metal Axe',
        "movement_frame_data": {'right': [{'offset': (15, 21), 'rotation': 2}, {'offset': (21, 18), 'rotation': 7}, {'offset': (17, 3), 'rotation': 45}, {'offset': (21, 18), 'rotation': 7}, {'offset': (15, 21), 'rotation': 0}, {'offset': (11, 21), 'rotation': 0}, {'offset': (7, 21), 'rotation': 0}, {'offset': (11, 21), 'rotation': 0}], 'left': [{'offset': (5, 21), 'rotation': 0}, {'offset': (9, 21), 'rotation': 2}, {'offset': (11, 21), 'rotation': 4}, {'offset': (9, 21), 'rotation': 2}, {'offset': (5, 21), 'rotation': 0}, {'offset': (-5, 16), 'rotation': -9}, {'offset': (-13, 2), 'rotation': -45}, {'offset': (-5, 16), 'rotation': -9}], 'up': [{'offset': (13, 20), 'rotation': 0}, {'offset': (9, 17), 'rotation': 2}, {'offset': (8, 11), 'rotation': 5}, {'offset': (9, 17), 'rotation': 2}, {'offset': (13, 20), 'rotation': 0}, {'offset': (9, 17), 'rotation': 2}, {'offset': (8, 15), 'rotation': 5}, {'offset': (9, 17), 'rotation': 2}], 'down': [{'offset': (0, 20), 'rotation': 0}, {'offset': (1, 18), 'rotation': -5}, {'offset': (3, 16), 'rotation': 0}, {'offset': (1, 18), 'rotation': 5}, {'offset': (0, 20), 'rotation': 0}, {'offset': (1, 18), 'rotation': -5}, {'offset': (3, 16), 'rotation': 0}, {'offset': (1, 18), 'rotation': 5}]},
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 8}, {'item_tag': 'wood', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool', 'weapon'],
        "type": 'tool',
        "use_effect": None,
        "weight": 8
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": "It's a bucket... with sand in it... I call it a bucket of sand.",
        "durability": None,
        "icon": 'SandBucket.png',
        "item_name": 'Bucket of Sand',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Bucket', 'amount': 1}],
        "smeltable": True,
        "stack_size": 100,
        "tags": ['item'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 3
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'Fresh water in a small cup. Quenches thirst.',
        "durability": None,
        "icon": 'SmallWater.png',
        "item_name": 'Small Water',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Wooden Cup', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'consumable'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 15',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": "Fresh milk in a small cup. Unless you're the size of a pea. Then it's a ginormous cup. Way too big for one little pea-sized guy or gal to drink. Creamy and nutritious.",
        "durability": None,
        "icon": 'SmallMilk.png',
        "item_name": 'Small Milk',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Wooden Cup', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'consumable'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 12; player.hunger += 3',
        "weight": 0.7
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": "Water in a medium glass bottle. Very refreshing. So refreshing. You'll feel so refreshed.",
        "durability": None,
        "icon": 'MediumGlassWater.png',
        "item_name": 'Medium Glass Water',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Glass Bottle', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'consumable'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 50',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": "Milk in a medium glass bottle. Rich and filling. Whether cow or coconut, you'll be craving the goods.",
        "durability": None,
        "icon": 'MediumGlassMilk.png',
        "item_name": 'Medium Glass Milk',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Glass Bottle', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'consumable'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 40; player.hunger += 10',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'Orange juice in a medium bottle. Tangy and sweet.',
        "durability": None,
        "icon": 'MediumGlassOrangeJuice.png',
        "item_name": 'Medium Glass Orange Juice',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Oranges', 'amount': 5}, {'item': 'Glass Bottle', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'consumable'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 35; player.hunger += 10; player.stamina += 20',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'Anti-thirst in a large metal canteen. Lasts a long time.',
        "durability": None,
        "icon": 'LargeMetalWater.png',
        "item_name": 'Large Metal Water',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Large Metal Canteen', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 100',
        "weight": 2
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'Cow sauce in a large metal canteen. Very satisfying.',
        "durability": None,
        "icon": 'LargeMetalMilk.png',
        "item_name": 'Large Metal Milk',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Large Metal Canteen', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 80; player.hunger += 20',
        "weight": 2
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'Orange juice in a large canteen. Packed with flavor.',
        "durability": None,
        "icon": 'LargeMetalOrangeJuice.png',
        "item_name": 'Large Metal Orange Juice',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Oranges', 'amount': 8}, {'item': 'Large Metal Canteen', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'consumable',
        "use_effect": 'player.thirst += 60; player.hunger += 15; player.stamina += 40',
        "weight": 2
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'Olive oil in a medium glass bottle. Perfect for fuel refills.',
        "durability": None,
        "icon": 'MediumGlassOliveOil.png',
        "item_name": 'Medium Glass Olive Oil',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Olives', 'amount': 15}, {'item': 'Glass Bottle', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['crafted', 'material'],
        "type": 'crafted_material',
        "use_effect": 'player.thirst += 5',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": "Olive oil in a large metal canteen. All of the oil's in a large metal canteen. I love oil straight from the canteen made of metal. I'll live better knowing I have my metal canteen of oil pressed from all of the olives of all of the olive trees.",
        "durability": None,
        "icon": 'LargeMetalOliveOil.png',
        "item_name": 'Large Metal Olive Oil',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Olives', 'amount': 20}, {'item': 'Large Metal Canteen', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'crafted_material',
        "use_effect": 'player.thirst += 10',
        "weight": 2
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A medium healing potion. Restores substantial health.',
        "durability": None,
        "icon": 'MediumGlassHealthBrew.png',
        "item_name": 'Medium Glass Health Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Blood Berries', 'amount': 15}, {'item': 'Vio Berries', 'amount': 4}, {'item': 'Medium Glass Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.health += 80',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A medium stamina potion. Restores substantial stamina.',
        "durability": None,
        "icon": 'MediumGlassStaminaBrew.png',
        "item_name": 'Medium Glass Stamina Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Fiber', 'amount': 15}, {'item': 'Twilight Drupes', 'amount': 4}, {'item': 'Medium Glass Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.stamina += 80',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A glowing brew. Provides extended glowy-glowyness.',
        "durability": None,
        "icon": 'MediumGlassBrightBrew.png',
        "item_name": 'Medium Glass Bright Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Dawn Berries', 'amount': 15}, {'item': 'Dawnshroom', 'amount': 4}, {'item': 'Medium Glass Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.glow = True; player.glow_time = 1000',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A cooling brew. Provides exxtteeeended heat resistance.',
        "durability": None,
        "icon": 'MediumGlassChillBrew.png',
        "item_name": 'Medium Glass Chill Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Teal Berries', 'amount': 15}, {'item': 'Frost Fern Leaf', 'amount': 4}, {'item': 'Medium Glass Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.temp_heat_resistance_increase +=.3; player.temp_heat_resistance_timer += 200',
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A warming tasty bev. Provides extended cold resistance.',
        "durability": None,
        "icon": 'MediumGlassHeatBrew.png',
        "item_name": 'Medium Glass Heat Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Sun Berries', 'amount': 15}, {'item': 'Fire Fern Leaf', 'amount': 4}, {'item': 'Medium Glass Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['potion', 'consumable'],
        "type": 'potion',
        "use_effect": 'player.temp_cold_resistance_increase +=.3; player.temp_cold_resistance_timer += 200',
        "weight": 1.4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A large empty metal canteen. Holds lots of liquid. This baby can hold a LOT of liquids. Not as much as a cooking pot, but like, a lot.',
        "durability": None,
        "icon": 'LargeMetalCanteen.png',
        "item_name": 'Large Metal Canteen',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 10}, {'item': 'Sealing Paste', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore', 'container'],
        "type": 'crafted_material',
        "use_effect": None,
        "weight": 1.4
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A large healing potion. Restores to full health.',
        "durability": None,
        "icon": 'LargeMetalHealthBrew.png',
        "item_name": 'Large Metal Health Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Blood Berries', 'amount': 30}, {'item': 'Vio Berries', 'amount': 10}, {'item': 'Duskshroom', 'amount': 2}, {'item': 'Large Metal Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'potion',
        "use_effect": 'player.health = player.max_health',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A large stamina potion. Restores to full stamina.',
        "durability": None,
        "icon": 'LargeMetalStaminaBrew.png',
        "item_name": 'Large Metal Stamina Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Sun Berries', 'amount': 30}, {'item': 'Twilight Drupes', 'amount': 10}, {'item': 'Dawn Berries', 'amount': 5}, {'item': 'Large Metal Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'potion',
        "use_effect": 'player.stamina = player.max_stamina',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": "A glowing brew. It's a glow up for you. Or maybe this drink just gives everyone else bad eyesight...",
        "durability": None,
        "icon": 'LargeMetalBrightBrew.png',
        "item_name": 'Large Metal Bright Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Dawn Berries', 'amount': 30}, {'item': 'Dawnshroom', 'amount': 10}, {'item': 'Sun Berries', 'amount': 5}, {'item': 'Large Metal Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'potion',
        "use_effect": 'player.glow = True; player.glow_time = 3000',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'A suuuuuper chill cooling brew. Provides long-lasting heat resistance.',
        "durability": None,
        "icon": 'LargeMetalChillBrew.png',
        "item_name": 'Large Metal Chill Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Teal Berries', 'amount': 30}, {'item': 'Frost Fern Leaf', 'amount': 10}, {'item': 'Duskshroom', 'amount': 5}, {'item': 'Large Metal Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'potion',
        "use_effect": 'player.temp_heat_resistance_increase +=.6; player.temp_heat_resistance_timer += 500',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'alchemy_bench',
        "description": 'An exceedingly warming brew. Provides long-lasting cold resistance.',
        "durability": None,
        "icon": 'LargeMetalHeatBrew.png',
        "item_name": 'Large Metal Heat Brew',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Sun Berries', 'amount': 30}, {'item': 'Fire Fern Leaf', 'amount': 10}, {'item': 'Dusk Berries', 'amount': 5}, {'item': 'Large Metal Water', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'ore'],
        "type": 'potion',
        "use_effect": 'player.temp_cold_resistance_increase +=.6; player.temp_cold_resistance_timer += 500',
        "weight": 1
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'Fresh water collected from a pond or lake or stream. Can be used for drinking or cooking.',
        "durability": None,
        "icon": 'Waterbucket.png',
        "item_name": 'Waterbucket',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['liquid', 'water', 'consumable'],
        "type": 'raw_material',
        "use_effect": 'player.thirst += 100',
        "weight": 10
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'Molten lava collected from a lava pond or stream or river or lake. Extremely hot and dangerous. Used for something, probably.',
        "durability": None,
        "icon": 'Lavabucket.png',
        "item_name": 'Lavabucket',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['liquid', 'lava', 'material'],
        "type": 'raw_material',
        "use_effect": 'player.is_alive = False; player.health = 0',
        "weight": 10
    },
    {
        "cat_object": None,
        "cat_type": 'black',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed black cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/BlackCatRightStanding.png',
        "item_name": 'Tamed Black Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'salt_and_pepper',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed salt and pepper cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/SandPCatRightStanding.png',
        "item_name": 'Tamed Salt and Pepper Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'white',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed white cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/WhiteCatRightStanding.png',
        "item_name": 'Tamed White Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'white_and_black',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed black and white cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/WandBCatRightStanding.png',
        "item_name": 'Tamed Black and White Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'sandy',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed sandy cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/SandyCatRightStanding.png',
        "item_name": 'Tamed Sandy Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'orange',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed orange cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/OrangeCatRightStanding.png',
        "item_name": 'Tamed Orange Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'calico',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed calico cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/CalicoCatRightStanding.png',
        "item_name": 'Tamed Calico Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'gray',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed gray cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/GrayCatRightStanding.png',
        "item_name": 'Tamed Gray Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "cat_object": None,
        "cat_type": 'white_and_orange',
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A tamed orange and white cat companion. Loyal and ready to fight.',
        "durability": None,
        "icon": 'assets/sprites/mobs/WandOCatRightStanding.png',
        "item_name": 'Tamed Orange and White Cat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 1,
        "tags": ['pet', 'tamed_cat'],
        "type": 'pet',
        "use_effect": None,
        "weight": 5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Nailed it. A sturdy metal nail. Used in various building recipes.',
        "durability": None,
        "icon": 'MetalNail.png',
        "item_name": 'Metal Nail',
        "output_amount": 15,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material', 'metal'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 0.01
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A pointy, pointy arrow. Perfect for poking people super hard from really far away.',
        "durability": None,
        "icon": 'Arrow.png',
        "item_name": 'Arrow',
        "output_amount": 3,
        "placeable": False,
        "recipe": [{'item': 'Flint', 'amount': 1}, {'item': 'Sticks', 'amount': 1}, {'item': 'Feathers', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['weapon', 'projectile'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A rare lotus flower with ashy petals. Prized for crafting. Craft for a prize.',
        "durability": None,
        "icon": 'AshLotus.png',
        "item_name": 'Ash Lotus',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['plant', 'material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": "A bird's egg. Either the period or the offspring of one of our fine feathered friends. Can be cooked or used in crafting.",
        "durability": None,
        "icon": 'BirdEgg.png',
        "item_name": 'Bird Egg',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['egg', 'food'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A throwing weapon made of rope and weights. Effective for controlling enemies. Kinky.',
        "durability": None,
        "icon": 'Bola.png',
        "item_name": 'Bola',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Rope', 'amount': 3}, {'item': 'Stone', 'amount': 3}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['weapon', 'throwing'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 0.8
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'Mortar and Pestle',
        "description": "Ground bone powder. Not from the ground. It has been ground. Not as in it used to be ground, but like... it's bone that has been all ground up. Useful for various crafting recipes, probably.",
        "durability": None,
        "icon": 'BonePowder.png',
        "item_name": 'Bone Powder',
        "output_amount": 2,
        "placeable": False,
        "recipe": [{'item': 'Bone', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'powder'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An upgraded bola with metal chains. More effective and durable and freakishly heavy. Good luck throwing one of these.',
        "durability": None,
        "icon": 'ChainBola.png',
        "item_name": 'Chain Bola',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 3}, {'item': 'Metal Chain', 'amount': 3}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['weapon', 'throwing'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 1.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'Hard shelly chitin. Used in advanced crafting.',
        "durability": None,
        "icon": 'Chitin.png',
        "item_name": 'Chitin',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'insect'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A scale from a dusk dragon. Mystical and powerful.',
        "durability": None,
        "icon": 'DuskDragonScale.png',
        "item_name": 'Dusk Dragon Scale',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['dragon', 'material', 'scale'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'An egg from a mysterious dusk creature. Possibly Nutritious?',
        "durability": None,
        "icon": 'DuskEgg.png',
        "item_name": 'Dusk Egg',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['egg'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A scale from an electric dragon. Crackles with energy.',
        "durability": None,
        "icon": 'ElectricDragonScale.png',
        "item_name": 'Electric Dragon Scale',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['dragon', 'material', 'scale'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": "An empty waterskin. Can be filled with water. It's called a WATERskin, not a milkskin or a potionskin. Don't even try it.",
        "durability": None,
        "icon": 'Waterskin.png',
        "item_name": 'Waterskin',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 2}, {'item': 'Fiber', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['container'],
        "type": 'container',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "description": 'A sturdy ceramic pot. Can be used to make explosive bombs. Or flower containers. The bold and the beautiful.',
        "durability": None,
        "icon": 'CeramicPot.png',
        "item_name": 'Ceramic Pot',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Clay', 'amount': 5}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['decoration', 'clay'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 0.6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An explosive bomb filled with fire. Dangerous and effective.',
        "durability": None,
        "icon": 'FireBomb.png',
        "item_name": 'Fire Bomb',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Fire Material', 'amount': 2}, {'item': 'Sealing Paste', 'amount': 2}, {'item': 'Twine', 'amount': 1}, {'item': 'Ceramic Pot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['weapon', 'explosive'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 0.6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'An explosive bomb filled with Ice. Dangerous and effective.',
        "durability": None,
        "icon": 'IceBomb.png',
        "item_name": 'Ice Bomb',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Ice Material', 'amount': 2}, {'item': 'Sealing Paste', 'amount': 2}, {'item': 'Twine', 'amount': 1}, {'item': 'Ceramic Pot', 'amount': 1}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['weapon', 'explosive'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 0.6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'An egg from a fire dragon. Radiates intense heat.',
        "durability": None,
        "icon": 'FireDragonEgg.png',
        "item_name": 'Fire Dragon Egg',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['egg', 'dragon'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A scale from a fire dragon. Hot to the touch.',
        "durability": None,
        "icon": 'FireDragonScale.png',
        "item_name": 'Fire Dragon Scale',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['dragon', 'material', 'scale', 'Fire Material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden flute. Can be played to produce soothing sounds and gather your peeps. Very intricate, requires great skill and tools when crafting.',
        "durability": 300,
        "icon": 'Flute.png',
        "item_name": 'Flute',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Wood', 'amount': 1}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool', 'instrument'],
        "type": 'tool',
        "use_effect": None,
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A scale from an ice dragon. Cold to the touch.',
        "durability": None,
        "icon": 'IceDragonScale.png',
        "item_name": 'Ice Dragon Scale',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['dragon', 'material', 'scale', 'Ice Material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A horn from an inferno beast. Burns with inner fire.',
        "durability": None,
        "icon": 'InfernoHorn.png',
        "item_name": 'Inferno Horn',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'horn', 'Fire Material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Protective leather boots. Provides moderate defense.',
        "durability": 500,
        "icon": 'LeatherBoots.png',
        "item_name": 'Leather Boots',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 15}, {'item': 'Twine', 'amount': 10}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['armor', 'leather'],
        "type": 'armor',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Protective leather chestplate. Provides moderate defense.',
        "durability": 600,
        "icon": 'LeatherChestplate.png',
        "item_name": 'Leather Chestplate',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 25}, {'item': 'Twine', 'amount': 15}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['armor', 'leather'],
        "type": 'armor',
        "use_effect": None,
        "weight": 4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Protective leather gloves. Provides light defense.',
        "durability": 400,
        "icon": 'LeatherGloves.png',
        "item_name": 'Leather Gloves',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 12}, {'item': 'Twine', 'amount': 6}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['armor', 'leather'],
        "type": 'armor',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Protective leather helmet. Provides light to moderate defense.',
        "durability": 450,
        "icon": 'LeatherHelmet.png',
        "item_name": 'Leather Helmet',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 10}, {'item': 'Twine', 'amount': 6}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['armor', 'leather'],
        "type": 'armor',
        "use_effect": None,
        "weight": 1.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Protective leather leggings. Provides moderate defense.',
        "durability": 550,
        "icon": 'LeatherLeggings.png',
        "item_name": 'Leather Leggings',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 18}, {'item': 'Twine', 'amount': 12}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['armor', 'leather'],
        "type": 'armor',
        "use_effect": None,
        "weight": 2.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'An egg from a lizard. Warm and white.',
        "durability": None,
        "icon": 'LizardEgg.png',
        "item_name": 'Lizard Egg',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['egg'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A reed from a marsh. Flexible and useful for crafting.',
        "durability": None,
        "icon": 'MarshReed.png',
        "item_name": 'Marsh Reed',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['plant', 'material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.15
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal floor tile. Used for building and construction.',
        "durability": None,
        "icon": 'MetalFloor.png',
        "item_name": 'Metal Floor',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 10}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal hoe. Perfect for tilling soil.',
        "durability": 1000,
        "icon": 'MetalHoe.png',
        "item_name": 'Metal Hoe',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 2}, {'item': 'Stick', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool', 'farming'],
        "type": 'tool',
        "use_effect": None,
        "weight": 3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal ladder. Used for climbing and construction.',
        "durability": None,
        "icon": 'MetalLadder.png',
        "item_name": 'Metal Ladder',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 12}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A heavy metal mace. Excellent for crushing enemies.',
        "durability": 800,
        "icon": 'MetalMace.png',
        "item_name": 'Metal Mace',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 5}, {'item': 'Stick', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'melee'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal pickaxe. Essential for mining ore and stone.',
        "durability": 1200,
        "icon": 'MetalPickaxe.png',
        "item_name": 'Metal Pickaxe',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 6}, {'item': 'Stick', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool', 'mining'],
        "type": 'tool',
        "use_effect": None,
        "weight": 5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal shovel. Great for digging.',
        "durability": 1000,
        "icon": 'MetalShovel.png',
        "item_name": 'Metal Shovel',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 4}, {'item': 'Stick', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool', 'digging'],
        "type": 'tool',
        "use_effect": None,
        "weight": 4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal spear. Effective for ranged melee combat.',
        "durability": 700,
        "icon": 'MetalSpear.png',
        "item_name": 'Metal Spear',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 4}, {'item': 'Stick', 'amount': 6}, {'item': 'Twine', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'melee'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Metal stairs. Used for building and construction.',
        "durability": None,
        "icon": 'MetalStairs.png',
        "item_name": 'Metal Stairs',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Metal Ingot', 'amount': 25}, {'item': 'Metal Nail', 'amount': 15}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 30
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A metal sword. A classic melee weapon.',
        "durability": 800,
        "icon": 'MetalSword.png',
        "item_name": 'Metal Sword',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Metal Ingot', 'amount': 8}, {'item': 'Stick', 'amount': 2}, {'item': 'Hide', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'melee'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 3
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'A bucket of fresh milk. Nutritious and useful.',
        "durability": None,
        "icon": 'MilkBucket.png',
        "item_name": 'Milk Bucket',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 10,
        "tags": ['food', 'container'],
        "type": 'container',
        "use_effect": 'player.hunger += 20; player.thirst += 70',
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Meat from a monster. Is probably fine to eat.',
        "durability": None,
        "icon": 'MonsterMeat.png',
        "item_name": 'Monster Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Oak wood stairs. Strong and reliable for building.',
        "durability": None,
        "icon": 'OakWoodStairs.png',
        "item_name": 'Oak Wood Stairs',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'OakWood', 'amount': 25}, {'item': 'Metal Nail', 'amount': 15}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material', 'wood'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 25
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A shard of obsidian. Sharp and useful for crafting.',
        "durability": None,
        "icon": 'ObsidianShard.png',
        "item_name": 'Obsidian Shard',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A feather from a phoenix. Glows with inner flame.',
        "durability": None,
        "icon": 'PhoenixFeather.png',
        "item_name": 'Phoenix Feather',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'feather', 'Fire Material'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A scale from a poison dragon. Toxic and powerful.',
        "durability": None,
        "icon": 'PoisonDragonScale.png',
        "item_name": 'Poison Dragon Scale',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['dragon', 'material', 'scale'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A rope ladder. Portable and useful for climbing.',
        "durability": None,
        "icon": 'RopeLadder.png',
        "item_name": 'Rope Ladder',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Twine', 'amount': 10}, {'item': 'Rope', 'amount': 12}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'Salt. Contains: Salt. Used for preservation and cooking.',
        "durability": None,
        "icon": 'Salt.png',
        "item_name": 'Salt',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'food'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": True,
        "cookable": True,
        "crafting_medium": None,
        "description": 'Meat from a sea creature. Exotic and flavorful.',
        "durability": None,
        "icon": 'SeaMeat.png',
        "item_name": 'Sea Meat',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['food', 'meat'],
        "type": 'raw_material',
        "use_effect": 'player.hunger -= 3',
        "weight": 0.6
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A packed ball of snow. Can be thrown for damage or just for funsies.',
        "durability": None,
        "icon": 'Snowball.png',
        "item_name": 'Snowball',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['weapon', 'throwing'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 0.2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden club with spikes. More effective than a regular club.',
        "durability": 600,
        "icon": 'SpikedWoodenClub.png',
        "item_name": 'Spiked Wooden Club',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Wooden Club', 'amount': 1}, {'item': 'Metal Nail', 'amount': 10}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'melee'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A stone floor tile. Durable and looks solid.',
        "durability": None,
        "icon": 'StoneFloor.png',
        "item_name": 'Stone Floor',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Stone', 'amount': 10}, {'item': 'Clay', 'amount': 4}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'Stone stairs. Sturdy and reliable.',
        "durability": None,
        "icon": 'StoneStairs.png',
        "item_name": 'Stone Stairs',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Stone', 'amount': 25}, {'item': 'Metal Nail', 'amount': 15}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A sturdy cloak for travelers. Provides protection from the elements.',
        "durability": 400,
        "icon": 'TravelersCloak.png',
        "item_name": 'Travelers Cloak',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item': 'Hide', 'amount': 20}, {'item': 'Rope', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['clothing', 'armor'],
        "type": 'clothing',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": None,
        "description": 'A large tusk from a beast. Valuable and useful.',
        "durability": None,
        "icon": 'Tusk.png',
        "item_name": 'Tusk',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 100,
        "tags": ['material', 'bone'],
        "type": 'raw_material',
        "use_effect": None,
        "weight": 0.4
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A well for drawing water. Can be placed pretty much anywhere to get some of that moist, dank water your body so desperately craves.',
        "durability": None,
        "icon": 'WaterWell.png',
        "item_name": 'Water Well',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item': 'Stone', 'amount': 20}, {'item': 'Metal Ingot', 'amount': 2}, {'item': 'Metal Bucket', 'amount': 1}, {'item_tag': 'Wood', 'amount': 10}, {'item': 'Rope', 'amount': 5}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['building', 'water'],
        "type": 'placeable',
        "use_effect": None,
        "weight": 20
    },
    {
        "consumable": True,
        "cookable": False,
        "crafting_medium": 'gameplay',
        "description": 'A waterskin filled with water. Quenches a bit of thirst.',
        "durability": None,
        "icon": 'FilledWaterskin.png',
        "item_name": 'Filled Waterskin',
        "output_amount": 1,
        "placeable": False,
        "recipe": None,
        "smeltable": False,
        "stack_size": 10,
        "tags": ['food', 'container'],
        "type": 'container',
        "use_effect": 'player.thirst += 15',
        "weight": 0.5
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden boat. Useful for traveling across water.',
        "durability": 500,
        "icon": 'WoodBoat.png',
        "item_name": 'Wood Boat',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Wood', 'amount': 20}, {'item': 'Fiber', 'amount': 3}, {'item': 'Sealing Paste', 'amount': 6}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['tool', 'transport'],
        "type": 'tool',
        "use_effect": None,
        "weight": 20
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden bow. Classic ranged weapon.',
        "durability": 400,
        "icon": 'WoodBow.png',
        "item_name": 'Wood Bow',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Wood', 'amount': 5}, {'item': 'Twine', 'amount': 5}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'ranged'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 1
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden floor tile. Warm and natural.',
        "durability": None,
        "icon": 'WoodFloor.png',
        "item_name": 'Wood Floor',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item_tag': 'Wood', 'amount': 10}, {'item': 'Metal Nail', 'amount': 12}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material', 'wood'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden ladder. Simple and effective.',
        "durability": None,
        "icon": 'WoodLadder.png',
        "item_name": 'Wood Ladder',
        "output_amount": 1,
        "placeable": True,
        "recipe": [{'item_tag': 'Wood', 'amount': 15}, {'item': 'Stick', 'amount': 5}, {'item': 'Metal Nail', 'amount': 15}],
        "smeltable": False,
        "stack_size": 100,
        "tags": ['building', 'material', 'wood'],
        "type": 'building_material',
        "use_effect": None,
        "weight": 2
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'hand',
        "description": 'A wooden club. Simple but effective.',
        "durability": 400,
        "icon": 'WoodenClub.png',
        "item_name": 'Wooden Club',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Wood', 'amount': 8}, {'item': 'Hide', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'melee'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 3
    },
    {
        "consumable": False,
        "cookable": False,
        "crafting_medium": 'workbench',
        "description": 'A wooden crossbow. Powerful ranged weapon.',
        "durability": 500,
        "icon": 'WoodenCrossbow.png',
        "item_name": 'Wooden Crossbow',
        "output_amount": 1,
        "placeable": False,
        "recipe": [{'item_tag': 'Wood', 'amount': 6}, {'item': 'Metal Ingot', 'amount': 2}, {'item': 'Twine', 'amount': 2}],
        "smeltable": False,
        "stack_size": 1,
        "tags": ['weapon', 'ranged'],
        "type": 'weapon',
        "use_effect": None,
        "weight": 3
    }
]

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
        for direction, frame_name in item["held_item_frames"].items():
            try:
                img = pygame.image.load(f"{itemframes_path}/{frame_name}").convert_alpha()
                item["held_item_images"][direction] = img
            except:
                item["held_item_images"][direction] = None

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
        self.inventory_full_message_timer = 0
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        self.inventory_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/inventory_screen.png").convert_alpha(), (1100, 600))
        self.crafting_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/crafting_screen.png").convert_alpha(), (1100, 600))
        self.level_up_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/level_up_screen.png").convert_alpha(), (1100, 600))
        self.cat_screen_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/cats_screen.png").convert_alpha(), (1100, 600))
        
        self.selected_crafting_item = None
        self.crafting_slot_positions = {}
        self.last_click_time = 0
        self.last_click_slot = None
        self.crafting_completion_flash = False
        self.crafting_completion_slot = None
        self.crafting_completion_time = 0
        self.crafting_flash_duration = 0.3  # 0.3 second flash

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

            inventory_tab_unused.draw(screen)
            crafting_tab_unused.draw(screen)
            screen.blit(level_up_tab, (width // 2 - 261, height // 2 - 303))
            cats_tab_unused.draw(screen)

        elif self.state == "cats":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.cat_screen_image, (x_pos, y_pos - 20))

            inventory_tab_unused.draw(screen)
            crafting_tab_unused.draw(screen)
            level_up_tab_unused.draw(screen)
            screen.blit(cats_tab, (width // 2 - 125, height // 2 - 303))

    def draw_hotbar(self, screen):
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        screen.blit(hotbar_image, (hotbar_x, hotbar_y))
        slot_size = self.slot_size * .75
        hotbar_font = pygame.font.SysFont(None, 15)
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        
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
                        
                        break
        
    def draw_items(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 18
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
        font = pygame.font.SysFont(None, 20)
        self.total_inventory_weight = 0

        for hotbar_slot in self.hotbar_slots:
            if hotbar_slot is not None:
                item_name = hotbar_slot["item_name"]
                quantity = hotbar_slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        stack_weight = round(quantity * item["weight"], 1)
                        self.total_inventory_weight += stack_weight
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
                        
                        stack_weight = round(quantity * item["weight"], 1)
                        self.total_inventory_weight += stack_weight
                        
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
                        
                        break
        
        player.weight = self.total_inventory_weight
        weight_text = font.render("Weight: ", True, (200, 200, 50))
        weight_num_text = font.render(str(f"{round(self.total_inventory_weight, 1)} / {player.max_weight}"), True, (200, 200, 50))
        total_weight_pos_x = screen.get_width()/2
        screen.blit(weight_text, (total_weight_pos_x + 20, 110))
        screen.blit(weight_num_text, (total_weight_pos_x + 20, 125))

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
    def draw_crafting(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 18
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
        
        font_small = pygame.font.SysFont(None, 30)
        font_medium = pygame.font.SysFont(None, 40)
        font_large = pygame.font.SysFont(None, 50)

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
        
        for item_name in resource:
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
                                self.hotbar_slots[i] = {
                                    "item_name": item_name,
                                    "quantity": 1
                                }
                                stacked = True
                                break
                    
                    if not stacked:
                        for i in range(self.capacity):
                            if self.inventory_list[i] is None:
                                self.inventory_list[i] = {
                                    "item_name": item_name,
                                    "quantity": 1
                                }
                                stacked = True
                                break
                    
                    break
            
            if not stacked:
                all_added = False
                if self.inventory_full_message_timer <= 0:
                    self.inventory_full_message_timer = 2.0
        
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
        
        if self.state == "inventory":
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
        if is_hotbar:
            slot = self.hotbar_slots[slot_index]
        else:
            slot = self.inventory_list[slot_index]
        
        if slot is not None:
            self.dragging = True
            self.dragged_item = slot.copy()
            self.dragged_from_slot = slot_index
            self.dragged_from_hotbar = is_hotbar
            
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None

    def update_drag(self, mouse_pos):
        pass

    def end_drag(self, slot_index, is_hotbar, screen):
        if not self.dragging:
            return
        
        if is_hotbar:
            target_slot = self.hotbar_slots[slot_index]
        else:
            target_slot = self.inventory_list[slot_index]
        
        if target_slot is None:
            if is_hotbar:
                self.hotbar_slots[slot_index] = self.dragged_item
            else:
                self.inventory_list[slot_index] = self.dragged_item
        
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
        
        else:
            if is_hotbar:
                self.hotbar_slots[slot_index] = self.dragged_item
            else:
                self.inventory_list[slot_index] = self.dragged_item
            
            if self.dragged_from_hotbar:
                self.hotbar_slots[self.dragged_from_slot] = target_slot
            else:
                self.inventory_list[self.dragged_from_slot] = target_slot
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False

    def cancel_drag(self):
        if not self.dragging:
            return
        
        if self.dragged_from_hotbar:
            self.hotbar_slots[self.dragged_from_slot] = self.dragged_item
        else:
            self.inventory_list[self.dragged_from_slot] = self.dragged_item
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False

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
                    font = pygame.font.SysFont(None, 20)
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
            
            return (slot_index, is_hotbar)
        
        return (None, None)
    
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
        Returns: (success: bool, tags: list) - True if item removed, and the item's tags
        """
        # Determine which slot to throw from based on selection mode
        if self.selection_mode == "hotbar":
            slot_index = self.selected_hotbar_slot
            slot = self.hotbar_slots[slot_index]
            is_hotbar = True
        elif self.selection_mode == "inventory":
            if self.selected_inventory_slot is None:
                return (False, [])
            slot_index = self.selected_inventory_slot
            slot = self.inventory_list[slot_index]
            is_hotbar = False
        else:
            return (False, [])
        
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
            return (False, [])
        
        # Reduce quantity by 1
        slot["quantity"] -= 1
        
        # Remove item from slot if quantity reaches 0
        if slot["quantity"] <= 0:
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None
        
        return (True, item_data.get("tags", []))

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
        
        # Return the empty container to inventory if this item used one
        recipe = item_data.get("recipe")
        if recipe and isinstance(recipe, list):
            for recipe_item in recipe:
                if isinstance(recipe_item, dict) and "item" in recipe_item:
                    container_name = recipe_item["item"]
                    # Add the empty container back to inventory (must pass as list)
                    self.add([container_name])
        
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

inventory = Inventory(64)