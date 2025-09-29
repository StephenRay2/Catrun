import pygame
import sys
import time, random, math
from world import *

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
player_speed = 300
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
for i in range(3):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(3, 10):
    tiles.append((i * BACKGROUND_SIZE, bg_dirt))
for i in range(10, 20):
    tiles.append((i * BACKGROUND_SIZE, bg_compact))
for i in range(20, 30):
    tiles.append((i * BACKGROUND_SIZE, bg_sand))
for i in range(30, 43):
    tiles.append((i * BACKGROUND_SIZE, bg_savannah))
for i in range(43, 58):
    tiles.append((i * BACKGROUND_SIZE, bg_riverrock))
for i in range(58, 72):
    tiles.append((i * BACKGROUND_SIZE, bg_bigrock))
for i in range(72, 75):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(75, 90):
    tiles.append((i * BACKGROUND_SIZE, bg_duskstone))
for i in range(90, 108):
    tiles.append((i * BACKGROUND_SIZE, bg_lavastone))
for i in range(108, 120):
    tiles.append((i * BACKGROUND_SIZE, bg_wasteland))
for i in range(120, 128):
    tiles.append((i * BACKGROUND_SIZE, bg_dirt))
for i in range(128, 145):
    tiles.append((i * BACKGROUND_SIZE, bg_snow))
for i in range(145, 170):
    tiles.append((i * BACKGROUND_SIZE, bg_blackstone))
for i in range(170, 190):
    tiles.append((i * BACKGROUND_SIZE, bg_redrock))
for i in range(190, 195):
    tiles.append((i * BACKGROUND_SIZE, bg_grass))
for i in range(195, 200):
    tiles.append((i * BACKGROUND_SIZE, bg_redrock))



cam_x = 0


rocks = []
for _ in range(20):  # make 20 rocks
    x = random.randint(0, 1280 * 5)  # example world width
    y = random.randint(0, 720)
    rocks.append(Rock(x, y))

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for tile_x, tile_image in tiles:
        screen_x = tile_x - cam_x
        if -BACKGROUND_SIZE < screen_x < width:
            screen.blit(tile_image, (screen_x, floor_y))


    screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))

    for rock in rocks:
        rock.draw(screen, cam_x)


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
        player_pos.y -= player_speed * dt * shift_multiplier
    
    
    if keys[pygame.K_s] and (player_pos.y + (size/2)) <= height:
        player_pos.y += player_speed * dt * shift_multiplier

    
    if keys[pygame.K_a] and 0 < dungeon_depth < 50000:
        cam_x -= player_speed * dt * shift_multiplier
        dungeon_depth = max(0, dungeon_depth - dungeon_traversal_speed * shift_multiplier)
    elif keys[pygame.K_a] and dungeon_depth <= 0:
        player_pos.x -= player_speed * dt * shift_multiplier
        dungeon_depth -= dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_a] and dungeon_depth >= 50000:
        player_pos.x -= player_speed * dt * shift_multiplier
        dungeon_depth -= dungeon_traversal_speed * shift_multiplier

    
    if keys[pygame.K_d] and 0 < dungeon_depth < 50000:
        cam_x += player_speed * dt * shift_multiplier
        dungeon_depth += dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_d] and dungeon_depth <= 0:
        player_pos.x += player_speed * dt * shift_multiplier
        dungeon_depth += dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_d] and dungeon_depth >= 50000:
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
        shift_multiplier = 1.4
    else:
        shift_multiplier = 1

    
    depth_text = font.render(f"Dungeon Depth: {dungeon_depth:.1f}", True, (255, 255, 255))
    depth_rect = pygame.Rect(20, 20, depth_text.get_width(), depth_text.get_height())
    temp_surface = pygame.Surface((depth_rect.width + 10, depth_rect.height + 10), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 100))
    screen.blit(temp_surface, (depth_rect.x, depth_rect.y))
    screen.blit(depth_text, (depth_rect.x + 5, depth_rect.y + 5))


    pygame.display.flip()
    dt = clock.tick(60) / 1000

    

pygame.quit()

