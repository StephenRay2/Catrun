import pygame
import sys
import time, random, math

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
running = True
dt = 0
size = 64
shift_multiplier = 1
dungeon_depth = 0
font = pygame.font.SysFont(None, 48)
scroll = 0
player_speed = 300
dungeon_traversal_speed = 50

# ########## BACKGROUND IMAGES ####################


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


def zone():
    global background_image

    
    if dungeon_depth < 200:
            background_image = bg_grass
    elif 200 <= dungeon_depth < 800:
            background_image = bg_dirt
    elif 800 <= dungeon_depth < 1500:
            background_image = bg_compact
    elif 1500 <= dungeon_depth < 2500:
            background_image = bg_sand
    elif 2500 <= dungeon_depth < 3750:
            background_image = bg_savannah
    elif 3750 <= dungeon_depth < 5000:
            background_image = bg_riverrock
    elif 5000 <= dungeon_depth < 7500:
            background_image = bg_bigrock
    elif 7500 <= dungeon_depth < 11000:
            background_image = bg_duskstone
    elif 11000 <= dungeon_depth < 11200:
            background_image = bg_grass
    elif 11200 <= dungeon_depth < 15000:
            background_image = bg_lavastone
    elif 15000 <= dungeon_depth < 20000:
            background_image = bg_wasteland
    elif 20000 <= dungeon_depth < 30000:
            background_image = bg_snow
    elif 30000 <= dungeon_depth < 31000:
            background_image = bg_grass
    elif 31000 <= dungeon_depth < 40000:
            background_image = bg_blackstone
    elif 40000 <= dungeon_depth < 47000:
            background_image = bg_redrock
    elif 47000 <= dungeon_depth < 48000:
            background_image = bg_grass
    elif 48000 <= dungeon_depth:
            background_image = bg_redrock
    else:
            background_image = bg_green

    background_image = pygame.transform.scale(background_image, (width, height))


scroll_x = 0
scroll_y = 0

while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    zone()
    screen.blit(background_image, (0, 0))

    background_image = pygame.transform.scale(background_image, (width, height))

    tiles = math.ceil(width /background_image.get_width()) + 1  

    bg_width = background_image.get_width()
    bg_height = background_image.get_height()


    for x in range(-1, math.ceil(width/ bg_width) + 1):
        for y in range(-1, math.ceil(height/ bg_height) + 1):
            screen.blit(background_image, (x * bg_width + scroll_x % bg_width,
                         y * bg_height + scroll_y % bg_height))


    pygame.draw.rect(screen, "red", (player_pos.x - size/2, player_pos.y - size/2, size, size))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= player_speed * dt * shift_multiplier
    if keys[pygame.K_s]:
        player_pos.y += player_speed * dt * shift_multiplier
    if keys[pygame.K_a] and 0 < dungeon_depth < 50000:
        scroll_x += player_speed * dt * shift_multiplier
        dungeon_depth -= dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_a] and dungeon_depth <= 0:
        player_pos.x -= player_speed * dt * shift_multiplier
        dungeon_depth -= dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_a] and dungeon_depth >= 50000:
        player_pos.x -= player_speed * dt * shift_multiplier
        dungeon_depth -= dungeon_traversal_speed * shift_multiplier
    if keys[pygame.K_d] and 0 < dungeon_depth < 50000:
        scroll_x -= player_speed * dt * shift_multiplier
        dungeon_depth += dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_d] and dungeon_depth <= 0:
        player_pos.x += player_speed * dt * shift_multiplier
        dungeon_depth += dungeon_traversal_speed * shift_multiplier
    elif keys[pygame.K_d] and dungeon_depth >= 50000:
        player_pos.x += player_speed * dt * shift_multiplier
        dungeon_depth += dungeon_traversal_speed * shift_multiplier
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LSHIFT or pygame.K_RSHIFT]:
        shift_multiplier = 1.4
    else:
        shift_multiplier = 1


    depth_text = font.render(f"Dungeon Depth: {dungeon_depth:.1f}", True, (255, 255, 255))
    screen.blit(depth_text, (20,20))


    pygame.display.flip()
    dt = clock.tick(60) / 1000

    

pygame.quit()

