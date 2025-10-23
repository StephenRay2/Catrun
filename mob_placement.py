from mobs import *
player = Player(width/2, height/2, "Corynn")



allowed_squirrel_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_snow, bg_wasteland]

squirrel_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_squirrel_tiles]

squirrel_spawn_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 2,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 1,
    bg_wasteland: 1,
    bg_blackstone: 0,
    bg_redrock: 0

}

weighted_squirrel_tiles = []
for tile_x, tile_image in tiles:
    weight = squirrel_spawn_weights.get(tile_image, 1)
    weighted_squirrel_tiles.extend([(tile_x, tile_image)] * weight)

squirrels = []
num_squirrels = 200
for _ in range(num_squirrels):
    tile_x, tile_image = random.choice(weighted_squirrel_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    squirrels.append(Squirrel(x, y, "Squirrel"))

allowed_cat_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_sand, bg_duskstone, bg_lavastone, bg_snow, bg_wasteland, bg_blackstone, bg_redrock]

cat_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_cat_tiles]

cat_spawn_weights = {
    bg_grass: 2,
    bg_dirt: 1,
    bg_compact: 1,
    bg_sand: 1,
    bg_savannah: 2,
    bg_riverrock: 1,
    bg_bigrock: 1,
    bg_duskstone: 1,
    bg_lavastone: 1,
    bg_snow: 1,
    bg_wasteland: 1,
    bg_blackstone: 1,
    bg_redrock: 0

}

weighted_cat_tiles = []
for tile_x, tile_image in tiles:
    weight = cat_spawn_weights.get(tile_image, 1)
    weighted_cat_tiles.extend([(tile_x, tile_image)] * weight)

cats = []
num_cats = 500
for _ in range(num_cats):
    tile_x, tile_image = random.choice(weighted_cat_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    cats.append(Cat(x, y, "Cat"))

allowed_cow_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah]

cow_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_cow_tiles]

cow_spawn_weights = {
    bg_grass: 2,
    bg_dirt: 1,
    bg_compact: 1,
    bg_savannah: 3,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0

}

weighted_cow_tiles = []
for tile_x, tile_image in tiles:
    weight = cow_spawn_weights.get(tile_image, 1)
    weighted_cow_tiles.extend([(tile_x, tile_image)] * weight)

cows = []
num_cows = 100
for _ in range(num_cows):
    tile_x, tile_image = random.choice(weighted_cow_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    cows.append(Cow(x, y, "Cow"))

allowed_chicken_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah]

chicken_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_chicken_tiles]

chicken_spawn_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 2,
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

weighted_chicken_tiles = []
for tile_x, tile_image in tiles:
    weight = chicken_spawn_weights.get(tile_image, 1)
    weighted_chicken_tiles.extend([(tile_x, tile_image)] * weight)

chickens = []
num_chickens = 100
for _ in range(num_chickens):
    tile_x, tile_image = random.choice(weighted_chicken_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    chickens.append(Chicken(x, y, "Chicken"))

allowed_crawler_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_snow, bg_wasteland]

crawler_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_crawler_tiles]

crawler_spawn_weights = {
    bg_grass: 2,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 2,
    bg_riverrock: 2,
    bg_bigrock: 2,
    bg_duskstone: 2,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 1,
    bg_blackstone: 0,
    bg_redrock: 3

}

weighted_crawler_tiles = []
for tile_x, tile_image in tiles:
    weight = crawler_spawn_weights.get(tile_image, 1)
    weighted_crawler_tiles.extend([(tile_x, tile_image)] * weight)

crawlers = []
num_crawlers = 200
for _ in range(num_crawlers):
    tile_x, tile_image = random.choice(weighted_crawler_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    crawlers.append(Crawler(x, y, "Crawler"))


allowed_duskwretch_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_snow, bg_wasteland]

duskwretch_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_duskwretch_tiles]

duskwretch_spawn_weights = {
    bg_grass: 2,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 2,
    bg_riverrock: 2,
    bg_bigrock: 2,
    bg_duskstone: 8,
    bg_lavastone: 0,
    bg_snow: 2,
    bg_wasteland: 5,
    bg_blackstone: 2,
    bg_redrock: 3

}

weighted_duskwretch_tiles = []
for tile_x, tile_image in tiles:
    weight = duskwretch_spawn_weights.get(tile_image, 1)
    weighted_duskwretch_tiles.extend([(tile_x, tile_image)] * weight)

duskwretches = []
num_duskwretches = 75
for _ in range(num_duskwretches):
    tile_x, tile_image = random.choice(weighted_duskwretch_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    duskwretches.append(Duskwretch(x, y, "Duskwretch"))

allowed_pock_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_lavastone, bg_snow, bg_wasteland, bg_blackstone, bg_redrock]

pock_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_pock_tiles]

pock_spawn_weights = {
    bg_grass: 1,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 1,
    bg_riverrock: 3,
    bg_bigrock: 3,
    bg_duskstone: 4,
    bg_lavastone: 4,
    bg_snow: 2,
    bg_wasteland: 5,
    bg_blackstone: 4,
    bg_redrock: 5
}

weighted_pock_tiles = []
for tile_x, tile_image in tiles:
    weight = pock_spawn_weights.get(tile_image, 1)
    weighted_pock_tiles.extend([(tile_x, tile_image)] * weight)

pocks = []
num_pocks = 150
for _ in range(num_pocks):
    tile_x, tile_image = random.choice(weighted_pock_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    pocks.append(Pock(x, y, "Pock"))

allowed_deer_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah]

deer_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_deer_tiles]

deer_spawn_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 2,
    bg_riverrock: 2,
    bg_bigrock: 2,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 1,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_deer_tiles = []
for tile_x, tile_image in tiles:
    weight = deer_spawn_weights.get(tile_image, 1)
    weighted_deer_tiles.extend([(tile_x, tile_image)] * weight)

deers = []
num_deers = 200
for _ in range(num_deers):
    tile_x, tile_image = random.choice(weighted_deer_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    deers.append(Deer(x, y, "Deer"))

allowed_black_bear_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock]

black_bear_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_black_bear_tiles]

black_bear_spawn_weights = {
    bg_grass: 2,
    bg_dirt: 3,
    bg_compact: 2,
    bg_savannah: 1,
    bg_riverrock: 4,
    bg_bigrock: 5,
    bg_duskstone: 3,
    bg_lavastone: 0,
    bg_snow: 2,
    bg_wasteland: 1,
    bg_blackstone: 2,
    bg_redrock: 0
}

weighted_black_bear_tiles = []
for tile_x, tile_image in tiles:
    weight = black_bear_spawn_weights.get(tile_image, 1)
    weighted_black_bear_tiles.extend([(tile_x, tile_image)] * weight)

black_bears = []
num_black_bears = 100
for _ in range(num_black_bears):
    tile_x, tile_image = random.choice(weighted_black_bear_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    black_bears.append(BlackBear(x, y, "Black Bear"))

allowed_brown_bear_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock, bg_duskstone, bg_snow]

brown_bear_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_brown_bear_tiles]

brown_bear_spawn_weights = {
    bg_grass: 2,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 1,
    bg_riverrock: 3,
    bg_bigrock: 4,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 2,
    bg_wasteland: 2,
    bg_blackstone: 3,
    bg_redrock: 0
}

weighted_brown_bear_tiles = []
for tile_x, tile_image in tiles:
    weight = brown_bear_spawn_weights.get(tile_image, 1)
    weighted_brown_bear_tiles.extend([(tile_x, tile_image)] * weight)

brown_bears = []
num_brown_bears = 100
for _ in range(num_brown_bears):
    tile_x, tile_image = random.choice(weighted_brown_bear_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    brown_bears.append(BrownBear(x, y, "Brown Bear"))

allowed_gila_tiles = [bg_sand, bg_wasteland, bg_redrock]

gila_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_gila_tiles]

gila_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 5,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 3,
    bg_blackstone: 0,
    bg_redrock: 4
}

weighted_gila_tiles = []
for tile_x, tile_image in tiles:
    weight = gila_spawn_weights.get(tile_image, 1)
    weighted_gila_tiles.extend([(tile_x, tile_image)] * weight)

gilas = []
num_gilas = 100
for _ in range(num_gilas):
    tile_x, tile_image = random.choice(weighted_gila_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    gilas.append(Gila(x, y, "Gila"))

allowed_crow_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock]

crow_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_crow_tiles]

crow_spawn_weights = {
    bg_grass: 4,
    bg_dirt: 3,
    bg_compact: 2,
    bg_savannah: 2,
    bg_riverrock: 1,
    bg_bigrock: 1,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 8,
    bg_blackstone: 0,
    bg_redrock: 2
}

weighted_crow_tiles = []
for tile_x, tile_image in tiles:
    weight = crow_spawn_weights.get(tile_image, 1)
    weighted_crow_tiles.extend([(tile_x, tile_image)] * weight)

crows = []
num_crows = 150
for _ in range(num_crows):
    tile_x, tile_image = random.choice(weighted_crow_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    crows.append(Crow(x, y, "Crow"))