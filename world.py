import pygame
import random
import time

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

rocks = []
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


pond_images = ["assets/sprites/biomes/grassland/pond1.png", "assets/sprites/biomes/grassland/pond2.png", "assets/sprites/biomes/grassland/pond3.png", "assets/sprites/biomes/grassland/pond4.png", "assets/sprites/biomes/grassland/pond5.png", "assets/sprites/biomes/grassland/pond6.png", "assets/sprites/biomes/grassland/pond7.png", "assets/sprites/biomes/grassland/pond8.png", "assets/sprites/biomes/grassland/pond9.png", "assets/sprites/biomes/grassland/pond10.png"]

lava_pond_images = ["assets/sprites/biomes/lavastone/lavapond1.png", "assets/sprites/biomes/lavastone/lavapond2.png", "assets/sprites/biomes/lavastone/lavapond3.png", "assets/sprites/biomes/lavastone/lavapond4.png", "assets/sprites/biomes/lavastone/lavapond5.png", "assets/sprites/biomes/lavastone/lavapond6.png", "assets/sprites/biomes/lavastone/lavapond7.png", "assets/sprites/biomes/lavastone/lavapond8.png", "assets/sprites/biomes/lavastone/lavapond9.png", "assets/sprites/biomes/lavastone/lavapond10.png"]

rock_images = ["assets/sprites/biomes/grassland/Rock1.png", "assets/sprites/biomes/grassland/Rock2.png", "assets/sprites/biomes/grassland/Rock3.png", "assets/sprites/biomes/grassland/Rock4.png", "assets/sprites/biomes/grassland/Rock6.png"]


grassland_tree_types = [
    {"type": "Apple Tree", "image": "assets/sprites/biomes/grassland/AppleTree.png", "bare_image": "assets/sprites/biomes/grassland/BareAppleTree.png", "fruit": "Apples", "wood": "Apple Wood", "width" : 64, "height" : 128},
    {"type": "Duskwood Tree", "image": "assets/sprites/biomes/grassland/DuskwoodTree.png", "bare_image": None, "fruit": None, "wood": "Dusk Wood", "width" : 64, "height" : 128},
    {"type": "Fir Tree", "image": "assets/sprites/biomes/grassland/FirTree.png", "bare_image": None, "fruit": None, "wood": "Fir Wood", "width" : 64, "height" : 128},
    {"type": "Oak Tree", "image": "assets/sprites/biomes/grassland/OakTree.png", "bare_image": None, "fruit": None, "wood": "Oak Wood", "width" : 64, "height" : 128}, 
    {"type": "Willow Tree", "image": "assets/sprites/biomes/grassland/WillowTree.png", "bare_image": None, "fruit": None, "wood": "Willow Wood", "width" : 128, "height" : 128}
]

savannah_tree_types = [{"type": "Orange Tree", "image": "assets/sprites/biomes/grassland/OrangeTree.png", "bare_image": "assets/sprites/biomes/grassland/BareOrangeTree.png", "fruit": "Oranges", "wood": "Orange Wood", "width" : 96, "height" : 96}, 
{"type": "Olive Tree", "image": "assets/sprites/biomes/grassland/OliveTree.png", "bare_image": "assets/sprites/biomes/grassland/BareOliveTree.png", "fruit": "Olives", "wood": "Olive Wood", "width" : 96, "height" : 128}]

beach_tree_types = [{"type": "Palm Tree", "image": "assets/sprites/biomes/beach/PalmTree.png", "bare_image": "assets/sprites/biomes/beach/BarePalmTree.png", "fruit": "Coconuts", "wood": "Palm Wood", "width" : 64, "height" : 128}]

fruit_plant_types = [{"type": "Pineapple", "image": "assets/sprites/biomes/grassland/PineapplePlant.png", "bare_image": "assets/sprites/biomes/grassland/BarePineapplePlant.png", "fruit": "Pineapple", "resource": "Fiber", "width" : 64, "height" : 64},
{"type": "Watermelon", "image": "assets/sprites/biomes/grassland/WatermelonPlant.png", "bare_image": "assets/sprites/biomes/grassland/BareWatermelonPlant.png", "fruit": "Watermelon", "resource": "Fiber", "width" : 32, "height" : 32}]

boulder_images = ["assets/sprites/biomes/grassland/Boulder1.png", "assets/sprites/biomes/grassland/Boulder2.png", "assets/sprites/biomes/grassland/Boulder3.png", "assets/sprites/biomes/grassland/Boulder4.png", "assets/sprites/biomes/grassland/Boulder5.png", "assets/sprites/biomes/grassland/Boulder6.png", "assets/sprites/biomes/grassland/Boulder7.png", ]

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
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image1": "assets/sprites/biomes/grassland/SavannahGrass1.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image2": "assets/sprites/biomes/grassland/SavannahGrass2.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image3": "assets/sprites/biomes/grassland/SavannahGrass3.png"},
    {"resource": "Fiber", "icon": "assets/sprites/items/SavannahGrass.png", "image4": "assets/sprites/biomes/grassland/SavannahGrass4.png"}
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
            player.experience += harvest_experience * resource_collected
            player.exp_total += harvest_experience * resource_collected
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
    
    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = min(self.resource_amount, (1 * player.attack))
            self.resource_amount -= resource_collected
            
            if self.resource_amount <= 0:
                self.destroyed = True
            player.experience += harvest_experience * resource_collected
            player.exp_total += harvest_experience * resource_collected
            return [self.resource] * resource_collected
        return []
    

class Rock(Solid):
    def __init__(self, x, y):
        img = random.choice(rock_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(10, 15)
    
    def harvest(self, player=None):
        resources = super().harvest(player)
        if random.random() < 0.07:
            resources.append("Flint")
        if random.random() < 0.05:
            resources.append("Raw Metal")
        if random.random() < 0.002:
            resources.append("Raw Gold")
        
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
    
    def harvest(self, player=None):
        resources = super().harvest(player)
        if random.random() < 0.07:
            resources.append("Flint")
        if random.random() < 0.05:
            resources.append("Raw Metal")
        if random.random() < 0.002:
            resources.append("Raw Gold")
        
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

    def harvest(self, player=None):
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

    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = random.randint(3, 9)
            self.destroyed = True
            player.experience += harvest_experience * resource_collected
            player.exp_total += harvest_experience * resource_collected
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
        
    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = min(self.wood_amount, random.randint((1 * player.attack), (3 * player.attack)))
            self.wood_amount -= resource_collected
            if self.wood_amount <= 0:
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


    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = min(self.amount, random.randint((1 * player.attack), (2 * player.attack)))
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
        
    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = min(self.resource_amount, random.randint((1 * player.attack), (2 * player.attack)))
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
    def __init__(self, x, y, image, resource, size=(48, 48)):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)
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
        
class Grass(Collectible):
    def __init__(self, x, y):
        image_index = random.randint(1, 4)
        image_path = f"assets/sprites/biomes/grassland/Grass{image_index}.png"
        super().__init__(x, y, image_path, "Fiber", size=(64, 64))

class SavannahGrass(Collectible):
    def __init__(self, x, y):
        self.amount = random.randint(3, 6)
        image_index = random.randint(1, 4)
        image_path = f"assets/sprites/biomes/grassland/SavannahGrass{image_index}.png"
        super().__init__(x, y, image_path, "Fiber", size=(64, 64))

class Mushroom(Collectible):
    def __init__(self, x, y):
        mushroom_type = random.choice(mushroom_data)
        resource = mushroom_type["resource"]
        image_path = mushroom_type["image1"]
        super().__init__(x, y, image_path, resource, size=(20, 20))



bg_green = pygame.Surface((width, height))
bg_grass = pygame.image.load("assets/sprites/biomes/backgrounds/bg_grass.png").convert()
bg_dirt = pygame.image.load("assets/sprites/biomes/backgrounds/bg_dirt.png").convert()
bg_compact = pygame.image.load("assets/sprites/biomes/backgrounds/bg_compact_dirt.png").convert()
bg_sand = pygame.image.load("assets/sprites/biomes/backgrounds/bg_sand.png").convert()
bg_savannah = pygame.image.load("assets/sprites/biomes/backgrounds/bg_savannah.png").convert()
bg_riverrock = pygame.image.load("assets/sprites/biomes/backgrounds/bg_riverrock.png").convert()
bg_bigrock = pygame.image.load("assets/sprites/biomes/backgrounds/bg_bigrock.png").convert()
bg_duskstone = pygame.image.load("assets/sprites/biomes/backgrounds/bg_duskstone.png").convert()
bg_lavastone = pygame.image.load("assets/sprites/biomes/backgrounds/bg_lavastone.png").convert()
bg_snow = pygame.image.load("assets/sprites/biomes/backgrounds/bg_snow.png").convert()
bg_wasteland = pygame.image.load("assets/sprites/biomes/backgrounds/bg_wasteland.png").convert()
bg_blackstone = pygame.image.load("assets/sprites/biomes/backgrounds/bg_blackstone.png").convert()
bg_redrock = pygame.image.load("assets/sprites/biomes/backgrounds/bg_redrock.png").convert()

bg_dirt = pygame.transform.scale(bg_dirt, (width, height))
bg_grass = pygame.transform.scale(bg_grass, (width, height))
bg_compact = pygame.transform.scale(bg_compact, (width, height))
bg_sand = pygame.transform.scale(bg_sand, (width, height))
bg_savannah = pygame.transform.scale(bg_savannah, (width, height))
bg_riverrock = pygame.transform.scale(bg_riverrock, (width, height))
bg_bigrock = pygame.transform.scale(bg_bigrock, (width, height))
bg_duskstone = pygame.transform.scale(bg_duskstone, (width, height))
bg_lavastone = pygame.transform.scale(bg_lavastone, (width, height))
bg_wasteland = pygame.transform.scale(bg_wasteland, (width, height))
bg_snow = pygame.transform.scale(bg_snow, (width, height))
bg_blackstone = pygame.transform.scale(bg_blackstone, (width, height))
bg_redrock = pygame.transform.scale(bg_redrock, (width, height))
bg_green.fill((0, 120, 0))

background_image = bg_grass
background_image = pygame.transform.scale(background_image, (width, height))


BACKGROUND_SIZE = background_image.get_width()

tiles = []
for i in range(-1, 6):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(6, 20):
    tiles.append((i * BACKGROUND_SIZE, bg_dirt))
for i in range(20, 40):
    tiles.append((i * BACKGROUND_SIZE, bg_compact))
for i in range(40, 60):
    tiles.append((i * BACKGROUND_SIZE, bg_sand))
for i in range(60, 86):
    tiles.append((i * BACKGROUND_SIZE, bg_savannah))
for i in range(86, 116):
    tiles.append((i * BACKGROUND_SIZE, bg_riverrock))
for i in range(116, 144):
    tiles.append((i * BACKGROUND_SIZE, bg_bigrock))
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



allowed_rock_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_lavastone, bg_wasteland, bg_blackstone, bg_redrock]

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
    bg_snow: 0,
    bg_wasteland: 1,
    bg_blackstone: 1,
    bg_redrock: 1
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
    bg_snow: 0,
    bg_wasteland: 3,
    bg_blackstone: 2,
    bg_redrock: 2
}

weighted_boulder_tiles = []
for tile_x, tile_image in tiles:
    weight = boulder_weights.get(tile_image, 1)
    weighted_boulder_tiles.extend([(tile_x, tile_image)] * weight)



allowed_stick_tiles = [bg_grass, bg_dirt, bg_compact, bg_sand, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_wasteland, bg_blackstone, bg_redrock]

stick_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_stick_tiles]

stick_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 1,
    bg_sand: 1,
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



allowed_stone_tiles = [bg_grass, bg_dirt, bg_compact, bg_sand, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_wasteland, bg_blackstone, bg_redrock]

stone_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_stone_tiles]

stone_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 1,
    bg_sand: 1,
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



allowed_dead_bush_tiles = [bg_grass, bg_dirt, bg_compact, bg_duskstone, bg_wasteland]

dead_bush_weights = {
    bg_grass: 2,
    bg_dirt: 4,
    bg_compact: 6,
    bg_sand: 4,
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


def generate_world():
    global rocks, dead_bushes, grasses, stones, boulders, berry_bushes, trees, sticks, savannah_grasses, mushrooms, fruit_plants, ferns, ponds, lavas
    
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

    for _ in range(num_rocks):
        tile_x, tile_image = random.choice(weighted_rock_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        rocks.append(Rock(x, y))

    rock_border_locations = [(0, i * 28) for i in range(28)] + [(512000, i * 28) for i in range(28)]

    for i, pos in enumerate(rock_border_locations):
        x, y = pos
        chosen_image = random.choice(rock_images)
        rock = Rock(x, y)
        rock.image = pygame.image.load(chosen_image).convert_alpha()
        rock.image = pygame.transform.scale(rock.image, (64, 64))
        rock.rect = rock.image.get_rect(topleft=(x, y))
        rocks.append(rock)
    
    
    for _ in range(num_boulders):
        tile_x, tile_image = random.choice(weighted_boulder_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        boulders.append(Boulder(x, y))
    
    for _ in range(num_bushes):
        tile_x, tile_image = random.choice(weighted_berry_bush_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        berry_bush_type = random.choice(berry_bush_types)
        berry_bushes.append(BerryBush(x, y, berry_bush_type))
    
    def spawn_trees(tree_list, tree_types, weighted_tiles, num_trees, height):
        for _ in range(num_trees):
            tile_x, tile_image = random.choice(weighted_tiles)
            x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
            y = random.randint(0, height - 80)
            tree_type = random.choice(tree_types)
            tree_list.append(Tree(x, y, tree_type))

    spawn_trees(trees, grassland_tree_types, weighted_grassland_tiles, num_grassland_trees, height)
    spawn_trees(trees, savannah_tree_types, weighted_savannah_tiles, num_savannah_trees, height)
    spawn_trees(trees, beach_tree_types, weighted_beach_tiles, num_beach_trees, height)
    
    
    for _ in range(num_sticks):
        tile_x, tile_image = random.choice(weighted_stick_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        sticks.append(Stick(x, y))
    
  
    for _ in range(num_stones):
        tile_x, tile_image = random.choice(weighted_stone_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        stones.append(Stone(x, y))
    
    
    for _ in range(num_grasses):
        tile_x, tile_image = random.choice(weighted_grass_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        grasses.append(Grass(x, y))
   
    for _ in range(num_savannah_grasses):
        tile_x, tile_image = random.choice(weighted_savannah_grass_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        savannah_grasses.append(SavannahGrass(x, y))
    
    for _ in range(num_mushrooms):
        tile_x, tile_image = random.choice(weighted_mushroom_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        mushrooms.append(Mushroom(x, y))
    
    
    for _ in range(num_dead_bushes):
        tile_x, tile_image = random.choice(weighted_dead_bush_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        dead_bushes.append(DeadBush(x, y))

    if weighted_fruit_plant_tiles:
        for _ in range(num_fruit_plants):
            tile_x, tile_image = random.choice(weighted_fruit_plant_tiles)
            x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
            y = random.randint(0, height - 64)
            plant_type = random.choice(fruit_plant_types)
            fruit_plants.append(FruitPlant(x, y, plant_type))
    
    if weighted_fire_fern_tiles:
        for _ in range(num_fire_ferns):
            tile_x, tile_image = random.choice(weighted_fire_fern_tiles)
            x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
            y = random.randint(0, height - 64)
            ferns.append(Fern(x, y, fern_data[0]))

    if weighted_frost_fern_tiles:
        for _ in range(num_frost_ferns):
            tile_x, tile_image = random.choice(weighted_frost_fern_tiles)
            x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
            y = random.randint(0, height - 64)
            ferns.append(Fern(x, y, fern_data[1]))
    
    for _ in range(num_ponds):
        x = random.randint(0, 512000)
        y = random.randint(0, height - 128)
        ponds.append(Pond(x, y))
    
    lavastone_start = 180 * BACKGROUND_SIZE
    lavastone_end = 216 * BACKGROUND_SIZE
    for _ in range(num_lavaponds):
        x = random.randint(int(lavastone_start), int(lavastone_end - 128))
        y = random.randint(0, height - 128)
        lavas.append(Lavapond(x, y))
    
    return rocks, boulders, berry_bushes, trees, sticks, stones, grasses, savannah_grasses, mushrooms, dead_bushes, fruit_plants, ferns, ponds, lavas