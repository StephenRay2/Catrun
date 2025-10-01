import pygame
import sys
import time, random, math
from world import *
from mobs import *

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
running = True
dt = 0
size = 64
world_x = 0.0
floor_y = 0
shift_multiplier = 1
dungeon_depth = 0
font = pygame.font.SysFont(None, 24)
scroll = 0
player_speed = 350
dungeon_traversal_speed = .1



############ PLAYER IMAGES #################

player_stand_image = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CharacterCorynnFrontStanding.png")
player_stand_image_back = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CharacterCorynnBackStanding.png")
player_stand_left = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CharacterCorynnLeftStanding.png")
player_stand_right = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CharacterCorynnRightStanding.png")
player_walk_down_images = [pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkDown1.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkDown2.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkDown3.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkDown4.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkDown5.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkDown6.png").convert_alpha()]
player_walk_up_images = [pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkUp1.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkUp2.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkUp3.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkUp4.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkUp5.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkUp6.png").convert_alpha()]
player_walk_left_images = [pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft1.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft2.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft3.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft4.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft5.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft6.png").convert_alpha(), pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/player/CorynnWalkLeft7.png").convert_alpha()]


player_stand_image = pygame.transform.scale(player_stand_image, (size, size))
player_stand_image_back = pygame.transform.scale(player_stand_image_back, (size, size))
player_stand_left = pygame.transform.scale(player_stand_left, (size, size))
player_stand_right = pygame.transform.scale(player_stand_right, (size, size))
player_walk_down_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_down_images]
player_walk_up_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_up_images]
player_walk_left_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_left_images]
player_walk_right_images = [pygame.transform.flip(img, True, False) for img in player_walk_left_images]

player_frame_index = 0
player_animation_timer = 0
player_current_image = player_stand_image
last_direction = "down"

############ BACKGROUND IMAGES ####################


bg_green = pygame.Surface((width, height))
bg_grass = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_grass.png").convert()
bg_dirt = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_dirt.png").convert()
bg_compact = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_compact_dirt.png").convert()
bg_sand = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_sand.png").convert()
bg_savannah = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_savannah.png").convert()
bg_riverrock = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_riverrock.png").convert()
bg_bigrock = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_bigrock.png").convert()
bg_duskstone = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_duskstone.png").convert()
bg_lavastone = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_lavastone.png").convert()
bg_snow = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_snow.png").convert()
bg_wasteland = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_wasteland.png").convert()
bg_blackstone = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_blackstone.png").convert()
bg_redrock = pygame.image.load("/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/backgrounds/bg_redrock.png").convert()

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

player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

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



cam_x = 0
cam_y = 0

player = Player(width/2, height/2, "Corynn")
allowed_rock_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_lavastone, bg_wasteland, bg_blackstone, bg_redrock]



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

allowed_tree_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_wasteland]

tree_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_tree_tiles]

tree_weights = {
    bg_grass: 30,
    bg_dirt: 20,
    bg_compact: 10,
    bg_savannah: 10,
    bg_wasteland: 1,

}

weighted_tree_tiles = []
for tile_x, tile_image in tiles:
    weight = tree_weights.get(tile_image, 1)
    weighted_tree_tiles.extend([(tile_x, tile_image)] * weight)

tree = Tree(x,y)
trees = []
num_trees = 2000

for _ in range(num_trees):
    tile_x, tile_image = random.choice(tree_spawn_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    trees.append(Tree(x, y))


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for tile_x, tile_image in tiles:
        screen_x = tile_x - cam_x
        if -BACKGROUND_SIZE < screen_x < width:
            screen.blit(tile_image, (screen_x, floor_y))

    all_objects = rocks + trees
    visible_objects = [obj for obj in all_objects 
                       if obj.rect.x - cam_x > -100 and obj.rect.x - cam_x < width + 100]
    visible_objects.sort(key=lambda obj: obj.rect.y + obj.rect.height)

    player_drawn = False

    for obj in visible_objects:
        object_mid_y = obj.rect.y + obj.rect.height / 2
        if not player_drawn and player.rect.centery <= object_mid_y:
            screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))
            player_drawn = True
        obj.draw(screen, cam_x)

    if not player_drawn:
        screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))

    player.rect.center = (player_pos.x, player_pos.y)
        
            

    nearby_objects = [obj for obj in all_objects 
                      if abs(obj.rect.x - (player_pos.x + cam_x)) < 200 
                      and abs(obj.rect.y - player_pos.y) < 200]

    left_player_check = pygame.Rect(player.rect.left - 1, player.rect.top + 5, 1, player.rect.height - 12)
    right_player_check = pygame.Rect(player.rect.right, player.rect.top + 5, 1, player.rect.height - 12)
    top_player_check = pygame.Rect(player.rect.left + 5, player.rect.top - 1, player.rect.width - 12, 1)
    bottom_player_check = pygame.Rect(player.rect.left + 5, player.rect.bottom, player.rect.width - 12, 1)

    left_collision = any(left_player_check.colliderect(pygame.Rect(obj.rect.x - cam_x + 10, obj.rect.y + (obj.rect.height * .2), obj.rect.width - 20, obj.rect.height - 50)) for obj in nearby_objects)
    right_collision = any(right_player_check.colliderect(pygame.Rect(obj.rect.x - cam_x + 10, obj.rect.y + (obj.rect.height * .2), obj.rect.width - 20, obj.rect.height - 50)) for obj in nearby_objects)
    up_collision = any(top_player_check.colliderect(pygame.Rect(obj.rect.x - cam_x + 10, obj.rect.y + (obj.rect.height * .2), obj.rect.width - 20, obj.rect.height - 50)) for obj in nearby_objects)
    down_collision = any(bottom_player_check.colliderect(pygame.Rect(obj.rect.x - cam_x + 10, obj.rect.y + (obj.rect.height * .2), obj.rect.width - 20, obj.rect.height - 50)) for obj in nearby_objects)

    if left_collision == True:
        up_collision = False
        down_collision = False
    
    if right_collision == True:
        up_collision = False
        down_collision = False
    
    if up_collision == True:
        left_collision = False
        right_collision = False

    if down_collision == True:
        left_collision = False
        right_collision = False

    keys = pygame.key.get_pressed()
    if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
        if last_direction == "down":
            player_current_image = player_stand_image
        elif last_direction == "up":
            player_current_image = player_stand_image_back
        elif last_direction == "left":
            player_current_image = player_stand_left
        elif last_direction == "right":
            player_current_image = player_stand_right
    
    if keys[pygame.K_w] and (player_pos.y - (size/2)) >= 0:
        if not up_collision:
            player_pos.y -= player_speed * dt * shift_multiplier
    
    
    if keys[pygame.K_s] and (player_pos.y + (size/2)) <= height:
        if not down_collision:
            player_pos.y += player_speed * dt * shift_multiplier

    
    if keys[pygame.K_a] and 0 < dungeon_depth < 50000:
        if not left_collision:
            cam_x -= player_speed * dt * shift_multiplier
            dungeon_depth = max(0, dungeon_depth - dungeon_traversal_speed * shift_multiplier)
    elif keys[pygame.K_a] and dungeon_depth <= 0:
        if not left_collision:
            player_pos.x -= player_speed * dt * shift_multiplier
            dungeon_depth -= dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_a] and dungeon_depth >= 50000:
        if not left_collision:
            player_pos.x -= player_speed * dt * shift_multiplier
            dungeon_depth -= dungeon_traversal_speed * shift_multiplier

    
    if keys[pygame.K_d] and 0 < dungeon_depth < 50000:
        if not right_collision:
            cam_x += player_speed * dt * shift_multiplier
            dungeon_depth += dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_d] and dungeon_depth <= 0:
        if not right_collision:
            player_pos.x += player_speed * dt * shift_multiplier
            dungeon_depth += dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_d] and dungeon_depth >= 50000:
        if not right_collision:
            player_pos.x += player_speed * dt * shift_multiplier
            dungeon_depth += dungeon_traversal_speed * shift_multiplier


    if keys[pygame.K_d]:
        last_direction = "right"
        player_animation_timer += dt
        if keys[pygame.K_LSHIFT]:
            if player_animation_timer > .04:
                player_frame_index = (player_frame_index + 1) % len(player_walk_right_images)
                player_current_image = player_walk_right_images[player_frame_index]
                player_animation_timer = 0
        else:
            if player_animation_timer > .07:
                player_frame_index = (player_frame_index + 1) % len(player_walk_right_images)
                player_current_image = player_walk_right_images[player_frame_index]
                player_animation_timer = 0

    elif keys[pygame.K_a]:
        last_direction = "left"
        player_animation_timer += dt
        if keys[pygame.K_LSHIFT]:
            if player_animation_timer > .04:
                player_frame_index = (player_frame_index + 1) % len(player_walk_left_images)
                player_current_image = player_walk_left_images[player_frame_index]
                player_animation_timer = 0
        else:
            if player_animation_timer > .07:
                player_frame_index = (player_frame_index + 1) % len(player_walk_left_images)
                player_current_image = player_walk_left_images[player_frame_index]
                player_animation_timer = 0

    elif keys[pygame.K_w]:
        last_direction = "up"
        player_animation_timer += dt
        if keys[pygame.K_LSHIFT]:
            if player_animation_timer > .04:
                player_frame_index = (player_frame_index + 1) % len(player_walk_up_images)
                player_current_image = player_walk_up_images[player_frame_index]
                player_animation_timer = 0
        else:
            if player_animation_timer > .07:
                player_frame_index = (player_frame_index + 1) % len(player_walk_up_images)
                player_current_image = player_walk_up_images[player_frame_index]
                player_animation_timer = 0

    elif keys[pygame.K_s]:
        last_direction = "down"
        player_animation_timer += dt
        if keys[pygame.K_LSHIFT]:
            if player_animation_timer > .04:
                player_frame_index = (player_frame_index + 1) % len(player_walk_down_images)
                player_current_image = player_walk_down_images[player_frame_index]
                player_animation_timer = 0
        else:
            if player_animation_timer > .07:
                player_frame_index = (player_frame_index + 1) % len(player_walk_down_images)
                player_current_image = player_walk_down_images[player_frame_index]
                player_animation_timer = 0


    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        shift_multiplier = 1.5
    else:
        shift_multiplier = 1

    
    depth_text = font.render(f"Dungeon Depth: {dungeon_depth:.1f}", True, (255, 255, 255))
    depth_rect = pygame.Rect(20, 20, depth_text.get_width(), depth_text.get_height())
    temp_surface = pygame.Surface((depth_rect.width + 10, depth_rect.height + 10), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 100))
    screen.blit(temp_surface, (depth_rect.x, depth_rect.y))
    screen.blit(depth_text, (depth_rect.x + 5, depth_rect.y + 5))


    if keys[pygame.K_e]:
        target_depth = 10000
        dungeon_depth = target_depth
        cam_x = 500000
        player_pos.x = width / 2


    pygame.display.flip()
    dt = clock.tick(60) / 1000

    

pygame.quit()