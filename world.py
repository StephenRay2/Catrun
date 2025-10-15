import pygame
import random
import time

screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()

rock_images = ["/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock1.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock2.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock3.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock4.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock6.png"]


grassland_tree_types = [
    {"type": "Apple Tree", "image": "assets/sprites/biomes/grassland/AppleTree.png", "bare_image": "assets/sprites/biomes/grassland/BareAppleTree.png", "fruit": "Apples", "wood": "Apple Wood", "width" : 64, "height" : 128},
    {"type": "Duskwood Tree", "image": "assets/sprites/biomes/grassland/DuskwoodTree.png", "bare_image": None, "fruit": None, "wood": "Dusk Wood", "width" : 64, "height" : 128},
    {"type": "Fir Tree", "image": "assets/sprites/biomes/grassland/FirTree.png", "bare_image": None, "fruit": None, "wood": "Fir Wood", "width" : 64, "height" : 128},
    {"type": "Oak Tree", "image": "assets/sprites/biomes/grassland/OakTree.png", "bare_image": None, "fruit": None, "wood": "Oak Wood", "width" : 64, "height" : 128}, 
]

savannah_tree_types = [{"type": "Orange Tree", "image": "assets/sprites/biomes/grassland/OrangeTree.png", "bare_image": "assets/sprites/biomes/grassland/BareOrangeTree.png", "fruit": "Oranges", "wood": "Orange Wood", "width" : 96, "height" : 96}]

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

collect_experience = 1
harvest_experience = 1.5


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
        # Create a thinner collision box centered on the trunk
        # Make it 40% of the width for a thinner trunk feel
        collision_width = int(self.rect.width * 0.4)
        x_offset = (self.rect.width - collision_width) // 2
        
        return pygame.Rect(
            self.rect.x - cam_x + x_offset, self.rect.y + 10, collision_width, self.rect.height - 40
        )
    
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

rocks = []
num_rocks = 2000
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

grassland_tree_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah]
savannah_tree_tiles = [bg_savannah]

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

def spawn_trees(tree_list, tree_types, weighted_tiles, num_trees, height):
    for _ in range(num_trees):
        tile_x, tile_image = random.choice(weighted_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        tree_type = random.choice(tree_types)
        tree_list.append(Tree(x, y, tree_type))

trees = []
spawn_trees(trees, grassland_tree_types, weighted_grassland_tiles, 400, height)
spawn_trees(trees, savannah_tree_types, weighted_savannah_tiles, 100, height)


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

berry_bushes = []
num_bushes = 400
for _ in range(num_bushes):
    tile_x, tile_image = random.choice(weighted_berry_bush_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    berry_bush_type = random.choice(berry_bush_types)
    berry_bushes.append(BerryBush(x, y, berry_bush_type))

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

boulders = []
num_boulders = 300
for _ in range(num_boulders):
    tile_x, tile_image = random.choice(weighted_boulder_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    boulders.append(Boulder(x, y))