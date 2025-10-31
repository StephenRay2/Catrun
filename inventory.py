import pygame
from mob_placement import player
from buttons import inventory_tab, crafting_tab, level_up_tab, cats_tab, inventory_tab_unused, crafting_tab_unused, level_up_tab_unused, cats_tab_unused


hotbar_image = pygame.image.load("assets/sprites/buttons/hotbar.png").convert_alpha()
hotbar_image = pygame.transform.scale(hotbar_image, (686, 74))
player_inventory_image = pygame.image.load("assets/sprites/player/CharacterCorynnFrontStanding.png")
player_inventory_image = pygame.transform.scale(player_inventory_image, (500, 500))

image_path = "assets/sprites/items"

items_list = [
    # Raw Materials
    {
        "item_name": "Apples",
        "icon": "Apple.png",
        "stack_size": 100,
        "weight": .5,
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
        "weight": .5,
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
        "weight": 1,
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
        "weight": 1,
        "type": "raw_material",
        "description": "Sturdy wood from an apple tree. Good for crafting.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Dusk Wood",
        "icon": "DuskWood.png",
        "stack_size": 100,
        "weight": 1,
        "type": "raw_material",
        "description": "Dark purple-brown wood. Has a mysterious quality.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Fir Wood",
        "icon": "FirWood.png",
        "stack_size": 100,
        "weight": 1,
        "type": "raw_material",
        "description": "Light and flexible fir wood. Easy to work with.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Oak Wood",
        "icon": "OakWood.png",
        "stack_size": 100,
        "weight": 1,
        "type": "raw_material",
        "description": "Strong oak wood. Excellent for construction.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["wood", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Blood Berries",
        "icon": "BloodBerries.png",
        "stack_size": 100,
        "weight": .05,
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
        "weight": .05,
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
        "weight": .05,
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
        "weight": .05,
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
        "weight": .05,
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
        "weight": .05,
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
        "weight": .05,
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
        "weight": .1,
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
        "weight": .1,
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
        "weight": .1,
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
        "weight": .4,
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
        "item_name": "Raw Chicken",
        "icon": "RawChicken.png",
        "stack_size": 100,
        "weight": .3,
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
        "weight": .6,
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
        "weight": .4,
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
        "icon": "GilaMeat.png",
        "stack_size": 100,
        "weight": .3,
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
        "weight": 1,
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
        "item_name": "Raw Metal",
        "icon": "RawMetal.png",
        "stack_size": 100,
        "weight": 2,
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
        "weight": .1,
        "type": "raw_material",
        "description": "Simple wooden sticks. Basic crafting material.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "stick"],
        "output_amount": 1
    },
    {
        "item_name": "Raw Gold",
        "icon": "RawGold.png",
        "stack_size": 100,
        "weight": 2,
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
        "weight": .1,
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
        "weight": .05,
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
        "weight": .2,
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
        "weight": 1,
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
        "weight": 3,
        "type": "raw_material",
        "description": "Sharp, durable claws cut from a duskwretch. Like, super sharp. Razor-sharp.",
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
        "item_name": "Pock Eye",
        "icon": "PockEye.png",
        "stack_size": 100,
        "weight": .3,
        "type": "raw_material",
        "description": "A strange eye from a lifeless Pock. Unnerving to look at. May have qualities some might consider to be... unnatural.",
        "use_effect": "player.poison = True; player.poison_time += 100; self.temp_attack_boost += .1",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["material", "animal_parts"],
        "output_amount": 1
    },
    {
        "item_name": "Flint",
        "icon": "Flint.png",
        "stack_size": 100,
        "weight": .5,
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
        "weight": .5,
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
        "weight": 1,
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
        "weight": .2,
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
        "weight": .8,
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
        "weight": .01,
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
        "item_name": "Snake Fangs",
        "icon": "SnakeFangs.png",
        "stack_size": 100,
        "weight": .3,
        "type": "raw_material",
        "description": "Sharp front fangs of a giant snake. Useful for crafting and ripping through flesh, if you're into that kind of thing.",
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
        "weight": 1,
        "type": "raw_material",
        "description": "The little tiny baby claw of a creepy crawly purple crustacean. Useful for crafting and clamping things together really tighly, if you'd like.",
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
        "item_name": "Amethyst",
        "icon": "Amethyst.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A beautiful purple gemstone. Quite valuable. You feel lighter just lookig at it",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Aquamarine",
        "icon": "Aquamarine.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A clear blue gemstone. Reminds you of the ocean, and yet, you somehow feel a little more quenched.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Garnet",
        "icon": "Garnet.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A shiny reddish gemstone. Is it hot in here? Because I don't mind at all.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Diamond",
        "icon": "Diamond.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A flawless diamond. Extremely rare and valuable. You feel a little tougher just holding it.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Emerald",
        "icon": "Emerald.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A vibrant and energizing green gemstone. Highly prized.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Opal",
        "icon": "Opal.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "An iridescent gemstone. Shimmers with many colors that feed your very soul.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Pearl",
        "icon": "Pearl.png",
        "stack_size": 100,
        "weight": .1,
        "type": "gem",
        "description": "A lustrous pearl. Smooth and elegant. Created in the violent and raging depths of the sea.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Ruby",
        "icon": "Ruby.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A deep red gemstone. Burns with inner fire and ignites your passion for living",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Sapphire",
        "icon": "Sapphire.png",
        "stack_size": 100,
        "weight": .2,
        "type": "gem",
        "description": "A brilliant blue gemstone. Clear as the sky. Must be your lucky day",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Topaz",
        "icon": "Topaz.png",
        "stack_size": 100,
        "weight": 1,
        "type": "gem",
        "description": "A golden yellow gemstone. Warm and radiant. A swift reward for those patient enough to obtain it.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["gemstone"],
        "output_amount": 1
    },
    {
        "item_name": "Cage Key",
        "icon": "CageKey.png",
        "stack_size": 10,
        "weight": .3,
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
        "weight": .3,
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
        "weight": .7,
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
        "weight": .8,
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
        "weight": .1,
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
        "weight": .1,
        "type": "raw_material",
        "description": "A warm leaf that radiates heat. Used in alchemy.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["herb", "potion_ingredient"],
        "output_amount": 1
    },
    {
        "item_name": "Frost Fern Leaf",
        "icon": "FrostFernLeaf.png",
        "stack_size": 100,
        "weight": .1,
        "type": "raw_material",
        "description": "A cold leaf that feels icy to touch. Used in alchemy.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": None,
        "crafting_medium": None,
        "tags": ["herb", "potion_ingredient"],
        "output_amount": 1
    },

    # Cooked Items
    {
        "item_name": "Baked Apples",
        "icon": "BakedApple.png",
        "stack_size": 100,
        "weight": .5,
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
        "weight": .4,
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
        "item_name": "Cooked Chicken",
        "icon": "CookedChicken.png",
        "stack_size": 100,
        "weight": .3,
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
        "weight": .6,
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
        "weight": .4,
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
        "icon": "CookedGilaMeat.png",
        "stack_size": 100,
        "weight": .3,
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
        "weight": 2,
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
        "weight": 2,
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
        "weight": 1,
        "type": "crafted_material",
        "description": "Clear glass. Made from melted sand.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Bucket of Sand", "amount": 1}],
        "output_amount": 5,
        "crafting_medium": "smelter",
        "tags": ["crafted", "material"]
    },

    # Crafted Items by Hand
    {
        "item_name": "Mushroom Stew",
        "icon": "MushroomStew.png",
        "stack_size": 100,
        "weight": .5,
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
        "weight": 1,
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
        "weight": .2,
        "type": "crafted_material",
        "description": "Simple twine woven from plant fibers.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Fiber", "amount": 4}],
        "crafting_medium": "hand",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Ball Of Twine",
        "icon": "BallOfTwine.png",
        "stack_size": 100,
        "weight": 2,
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
        "weight": 1.5,
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
        "icon": "Torch1.png",
        "stack_size": 100,
        "weight": 1,
        "type": "tool",
        "description": "A simple torch. Provides light in darkness.",
        "use_effect": "provide_light; provide_warmth",
        "placeable": True,
        "consumable": False,
        "durability": 300,
        "recipe": [{"item": "Sticks", "amount": 5}, {"item": "Flint", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["tool"],
        "output_amount": 1
    },
    {
        "item_name": "Small Orange Juice",
        "icon": "SmallOrangeJuice.png",
        "stack_size": 100,
        "weight": 1,
        "type": "consumable",
        "description": "Fresh squeezed orange juice. Refreshing!",
        "use_effect": "player.thirst += 20; player.hunger += 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Oranges", "amount": 3}, {"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Wooden Bowl",
        "icon": "WoodenBowl.png",
        "stack_size": 100,
        "weight": 1,
        "type": "crafted_material",
        "description": "A simple wooden bowl. Holds food and liquids.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 2}],
        "crafting_medium": "hand",
        "tags": ["wooden", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Wooden Cup",
        "icon": "WoodenCup.png",
        "stack_size": 100,
        "weight": .5,
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
        "weight": 30,
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
        "item_name": "Campfire",
        "icon": "Campfire1.png",
        "stack_size": 100,
        "weight": 2,
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
        "icon": "OilLamp1.png",
        "stack_size": 100,
        "weight": 1,
        "type": "tool",
        "description": "An oil lamp burning brightly. Provides steady light.",
        "use_effect": "provide_light; provide_warmth",
        "placeable": True,
        "consumable": False,
        "durability": 600,
        "recipe": [{"item": "Empty Oil Lamp", "amount": 1}, {"item_tag": "oil", "amount": 1}],
        "crafting_medium": "hand",
        "tags": ["tool"],
        "output_amount": 1
    },

    # Crafted Items at Mortar and Pestle
    {
        "item_name": "Small Olive Oil",
        "icon": "SmallOliveOil.png",
        "stack_size": 100,
        "weight": .7,
        "type": "crafted_material",
        "description": "Pressed olive oil in a small container.",
        "use_effect": "player.thirst += 2",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Olives", "amount": 5}, {"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Sealing Paste",
        "icon": "SealingPaste.png",
        "stack_size": 100,
        "weight": .1,
        "type": "crafted_material",
        "description": "A thick and viscous liquid that keeps water out of where it's not wanted, and keeps it in where it's enslaved. I wouldn't it this if I were you.",
        "use_effect": "player.health -= 50; player.poison = True; player.poison_time = 10; player.poison_strength += 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 1}, {"item_tag": "oil", "amount": 1}, {"item": "Fiber", "amount": 1}],
        "output_amount": 20,
        "crafting_medium": "mortar_and_pestle",
        "tags": ["crafted", "material"]
    },
    {
        "item_name": "Small Health Brew",
        "icon": "SmallHealthBrew.png",
        "stack_size": 100,
        "weight": .7,
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
        "weight": .7,
        "type": "potion",
        "description": "A small stamina potion. Restores some stamina.",
        "use_effect": "player.stamina += 30",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Fiber", "amount": 10}, {"item": "Twilight Drupes", "amount": 3}, {"item": "Small Water", "amount": 1}],
        "crafting_medium": "mortar_and_pestle",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Small Bright Brew",
        "icon": "SmallBrightBrew.png",
        "stack_size": 100,
        "weight": .7,
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
        "weight": .7,
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
        "weight": .7,
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
        "weight": 1,
        "type": "special",
        "description": "A mystical, valuable, and powerful coin. Grants a second chance at life.... or nine",
        "use_effect": "player.resurrect",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Gold Ingot", "amount": 5}, {"item": "Diamond", "amount": 1}, {"item": "Ruby", "amount": 1}, {"item": "Emerald", "amount": 1}, {"item": "Sapphire", "amount": 1}, {"item": "Garnet", "amount": 1}, {"item": "Aquamarine", "amount": 1}, {"item": "Topaz", "amount": 1}, {"item": "Amethyst", "amount": 1}, {"item": "Opal", "amount": 1}, {"item": "Pearl", "amount": 1}, {"item": "Duskwood", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Throwing Knife",
        "icon": "ThrowingKnife.png",
        "stack_size": 100,
        "weight": .5,
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
        "weight": .5,
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
        "weight": .8,
        "type": "crafted_material",
        "description": "An empty oil lamp. Needs oil to function.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 5}, {"item": "Fiber", "amount": 1}, {"item": "Flint", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Small Metal Ring",
        "icon": "SmallMetalRing.png",
        "stack_size": 1,
        "weight": .7,
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
        "weight": .6,
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
        "weight": 1,
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
        "weight": 1,
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
        "weight": .3,
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
        "weight": .3,
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
        "weight": 1,
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
        "weight": 1,
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
        "weight": 1.5,
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
        "weight": 1.5,
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
        "weight": 2,
        "type": "equipment",
        "description": "A large metal amulet. Feels powerful. Becuase it is. Well, it could be... If you stuck some shiny, pretty, precious little gems inside all those holes you made.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 2}, {"item": "Medium Metal Amulet", "amount": 1}, {"item": "Snake Fangs", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Gold Amulet",
        "icon": "LargeGoldAmulet.png",
        "stack_size": 1,
        "weight": 2,
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
        "icon": "CookingPot1.png",
        "stack_size": 1,
        "weight": 10,
        "type": "structure",
        "description": "A large cooking pot. Used for making massive stews. Like, huge.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 10}, {"item": "Campfire", "amount": 1}, {"item": "Hide", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Smelter",
        "icon": "Smelter.png",
        "stack_size": 1,
        "weight": 50,
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
        "weight": 15,
        "type": "structure",
        "description": "An empty cage. Can hold captured animals.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Ingot", "amount": 10}, {"item": "Metal Chain", "amount": 3}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Alchemy Bench",
        "icon": "AlchemyBench.png",
        "stack_size": 1,
        "weight": 30,
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
        "weight": 5,
        "type": "structure",
        "description": "A wooden fence section. Marks boundaries. Can keep things in or out. Of what? That's for you to decide.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 5}, {"item": "Sticks", "amount": 10}, {"item": "Rope", "amount": 1}],
        "output_amount": 2,
        "crafting_medium": "workbench",
        "tags": ["item"]
    },
    {
        "item_name": "Chest",
        "icon": "ChestClosed.png",
        "stack_size": 1,
        "weight": 20,
        "type": "structure",
        "description": "A storage chest. Holds many items safely.",
        "use_effect": None,
        "placeable": True,
        "consumable": False,
        "durability": None,
        "recipe": [{"item_tag": "wood", "amount": 8}, {"item": "Metal Ingot", "amount": 2}],
        "crafting_medium": "workbench",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Tent",
        "icon": "Tent.png",
        "stack_size": 1,
        "weight": 15,
        "type": "structure",
        "description": "A portable tent. Provides shelter anywhere. Except for underwater. Or space. Or in lava.",
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
        "weight": 1,
        "type": "crafted_material",
        "description": "An empty glass bottle. Can hold liquids a lot better than your hands.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Glass", "amount": 2}, {"item": "Sealing Paste", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["crafted", "material", "container"],
        "output_amount": 1
    },
    {
        "item_name": "Lantern",
        "icon": "Lantern1.png",
        "stack_size": 100,
        "weight": 3,
        "type": "tool",
        "description": "A bright lantern. Lights up large areas. Impervious to inclement weather. I think that means it won't go out in the rain. The wicked witch of the west doesn't do that either. I think that means she's impervious to inclement weather. Just kidding, it's becasue she's dead.",
        "use_effect": "provide_light; provide_heat",
        "placeable": True,
        "consumable": False,
        "durability": 1000,
        "recipe": [{"item": "Metal Ingot", "amount": 4}, {"item": "Glass", "amount": 4}, {"item": "Torch", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["tool"],
        "output_amount": 1
    },
    {
        "item_name": "Mortar And Pestle",
        "icon": "MortarAndPestle.png",
        "stack_size": 1,
        "weight": 20,
        "type": "tool",
        "description": "A mortar and pestle. Grinds ingredients for alchemy. Rock and roll, baby.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Stone", "amount": 25}, {"item": "Hide", "amount": 10}],
        "crafting_medium": "workbench",
        "tags": ["tool"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Bucket",
        "icon": "MetalBucket.png",
        "stack_size": 100,
        "weight": 5,
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
        "weight": 1,
        "type": "tool",
        "description": "A fishing pole. Catch fish from rivers and ponds. Gotta catch 'em... most of 'em, because copyright laws are a thing.",
        "use_effect": "catch_fish",
        "placeable": False,
        "consumable": False,
        "durability": 500,
        "recipe": [{"item": "Twine", "amount": 5}, {"item": "Sticks", "amount": 5}, {"item": "Metal Ingot", "amount": 1}],
        "crafting_medium": "workbench",
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    {
        "item_name": "Metal Fishing Pole",
        "icon": "FishingPole.png",
        "stack_size": 1,
        "weight": 5,
        "type": "tool",
        "description": "A fishing pole. Catch fish from rivers and ponds BUT WITH METAL.",
        "use_effect": "catch_fish",
        "placeable": False,
        "consumable": False,
        "durability": 2000,
        "recipe": [{"item": "Twine", "amount": 5}, {"item": "Metal Ingot", "amount": 6}],
        "crafting_medium": "workbench",
        "tags": ["food", "meat"],
        "output_amount": 1
    },
    # Crafted through Gameplay
    {
    
        "item_name": "Bucket of Sand",
        "icon": "SandBucket.png",
        "stack_size": 100,
        "weight": 3,
        "type": "raw_material",
        "description": "It's a bucket... with sand in it... I call it a bucket of sand.",
        "use_effect": None,
        "placeable": False,
        "consumable": False,
        "durability": None,
        "recipe": [{"item": "Metal Bucket", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["item"],
        "output_amount": 1
    },
    {
        "item_name": "Small Water",
        "icon": "SmallWater.png",
        "stack_size": 100,
        "weight": .7,
        "type": "consumable",
        "description": "Fresh water in a small cup. Quenches thirst.",
        "use_effect": "player.thirst += 15",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Small Milk",
        "icon": "SmallMilk.png",
        "stack_size": 100,
        "weight": .7,
        "type": "consumable",
        "description": "Fresh milk in a small cup. Unless you're the size of a pea. Then it's a ginormous cup. Way too big for one little pea-sized guy or gal to drink. Creamy and nutritious.",
        "use_effect": "player.thirst += 12; player.hunger += 3",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Wooden Cup", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Water",
        "icon": "MediumGlassWater.png",
        "stack_size": 100,
        "weight": 1.4,
        "type": "consumable",
        "description": "Water in a medium glass bottle. Very refreshing. So refreshing. You'll feel so refreshed.",
        "use_effect": "player.thirst += 50",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Milk",
        "icon": "MediumGlassMilk.png",
        "stack_size": 100,
        "weight": 1.4,
        "type": "consumable",
        "description": "Milk in a medium glass bottle. Rich and filling. Whether cow or coconut, you'll be craving the goods.",
        "use_effect": "player.thirst += 40; player.hunger += 10",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Orange Juice",
        "icon": "MediumGlassOrangeJuice.png",
        "stack_size": 100,
        "weight": 1.4,
        "type": "consumable",
        "description": "Orange juice in a medium bottle. Tangy and sweet.",
        "use_effect": "player.thirst += 35; player.hunger += 10; player.stamina += 20",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Oranges", "amount": 5}, {"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["food", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Water",
        "icon": "LargeMetalWater.png",
        "stack_size": 100,
        "weight": 2,
        "type": "consumable",
        "description": "Anti-thirst in a large metal canteen. Lasts a long time.",
        "use_effect": "player.thirst += 100",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Milk",
        "icon": "LargeMetalMilk.png",
        "stack_size": 100,
        "weight": 2,
        "type": "consumable",
        "description": "Cow sauce in a large metal canteen. Very satisfying.",
        "use_effect": "player.thirst += 80; player.hunger += 20",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Orange Juice",
        "icon": "LargeMetalOrangeJuice.png",
        "stack_size": 100,
        "weight": 2,
        "type": "consumable",
        "description": "Orange juice in a large canteen. Packed with flavor.",
        "use_effect": "player.thirst += 60; player.hunger += 15; player.stamina += 40",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "gameplay",
        "tags": ["material", "ore"],
        "output_amount": 1
    },

    # Crafted at Alchemy Bench

    {
        "item_name": "Medium Glass Olive Oil",
        "icon": "MediumGlassOliveOil.png",
        "stack_size": 100,
        "weight": 1.4,
        "type": "crafted_material",
        "description": "Olive oil in a medium glass bottle. Perfect for fuel refills.",
        "use_effect": "player.thirst += 5",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Olives", "amount": 15}, {"item": "Glass Bottle", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["crafted", "material"],
        "output_amount": 1
    },
    {
        "item_name": "Large Metal Olive Oil",
        "icon": "LargeMetalOliveOil.png",
        "stack_size": 100,
        "weight": 2,
        "type": "crafted_material",
        "description": "Olive oil in a large metal canteen. All of the oil's in a large metal canteen. I love oil straight from the canteen made of metal. I'll live better knowing I have my metal canteen of oil pressed from all of the olives of all of the olive trees.",
        "use_effect": "player.thirst += 10",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Olives", "amount": 20}, {"item": "Large Metal Canteen", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["material", "ore"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Health Brew",
        "icon": "MediumGlassHealthBrew.png",
        "stack_size": 100,
        "weight": 1.4,
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
        "weight": 1.4,
        "type": "potion",
        "description": "A medium stamina potion. Restores substantial stamina.",
        "use_effect": "player.stamina += 80",
        "placeable": False,
        "consumable": True,
        "durability": None,
        "recipe": [{"item": "Fiber", "amount": 15}, {"item": "Twilight Drupes", "amount": 4}, {"item": "Medium Glass Water", "amount": 1}],
        "crafting_medium": "alchemy_bench",
        "tags": ["potion", "consumable"],
        "output_amount": 1
    },
    {
        "item_name": "Medium Glass Bright Brew",
        "icon": "MediumGlassBrightBrew.png",
        "stack_size": 100,
        "weight": 1.4,
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
        "weight": 1.4,
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
        "weight": 1.4,
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
        "weight": 1.4,
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
        "weight": 1,
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
        "weight": 1,
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
        "weight": 1,
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
        "weight": 1,
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
        "weight": 1,
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
        "weight": 10,
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
        "weight": 10,
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
    }

]

for item in items_list:
    item["image"] = pygame.transform.scale(
        pygame.image.load(f"{image_path}/{item['icon']}").convert_alpha(),
        (60, 60)
    )

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
            screen.blit(player_inventory_image, (700, 130))

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
            screen.blit(player_inventory_image, (700, 130))

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
        hotbar_y = screen.get_height() - 100
        screen.blit(hotbar_image, (hotbar_x, hotbar_y))
        
        font = pygame.font.SysFont(None, 20)
        large_font = pygame.font.SysFont(None, 32, bold=True)
        first_slot_x = hotbar_x + 6
        slot_y = hotbar_y + 6
        slot_spacing = 68
        
        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            
            if i == self.selected_hotbar_slot and self.selection_mode == "hotbar":
                highlight_surface = pygame.Surface((self.slot_size + 8, self.slot_size + 8), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (255, 255, 255, 200), (0, 0, self.slot_size + 8, self.slot_size + 8), 4)
                screen.blit(highlight_surface, (x - 6, y - 6))
                
            
            slot = self.hotbar_slots[i]
            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))
                        
                        stack_weight = round(quantity * item["weight"], 1)
                        weight_text = font.render(str(stack_weight), True, (250, 250, 20))
                        weight_x_pos = x + 39
                        if stack_weight == int(stack_weight) and stack_weight < 10:
                            weight_x_pos += 7
                        screen.blit(weight_text, (weight_x_pos, y + 4))
                        
                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity >= 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        
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
                        screen.blit(item["image"], (x, y))
                        
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
        hotbar_y = screen.get_height() - 100
        first_slot_x = hotbar_x + 6
        slot_y = hotbar_y + 6
        slot_spacing = 68
        
        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
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
                        success = self.craft_item(item)
                        self.last_click_slot = None
                        self.last_click_time = 0
                        return success
                else:
                    self.selected_crafting_item = item
                    self.last_click_slot = idx
                    self.last_click_time = current_time
                    return False
        
        return False
    
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
            print(f"{item_name} is not consumable!")
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

inventory = Inventory(64)