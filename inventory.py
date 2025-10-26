import pygame
from mob_placement import player
from buttons import inventory_tab, crafting_tab, level_up_tab, cats_tab, inventory_tab_unused, crafting_tab_unused, level_up_tab_unused, cats_tab_unused


hotbar_image = pygame.image.load("assets/sprites/buttons/hotbar.png").convert_alpha()
hotbar_image = pygame.transform.scale(hotbar_image, (686, 74))
player_inventory_image = pygame.image.load("assets/sprites/player/CharacterCorynnFrontStanding.png")
player_inventory_image = pygame.transform.scale(player_inventory_image, (500, 500))

image_path = "assets/sprites/items"

items_list = [
    # Fruits & Vegetables
    {"item_name" : "Apples", "icon": "Apple.png", "stack_size": 100, "weight": .25},
    {"item_name" : "Baked Apples", "icon": "BakedApple.png", "stack_size": 100, "weight": .3},
    {"item_name" : "Oranges", "icon": "Orange.png", "stack_size": 100, "weight": .3},
    {"item_name" : "Orange Juice", "icon": "OrangeJuice.png", "stack_size": 100, "weight": .2},
    {"item_name" : "Coconuts", "icon": "Coconut.png", "stack_size": 100, "weight": .4},

    # Wood Types
    {"item_name" : "Apple Wood", "icon": "AppleWood.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Dusk Wood", "icon": "DuskWood.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Fir Wood", "icon": "FirWood.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Oak Wood", "icon": "OakWood.png", "stack_size": 100, "weight": .5},

    # Berries & Mushrooms
    {"item_name" : "Blood Berries", "icon": "BloodBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Dawn Berries", "icon": "DawnBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Dusk Berries", "icon": "DuskBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Sun Berries", "icon": "SunBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Teal Berries", "icon": "TealBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Twilight Drupes", "icon": "TwilightDrupes.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Vio Berries", "icon": "VioBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Mushroom", "icon": "Mushroom.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Dawnshroom", "icon": "Dawnshroom.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Duskshroom", "icon": "Duskshroom.png", "stack_size": 100, "weight": .05},
    
    # Raw Meat & Fish
    {"item_name" : "Raw Beef", "icon": "RawBeef.png", "stack_size": 100, "weight": .25},
    {"item_name" : "Raw Chicken", "icon": "RawChicken.png", "stack_size": 100, "weight": .2},
    {"item_name" : "Fish", "icon": "Fish.png", "stack_size": 100, "weight": .15},
    {"item_name" : "Raw Venison", "icon": "RawVenison.png", "stack_size": 100, "weight": .3},
    {"item_name" : "Gila Meat", "icon": "GilaMeat.png", "stack_size": 100, "weight": .35},

    # Cooked Food
    {"item_name" : "Cooked Beef", "icon": "CookedBeef.png", "stack_size": 100, "weight": .28},
    {"item_name" : "Cooked Chicken", "icon": "CookedChicken.png", "stack_size": 100, "weight": .22},
    {"item_name" : "Cooked Fish", "icon": "CookedFish.png", "stack_size": 100, "weight": .18},
    {"item_name" : "Cooked Venison", "icon": "CookedVenison.png", "stack_size": 100, "weight": .32},
    {"item_name" : "Cooked Gila Meat", "icon": "CookedGilaMeat.png", "stack_size": 100, "weight": .38},
    {"item_name" : "Mushroom Stew", "icon": "MushroomStew.png", "stack_size": 100, "weight": .4},
    
    # Raw Materials & Resources
    {"item_name" : "Stone", "icon": "Stone.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Raw Metal", "icon": "RawMetal.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Metal Ingot", "icon": "MetalIngot.png", "stack_size": 100, "weight": 0.8},
    {"item_name" : "Raw Gold", "icon": "RawGold.png", "stack_size": 100, "weight": 1.2},
    {"item_name" : "Gold Ingot", "icon": "GoldIngot.png", "stack_size": 100, "weight": 0.95},
    {"item_name" : "Sticks", "icon": "Stick.png", "stack_size": 100, "weight": .2},
    {"item_name" : "Poisonous Mushroom", "icon": "PoisonousMushroom.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Fiber", "icon": "Fiber.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Hide", "icon": "Hide.png", "stack_size": 100, "weight": .3},
    {"item_name" : "Buck Antlers", "icon": "BuckAntlers.png", "stack_size": 50, "weight": 0.4},
    {"item_name" : "Duskwretch Claws", "icon": "DuskwretchClaws.png", "stack_size": 50, "weight": 0.35},
    
    # Crafted Materials
    {"item_name" : "Rope", "icon": "Rope.png", "stack_size": 100, "weight": .15},
    {"item_name" : "Twine", "icon": "Twine.png", "stack_size": 100, "weight": .08},
    {"item_name" : "Ball Of Twine", "icon": "BallOfTwine.png", "stack_size": 50, "weight": .1},
    {"item_name" : "Flint", "icon": "Flint.png", "stack_size": 100, "weight": .1},
    {"item_name" : "Glass", "icon": "Glass.png", "stack_size": 100, "weight": .2},

    # Tools & Equipment
    {"item_name" : "Fishing Pole", "icon": "FishingPole.png", "stack_size": 5, "weight": 1.5},
    {"item_name" : "Flint And Steel", "icon": "FlintAndSteel.png", "stack_size": 5, "weight": 0.5},
    {"item_name" : "Mortar And Pestle", "icon": "MortarAndPestle.png", "stack_size": 1, "weight": 1.0},
    {"item_name" : "Metal Bucket", "icon": "MetalBucket.png", "stack_size": 10, "weight": 2.0},
    
    # Lighting
    {"item_name" : "Torch", "icon": "Torch1.png", "stack_size": 100, "weight": 0.1},
    {"item_name" : "Lantern", "icon": "Lantern1.png", "stack_size": 10, "weight": 0.8},

    # Beverages & Potions
    {"item_name" : "Small Water", "icon": "SmallWater.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Milk", "icon": "SmallMilk.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Orange Juice", "icon": "SmallOrangeJuice.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Health Brew", "icon": "SmallHealthBrew.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Stamina Brew", "icon": "SmallStaminaBrew.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Bright Brew", "icon": "SmallBrightBrew.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Chill Brew", "icon": "SmallChillBrew.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Small Heat Brew", "icon": "SmallHeatBrew.png", "stack_size": 50, "weight": 0.15},
    
    {"item_name" : "Medium Glass Water", "icon": "MediumGlassWater.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Milk", "icon": "MediumGlassMilk.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Orange Juice", "icon": "MediumGlassOrangeJuice.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Health Brew", "icon": "MediumGlassHealthBrew.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Stamina Brew", "icon": "MediumGlassStaminaBrew.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Bright Brew", "icon": "MediumBrightBrew.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Bright Brew", "icon": "MediumGlassBrightBrew.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Chill Brew", "icon": "MediumGlassChillBrew.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Medium Glass Heat Brew", "icon": "MediumGlassHeatBrew.png", "stack_size": 30, "weight": 0.3},
    
    {"item_name" : "Large Metal Water", "icon": "LargeMetalWater.png", "stack_size": 1, "weight": 0.6},
    {"item_name" : "Large Metal Milk", "icon": "LargeMetalMilk.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Orange Juice", "icon": "LargeMetalOrangeJuice.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Canteen", "icon": "LargeMetalCanteen.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Health Brew", "icon": "LargeMetalHealthBrew.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Stamina Brew", "icon": "LargeMetalStaminaBrew.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Bright Brew", "icon": "LargeMetalBrightBrew.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Chill Brew", "icon": "LargeMetalChillBrew.png", "stack_size": 20, "weight": 0.6},
    {"item_name" : "Large Metal Heat Brew", "icon": "LargeMetalHeatBrew.png", "stack_size": 20, "weight": 0.6},

    # Containers & Special
    {"item_name" : "Glass Bottle", "icon": "GlassBottle.png", "stack_size": 50, "weight": 0.1},
    {"item_name" : "Wooden Bowl", "icon": "WoodenBowl.png", "stack_size": 20, "weight": 0.2},
    {"item_name" : "Wooden Cup", "icon": "WoodenCup.png", "stack_size": 50, "weight": 0.1},
    {"item_name" : "Pock Eye", "icon": "PockEye.png", "stack_size": 50, "weight": 0.05},

    # Building & Furniture
    {"item_name" : "Fence", "icon": "Fence.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Chest Closed", "icon": "ChestClosed.png", "stack_size": 5, "weight": 8},
    {"item_name" : "Chest Open", "icon": "ChestOpen.png", "stack_size": 5, "weight": 8},
    {"item_name" : "Tent", "icon": "Tent.png", "stack_size": 5, "weight": 4},
    {"item_name" : "Workbench", "icon": "Workbench.png", "stack_size": 1, "weight": 20},
    {"item_name" : "Smelter", "icon": "Smelter.png", "stack_size": 1, "weight": 25},
    
    # Misc
    {"item_name" : "Empty Cage", "icon": "EmptyCage.png", "stack_size": 1, "weight": 8},
    
    # New Items - Crafting & Building
    {"item_name" : "Alchemy Bench", "icon": "AlchemyBench.png", "stack_size": 1, "weight": 25},
    {"item_name" : "Campfire", "icon": "Campfire1.png", "stack_size": 1, "weight": 10},
    {"item_name" : "Campfire Active 2", "icon": "Campfire2.png", "stack_size": 1, "weight": 10},
    {"item_name" : "Campfire Active 3", "icon": "Campfire3.png", "stack_size": 1, "weight": 10},
    {"item_name" : "Campfire Active 4", "icon": "Campfire4.png", "stack_size": 1, "weight": 10},
    {"item_name" : "Campfire Active 5", "icon": "Campfire5.png", "stack_size": 1, "weight": 10},
    {"item_name" : "Cooking Pot", "icon": "CookingPot1.png", "stack_size": 1, "weight": 2.0},
    {"item_name" : "Cooking Pot Active 2", "icon": "CookingPot2.png", "stack_size": 1, "weight": 2.0},
    {"item_name" : "Cooking Pot Active 3", "icon": "CookingPot3.png", "stack_size": 1, "weight": 2.0},
    {"item_name" : "Cooking Pot Active 4", "icon": "CookingPot4.png", "stack_size": 1, "weight": 2.0},
    {"item_name" : "Cooking Pot Active 5", "icon": "CookingPot5.png", "stack_size": 1, "weight": 2.0},
    {"item_name" : "Dead Campfire", "icon": "DeadCampfire.png", "stack_size": 1, "weight": 10},
    {"item_name" : "Dead Cooking Pot", "icon": "DeadCookingPot.png", "stack_size": 1, "weight": 2.0},
    {"item_name" : "Oil Lamp", "icon": "OilLamp1.png", "stack_size": 5, "weight": 0.5},
    {"item_name" : "Oil Lamp Lit 2", "icon": "OilLamp2.png", "stack_size": 5, "weight": 0.5},
    {"item_name" : "Oil Lamp Lit 3", "icon": "OilLamp3.png", "stack_size": 5, "weight": 0.5},
    {"item_name" : "Empty Oil Lamp", "icon": "EmptyOilLamp.png", "stack_size": 10, "weight": 0.3},
    
    # New Items - Decorative & Special Materials
    {"item_name" : "Bone", "icon": "Bone.png", "stack_size": 100, "weight": 0.2},
    {"item_name" : "Fur", "icon": "Fur.png", "stack_size": 100, "weight": 0.1},
    {"item_name" : "Venom Sac", "icon": "VenomSac.png", "stack_size": 50, "weight": 0.15},
    
    # New Items - Gems & Jewelry
    {"item_name" : "Amethyst", "icon": "Amethyst.png", "stack_size": 50, "weight": 0.3},
    {"item_name" : "Aquamarine", "icon": "Aquamarine.png", "stack_size": 50, "weight": 0.3},
    {"item_name" : "Diamond", "icon": "Diamond.png", "stack_size": 50, "weight": 0.35},
    {"item_name" : "Emerald", "icon": "Emerald.png", "stack_size": 50, "weight": 0.3},
    {"item_name" : "Opal", "icon": "Opal.png", "stack_size": 50, "weight": 0.25},
    {"item_name" : "Pearl", "icon": "Pearl.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Ruby", "icon": "Ruby.png", "stack_size": 50, "weight": 0.3},
    {"item_name" : "Sapphire", "icon": "Sapphire.png", "stack_size": 50, "weight": 0.3},
    {"item_name" : "Topaz", "icon": "Topaz.png", "stack_size": 50, "weight": 0.25},
    
    # New Items - Rings & Amulets
    {"item_name" : "Small Metal Ring", "icon": "SmallMetalRing.png", "stack_size": 20, "weight": 0.1},
    {"item_name" : "Small Gold Ring", "icon": "SmallGoldRing.png", "stack_size": 20, "weight": 0.12},
    {"item_name" : "Metal Ring", "icon": "MetalRing.png", "stack_size": 20, "weight": 0.15},
    {"item_name" : "Gold Ring", "icon": "GoldRing.png", "stack_size": 20, "weight": 0.18},
    {"item_name" : "Small Metal Amulet", "icon": "SmallMetalAmulet.png", "stack_size": 10, "weight": 0.2},
    {"item_name" : "Small Gold Amulet", "icon": "SmallGoldAmulet.png", "stack_size": 10, "weight": 0.25},
    {"item_name" : "Medium Metal Amulet", "icon": "MediumMetalAmulet.png", "stack_size": 5, "weight": 0.4},
    {"item_name" : "Medium Gold Amulet", "icon": "MediumGoldAmulet.png", "stack_size": 5, "weight": 0.45},
    {"item_name" : "Large Metal Amulet", "icon": "LargeMetalAmulet.png", "stack_size": 3, "weight": 0.6},
    {"item_name" : "Large Gold Amulet", "icon": "LargeGoldAmulet.png", "stack_size": 3, "weight": 0.65},
    
    # New Items - Additional Beverages
    {"item_name" : "Small Olive Oil", "icon": "SmallOliveOIl.png", "stack_size": 50, "weight": 0.15},
    {"item_name" : "Medium Glass Olive Oil", "icon": "MediumGlassOliveOil.png", "stack_size": 30, "weight": 0.3},
    {"item_name" : "Large Metal Olive Oil", "icon": "LargeMetalOliveOil.png", "stack_size": 20, "weight": 0.6},
    
    # New Items - Torch Variants
    {"item_name" : "Torch (Lit)", "icon": "Torch2.png", "stack_size": 100, "weight": 0.12},
    {"item_name" : "Torch (Lit 2)", "icon": "Torch3.png", "stack_size": 100, "weight": 0.12},
    {"item_name" : "Torch (Lit 3)", "icon": "Torch4.png", "stack_size": 100, "weight": 0.12},
    
    # New Items - Lantern Variants
    {"item_name" : "Lantern (Lit)", "icon": "Lantern2.png", "stack_size": 10, "weight": 0.9},
    {"item_name" : "Lantern (Lit 2)", "icon": "Lantern3.png", "stack_size": 10, "weight": 0.9},
    {"item_name" : "Lantern (Lit 3)", "icon": "Lantern4.png", "stack_size": 10, "weight": 0.9},
    
    # New Items - Fence Variants
    {"item_name" : "Fence Corner Left Bottom", "icon": "FenceCornerLeftBottom.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Fence Corner Right Bottom", "icon": "FenceCornerRightBottom.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Fence End Left Top", "icon": "FenceEndLeftTop.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Fence End Right Top", "icon": "FenceEndRightTop.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Fence Front", "icon": "FenceFront.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Fence Left Side", "icon": "FenceLeftSide.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Fence Right Side", "icon": "FenceRightSide.png", "stack_size": 100, "weight": 6},
    
    # New Items - Keys & Special Items
    {"item_name" : "Cage Key", "icon": "CageKey.png", "stack_size": 10, "weight": 0.1},
    {"item_name" : "Chest Key", "icon": "ChestKey.png", "stack_size": 10, "weight": 0.1},
    {"item_name" : "Resurrection Coin", "icon": "ResurrectionCoin.png", "stack_size": 1, "weight": 0.05},
    
    # New Items - Weapons & Tools
    {"item_name" : "Throwing Knife", "icon": "ThrowingKnife.png", "stack_size": 50, "weight": 0.2},
    {"item_name" : "Throwing Star", "icon": "ThrowingStar.png", "stack_size": 50, "weight": 0.15},
    
    # New Items - Fruits & Vegetables
    {"item_name" : "Pineapple", "icon": "Pineapple.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Watermelon", "icon": "Watermelon.png", "stack_size": 100, "weight": 1.2},
    {"item_name" : "Olives", "icon": "Olives.png", "stack_size": 100, "weight": 0.1},
    
    # New Items - Plant Materials
    {"item_name" : "Fire Fern Leaf", "icon": "FireFernLeaf.png", "stack_size": 100, "weight": 0.05},
    {"item_name" : "Frost Fern Leaf", "icon": "FrostFernLeaf.png", "stack_size": 100, "weight": 0.05},
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
        self.inventory_full_message_timer = 0
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        self.inventory_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/inventory_screen.png").convert_alpha(), (1100, 600))
        self.crafting_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/crafting_screen.png").convert_alpha(), (1100, 600))
        self.level_up_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/level_up_screen.png").convert_alpha(), (1100, 600))
        self.cat_screen_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/cats_screen.png").convert_alpha(), (1100, 600))

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
        first_slot_x = hotbar_x + 6
        slot_y = hotbar_y + 6
        slot_spacing = 68
        
        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            
            if i == self.selected_hotbar_slot:
                highlight_surface = pygame.Surface((self.slot_size + 8, self.slot_size + 8), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (255, 255, 255, 150), (0, 0, self.slot_size + 8, self.slot_size + 8), 3)
                screen.blit(highlight_surface, (x - 6, y - 6))
            
            slot = self.hotbar_slots[i]
            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))
                        
                        stack_weight = round(quantity * item["weight"], 1)
                        weight_text = font.render(str(stack_weight), True, (200, 200, 50))
                        screen.blit(weight_text, (x + 38, y + 4))
                        
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
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 17
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

            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]

                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))
                        
                        stack_weight = round(quantity * item["weight"], 1)
                        self.total_inventory_weight += stack_weight
                        
                        weight_text = font.render(str(stack_weight), True, (200, 200, 50))
                        screen.blit(weight_text, (x + 38, y + 4))
                        
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

inventory = Inventory(64)