import pygame
import random
import time
from mobs import Player

clock = pygame.time.Clock()

rock_images = ["/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock1.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock2.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock3.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock4.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock6.png"]


tree_types = [
    {"type": "Apple Tree", "image": "assets/sprites/biomes/grassland/AppleTree.png", "bare_image": "assets/sprites/biomes/grassland/BareAppleTree.png", "fruit": "Apples", "wood": "Apple Wood"},
    {"type": "Duskwood Tree", "image": "assets/sprites/biomes/grassland/DuskwoodTree.png", "bare_image": None, "fruit": None, "wood": "Dusk Wood"},
    {"type": "Fir Tree", "image": "assets/sprites/biomes/grassland/FirTree.png", "bare_image": None, "fruit": None, "wood": "Fir Wood"},
    {"type": "Oak Tree", "image": "assets/sprites/biomes/grassland/OakTree.png", "bare_image": None, "fruit": None, "wood": "Oak Wood"}
]

boulder_images = ["assets/sprites/biomes/grassland/Boulder1.png", "assets/sprites/biomes/grassland/Boulder2.png", "assets/sprites/biomes/grassland/Boulder3.png", "assets/sprites/biomes/grassland/Boulder4.png", "assets/sprites/biomes/grassland/Boulder5.png", "assets/sprites/biomes/grassland/Boulder6.png", "assets/sprites/biomes/grassland/Boulder7.png", ]

berry_bush_types = [
    {"image": "assets/sprites/biomes/grassland/BloodBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareBloodBerryBush.png", "berry": "Blood Berries", "resource": "stick"},
    {"image": "assets/sprites/biomes/grassland/DawnBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareDawnBerryBush.png", "berry": "Dawn Berries", "resource": "stick"},
    {"image": "assets/sprites/biomes/grassland/DuskBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareDuskBerryBush.png", "berry": "Dusk Berries", "resource": "stick"},
    {"image": "assets/sprites/biomes/grassland/SunBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareSunBerryBush.png", "berry": "Sun Berries", "resource": "stick"},
    {"image": "assets/sprites/biomes/grassland/TealBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareTealBerryBush.png", "berry": "Teal Berries", "resource": "stick"},
    {"image": "assets/sprites/biomes/grassland/TwilightDrupesBush.png", "bare_image": "assets/sprites/biomes/grassland/BareTwilightDrupesBush.png", "berry": "Twilight Drupes", "resource": "stick"},
    {"image": "assets/sprites/biomes/grassland/VioBerryBush.png", "bare_image": "assets/sprites/biomes/grassland/BareVioBerryBush.png", "berry": "Vio Berries", "resource": "stick"},
]

collect_experience = 4
harvest_experience = 4


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
        """Get the collision rect for this object, accounting for camera offset"""
        return pygame.Rect(
            self.rect.x - cam_x + 10,
            self.rect.y + (self.rect.height * .2),
            self.rect.width - 20,
            self.rect.height - 50
        )
    
    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = min(self.resource_amount, (1 * player.attack))
            self.resource_amount -= resource_collected
            
            if self.resource_amount <= 0:
                self.destroyed = True
            player.experience += collect_experience * resource_collected
            player.exp_total += collect_experience * resource_collected
            return [self.resource] * resource_collected
        return []
    

class Rock(Solid):
    def __init__(self, x, y):
        img = random.choice(rock_images)
        super().__init__(img, x, y, (64, 64))
        self.resource = "Stone"
        self.resource_amount = random.randint(10, 15)



class Boulder(Solid):
    def __init__(self, x, y):
        img = random.choice(boulder_images)
        super().__init__(img, x, y, (128, 128))
        self.image_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y + 40, 128, 88)
        self.resource = "Stone"
        self.resource_amount = random.randint(40, 80)
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))


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

        self.regrow_time = 200 #(seconds)
        self.timer = 0
        self.is_empty = False
        self.destroyed = False
        self.resource = "Sticks"

    def collect(self, player = None):
        if not self.is_empty and self.amount > 0:
            berry_count = self.amount
            self.amount = 0
            self.image = self.bare_image
            self.is_empty = True
            self.timer = 0
            player.experience += collect_experience * berry_count
            player.exp_total += collect_experience * berry_count
            return [self.berry] * berry_count
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
            self.rect.x - cam_x + 10,
            self.rect.y + (self.rect.height * .2),
            self.rect.width - 20,
            self.rect.height - 50
        )
    
    def harvest(self, player=None):
        if not self.destroyed:
            resource_collected = random.randint(3, 7)
            self.destroyed = True
            player.experience += collect_experience * resource_collected
            player.exp_total += collect_experience * resource_collected
            return [self.resource] * resource_collected
        return []
    

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tree_type):
        super().__init__()
        self.type = tree_type
        self.full_image = pygame.transform.scale(
            pygame.image.load(tree_type["image"]).convert_alpha(), (64, 128)
        )
        
        if tree_type["bare_image"] is not None:
            self.bare_image = pygame.transform.scale(
                pygame.image.load(tree_type["bare_image"]).convert_alpha(), (64, 128)
            )
        else:
            self.bare_image = self.full_image
        
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y + 64, 64, 64)

        self.fruit = tree_type["fruit"]
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
            player.experience += collect_experience * resource_collected
            player.exp_total += collect_experience * resource_collected
            
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
        return pygame.Rect(
            self.rect.x - cam_x + 10,
            self.rect.y + (self.rect.height * .2),
            self.rect.width - 20,
            self.rect.height - 50
        )