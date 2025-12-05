import pygame
from mobs import *
from mobs import apply_wild_mob_level_scaling
from player import Player
from cats import Cat

player = Player(width/2, height/2, "Glenjamin")

# Keep hostile spawns away from the starting area so the player isn't spawn-killed.
SPAWN_PROTECTION_CENTER = (width / 2, height / 2)
SPAWN_PROTECTION_RADIUS = 900  # pixels
SPAWN_PROTECTION_RADIUS_SQ = SPAWN_PROTECTION_RADIUS ** 2

def is_in_spawn_protection(x, y):
    return False


# Simple respawn queue so animal populations can recover over time.
# Entries are dicts: {"kind": str, "spawn_time": ms_since_start}
pending_respawns = []


def schedule_respawn(kind, delay_ms=30000):
    """Schedule a new animal of the given kind to spawn after delay_ms."""
    spawn_time = pygame.time.get_ticks() + max(0, int(delay_ms))
    pending_respawns.append({"kind": kind, "spawn_time": spawn_time})


def _random_level_for_position(x, y, base_min=1, base_max=3):
    """Depth-agnostic level helper: farther from spawn = higher level."""
    cx, cy = SPAWN_PROTECTION_CENTER
    dx = x - cx
    dy = y - cy
    dist = (dx * dx + dy * dy) ** 0.5
    # Every 6000 px away from spawn increases difficulty.
    distance_factor = int(dist // 6000)
    min_lvl = base_min + distance_factor
    max_lvl = base_max + distance_factor * 2
    # Clamp into [1, 100] and ensure min <= max.
    min_lvl = max(1, min(min_lvl, 100))
    max_lvl = max(1, min(max_lvl, 100))
    if max_lvl < min_lvl:
        max_lvl = min_lvl
    return random.randint(min_lvl, max_lvl)


def _spawn_squirrel():
    if not weighted_squirrel_tiles:
        return
    tile_x, tile_image = random.choice(weighted_squirrel_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Squirrel(x, y, "Squirrel")
    mob.level = _random_level_for_position(x, y, 1, 2)
    apply_wild_mob_level_scaling(mob)
    squirrels.append(mob)

def _spawn_cat():
    if not weighted_cat_tiles:
        return
    tile_x, tile_image = random.choice(weighted_cat_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Cat(x, y, "Cat")
    mob.level = _random_level_for_position(x, y, 1, 3)
    cats.append(mob)

def _spawn_cow():
    if not weighted_cow_tiles:
        return
    tile_x, tile_image = random.choice(weighted_cow_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Cow(x, y, "Cow")
    mob.level = _random_level_for_position(x, y, 2, 4)
    apply_wild_mob_level_scaling(mob)
    cows.append(mob)

def _spawn_chicken():
    if not weighted_chicken_tiles:
        return
    tile_x, tile_image = random.choice(weighted_chicken_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Chicken(x, y, "Chicken")
    mob.level = _random_level_for_position(x, y, 1, 2)
    apply_wild_mob_level_scaling(mob)
    chickens.append(mob)

def _spawn_deer():
    if not weighted_deer_tiles:
        return
    tile_x, tile_image = random.choice(weighted_deer_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Deer(x, y, "Deer")
    mob.level = _random_level_for_position(x, y, 2, 7)
    apply_wild_mob_level_scaling(mob)
    deers.append(mob)

def _spawn_wolf():
    if not weighted_wolf_tiles:
        return
    tile_x, tile_image = random.choice(weighted_wolf_tiles)
    attempts = 0
    while attempts < 10:
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        if not is_in_spawn_protection(x, y):
            mob = Wolf(x, y, "Wolf")
            mob.level = _random_level_for_position(x, y, 4, 10)
            apply_wild_mob_level_scaling(mob)
            wolves.append(mob)
            break
        attempts += 1

def _spawn_redmite():
    if not weighted_redmite_tiles:
        return
    tile_x, tile_image = random.choice(weighted_redmite_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 32)
    y = random.randint(0, height - 32)
    mob = Redmite(x, y, "Redmite")
    mob.level = _random_level_for_position(x, y, 2, 6)
    apply_wild_mob_level_scaling(mob)
    redmites.append(mob)

def _spawn_gila():
    if not weighted_gila_tiles:
        return
    tile_x, tile_image = random.choice(weighted_gila_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gila(x, y, "Gila")
    mob.level = _random_level_for_position(x, y, 4, 10)
    apply_wild_mob_level_scaling(mob)
    gilas.append(mob)

def _spawn_salamander():
    if not weighted_salamander_tiles:
        return
    tile_x, tile_image = random.choice(weighted_salamander_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Salamander(x, y, "Salamander")
    mob.level = _random_level_for_position(x, y, 5, 11)
    apply_wild_mob_level_scaling(mob)
    salamanders.append(mob)

def _spawn_mudrustle_gorlin():
    if not weighted_mudrustle_gorlin_tiles:
        return
    tile_x, tile_image = random.choice(weighted_mudrustle_gorlin_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gorlin(x, y, "Mudrustle Gorlin", "mudrustle")
    mob.level = _random_level_for_position(x, y, 6, 12)
    apply_wild_mob_level_scaling(mob)
    mudrustle_gorlins.append(mob)

def _spawn_slateback_gorlin():
    if not weighted_slateback_gorlin_tiles:
        return
    tile_x, tile_image = random.choice(weighted_slateback_gorlin_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gorlin(x, y, "Slateback Gorlin", "slateback")
    mob.level = _random_level_for_position(x, y, 6, 12)
    apply_wild_mob_level_scaling(mob)
    slateback_gorlins.append(mob)

def _spawn_fluffy_gorlin():
    if not weighted_fluffy_gorlin_tiles:
        return
    tile_x, tile_image = random.choice(weighted_fluffy_gorlin_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gorlin(x, y, "Fluffy Gorlin", "fluffy")
    mob.level = _random_level_for_position(x, y, 6, 12)
    apply_wild_mob_level_scaling(mob)
    fluffy_gorlins.append(mob)

def process_respawns():
    """Spawn any pending animals whose timers have expired."""
    if not pending_respawns:
        return
    now = pygame.time.get_ticks()
    remaining = []
    for entry in pending_respawns:
        if entry.get("spawn_time", 0) > now:
            remaining.append(entry)
            continue
        kind = entry.get("kind")
        if kind == "squirrel":
            _spawn_squirrel()
        elif kind == "cat":
            _spawn_cat()
        elif kind == "cow":
            _spawn_cow()
        elif kind == "chicken":
            _spawn_chicken()
        elif kind == "deer":
            _spawn_deer()
        elif kind == "wolf":
            _spawn_wolf()
        elif kind == "gila":
            _spawn_gila()
        elif kind == "salamander":
            _spawn_salamander()
        elif kind == "redmite":
            _spawn_redmite()
        elif kind == "mudrustle_gorlin":
            _spawn_mudrustle_gorlin()
        elif kind == "slateback_gorlin":
            _spawn_slateback_gorlin()
        elif kind == "fluffy_gorlin":
            _spawn_fluffy_gorlin()
        # Unknown kinds are ignored.
    pending_respawns[:] = remaining


num_deers = 0
num_squirrels = 0
num_cats = 20
num_cows = 0
num_chickens = 0
num_crows = 5

num_wolves = 0
num_glowbirds = 75
num_gilas = 50
num_salamanders = 50
num_redmites = 120
num_black_bears = 0
num_brown_bears = 0
num_polar_bears = 20
num_pandas = 0

num_ashhounds = 20
num_wastedogs = 20
num_crawlers = 0
num_pocks = 0
num_duskwretches = 0
num_mudrustle_gorlins = 0
num_slateback_gorlins = 0
num_fluffy_gorlins = 0

num_fire_dragons = 50
num_ice_dragons = 50
num_electric_dragons = 50
num_poison_dragons = 50
num_dusk_dragons = 50


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
for _ in range(num_squirrels):
    tile_x, tile_image = random.choice(weighted_squirrel_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Squirrel(x, y, "Squirrel")
    mob.level = _random_level_for_position(x, y, 1, 2)
    squirrels.append(mob)

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
for _ in range(num_cats):
    tile_x, tile_image = random.choice(weighted_cat_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Cat(x, y, "Cat")
    mob.level = _random_level_for_position(x, y, 1, 3)
    cats.append(mob)

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
for _ in range(num_cows):
    tile_x, tile_image = random.choice(weighted_cow_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Cow(x, y, "Cow")
    mob.level = _random_level_for_position(x, y, 2, 4)
    cows.append(mob)

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
for _ in range(num_chickens):
    tile_x, tile_image = random.choice(weighted_chicken_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Chicken(x, y, "Chicken")
    mob.level = _random_level_for_position(x, y, 1, 2)
    chickens.append(mob)

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
for _ in range(num_crawlers):
    tile_x, tile_image = random.choice(weighted_crawler_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Crawler(x, y, "Crawler")
    mob.level = _random_level_for_position(x, y, 3, 6)
    crawlers.append(mob)


allowed_ashhound_tiles = [bg_lavastone]

ashhound_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_ashhound_tiles]

ashhound_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 6,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_ashhound_tiles = []
for tile_x, tile_image in tiles:
    weight = ashhound_spawn_weights.get(tile_image, 0)
    weighted_ashhound_tiles.extend([(tile_x, tile_image)] * weight)

ashhounds = []
for _ in range(num_ashhounds):
    if weighted_ashhound_tiles:
        tile_x, tile_image = random.choice(weighted_ashhound_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        mob = Ashhound(x, y, "Ashhound")
        mob.level = _random_level_for_position(x, y, 5, 9)
        ashhounds.append(mob)


allowed_wastedog_tiles = [bg_wasteland]

wastedog_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 6,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_wastedog_tiles = []
for tile_x, tile_image in tiles:
    weight = wastedog_spawn_weights.get(tile_image, 0)
    weighted_wastedog_tiles.extend([(tile_x, tile_image)] * weight)

wastedogs = []
for _ in range(num_wastedogs):
    if weighted_wastedog_tiles:
        tile_x, tile_image = random.choice(weighted_wastedog_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        mob = Wastedog(x, y, "Wastedog")
        mob.level = _random_level_for_position(x, y, 4, 8)
        wastedogs.append(mob)

allowed_wolf_tiles = [bg_grass, bg_dirt]

wolf_spawn_weights = {
    bg_grass: 4,
    bg_dirt: 4,
    bg_compact: 0,
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

weighted_wolf_tiles = []
for tile_x, tile_image in tiles:
    weight = wolf_spawn_weights.get(tile_image, 0)
    weighted_wolf_tiles.extend([(tile_x, tile_image)] * weight)

wolves = []
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
for _ in range(num_duskwretches):
    tile_x, tile_image = random.choice(weighted_duskwretch_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Duskwretch(x, y, "Duskwretch")
    mob.level = _random_level_for_position(x, y, 5, 12)
    duskwretches.append(mob)

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
for _ in range(num_pocks):
    tile_x, tile_image = random.choice(weighted_pock_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Pock(x, y, "Pock")
    mob.level = _random_level_for_position(x, y, 3, 9)
    pocks.append(mob)

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
for _ in range(num_deers):
    tile_x, tile_image = random.choice(weighted_deer_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Deer(x, y, "Deer")
    mob.level = _random_level_for_position(x, y, 2, 7)
    deers.append(mob)

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
for _ in range(num_black_bears):
    tile_x, tile_image = random.choice(weighted_black_bear_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = BlackBear(x, y, "Black Bear")
    mob.level = _random_level_for_position(x, y, 6, 14)
    black_bears.append(mob)

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
for _ in range(num_brown_bears):
    tile_x, tile_image = random.choice(weighted_brown_bear_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = BrownBear(x, y, "Brown Bear")
    mob.level = _random_level_for_position(x, y, 6, 14)
    brown_bears.append(mob)

allowed_polar_bear_tiles = [bg_snow]

polar_bear_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_polar_bear_tiles]

polar_bear_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 10,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_polar_bear_tiles = []
for tile_x, tile_image in tiles:
    weight = polar_bear_spawn_weights.get(tile_image, 0)
    weighted_polar_bear_tiles.extend([(tile_x, tile_image)] * weight)

polar_bears = []
for _ in range(num_polar_bears):
    if weighted_polar_bear_tiles:
        tile_x, tile_image = random.choice(weighted_polar_bear_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        mob = PolarBear(x, y, "Polar Bear")
        mob.level = _random_level_for_position(x, y, 7, 15)
        polar_bears.append(mob)

allowed_panda_tiles = [bg_grass, bg_dirt, bg_compact, bg_savannah, bg_riverrock, bg_bigrock]

panda_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_panda_tiles]

panda_spawn_weights = {
    bg_grass: 3,
    bg_dirt: 2,
    bg_compact: 2,
    bg_savannah: 2,
    bg_riverrock: 1,
    bg_bigrock: 1,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_panda_tiles = []
for tile_x, tile_image in tiles:
    weight = panda_spawn_weights.get(tile_image, 0)
    weighted_panda_tiles.extend([(tile_x, tile_image)] * weight)

pandas = []
for _ in range(num_pandas):
    if weighted_panda_tiles:
        tile_x, tile_image = random.choice(weighted_panda_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        mob = PandaBear(x, y, "Panda")
        mob.level = _random_level_for_position(x, y, 5, 12)
        pandas.append(mob)

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
for _ in range(num_gilas):
    tile_x, tile_image = random.choice(weighted_gila_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gila(x, y, "Gila")
    mob.level = _random_level_for_position(x, y, 4, 10)
    gilas.append(mob)

allowed_salamander_tiles = [bg_compact]

salamander_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_salamander_tiles]

salamander_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 6,
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

weighted_salamander_tiles = []
for tile_x, tile_image in tiles:
    weight = salamander_spawn_weights.get(tile_image, 0)
    weighted_salamander_tiles.extend([(tile_x, tile_image)] * weight)

salamanders = []
for _ in range(num_salamanders):
    if not weighted_salamander_tiles:
        break
    tile_x, tile_image = random.choice(weighted_salamander_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Salamander(x, y, "Salamander")
    mob.level = _random_level_for_position(x, y, 5, 11)
    salamanders.append(mob)

allowed_redmite_tiles = [bg_redrock]

redmite_spawn_weights = {
    bg_redrock: 6
}

weighted_redmite_tiles = []
for tile_x, tile_image in tiles:
    weight = redmite_spawn_weights.get(tile_image, 0)
    weighted_redmite_tiles.extend([(tile_x, tile_image)] * weight)

redmites = []
for _ in range(num_redmites):
    if not weighted_redmite_tiles:
        break
    tile_x, tile_image = random.choice(weighted_redmite_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 32)
    y = random.randint(0, height - 32)
    mob = Redmite(x, y, "Redmite")
    mob.level = _random_level_for_position(x, y, 2, 6)
    redmites.append(mob)

allowed_mudrustle_gorlin_tiles = [bg_grass, bg_dirt, bg_compact, bg_riverrock, bg_savannah, bg_bigrock]

mudrustle_gorlin_spawn_weights = {
    bg_grass: 3,
    bg_dirt: 3,
    bg_compact: 2,
    bg_sand: 0,
    bg_savannah: 1,
    bg_riverrock: 2,
    bg_bigrock: 1,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_mudrustle_gorlin_tiles = []
for tile_x, tile_image in tiles:
    weight = mudrustle_gorlin_spawn_weights.get(tile_image, 0)
    weighted_mudrustle_gorlin_tiles.extend([(tile_x, tile_image)] * weight)

mudrustle_gorlins = []
for _ in range(num_mudrustle_gorlins):
    if not weighted_mudrustle_gorlin_tiles:
        break
    tile_x, tile_image = random.choice(weighted_mudrustle_gorlin_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gorlin(x, y, "Mudrustle Gorlin", "mudrustle")
    mob.level = _random_level_for_position(x, y, 6, 12)
    apply_wild_mob_level_scaling(mob)
    mudrustle_gorlins.append(mob)

allowed_slateback_gorlin_tiles = [bg_bigrock, bg_duskstone, bg_blackstone, bg_redrock, bg_wasteland]

slateback_gorlin_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 3,
    bg_duskstone: 3,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 2,
    bg_blackstone: 2,
    bg_redrock: 2
}

weighted_slateback_gorlin_tiles = []
for tile_x, tile_image in tiles:
    weight = slateback_gorlin_spawn_weights.get(tile_image, 0)
    weighted_slateback_gorlin_tiles.extend([(tile_x, tile_image)] * weight)

slateback_gorlins = []
for _ in range(num_slateback_gorlins):
    if not weighted_slateback_gorlin_tiles:
        break
    tile_x, tile_image = random.choice(weighted_slateback_gorlin_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gorlin(x, y, "Slateback Gorlin", "slateback")
    mob.level = _random_level_for_position(x, y, 6, 12)
    apply_wild_mob_level_scaling(mob)
    slateback_gorlins.append(mob)

allowed_fluffy_gorlin_tiles = [bg_snow, bg_bigrock, bg_grass]

fluffy_gorlin_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 2,
    bg_riverrock: 0,
    bg_bigrock: 1,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 5,
    bg_wasteland: 0,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_fluffy_gorlin_tiles = []
for tile_x, tile_image in tiles:
    weight = fluffy_gorlin_spawn_weights.get(tile_image, 0)
    weighted_fluffy_gorlin_tiles.extend([(tile_x, tile_image)] * weight)

fluffy_gorlins = []
for _ in range(num_fluffy_gorlins):
    if not weighted_fluffy_gorlin_tiles:
        break
    tile_x, tile_image = random.choice(weighted_fluffy_gorlin_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Gorlin(x, y, "Fluffy Gorlin", "fluffy")
    mob.level = _random_level_for_position(x, y, 6, 12)
    apply_wild_mob_level_scaling(mob)
    fluffy_gorlins.append(mob)

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
for _ in range(num_crows):
    tile_x, tile_image = random.choice(weighted_crow_tiles)
    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
    y = random.randint(0, height - 64)
    mob = Crow(x, y, "Crow")
    mob.level = _random_level_for_position(x, y, 1, 4)
    crows.append(mob)

allowed_glowbird_tiles = [bg_duskstone, bg_blackstone]

glowbird_spawn_tiles = [(tile_x, tile_image) for tile_x, tile_image in tiles if tile_image in allowed_glowbird_tiles]

glowbird_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 4,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 0,
    bg_blackstone: 4,
    bg_redrock: 0
}

weighted_glowbird_tiles = []
for tile_x, tile_image in tiles:
    weight = glowbird_spawn_weights.get(tile_image, 0)
    weighted_glowbird_tiles.extend([(tile_x, tile_image)] * weight)

glowbirds = []
for _ in range(num_glowbirds):
    if weighted_glowbird_tiles:
        tile_x, tile_image = random.choice(weighted_glowbird_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        mob = Glowbird(x, y, "Glowbird")
        mob.level = _random_level_for_position(x, y, 1, 5)
        glowbirds.append(mob)

allowed_fire_dragon_tiles = [bg_lavastone, bg_sand, bg_wasteland, bg_redrock, bg_blackstone]

fire_dragon_spawn_weights = {
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
    bg_wasteland: 2,
    bg_blackstone: 2,
    bg_redrock: 4
}

weighted_fire_dragon_tiles = []
for tile_x, tile_image in tiles:
    weight = fire_dragon_spawn_weights.get(tile_image, 0)
    weighted_fire_dragon_tiles.extend([(tile_x, tile_image)] * weight)

fire_dragons = []
for _ in range(num_fire_dragons):
    if weighted_fire_dragon_tiles:
        tile_x, tile_image = random.choice(weighted_fire_dragon_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        lvl = _random_level_for_position(x, y, 10, 40)
        fire_dragons.append(Dragon(x, y, "Fire Dragon", "fire", lvl))

allowed_ice_dragon_tiles = [bg_snow, bg_riverrock, bg_bigrock, bg_compact]

ice_dragon_spawn_weights = {
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

weighted_ice_dragon_tiles = []
for tile_x, tile_image in tiles:
    weight = ice_dragon_spawn_weights.get(tile_image, 0)
    weighted_ice_dragon_tiles.extend([(tile_x, tile_image)] * weight)

ice_dragons = []
for _ in range(num_ice_dragons):
    if weighted_ice_dragon_tiles:
        tile_x, tile_image = random.choice(weighted_ice_dragon_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        lvl = _random_level_for_position(x, y, 10, 40)
        ice_dragons.append(Dragon(x, y, "Ice Dragon", "ice", lvl))

allowed_electric_dragon_tiles = [bg_duskstone, bg_blackstone, bg_bigrock, bg_wasteland]

electric_dragon_spawn_weights = {
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
    bg_wasteland: 5,
    bg_blackstone: 2,
    bg_redrock: 0
}

weighted_electric_dragon_tiles = []
for tile_x, tile_image in tiles:
    weight = electric_dragon_spawn_weights.get(tile_image, 0)
    weighted_electric_dragon_tiles.extend([(tile_x, tile_image)] * weight)

electric_dragons = []
for _ in range(num_electric_dragons):
    if weighted_electric_dragon_tiles:
        tile_x, tile_image = random.choice(weighted_electric_dragon_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        lvl = _random_level_for_position(x, y, 10, 40)
        electric_dragons.append(Dragon(x, y, "Electric Dragon", "electric", lvl))

allowed_poison_dragon_tiles = [bg_wasteland, bg_compact, bg_redrock, bg_blackstone]

poison_dragon_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 1,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 0,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 4,
    bg_blackstone: 0,
    bg_redrock: 0
}

weighted_poison_dragon_tiles = []
for tile_x, tile_image in tiles:
    weight = poison_dragon_spawn_weights.get(tile_image, 0)
    weighted_poison_dragon_tiles.extend([(tile_x, tile_image)] * weight)

poison_dragons = []
for _ in range(num_poison_dragons):
    if weighted_poison_dragon_tiles:
        tile_x, tile_image = random.choice(weighted_poison_dragon_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        lvl = _random_level_for_position(x, y, 10, 40)
        poison_dragons.append(Dragon(x, y, "Poison Dragon", "poison", lvl))

allowed_dusk_dragon_tiles = [bg_duskstone, bg_wasteland, bg_blackstone, bg_redrock, bg_dirt]

dusk_dragon_spawn_weights = {
    bg_grass: 0,
    bg_dirt: 0,
    bg_compact: 0,
    bg_sand: 0,
    bg_savannah: 0,
    bg_riverrock: 0,
    bg_bigrock: 0,
    bg_duskstone: 5,
    bg_lavastone: 0,
    bg_snow: 0,
    bg_wasteland: 1,
    bg_blackstone: 1,
    bg_redrock: 4
}

weighted_dusk_dragon_tiles = []
for tile_x, tile_image in tiles:
    weight = dusk_dragon_spawn_weights.get(tile_image, 0)
    weighted_dusk_dragon_tiles.extend([(tile_x, tile_image)] * weight)

dusk_dragons = []
for _ in range(num_dusk_dragons):
    if weighted_dusk_dragon_tiles:
        tile_x, tile_image = random.choice(weighted_dusk_dragon_tiles)
        x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
        y = random.randint(0, height - 64)
        lvl = _random_level_for_position(x, y, 10, 40)
        dusk_dragons.append(Dragon(x, y, "Dusk Dragon", "dusk", lvl))
