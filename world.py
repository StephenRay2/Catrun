import pygame
import random
import time
import math
import copy
from debug import font_path, font

screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
state = "menu"

def collect_multiple_resources(resource_list, player=None):
    all_resources = []
    for resource_data in resource_list:
        if isinstance(resource_data, dict):
            resource_name = resource_data["name"]
            amount = resource_data["amount"]
            all_resources.extend([resource_name] * amount)
        else:
            all_resources.append(resource_data)
    
    if player:
        total_exp = len(all_resources) * collect_experience
        player.experience += total_exp
        player.exp_total += total_exp
    
    return all_resources

num_lavaponds = 30
num_ponds = 200
num_rocks = 1500
num_boulders = 200
num_bushes = 400
num_grassland_trees = 400
num_savannah_trees = 50
num_beach_trees = 50
num_grasses = 1000
num_sticks = 500
num_stones = 500
num_savannah_grasses = 1600
num_mushrooms = 200
num_dead_bushes = 300
num_fruit_plants = 300
num_fire_ferns = 50
num_frost_ferns = 50
num_gemstone_rocks = 15
num_metal_ore_rocks = 50
num_metal_vein_rocks = 50
num_gold_ore_rocks = 50
num_gold_vein_rocks = 50
num_marsh_reeds = 1000
num_salt_banks = 20
num_clay_banks = 35
num_snow_banks = 20
num_sand_banks = 20

rocks = []
metal_ore_rocks = []
metal_vein_rocks = []
gold_ore_rocks = []
gold_vein_rocks = []
dead_bushes = []
grasses = []
stones = []
boulders = []
berry_bushes = []
trees = []
sticks = []
savannah_grasses = []
mushrooms = []
fruit_plants = []
ferns = []
ponds = []
lavas = []
gemstone_rocks = []
dropped_items = []
marsh_reeds = []
banks = []
spawn_min_x = 0
spawn_max_x = 0


pond_images = ["assets/sprites/biomes/grassland/pond1.png", "assets/sprites/biomes/grassland/pond2.png", "assets/sprites/biomes/grassland/pond3.png", "assets/sprites/biomes/grassland/pond4.png", "assets/sprites/biomes/grassland/pond5.png", "assets/sprites/biomes/grassland/pond6.png", "assets/sprites/biomes/grassland/pond7.png", "assets/sprites/biomes/grassland/pond8.png", "assets/sprites/biomes/grassland/pond9.png", "assets/sprites/biomes/grassland/pond10.png"]

lava_pond_images = ["assets/sprites/biomes/lavastone/lavapond1.png", "assets/sprites/biomes/lavastone/lavapond2.png", "assets/sprites/biomes/lavastone/lavapond3.png", "assets/sprites/biomes/lavastone/lavapond4.png", "assets/sprites/biomes/lavastone/lavapond5.png", "assets/sprites/biomes/lavastone/lavapond6.png", "assets/sprites/biomes/lavastone/lavapond7.png", "assets/sprites/biomes/lavastone/lavapond8.png", "assets/sprites/biomes/lavastone/lavapond9.png", "assets/sprites/biomes/lavastone/lavapond10.png"]

rock_images = ["assets/sprites/biomes/grassland/Rock1.png", "assets/sprites/biomes/grassland/Rock2.png", "assets/sprites/biomes/grassland/Rock3.png", "assets/sprites/biomes/grassland/Rock4.png", "assets/sprites/biomes/grassland/Rock6.png"]

metal_ore_images = ["assets/sprites/biomes/grassland/MetalOreRock1.png", "assets/sprites/biomes/grassland/MetalOreRock2.png", "assets/sprites/biomes/grassland/MetalOreRock3.png"]

metal_vein_images = ["assets/sprites/biomes/grassland/MetalVeinRock1.png", "assets/sprites/biomes/grassland/MetalVeinRock2.png", "assets/sprites/biomes/grassland/MetalVeinRock3.png"]

gold_ore_images = ["assets/sprites/biomes/grassland/GoldOreRock1.png", "assets/sprites/biomes/grassland/GoldOreRock2.png", "assets/sprites/biomes/grassland/GoldOreRock3.png"]

gold_vein_images = ["assets/sprites/biomes/grassland/GoldVeinRock1.png", "assets/sprites/biomes/grassland/GoldVeinRock2.png", "assets/sprites/biomes/grassland/GoldVeinRock3.png"]


grassland_tree_types = [
    {"type": "Apple Tree", "image": "assets/sprites/biomes/grassland/AppleTree.png", "bare_image": "assets/sprites/biomes/grassland/BareAppleTree.png", "fruit": "Apples", "wood": "Apple Wood", "width" : 64, "height" : 128},
    {"type": "Duskwood Tree", "image": "assets/sprites/biomes/grassland/DuskwoodTree.png", "bare_image": None, "fruit": None, "wood": "Dusk Wood", "width" : 64, "height" : 128},
    {"type": "Fir Tree", "image": "assets/sprites/biomes/grassland/FirTree.png", "bare_image": None, "fruit": None, "wood": "Fir Wood", "width" : 64, "height" : 128},
    {"type": "Oak Tree", "image": "assets/sprites/biomes/grassland/OakTree.png", "bare_image": None, "fruit": None, "wood": "Oak Wood", "width" : 64, "height" : 128}, 
    {"type": "Willow Tree", "image": "assets/sprites/biomes/marsh/WillowTree.png", "bare_image": None, "fruit": None, "wood": "Willow Wood", "width" : 128, "height" : 128}
]

savannah_tree_types = [
    {"type": "Orange Tree", "image": "assets/sprites/biomes/savannah/OrangeTree.png", "bare_image": "assets/sprites/biomes/savannah/BareOrangeTree.png", "fruit": "Oranges", "wood": "Orange Wood", "width" : 96, "height" : 96},
    {"type": "Olive Tree", "image": "assets/sprites/biomes/savannah/OliveTree.png", "bare_image": "assets/sprites/biomes/savannah/BareOliveTree.png", "fruit": "Olives", "wood": "Olive Wood", "width" : 96, "height" : 128}
]

beach_tree_types = [{"type": "Palm Tree", "image": "assets/sprites/biomes/beach/PalmTree.png", "bare_image": "assets/sprites/biomes/beach/BarePalmTree.png", "fruit": "Coconuts", "wood": "Palm Wood", "width" : 64, "height" : 128}]

snowy_tree_types = [
    {"type": "Snowy Oak Tree", "image": "assets/sprites/biomes/snow/SnowyOakTree.png", "bare_image": None, "fruit": None, "wood": "Oak Wood", "width": 64, "height": 128},
    {"type": "Snowy Fir Tree", "image": "assets/sprites/biomes/snow/SnowyFirTree.png", "bare_image": None, "fruit": None, "wood": "Fir Wood", "width": 64, "height": 128},
]

fruit_plant_types = [{"type": "Pineapple", "image": "assets/sprites/biomes/grassland/PineapplePlant.png", "bare_image": "assets/sprites/biomes/grassland/BarePineapplePlant.png", "fruit": "Pineapple", "resource": "Fiber", "width" : 64, "height" : 64},
{"type": "Watermelon", "image": "assets/sprites/biomes/grassland/WatermelonPlant.png", "bare_image": "assets/sprites/biomes/grassland/BareWatermelonPlant.png", "fruit": "Watermelon", "resource": "Fiber", "width" : 32, "height" : 32}]

boulder_images = ["assets/sprites/biomes/grassland/Boulder1.png", "assets/sprites/biomes/grassland/Boulder2.png", "assets/sprites/biomes/grassland/Boulder3.png", "assets/sprites/biomes/grassland/Boulder4.png", "assets/sprites/biomes/grassland/Boulder5.png", "assets/sprites/biomes/grassland/Boulder6.png", "assets/sprites/biomes/grassland/Boulder7.png", ]

snowy_rock_images = ["assets/sprites/biomes/snow/SnowyRock1.png", "assets/sprites/biomes/snow/SnowyRock2.png", "assets/sprites/biomes/snow/SnowyRock3.png", "assets/sprites/biomes/snow/SnowyRock4.png", "assets/sprites/biomes/snow/SnowyRock5.png", "assets/sprites/biomes/snow/SnowyRock6.png"]

snowy_boulder_images = ["assets/sprites/biomes/snow/SnowyBoulder1.png", "assets/sprites/biomes/snow/SnowyBoulder2.png", "assets/sprites/biomes/snow/SnowyBoulder3.png", "assets/sprites/biomes/snow/SnowyBoulder4.png", "assets/sprites/biomes/snow/SnowyBoulder5.png", "assets/sprites/biomes/snow/SnowyBoulder6.png", "assets/sprites/biomes/snow/SnowyBoulder7.png"]

snowy_stone_data = [
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image1": "assets/sprites/biomes/snow/SnowyStone1.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image2": "assets/sprites/biomes/snow/SnowyStone2.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image3": "assets/sprites/biomes/snow/SnowyStone3.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image4": "assets/sprites/biomes/snow/SnowyStone4.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image5": "assets/sprites/biomes/snow/SnowyStone5.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image6": "assets/sprites/biomes/snow/SnowyStone6.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image7": "assets/sprites/biomes/snow/SnowyStone7.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image8": "assets/sprites/biomes/snow/SnowyStone8.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image9": "assets/sprites/biomes/snow/SnowyStone9.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image10": "assets/sprites/biomes/snow/SnowyStone10.png"}
]

redrock_rock_images = [
    "assets/sprites/biomes/redrock/RedrockRock1.png",
    "assets/sprites/biomes/redrock/RedrockRock2.png",
    "assets/sprites/biomes/redrock/RedrockRock3.png",
    "assets/sprites/biomes/redrock/RedrockRock4.png",
    "assets/sprites/biomes/redrock/RedrockRock5.png",
    "assets/sprites/biomes/redrock/RedrockRock6.png",
]

redrock_boulder_images = [
    "assets/sprites/biomes/redrock/RedrockBoulder1.png",
    "assets/sprites/biomes/redrock/RedrockBoulder2.png",
    "assets/sprites/biomes/redrock/RedrockBoulder3.png",
    "assets/sprites/biomes/redrock/RedrockBoulder4.png",
    "assets/sprites/biomes/redrock/RedrockBoulder5.png",
    "assets/sprites/biomes/redrock/RedrockBoulder6.png",
    "assets/sprites/biomes/redrock/RedrockBoulder7.png",
]

berry_bush_types = [
    {"image": "assets/sprites/biomes/grassland/BloodBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareBloodBerryBush.png", "berry": "Blood Berries", "resource": "Sticks"},
    {"image": "assets/sprites/biomes/grassland/DawnBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareDawnBerryBush.png", "berry": "Dawn Berries", "resource": "Sticks"},
    {"image": "assets/sprites/biomes/grassland/DuskBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareDuskBerryBush.png", "berry": "Dusk Berries", "resource": "Sticks"},
    {"image": "assets/sprites/biomes/grassland/SunBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareSunBerryBush.png", "berry": "Sun Berries", "resource": "Sticks"},
    {"image": "assets/sprites/biomes/grassland/TealBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareTealBerryBush.png", "berry": "Teal Berries", "resource": "Sticks"},
    {"image": "assets/sprites/biomes/grassland/TwilightDrupesBush.png", "bare_image": "assets/sprites/biomes/grassland/BareTwilightDrupesBush.png", "berry": "Twilight Drupes", "resource": "Sticks"},
    {"image": "assets/sprites/biomes/grassland/VioBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareVioBerryBush.png", "berry": "Vio Berries", "resource": "Sticks"},
]

dead_bush_data = [
    {"resource": "Sticks", "icon": "assets/sprites/items/Sticks.png", "image": "assets/sprites/biomes/grassland/DeadBush1.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Sticks.png", "image": "assets/sprites/biomes/grassland/DeadBush2.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Sticks.png", "image": "assets/sprites/biomes/grassland/DeadBush3.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Sticks.png", "image": "assets/sprites/biomes/grassland/DeadBush4.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Sticks.png", "image": "assets/sprites/biomes/grassland/DeadBush5.png"},
]

stick_data = [
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image1": "assets/sprites/biomes/grassland/Stick1.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image2": "assets/sprites/biomes/grassland/Stick2.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image3": "assets/sprites/biomes/grassland/Stick3.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image4": "assets/sprites/biomes/grassland/Stick4.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image5": "assets/sprites/biomes/grassland/Stick5.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image6": "assets/sprites/biomes/grassland/Stick6.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image7": "assets/sprites/biomes/grassland/Stick7.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image8": "assets/sprites/biomes/grassland/Stick8.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image9": "assets/sprites/biomes/grassland/Stick9.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image10": "assets/sprites/biomes/grassland/Stick10.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image11": "assets/sprites/biomes/grassland/Stick11.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image12": "assets/sprites/biomes/grassland/Stick12.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image13": "assets/sprites/biomes/grassland/Stick13.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image14": "assets/sprites/biomes/grassland/Stick14.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image15": "assets/sprites/biomes/grassland/Stick15.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image16": "assets/sprites/biomes/grassland/Stick16.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image17": "assets/sprites/biomes/grassland/Stick17.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image18": "assets/sprites/biomes/grassland/Stick18.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image19": "assets/sprites/biomes/grassland/Stick19.png"},
    {"resource": "Sticks", "icon": "assets/sprites/items/Stick.png", "image20": "assets/sprites/biomes/grassland/Stick20.png"}
 ]

stone_data = [
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image1": "assets/sprites/biomes/grassland/Stone1.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image2": "assets/sprites/biomes/grassland/Stone2.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image3": "assets/sprites/biomes/grassland/Stone3.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image4": "assets/sprites/biomes/grassland/Stone4.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image5": "assets/sprites/biomes/grassland/Stone5.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image6": "assets/sprites/biomes/grassland/Stone6.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image7": "assets/sprites/biomes/grassland/Stone7.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image8": "assets/sprites/biomes/grassland/Stone8.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image9": "assets/sprites/biomes/grassland/Stone9.png"},
    {"resource": "Stone", "icon": "assets/sprites/items/Stone.png", "image10": "assets/sprites/biomes/grassland/Stone10.png"}
]

redrock_stone_data = [
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image1": "assets/sprites/biomes/grassland/RedrockStone1.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image2": "assets/sprites/biomes/grassland/RedrockStone2.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image3": "assets/sprites/biomes/grassland/RedrockStone3.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image4": "assets/sprites/biomes/grassland/RedrockStone4.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image5": "assets/sprites/biomes/grassland/RedrockStone5.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image6": "assets/sprites/biomes/grassland/RedrockStone6.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image7": "assets/sprites/biomes/grassland/RedrockStone7.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image8": "assets/sprites/biomes/grassland/RedrockStone8.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image9": "assets/sprites/biomes/grassland/RedrockStone9.png"},
    {"resource": "Redrock Stone", "icon": "assets/sprites/items/RedrockStone.png", "image10": "assets/sprites/biomes/grassland/RedrockStone10.png"}
]

mushroom_data = [
    {"resource": "Poisonous Mushroom", "icon": "assets/sprites/items/PoisonousMushroom.png", "image1": "assets/sprites/biomes/grassland/PoisonousMushroom.png"}, 
    {"resource": "Mushroom", "icon": "assets/sprites/items/Mushroom.png", "image1": "assets/sprites/biomes/grassland/Mushroom.png"}, 
    {"resource": "Dawnshroom", "icon": "assets/sprites/items/Dawnshroom.png", "image1": "assets/sprites/biomes/grassland/Dawnshroom.png"}, 
    {"resource": "Duskshroom", "icon": "assets/sprites/items/Duskshroom.png", "image1": "assets/sprites/biomes/grassland/Duskshroom.png"}
]

grass_data = [
    {"resource": "Fiber", "icon": "assets/sprites/items/Grass.png", "image1": "assets/sprites/biomes/grassland/Grass1.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/Grass.png", "image2": "assets/sprites/biomes/grassland/Grass2.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/Grass.png", "image3": "assets/sprites/biomes/grassland/Grass3.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/Grass.png", "image4": "assets/sprites/biomes/grassland/Grass4.png"}
]

savannah_grass_data = [
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image1": "assets/sprites/biomes/savannah/SavannahGrass1.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image2": "assets/sprites/biomes/savannah/SavannahGrass2.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image3": "assets/sprites/biomes/savannah/SavannahGrass3.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image4": "assets/sprites/biomes/savannah/SavannahGrass4.png"}
]

fern_data = [{"image": "assets/sprites/biomes/lavastone/FireFern.png", "resource": "Fire Fern Leaf", "biome" : "lavastone"}, 
{"image": "assets/sprites/biomes/snow/FrostFern.png", "resource": "Frost Fern Leaf", "biome" : "snow"}]

collect_experience = 1
harvest_experience = 1.5

class Liquid(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size, animation_frames=None):
        super().__init__()
        self.size = size
        self.animation_frames = []
        
        if animation_frames:
            for frame_path in animation_frames:
                frame = pygame.transform.scale(
                    pygame.image.load(frame_path).convert_alpha(), size
                )
                self.animation_frames.append(frame)
        else:
            single_image = pygame.transform.scale(
                pygame.image.load(image).convert_alpha(), size
            )
            self.animation_frames.append(single_image)
        
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1
        
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.destroyed = False
        self.resource = []
        self.mask = pygame.mask.from_surface(self.image)


    def update_animation(self, dt):
        if len(self.animation_frames) > 1:
            self.animation_timer += dt / 2
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame]
                self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def get_collision_rect(self, cam_x):
        mask_rect = self.mask.get_bounding_rects()
        if mask_rect:
            pixel_rect = mask_rect[0]
            return pygame.Rect(
                self.rect.x + pixel_rect.x - cam_x,
                self.rect.y + pixel_rect.y - 40,
                pixel_rect.width,
                pixel_rect.height
            )
        return self.rect.copy()
    
    def collect(self, player=None):
        if not self.destroyed:
            resource_collected = min(self.resource_amount, (1 * player.attack))
            self.resource_amount -= resource_collected
            
            if self.resource_amount <= 0:
                self.destroyed = True
            gain = harvest_experience * resource_collected
            player.experience += gain
            player.exp_total += gain

            # Tamed cats gain 10% of any EXP the player earns from harvesting.
            try:
                from mob_placement import cats as world_cats
                share = max(0, gain * 0.1)
                if share > 0:
                    for cat in world_cats:
                        if getattr(cat, "tamed", False):
                            cat.gain_experience(share)
            except Exception:
                pass
            return [self.resource] * resource_collected
        return []
    
class Pond(Liquid):
    def __init__(self, x, y):
        random_x = random.randint(160, 250)
        random_y = random.randint(100, 140)
        super().__init__(pond_images[0], x, y, (random_x, random_y), animation_frames=pond_images)
        self.resource = "Water"
        self.resource_amount = 100
        self.liquid_type = "water"
    
    def collect_from_pond(self, player=None, container_item=None):
        """Collect water from pond if holding a container"""
        if not self.destroyed and container_item:
            from inventory import items_list
            
            container_name = container_item.get("item_name", "")
            item_def = None
            for item in items_list:
                if item.get("item_name") == container_name:
                    item_def = item
                    break
            
            if item_def and "container" in item_def.get("tags", []):
                resource_collected = min(self.resource_amount, 1)
                self.resource_amount -= resource_collected
                
                if self.resource_amount <= 0:
                    self.destroyed = True
                
                if container_name == "Wooden Cup":
                    return ["Small Water"] * resource_collected
                elif container_name == "Glass Bottle":
                    return ["Medium Glass Water"] * resource_collected
                elif container_name == "Metal Bucket":
                    return ["Waterbucket"] * resource_collected
                elif container_name == "Large Metal Canteen":
                    return ["Large Metal Water"] * resource_collected
                elif container_name == "Waterskin":
                    return ["Filled Waterskin"] * resource_collected
        return []

class Lavapond(Liquid):
    def __init__(self, x, y):
        random_x = random.randint(200, 300)
        random_y = random.randint(140, 180)
        super().__init__(lava_pond_images[0], x, y, (random_x, random_y), animation_frames=lava_pond_images)
        self.resource = "Lavabucket"
        self.resource_amount = 100
        self.liquid_type = "lava"
    
    def collect_from_lava(self, player=None, container_item=None):
        """Collect lava from lavapond if holding a metal container"""
        if not self.destroyed and container_item:
            from inventory import items_list
            
            container_name = container_item.get("item_name", "")
            item_def = None
            for item in items_list:
                if item.get("item_name") == container_name:
                    item_def = item
                    break
            
            if item_def and "metal_container" in item_def.get("tags", []):
                resource_collected = min(self.resource_amount, 1)
                self.resource_amount -= resource_collected
                
                if self.resource_amount <= 0:
                    self.destroyed = True
                
                return ["Lavabucket"] * resource_collected
        return []



class Solid(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(), size
        )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.destroyed = False
        self.resource = []

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def get_collision_rect(self, cam_x):
        return pygame.Rect(
            self.rect.x - cam_x + 10,
            self.rect.y + (self.rect.height * .22),
            self.rect.width - 20,
            self.rect.height - 50
        )
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            power = max(1, int(harvest_power))
            resource_collected = min(self.resource_amount, power)
            self.resource_amount -= resource_collected

            if self.resource_amount <= 0:
                self.destroyed = True
            gain = harvest_experience * resource_collected
            player.experience += gain
            player.exp_total += gain

            try:
                from mob_placement import cats as world_cats
                share = max(0, gain * 0.1)
                if share > 0:
                    for cat in world_cats:
                        if getattr(cat, "tamed", False):
                            cat.gain_experience(share)
            except Exception:
                pass
            return [self.resource] * resource_collected
        return []
    

class CliffSide(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.destroyed = False

        # Collision uses the full drawn area to guarantee a hard boundary.
        self.collision_rect = self.rect.copy()
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def get_collision_rect(self, cam_x):
        return pygame.Rect(
            self.collision_rect.x - cam_x,
            self.collision_rect.y,
            self.collision_rect.width,
            self.collision_rect.height,
        )
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        # Cliffs are immovable boundaries; ignore harvest attempts.
        return []
    

class Rock(Solid):
    def __init__(self, x, y):
        img = random.choice(rock_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(10, 15)
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.07 * special_chance_mult):
            resources.extend(["Flint"] * special_yield)
        if random.random() < min(1.0, 0.05 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        if random.random() < min(1.0, 0.002 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)

        return resources



class Boulder(Solid):
    def __init__(self, x, y):
        img = random.choice(boulder_images)
        super().__init__(img, x, y, (128, 128))
        self.image_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y + 50, 128, 96)
        self.resource = "Stone"
        self.resource_amount = random.randint(40, 80)
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.07 * special_chance_mult):
            resources.extend(["Flint"] * special_yield)
        if random.random() < min(1.0, 0.05 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        if random.random() < min(1.0, 0.002 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)

        return resources


class GemstoneRock(Solid):
    def __init__(self, x, y):
        self.full_image = pygame.transform.scale(
            pygame.image.load("assets/sprites/biomes/grassland/GemstoneRock.png").convert_alpha(), (64, 64)
        )
        self.cracked_image = pygame.transform.scale(
            pygame.image.load("assets/sprites/biomes/grassland/CrackedGemstoneRock.png").convert_alpha(), (64, 64)
        )
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.destroyed = False
        self.resource = None
        self.max_health = 400
        self.resource_amount = self.max_health
        self.has_cracked = False
        
        self.gemstones = [
            "Amethyst", "Aquamarine", "Garnet", "Diamond", "Emerald",
            "Opal", "Pearl", "Ruby", "Sapphire", "Topaz"
        ]
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            power = max(1, int(harvest_power))
            damage = power
            self.resource_amount -= damage
            
            health_percent = self.resource_amount / self.max_health
            if health_percent <= 0.5 and not self.has_cracked:
                self.image = self.cracked_image
                self.has_cracked = True
            
            if self.resource_amount <= 0:
                self.destroyed = True
                chosen_gemstone = random.choice(self.gemstones)
                if player:
                    gain = harvest_experience * 10
                    player.experience += gain
                    player.exp_total += gain

                    try:
                        from mob_placement import cats as world_cats
                        share = max(0, gain * 0.1)
                        if share > 0:
                            for cat in world_cats:
                                if getattr(cat, "tamed", False):
                                    cat.gain_experience(share)
                    except Exception:
                        pass
                return [chosen_gemstone]
            
            return []
        return []


class MetalOreRock(Solid):
    def __init__(self, x, y):
        img = random.choice(metal_ore_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(20, 35)
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.75 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        return resources


class MetalVeinRock(Solid):
    def __init__(self, x, y):
        img = random.choice(metal_vein_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(20, 35)
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.35 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        return resources


class GoldOreRock(Solid):
    def __init__(self, x, y):
        img = random.choice(gold_ore_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(20, 35)
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.75 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)
        return resources


class GoldVeinRock(Solid):
    def __init__(self, x, y):
        img = random.choice(gold_vein_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(20, 35)
    
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.35 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)
        return resources


class BerryBush(pygame.sprite.Sprite):
    def __init__(self, x, y, bush_type):
        super().__init__()
        self.type = bush_type
        self.full_image = pygame.transform.scale(
            pygame.image.load(bush_type["image"]).convert_alpha(), (64, 64)
        )
        self.bare_image = pygame.transform.scale(
            pygame.image.load(bush_type["bare_image"]).convert_alpha(), (64, 64)
        )
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.berry = bush_type["berry"]
        self.amount = random.randint(3, 9)

        self.regrow_time = 200
        self.timer = 0
        self.is_empty = False
        self.destroyed = False
        self.resource = "Sticks"

    def collect(self, player=None):
        if not self.is_empty and self.amount > 0:
            berry_count = self.amount
            self.amount = 0
            self.image = self.bare_image
            self.is_empty = True
            self.timer = 0
            
            resources = [self.berry] * berry_count
            
            if player:
                player.experience += collect_experience * len(resources)
                player.exp_total += collect_experience * len(resources)
            
            return resources
        return []

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            resources = []

            stick_count = random.randint(3, 9)
            resources.extend([self.resource] * stick_count)
            
            if not self.is_empty and self.amount > 0:
                resources.extend([self.berry] * self.amount)
            
            self.destroyed = True
            if player:
                player.experience += harvest_experience * len(resources)
                player.exp_total += harvest_experience * len(resources)
            return resources
        return []

    def update(self, dt):
        if self.is_empty:
            self.timer += dt
            if self.timer >= self.regrow_time:
                self.amount = random.randint(3, 9)
                self.image = self.full_image
                self.is_empty = False

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def get_collision_rect(self, cam_x):
        return pygame.Rect(
            self.rect.x - cam_x + 15,
            self.rect.y + (self.rect.height * .35),
            self.rect.width - 35,
            self.rect.height - 40
        )

class DeadBush(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        bush_info = random.choice(dead_bush_data)
        img_path = bush_info["image"]
        self.image = pygame.transform.scale(
            pygame.image.load(img_path).convert_alpha(),
            (64, 64)
        )


        self.rect = self.image.get_rect(topleft=(x, y))
        self.timer = 0
        self.destroyed = False
        self.resource = "Sticks"

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    def get_collision_rect(self, cam_x):
        return pygame.Rect(
            self.rect.x - cam_x + 15,
            self.rect.y + (self.rect.height * 0.4),
            self.rect.width - 35,
            self.rect.height - 40
        )

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            resource_collected = random.randint(3, 9)
            self.destroyed = True
            gain = harvest_experience * resource_collected
            player.experience += gain
            player.exp_total += gain

            try:
                from mob_placement import cats as world_cats
                share = max(0, gain * 0.1)
                if share > 0:
                    for cat in world_cats:
                        if getattr(cat, "tamed", False):
                            cat.gain_experience(share)
            except Exception:
                pass
            return [self.resource] * resource_collected
        return []
    

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tree_type):
        super().__init__()
        self.type = tree_type
        self.full_image = pygame.transform.scale(
            pygame.image.load(tree_type["image"]).convert_alpha(), (tree_type["width"], tree_type["height"])
        )
        if tree_type["bare_image"] is not None:
            self.bare_image = pygame.transform.scale(
                pygame.image.load(tree_type["bare_image"]).convert_alpha(), (tree_type["width"], tree_type["height"])
            )
        else:
            self.bare_image = self.full_image
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_rect = self.rect.copy()
        collision_height = tree_type["height"] // 2
        collision_y_offset = tree_type["height"] - collision_height
        self.rect = pygame.Rect(self.rect.x, self.rect.y + collision_y_offset, tree_type["width"], collision_height)
        
        self.fruit = tree_type["fruit"]
        if tree_type["type"] == "Palm Tree":
            self.amount = random.randint(2, 4) if self.fruit else 0
        else:
            self.amount = random.randint(5, 15) if self.fruit else 0
        self.regrow_time = 400 #(seconds)
        self.timer = 0
        self.is_empty = False
        self.destroyed = False
        self.resource = tree_type["wood"]
        self.wood_amount = random.randint(30, 60)
        
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            power = max(1, int(harvest_power))
            resource_collected = min(self.wood_amount, power)
            self.wood_amount -= resource_collected
            if self.wood_amount <= 0:
                self.destroyed = True
            gain = harvest_experience * resource_collected
            player.experience += gain
            player.exp_total += gain

            try:
                from mob_placement import cats as world_cats
                share = max(0, gain * 0.1)
                if share > 0:
                    for cat in world_cats:
                        if getattr(cat, "tamed", False):
                            cat.gain_experience(share)
            except Exception:
                pass
            return [self.resource] * resource_collected
        return []
        
    def collect(self, player = None):
        if not self.is_empty and self.amount > 0:
            fruit_count = self.amount
            self.amount = 0
            self.image = self.bare_image
            self.is_empty = True
            self.timer = 0
            gain = collect_experience * fruit_count
            player.experience += gain
            player.exp_total += gain

            try:
                from mob_placement import cats as world_cats
                share = max(0, gain * 0.1)
                if share > 0:
                    for cat in world_cats:
                        if getattr(cat, "tamed", False):
                            cat.gain_experience(share)
            except Exception:
                pass
            return [self.fruit] * fruit_count
        return []
        
    def update(self, dt):
        if self.is_empty:
            self.timer += dt
            if self.timer >= self.regrow_time:
                self.amount = random.randint(5, 15)
                self.image = self.full_image
                self.is_empty = False
                
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))
        
    def get_collision_rect(self, cam_x):
        collision_width = int(self.rect.width * 0.4)
        x_offset = (self.rect.width - collision_width) // 2
        
        return pygame.Rect(
            self.rect.x - cam_x + x_offset, self.rect.y + 15, collision_width, self.rect.height - 30
        )
    
class Fern(pygame.sprite.Sprite):
    def __init__(self, x, y, fern_type):
        super().__init__()
        self.biome = fern_type["biome"]
        self.type = fern_type
        self.full_image = pygame.transform.scale(
            pygame.image.load(fern_type["image"]).convert_alpha(), (64, 64)
        )
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.amount = random.randint(3, 6)
        self.timer = 0
        self.destroyed = False
        self.resource = fern_type["resource"]


    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            power = max(1, int(harvest_power))
            resource_collected = min(self.amount, power)
            self.amount -= resource_collected
            if self.amount <= 0:
                self.destroyed = True
            player.experience += harvest_experience * resource_collected
            player.exp_total += harvest_experience * resource_collected
            return [self.resource] * resource_collected
        return []


    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def get_collision_rect(self, cam_x):
        return pygame.Rect(
            self.rect.x - cam_x + 15,
            self.rect.y + (self.rect.height * .4),
            self.rect.width - 35,
            self.rect.height - 40
        )

class FruitPlant(pygame.sprite.Sprite):
    def __init__(self, x, y, plant_type):
        super().__init__()
        self.type = plant_type
        self.full_image = pygame.transform.scale(
            pygame.image.load(plant_type["image"]).convert_alpha(), (plant_type["width"], plant_type["height"])
        )
        if plant_type["bare_image"] is not None:
            self.bare_image = pygame.transform.scale(
                pygame.image.load(plant_type["bare_image"]).convert_alpha(), (plant_type["width"], plant_type["height"])
            )
        else:
            self.bare_image = self.full_image
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_rect = self.rect.copy()
        collision_height = plant_type["height"] // 2
        collision_y_offset = plant_type["height"] - collision_height
        self.rect = pygame.Rect(self.rect.x, self.rect.y + collision_y_offset, plant_type["width"], collision_height)
        
        self.fruit = plant_type["fruit"]
        self.amount = 1 if self.fruit else 0
        self.regrow_time = 400 #(seconds)
        self.timer = 0
        self.is_empty = False
        self.destroyed = False
        self.resource = plant_type["resource"]
        self.resource_amount = random.randint(3, 6)
        
    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed:
            power = max(1, int(harvest_power))
            resource_collected = min(self.resource_amount, power)
            self.resource_amount -= resource_collected
            if self.resource_amount <= 0:
                self.destroyed = True
            player.experience += harvest_experience * resource_collected
            player.exp_total += harvest_experience * resource_collected
            return [self.resource] * resource_collected
        return []
        
    def collect(self, player = None):
        if not self.is_empty and self.amount > 0:
            fruit_count = self.amount
            self.amount = 0
            self.image = self.bare_image
            self.is_empty = True
            self.timer = 0
            player.experience += collect_experience * fruit_count
            player.exp_total += collect_experience * fruit_count
            return [self.fruit] * fruit_count
        return []
        
    def update(self, dt):
        if self.is_empty:
            self.timer += dt
            if self.timer >= self.regrow_time:
                self.amount = 1
                self.image = self.full_image
                self.is_empty = False
                
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))
        
    def get_collision_rect(self, cam_x):
        collision_width = int(self.rect.width * 0.5)
        x_offset = (self.rect.width - collision_width) // 2
        
        return pygame.Rect(
            self.rect.x - cam_x + x_offset, self.rect.y - 15, collision_width, self.rect.height - 10
        )
    

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image, resource, size=(48, 48), image_surface=None):
        super().__init__()
        self.x = x
        self.y = y
        base_image = image_surface
        if base_image is None:
            base_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(base_image, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.resource = resource
        self.amount = 1
        self.destroyed = False

    def get_collision_rect(self, cam_x):
        collision_width = int(self.rect.width * 0.4)
        x_offset = (self.rect.width - collision_width) // 2
        
        return pygame.Rect(
            self.rect.x - cam_x + x_offset, self.rect.y + 10, collision_width, self.rect.height - 40
        )
        

    def collect(self, player=None):
        if not self.destroyed and self.amount > 0:
            self.destroyed = True
            if player:
                player.experience += collect_experience
                player.exp_total += collect_experience
            return [self.resource] * self.amount
        return []

    def draw(self, screen, cam_x):
        if not self.destroyed:
            screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))


class DroppedItem(Collectible):
    ICON_SIZE = 16
    DESPAWN_TIME = 180.0

    @classmethod
    def get_drop_font(cls):
        if not hasattr(cls, '_drop_font'):
            cls._drop_font = pygame.font.Font(font_path, 14)
        return cls._drop_font

    def __init__(self, x, y, resource, icon_path, amount=1, item_instance=None):
        size = (self.ICON_SIZE, self.ICON_SIZE)
        image_surface = None
        if icon_path:
            try:
                image_surface = pygame.image.load(icon_path).convert_alpha()
            except:
                image_surface = None
        if image_surface is None:
            image_surface = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.rect(image_surface, (90, 90, 90, 220), (0, 0, size[0], size[1]), border_radius=6)
        super().__init__(int(x), int(y), icon_path or "", resource, size=size, image_surface=image_surface)
        self.amount = max(1, int(amount))
        self._float_phase = random.random() * math.tau
        self.age = 0.0
        self.item_instance = copy.deepcopy(item_instance) if item_instance else None

    def collect(self, player=None):
        if self.destroyed or self.amount <= 0:
            return []
        self.destroyed = True
        if player:
            player.experience += collect_experience
            player.exp_total += collect_experience
        if self.item_instance:
            return [{"__full_item__": copy.deepcopy(self.item_instance)}]
        return [self.resource] * self.amount

    def draw(self, screen, cam_x):
        if self.destroyed:
            return
        # Floating animation
        t = pygame.time.get_ticks() / 1000.0
        offset_y = int(math.sin(t * 2 + self._float_phase) * 3)

        # Simple shadow ellipse for float effect
        shadow_width = max(8, self.rect.width - 4)
        shadow_height = max(4, self.rect.height // 3)
        shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), shadow_surface.get_rect())
        shadow_x = self.rect.x - cam_x + (self.rect.width - shadow_width) // 2
        shadow_y = self.rect.y + self.rect.height - shadow_height // 2
        screen.blit(shadow_surface, (shadow_x, shadow_y))

        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y + offset_y))
        if self.amount > 1:
            qty_text = self.get_drop_font().render(str(self.amount), True, (255, 255, 255))
            shadow = self.get_drop_font().render(str(self.amount), True, (0, 0, 0))
            text_x = self.rect.x - cam_x + self.rect.width - qty_text.get_width() - 2
            text_y = self.rect.y + self.rect.height - qty_text.get_height() - 4 + offset_y
            screen.blit(shadow, (text_x + 1, text_y + 1))
            screen.blit(qty_text, (text_x, text_y))

    def update_lifetime(self, dt):
        if self.destroyed:
            return
        self.age += dt
        if self.age >= self.DESPAWN_TIME:
            self.destroyed = True

class Stick(Collectible):
    def __init__(self, x, y):
        image_index = random.randint(1, 20)
        image_path = f"assets/sprites/biomes/grassland/Stick{image_index}.png"
        super().__init__(x, y, image_path, "Sticks", size=(40, 40))

class Stone(Collectible):
    def __init__(self, x, y):
        image_index = random.randint(1, 10)
        image_path = f"assets/sprites/biomes/grassland/Stone{image_index}.png"
        super().__init__(x, y, image_path, "Stone", size=(25, 25))

class SnowyStone(Collectible):
    def __init__(self, x, y):
        image_index = random.randint(1, 10)
        image_path = f"assets/sprites/biomes/snow/SnowyStone{image_index}.png"
        super().__init__(x, y, image_path, "Stone", size=(25, 25))

class RedrockStone(Collectible):
    def __init__(self, x, y):
        image_index = random.randint(1, 10)
        image_path = f"assets/sprites/biomes/grassland/Stone{image_index}.png"
        super().__init__(x, y, image_path, "Redrock Stone", size=(25, 25))

class SnowyRock(Solid):
    def __init__(self, x, y):
        img = random.choice(snowy_rock_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(10, 15)

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.07 * special_chance_mult):
            resources.extend(["Flint"] * special_yield)
        if random.random() < min(1.0, 0.05 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        if random.random() < min(1.0, 0.002 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)
        return resources

class RedrockRock(Solid):
    def __init__(self, x, y):
        img = random.choice(redrock_rock_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Redrock Stone"
        self.resource_amount = random.randint(10, 15)

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.07 * special_chance_mult):
            resources.extend(["Flint"] * special_yield)
        if random.random() < min(1.0, 0.05 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        if random.random() < min(1.0, 0.002 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)
        return resources

class SnowyBoulder(Solid):
    def __init__(self, x, y):
        img = random.choice(snowy_boulder_images)
        super().__init__(img, x, y, (128, 128))
        self.image_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y + 50, 128, 96)
        self.resource = "Stone"
        self.resource_amount = random.randint(40, 80)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.07 * special_chance_mult):
            resources.extend(["Flint"] * special_yield)
        if random.random() < min(1.0, 0.05 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        if random.random() < min(1.0, 0.002 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)
        return resources

class RedrockBoulder(Solid):
    def __init__(self, x, y):
        img = random.choice(redrock_boulder_images)
        super().__init__(img, x, y, (128, 128))
        self.image_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y + 50, 128, 96)
        self.resource = "Redrock Stone"
        self.resource_amount = random.randint(40, 80)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        resources = super().harvest(player, harvest_power, special_chance_mult, special_yield_mult)
        special_yield = max(1, int(special_yield_mult))
        if random.random() < min(1.0, 0.07 * special_chance_mult):
            resources.extend(["Flint"] * special_yield)
        if random.random() < min(1.0, 0.05 * special_chance_mult):
            resources.extend(["Raw Metal"] * special_yield)
        if random.random() < min(1.0, 0.002 * special_chance_mult):
            resources.extend(["Raw Gold"] * special_yield)
        return resources
        
class Bank(Solid):
    def __init__(self, image, x, y, resource, resource_amount=40, size=(64, 64)):
        super().__init__(image, x, y, size)
        self.resource = resource
        self.resource_amount = resource_amount

class SaltBank(Bank):
    def __init__(self, x, y):
        super().__init__("assets/sprites/biomes/beach/SaltBank.png", x, y, "Salt", resource_amount=random.randint(20, 40))

class ClayBank(Bank):
    def __init__(self, x, y):
        super().__init__("assets/sprites/biomes/marsh/ClayBank.png", x, y, "Clay", resource_amount=random.randint(20, 40))

class SnowBank(Bank):
    def __init__(self, x, y):
        super().__init__("assets/sprites/biomes/snow/SnowBank.png", x, y, "Snowball", resource_amount=random.randint(20, 40))

class BeachSandBank(Bank):
    def __init__(self, x, y):
        super().__init__("assets/sprites/biomes/beach/BeachSandBank.png", x, y, "Sand", resource_amount=random.randint(20, 40))

class DesertSandBank(Bank):
    def __init__(self, x, y):
        super().__init__("assets/sprites/biomes/desert/DesertSandBank.png", x, y, "Sand", resource_amount=random.randint(20, 40))

class Grass(Collectible):
    def __init__(self, x, y):
        image_index = random.randint(1, 4)
        image_path = f"assets/sprites/biomes/grassland/Grass{image_index}.png"
        super().__init__(x, y, image_path, "Fiber", size=(64, 64))

class SavannahGrass(Collectible):
    def __init__(self, x, y):
        self.amount = random.randint(3, 6)
        image_index = random.randint(1, 4)
        image_path = f"assets/sprites/biomes/savannah/SavannahGrass{image_index}.png"
        super().__init__(x, y, image_path, "Fiber", size=(64, 64))

class MarshReed(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/sprites/biomes/marsh/MarshReed.png", "Marsh Reed", size=(64, 64))

    def draw(self, screen, cam_x):
        if self.destroyed:
            return
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

class Mushroom(Collectible):
    def __init__(self, x, y):
        mushroom_type = random.choice(mushroom_data)
        resource = mushroom_type["resource"]
        image_path = mushroom_type["image1"]
        super().__init__(x, y, image_path, resource, size=(20, 20))



bg_green = pygame.Surface((width, height))
bg_grass = pygame.image.load("assets/sprites/biomes/backgrounds/bg_grass.png").convert()
bg_dirt = pygame.image.load("assets/sprites/biomes/backgrounds/bg_dirt.png").convert()
bg_marsh = pygame.image.load("assets/sprites/biomes/backgrounds/bg_marsh.png").convert()
bg_beach = pygame.image.load("assets/sprites/biomes/backgrounds/bg_beach.png").convert()
bg_desert = pygame.image.load("assets/sprites/biomes/backgrounds/bg_desert.png").convert()
bg_savannah = pygame.image.load("assets/sprites/biomes/backgrounds/bg_savannah.png").convert()
bg_river = pygame.image.load("assets/sprites/biomes/backgrounds/bg_river.png").convert()
bg_mountain = pygame.image.load("assets/sprites/biomes/backgrounds/bg_mountain.png").convert()
bg_duskstone = pygame.image.load("assets/sprites/biomes/backgrounds/bg_duskstone.png").convert()
bg_lavastone = pygame.image.load("assets/sprites/biomes/backgrounds/bg_lavastone.png").convert()
bg_snow = pygame.image.load("assets/sprites/biomes/backgrounds/bg_snow.png").convert()
bg_wasteland = pygame.image.load("assets/sprites/biomes/backgrounds/bg_wasteland.png").convert()
bg_blackstone = pygame.image.load("assets/sprites/biomes/backgrounds/bg_blackstone.png").convert()
bg_redrock = pygame.image.load("assets/sprites/biomes/backgrounds/bg_redrock.png").convert()
bg_valley_raw = pygame.image.load("assets/sprites/biomes/backgrounds/valleybackground.png").convert()
bg_double_valley_raw = pygame.image.load("assets/sprites/biomes/backgrounds/double_valley_background.png").convert()

bg_dirt = pygame.transform.scale(bg_dirt, (width, height))
bg_grass = pygame.transform.scale(bg_grass, (width, height))
bg_marsh = pygame.transform.scale(bg_marsh, (width, height))
bg_beach = pygame.transform.scale(bg_beach, (width, height))
bg_desert = pygame.transform.scale(bg_desert, (width, height))
bg_savannah = pygame.transform.scale(bg_savannah, (width, height))
bg_river = pygame.transform.scale(bg_river, (width, height))
bg_mountain = pygame.transform.scale(bg_mountain, (width, height))
bg_duskstone = pygame.transform.scale(bg_duskstone, (width, height))
bg_lavastone = pygame.transform.scale(bg_lavastone, (width, height))
bg_wasteland = pygame.transform.scale(bg_wasteland, (width, height))
bg_snow = pygame.transform.scale(bg_snow, (width, height))
bg_blackstone = pygame.transform.scale(bg_blackstone, (width, height))
bg_redrock = pygame.transform.scale(bg_redrock, (width, height))
bg_valley = pygame.transform.scale(bg_valley_raw, (width, height))
bg_double_valley = pygame.transform.scale(bg_double_valley_raw, (width, height))
bg_green.fill((0, 120, 0))

cliff_side_left_raw = pygame.image.load("assets/sprites/biomes/backgrounds/CliffSideLeft.png").convert_alpha()
cliff_side_left = pygame.transform.scale(cliff_side_left_raw, (cliff_side_left_raw.get_width(), height))
cliff_side_right = pygame.transform.flip(cliff_side_left, True, False)
CLIFF_SIDE_WIDTH = cliff_side_left.get_width()
# Legacy aliases to avoid touching all downstream references
bg_compact = bg_marsh
bg_sand = bg_beach
bg_riverrock = bg_river
bg_bigrock = bg_mountain

background_image = bg_grass
background_image = pygame.transform.scale(background_image, (width, height))


BACKGROUND_SIZE = background_image.get_width()

tiles = []
for i in range(0, 6):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(6, 20):
    tiles.append((i * BACKGROUND_SIZE, bg_dirt))
for i in range(20, 40):
    tiles.append((i * BACKGROUND_SIZE, bg_marsh))
for i in range(40, 60):
    tiles.append((i * BACKGROUND_SIZE, bg_beach))
for i in range(60, 86):
    tiles.append((i * BACKGROUND_SIZE, bg_savannah))
for i in range(86, 116):
    tiles.append((i * BACKGROUND_SIZE, bg_river))
for i in range(116, 144):
    tiles.append((i * BACKGROUND_SIZE, bg_mountain))
for i in range(144, 150):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(150, 180):
    tiles.append((i * BACKGROUND_SIZE, bg_duskstone))
for i in range(180, 216):
    tiles.append((i * BACKGROUND_SIZE, bg_lavastone))
for i in range(216, 240):
    tiles.append((i * BACKGROUND_SIZE, bg_wasteland))
for i in range(240, 256):
    tiles.append((i * BACKGROUND_SIZE, bg_dirt))
for i in range(256, 290):
    tiles.append((i * BACKGROUND_SIZE, bg_snow))
for i in range(290, 340):
    tiles.append((i * BACKGROUND_SIZE, bg_blackstone))
for i in range(340, 380):
    tiles.append((i * BACKGROUND_SIZE, bg_redrock))
for i in range(380, 390):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(390, 401):
    tiles.append((i * BACKGROUND_SIZE, bg_redrock))
for i in range(401, 421):
    tiles.append((i * BACKGROUND_SIZE, bg_desert))



allowed_rock_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_lavastone, bg_wasteland, bg_blackstone, bg_redrock, bg_desert]

rock_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_rock_tiles]

rock_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 1,
    bg_savannah: 1,
    bg_riverrock: 4,
    bg_bigrock: 4,
    bg_duskstone: 1,
    bg_lavastone: 1,
    bg_snow: 1,
    bg_wasteland: 1,
    bg_blackstone: 1,
    bg_redrock: 10,
    bg_desert: 3
}

weighted_rock_tiles = []
for tile_x, tile_image in tiles:
    weight = rock_weights.get(tile_image, 1)
    weighted_rock_tiles.extend([(tile_x, tile_image)] * weight)


grassland_tree_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah]
savannah_tree_tiles = [bg_savannah]
beach_tree_tiles = [bg_sand]

grassland_tree_weights = {
    bg_grass: 30,
    bg_dirt: 20,
    bg_compact: 10,
    bg_sand: 0,
    bg_savannah: 5,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 1,
    bg_blackstone: 0,
    bg_redrock: 0
}

savannah_tree_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 1,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

beach_tree_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 3,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_grassland_tiles = []
for tile_x, tile_image in tiles:
    if tile_image in grassland_tree_tiles:
        weight = grassland_tree_weights.get(tile_image, 1)
        weighted_grassland_tiles.extend([(tile_x, tile_image)] * weight)

weighted_savannah_tiles = []
for tile_x, tile_image in tiles:
    if tile_image in savannah_tree_tiles:
        weight = savannah_tree_weights.get(tile_image, 1)
        weighted_savannah_tiles.extend([(tile_x, tile_image)] * weight)

weighted_beach_tiles = []
for tile_x, tile_image in tiles:
    if tile_image in beach_tree_tiles:
        weight = beach_tree_weights.get(tile_image, 1)
        weighted_beach_tiles.extend([(tile_x, tile_image)] * weight)


allowed_berry_bush_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah]

berry_bush_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_berry_bush_tiles]

berry_bush_weights = {
    bg_grass: 30,
    bg_dirt: 20,
    bg_compact: 10,
    bg_sand: 0,
    bg_savannah: 10,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 1,
    bg_blackstone: 0,
    bg_redrock: 0

}

weighted_berry_bush_tiles = []
for tile_x, tile_image in tiles:
    weight = berry_bush_weights.get(tile_image, 1)
    weighted_berry_bush_tiles.extend([(tile_x, tile_image)] * weight)



allowed_boulder_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_lavastone, bg_wasteland, bg_blackstone, bg_redrock]
boulder_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_boulder_tiles]

boulder_weights = {
    bg_grass: 2,
    bg_dirt: 4,
    bg_compact: 1,
    bg_savannah: 1,
    bg_riverrock: 4,
    bg_bigrock: 4,
    bg_duskstone: 3,
    bg_lavastone: 1,
    bg_snow: 1,
    bg_wasteland: 3,
    bg_blackstone: 2,
    bg_redrock: 10
}

weighted_boulder_tiles = []
for tile_x, tile_image in tiles:
    weight = boulder_weights.get(tile_image, 1)
    weighted_boulder_tiles.extend([(tile_x, tile_image)] * weight)



allowed_stick_tiles = [bg_grass, bg_dirt, bg_compact, bg_sand, bg_desert, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_wasteland, bg_blackstone, bg_redrock]

stick_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_stick_tiles]

stick_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 1,
    bg_sand: 1,
    bg_desert: 1,
    bg_savannah: 3,
    bg_riverrock: 1,
    bg_bigrock: 1,
    bg_duskstone: 1,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 2,
    bg_blackstone: 1,
    bg_redrock: 1

}

weighted_stick_tiles = []
for tile_x, tile_image in tiles:
    weight = stick_weights.get(tile_image, 1)
    weighted_stick_tiles.extend([(tile_x, tile_image)] * weight)



allowed_stone_tiles = [bg_grass, bg_dirt, bg_compact, bg_sand, bg_desert, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_wasteland, bg_blackstone, bg_redrock]

stone_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_stone_tiles]

stone_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 1,
    bg_sand: 1,
    bg_desert: 1,
    bg_savannah: 3,
    bg_riverrock: 1,
    bg_bigrock: 1,
    bg_duskstone: 1,
    bg_lavastone: 0,
    bg_snow: 1,
    bg_wasteland: 2,
    bg_blackstone: 1,
    bg_redrock: 10

}

weighted_stone_tiles = []
for tile_x, tile_image in tiles:
    weight = stone_weights.get(tile_image, 1)
    weighted_stone_tiles.extend([(tile_x, tile_image)] * weight)



allowed_grass_tiles = [bg_grass, bg_dirt, bg_compact]

grass_weights = {
    bg_grass: 10,
    bg_dirt: 5,
    bg_compact: 3,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_grass_tiles = []
for tile_x, tile_image in tiles:
    weight = grass_weights.get(tile_image, 1)
    weighted_grass_tiles.extend([(tile_x, tile_image)] * weight)

allowed_savannah_grass_tiles = [bg_savannah]

savannah_grass_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 10,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_savannah_grass_tiles = []
for tile_x, tile_image in tiles:
    weight = savannah_grass_weights.get(tile_image, 1)
    weighted_savannah_grass_tiles.extend([(tile_x, tile_image)] * weight)



allowed_mushroom_tiles = [bg_grass, bg_dirt, bg_compact, bg_duskstone, bg_wasteland]

mushroom_weights = {
    bg_grass: 5,
    bg_dirt: 3,
    bg_compact: 2,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 8,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 6,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_mushroom_tiles = []
for tile_x, tile_image in tiles:
    weight = mushroom_weights.get(tile_image, 1)
    weighted_mushroom_tiles.extend([(tile_x, tile_image)] * weight)


allowed_clay_bank_tiles = [bg_marsh, bg_river, bg_mountain, bg_wasteland]
clay_bank_weights = {
    bg_marsh: 4,
    bg_river: 2,
    bg_mountain: 1,
    bg_wasteland: 1
}
weighted_clay_bank_tiles = []
for tile_x, tile_image in tiles:
    weight = clay_bank_weights.get(tile_image, 0)
    if weight > 0:
        weighted_clay_bank_tiles.extend([(tile_x, tile_image)] * weight)

allowed_salt_bank_tiles = [bg_beach]
salt_bank_weights = {
    bg_beach: 1
}
weighted_salt_bank_tiles = []
for tile_x, tile_image in tiles:
    weight = salt_bank_weights.get(tile_image, 0)
    if weight > 0:
        weighted_salt_bank_tiles.extend([(tile_x, tile_image)] * weight)

allowed_beach_sand_bank_tiles = [bg_beach]
allowed_desert_sand_bank_tiles = [bg_desert]
beach_sand_bank_weights = {
    bg_beach: 1
}
desert_sand_bank_weights = {
    bg_desert: 1
}
weighted_beach_sand_bank_tiles = []
weighted_desert_sand_bank_tiles = []
for tile_x, tile_image in tiles:
    weight = beach_sand_bank_weights.get(tile_image, 0)
    if weight > 0:
        weighted_beach_sand_bank_tiles.extend([(tile_x, tile_image)] * weight)
    weight = desert_sand_bank_weights.get(tile_image, 0)
    if weight > 0:
        weighted_desert_sand_bank_tiles.extend([(tile_x, tile_image)] * weight)

allowed_snow_bank_tiles = [bg_snow]
snow_bank_weights = {
    bg_snow: 1
}
weighted_snow_bank_tiles = []
for tile_x, tile_image in tiles:
    weight = snow_bank_weights.get(tile_image, 0)
    if weight > 0:
        weighted_snow_bank_tiles.extend([(tile_x, tile_image)] * weight)


allowed_dead_bush_tiles = [bg_grass, bg_dirt, bg_compact, bg_duskstone, bg_wasteland]

dead_bush_weights = {
    bg_grass: 2,
    bg_dirt: 4,
    bg_compact: 6,
    bg_sand: 4,
    bg_desert: 4,
    bg_savannah: 4,
    bg_riverrock: 4,
    bg_bigrock: 4,
    bg_duskstone: 2,
    bg_lavastone: 2,
    bg_snow: 4,
    bg_wasteland: 6,
    bg_blackstone: 2,
    bg_redrock: 5
}

weighted_dead_bush_tiles = []
for tile_x, tile_image in tiles:
    weight = dead_bush_weights.get(tile_image, 1)
    weighted_dead_bush_tiles.extend([(tile_x, tile_image)] * weight)


fruit_plant_weights = {
    bg_grass: 2,
    bg_dirt: 1,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 5,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_fruit_plant_tiles = []
for tile_x, tile_image in tiles:
    weight = fruit_plant_weights.get(tile_image, 0)
    if weight > 0:
        weighted_fruit_plant_tiles.extend([(tile_x, tile_image)] * weight)


fire_fern_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 5,
    bg_snow: 0,
    bg_wasteland: 1,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_fire_fern_tiles = []
for tile_x, tile_image in tiles:
    weight = fire_fern_weights.get(tile_image, 0)
    if weight > 0:
        weighted_fire_fern_tiles.extend([(tile_x, tile_image)] * weight)

frost_fern_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 5,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_frost_fern_tiles = []
for tile_x, tile_image in tiles:
    weight = frost_fern_weights.get(tile_image, 0)
    if weight > 0:
        weighted_frost_fern_tiles.extend([(tile_x, tile_image)] * weight)

weighted_snow_tiles = []
for tile_x, tile_image in tiles:
    if tile_image == bg_snow:
        weighted_snow_tiles.append((tile_x, tile_image))

weighted_redrock_tiles = []
for tile_x, tile_image in tiles:
    if tile_image == bg_redrock:
        weighted_redrock_tiles.append((tile_x, tile_image))


def generate_world():
    global rocks, dead_bushes, grasses, stones, boulders, berry_bushes, trees, sticks, savannah_grasses, mushrooms, fruit_plants, ferns, ponds, lavas, gemstone_rocks, metal_ore_rocks, metal_vein_rocks, gold_ore_rocks, gold_vein_rocks, dropped_items, marsh_reeds, spawn_min_x, spawn_max_x
    
    rocks.clear()
    dead_bushes.clear()
    grasses.clear()
    stones.clear()
    boulders.clear()
    berry_bushes.clear()
    trees.clear()
    sticks.clear()
    savannah_grasses.clear()
    mushrooms.clear()
    fruit_plants.clear()
    ferns.clear()
    ponds.clear()
    lavas.clear()
    gemstone_rocks.clear()
    metal_ore_rocks.clear()
    metal_vein_rocks.clear()
    gold_ore_rocks.clear()
    gold_vein_rocks.clear()
    dropped_items.clear()
    marsh_reeds.clear()
    banks.clear()

    map_end_x = tiles[-1][0] + BACKGROUND_SIZE
    half_cliff = CLIFF_SIDE_WIDTH // 2
    left_cliff_x = -half_cliff - 10
    right_cliff_x = map_end_x - half_cliff + 5
    rocks.append(CliffSide(cliff_side_left, left_cliff_x))
    rocks.append(CliffSide(cliff_side_right, right_cliff_x))

    # Keep spawns away from the first/last 100px of the map.
    spawn_min_x = 100
    spawn_max_x = map_end_x - 100

    def rand_x_for_tile(tile_x, margin=64):
        min_x = max(tile_x, spawn_min_x)
        max_x = min(tile_x + BACKGROUND_SIZE - margin, spawn_max_x)
        if max_x < min_x:
            return None
        return random.randint(min_x, max_x)

    def rand_x_global(margin=64):
        min_x = spawn_min_x
        max_x = spawn_max_x - margin
        if max_x < min_x:
            return None
        return random.randint(min_x, max_x)

    for _ in range(num_rocks):
        tile_x, tile_image = random.choice(weighted_rock_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        if tile_image == bg_snow:
            rocks.append(SnowyRock(x, y))
        elif tile_image == bg_redrock:
            rocks.append(RedrockRock(x, y))
        else:
            rocks.append(Rock(x, y))

    for _ in range(num_boulders):
        tile_x, tile_image = random.choice(weighted_boulder_tiles)
        x = rand_x_for_tile(tile_x, margin=128)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        if tile_image == bg_snow:
            boulders.append(SnowyBoulder(x, y))
        elif tile_image == bg_redrock:
            boulders.append(RedrockBoulder(x, y))
        else:
            boulders.append(Boulder(x, y))
    
    for _ in range(num_gemstone_rocks):
        x = rand_x_global()
        if x is None:
            continue
        y = random.randint(0, height - 64)
        gemstone_rocks.append(GemstoneRock(x, y))
    
    for _ in range(num_metal_ore_rocks):
        tile_x, tile_image = random.choice(weighted_rock_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        metal_ore_rocks.append(MetalOreRock(x, y))
    
    for _ in range(num_metal_vein_rocks):
        tile_x, tile_image = random.choice(weighted_rock_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        metal_vein_rocks.append(MetalVeinRock(x, y))
    
    for _ in range(num_gold_ore_rocks):
        tile_x, tile_image = random.choice(weighted_rock_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        gold_ore_rocks.append(GoldOreRock(x, y))
    
    for _ in range(num_gold_vein_rocks):
        tile_x, tile_image = random.choice(weighted_rock_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        gold_vein_rocks.append(GoldVeinRock(x, y))
    
    for _ in range(num_bushes):
        tile_x, tile_image = random.choice(weighted_berry_bush_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        berry_bush_type = random.choice(berry_bush_types)
        berry_bushes.append(BerryBush(x, y, berry_bush_type))
    
    def spawn_trees(tree_list, tree_types, weighted_tiles, num_trees, height):
        for _ in range(num_trees):
            tile_x, tile_image = random.choice(weighted_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 80)
            tree_type = random.choice(tree_types)
            tree_list.append(Tree(x, y, tree_type))

    spawn_trees(trees, grassland_tree_types, weighted_grassland_tiles, num_grassland_trees, height)
    spawn_trees(trees, savannah_tree_types, weighted_savannah_tiles, num_savannah_trees, height)
    spawn_trees(trees, beach_tree_types, weighted_beach_tiles, num_beach_trees, height)

    weighted_snow_tree_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image == bg_snow]
    if weighted_snow_tree_tiles:
        num_snow_trees = 50
        spawn_trees(trees, snowy_tree_types, weighted_snow_tree_tiles, num_snow_trees, height)


    for _ in range(num_sticks):
        tile_x, tile_image = random.choice(weighted_stick_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        sticks.append(Stick(x, y))
    
  
    for _ in range(num_stones):
        tile_x, tile_image = random.choice(weighted_stone_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        if tile_image == bg_snow:
            stones.append(SnowyStone(x, y))
        elif tile_image == bg_redrock:
            stones.append(RedrockStone(x, y))
        else:
            stones.append(Stone(x, y))
    
    
    for _ in range(num_grasses):
        tile_x, tile_image = random.choice(weighted_grass_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        grasses.append(Grass(x, y))
   
    for _ in range(num_savannah_grasses):
        tile_x, tile_image = random.choice(weighted_savannah_grass_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        savannah_grasses.append(SavannahGrass(x, y))

    weighted_compact_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image == bg_compact]
    for _ in range(num_marsh_reeds):
        tile_x, tile_image = random.choice(weighted_compact_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        marsh_reeds.append(MarshReed(x, y))

    for _ in range(num_mushrooms):
        tile_x, tile_image = random.choice(weighted_mushroom_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        mushrooms.append(Mushroom(x, y))
    
    
    for _ in range(num_dead_bushes):
        tile_x, tile_image = random.choice(weighted_dead_bush_tiles)
        x = rand_x_for_tile(tile_x)
        if x is None:
            continue
        y = random.randint(0, height - 64)
        dead_bushes.append(DeadBush(x, y))

    if weighted_clay_bank_tiles:
        for _ in range(num_clay_banks):
            tile_x, tile_image = random.choice(weighted_clay_bank_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            banks.append(ClayBank(x, y))

    if weighted_salt_bank_tiles:
        for _ in range(num_salt_banks):
            tile_x, tile_image = random.choice(weighted_salt_bank_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            banks.append(SaltBank(x, y))

    if weighted_beach_sand_bank_tiles:
        for _ in range(max(1, num_sand_banks // 2)):
            tile_x, tile_image = random.choice(weighted_beach_sand_bank_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            banks.append(BeachSandBank(x, y))

    if weighted_desert_sand_bank_tiles:
        for _ in range(num_sand_banks - max(1, num_sand_banks // 2)):
            tile_x, tile_image = random.choice(weighted_desert_sand_bank_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            banks.append(DesertSandBank(x, y))

    if weighted_snow_bank_tiles:
        for _ in range(num_snow_banks):
            tile_x, tile_image = random.choice(weighted_snow_bank_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            banks.append(SnowBank(x, y))

    if weighted_fruit_plant_tiles:
        for _ in range(num_fruit_plants):
            tile_x, tile_image = random.choice(weighted_fruit_plant_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            plant_type = random.choice(fruit_plant_types)
            fruit_plants.append(FruitPlant(x, y, plant_type))
    
    if weighted_fire_fern_tiles:
        for _ in range(num_fire_ferns):
            tile_x, tile_image = random.choice(weighted_fire_fern_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            ferns.append(Fern(x, y, fern_data[0]))

    if weighted_frost_fern_tiles:
        for _ in range(num_frost_ferns):
            tile_x, tile_image = random.choice(weighted_frost_fern_tiles)
            x = rand_x_for_tile(tile_x)
            if x is None:
                continue
            y = random.randint(0, height - 64)
            ferns.append(Fern(x, y, fern_data[1]))
    
    lavastone_start = 180 * BACKGROUND_SIZE
    lavastone_end = 216 * BACKGROUND_SIZE
    
    for _ in range(num_ponds):
        valid = False
        x = None
        while not valid:
            x = rand_x_global(margin=128)
            if x is None:
                break
            if not (lavastone_start <= x < lavastone_end):
                valid = True
        if x is not None and valid:
            y = random.randint(0, height - 128)
            ponds.append(Pond(x, y))
    for _ in range(num_lavaponds):
        min_x = max(int(lavastone_start), int(spawn_min_x))
        max_x = min(int(lavastone_end - 128), int(spawn_max_x))
        if max_x < min_x:
            continue
        x = random.randint(min_x, max_x)
        y = random.randint(0, height - 128)
        lavas.append(Lavapond(x, y))
    
    return rocks, boulders, berry_bushes, trees, sticks, stones, grasses, savannah_grasses, mushrooms, dead_bushes, fruit_plants, ferns, ponds, lavas, gemstone_rocks, metal_ore_rocks, metal_vein_rocks, gold_ore_rocks, gold_vein_rocks, marsh_reeds
