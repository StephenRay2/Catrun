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