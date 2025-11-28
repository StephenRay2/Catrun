import pygame
import math
pygame.init()
from buttons import *
from mob_placement import *
from sounds import *
from crafting_bench import CraftingBench
from smelter import Smelter

clock = pygame.time.Clock()
from inventory import *
running = True
dt = 0
size = 64
world_x = 0.0
absolute_cam_x = 0.0
floor_y = 0
shift_multiplier = 1
dungeon_depth = absolute_cam_x
dungeon_depth_high = 0
font = pygame.font.SysFont(None, 24)
scroll = 0
dungeon_traversal_speed = .1
time_of_day = 12.00
total_elapsed_time = 00.00
stamina_depleted_message_timer = 0
player_world_x = player_pos.x + cam_x
player_world_y = player_pos.y

collection_messages = []

# Cat naming system
naming_cat = None
cat_name_input = ""

paused = False
inventory_in_use = False
debug_step_mode = False
debug_should_step_frame = False

step_sound_timer = 0
step_sound_delay = 0.4
collect_cooldown = 0
collect_delay = 100
harvest_cooldown = 0
harvest_delay = 300
inventory_resources = []
state = "menu"
generate_world()
previous_state = state
sound_manager.play_music("assets/music/Settler's End.wav")

# Throw mechanic variables
throw_charge_start = None
max_throw_charge = 1.0
min_throw_power = 2
max_throw_power = 8
min_throw_hold_time = 0.15  # Minimum hold time (in seconds) to trigger throw instead of pickup
thrown_items = []
loaded_item_sprites = {}  # Cache for loaded item sprites

# Placement system variables
placement_mode = False
placement_item = None
placement_position = (0, 0)
placed_structures = []

# Crafting bench variables
crafting_bench = None
crafting_bench_in_use = False
smelter = None
smelter_in_use = False

default_placeable_sprite_size = (64, 64)

placeable_size_settings = {
    "Torch": {
        "sprite": (24, 24),
        "collision": {
            "width_ratio": 0.5,
            "height_ratio": 0.3,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Workbench": {
        "sprite": (64, 64),
        "collision": {
            "width_ratio": 0.8,
            "height_ratio": 0.4,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Campfire": {
        "sprite": (48, 48),
        "collision": {
            "width_ratio": 0.6,
            "height_ratio": 0.3,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Oil Lamp": {
        "sprite": (32, 32),
        "collision": {
            "width_ratio": 0.4,
            "height_ratio": 0.25,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Cooking Pot": {
        "sprite": (32, 32),
        "collision": {
            "width_ratio": 0.5,
            "height_ratio": 0.3,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Smelter": {
        "sprite": (64, 64),
        "collision": {
            "width_ratio": 0.6,
            "height_ratio": 0.2,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -.75
        }
    },
    "Empty Cage": {
        "sprite": (48, 48),
        "collision": {
            "width_ratio": 0.7,
            "height_ratio": 0.5,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Alchemy Bench": {
        "sprite": (64, 64),
        "collision": {
            "width_ratio": 0.8,
            "height_ratio": 0.4,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Fence": {
        "sprite": (48, 48),
        "collision": {
            "width_ratio": 0.9,
            "height_ratio": 0.6,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Chest": {
        "sprite": (48, 48),
        "collision": {
            "width_ratio": 0.6,
            "height_ratio": 0.3,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Tent": {
        "sprite": (96, 96),
        "collision": {
            "width_ratio": 0.8,
            "height_ratio": 0.5,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Lantern": {
        "sprite": (24, 24),
        "collision": {
            "width_ratio": 0.4,
            "height_ratio": 0.25,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        }
    },
    "Mortar And Pestle": {
        "sprite": (24, 24),
        "collision": {
            "width_ratio": 0.45,
            "height_ratio": 0.25,
            "offset_x_ratio": -0.6,
            "offset_y_ratio": -5
        }
    },
}

# Debug variables
debug_movement_rotation = 15

def calculate_proportional_collision(sprite_width, sprite_height, custom_collision=None):
    """Generate a collision box proportionate to the sprite scale.
    
    Args:
        sprite_width: Width of the sprite
        sprite_height: Height of the sprite
        custom_collision: Optional dict with 'width_ratio', 'height_ratio', 'offset_x_ratio', 'offset_y_ratio'
    
    Returns:
        Tuple of (collision_x_offset, collision_y_offset, collision_width, collision_height)
    """
    if custom_collision:
        # Use custom collision settings
        width_ratio = custom_collision.get("width_ratio", 0.55)
        height_ratio = custom_collision.get("height_ratio", 0.25)
        offset_x_ratio = custom_collision.get("offset_x_ratio", -0.5)
        offset_y_ratio = custom_collision.get("offset_y_ratio", -1.0)
    else:
        # Use default proportional settings
        width_ratio = 0.55
        height_ratio = 0.25
        offset_x_ratio = -0.5
        offset_y_ratio = -1

    collision_width = max(1, int(sprite_width * width_ratio))
    collision_height = max(1, int(sprite_height * height_ratio))

    collision_x_offset = int(collision_width * offset_x_ratio)
    collision_y_offset = int(collision_height * offset_y_ratio)

    return (collision_x_offset, collision_y_offset, collision_width, collision_height)


def get_placeable_sizes(item_data):
    """Return sprite and collision sizes for a placeable item."""
    if not item_data:
        return (
            default_placeable_sprite_size,
            calculate_proportional_collision(*default_placeable_sprite_size),
        )
    
    item_name = item_data.get("item_name")
    size_settings = placeable_size_settings.get(item_name, {})
    sprite_size = size_settings.get("sprite", default_placeable_sprite_size)
    
    # Get custom collision settings if available, otherwise use default proportions
    collision_settings = size_settings.get("collision", None)
    collision_size = calculate_proportional_collision(sprite_size[0], sprite_size[1], collision_settings)
    
    return sprite_size, collision_size


def update_placeable_collision(item_name, collision_settings):
    """Update collision settings for a specific placeable item.
    
    Args:
        item_name: Name of the placeable item
        collision_settings: Dict with collision parameters:
            - width_ratio: Fraction of sprite width for collision box (0.0 to 1.0)
            - height_ratio: Fraction of sprite height for collision box (0.0 to 1.0)  
            - offset_x_ratio: Horizontal offset as fraction of collision width (-1.0 to 1.0)
            - offset_y_ratio: Vertical offset as fraction of collision height (-2.0 to 1.0)
    
    Example:
        update_placeable_collision("Workbench", {
            "width_ratio": 0.8,
            "height_ratio": 0.4,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
        })
    """
    if item_name in placeable_size_settings:
        if "collision" not in placeable_size_settings[item_name]:
            placeable_size_settings[item_name]["collision"] = {}
        
        placeable_size_settings[item_name]["collision"].update(collision_settings)
    else:
        # Create new entry for the item
        placeable_size_settings[item_name] = {
            "sprite": default_placeable_sprite_size,
            "collision": collision_settings
        }


# COLLISION BOX EDITING EXAMPLES
# ================================
# 
# You can customize collision boxes for any placeable item using the update_placeable_collision() function:
# 
# # Make Torch have a smaller, centered collision box
# update_placeable_collision("Torch", {
#     "width_ratio": 0.3,
#     "height_ratio": 0.2,
#     "offset_x_ratio": 0.0,
#     "offset_y_ratio": -1.0
# })
# 
# # Make Tent have a wider collision box  
# update_placeable_collision("Tent", {
#     "width_ratio": 1.0,
#     "height_ratio": 0.6,
#     "offset_x_ratio": -0.5,
#     "offset_y_ratio": -1.0
# })
# 
# # Make Chest have a taller collision box
# update_placeable_collision("Chest", {
#     "width_ratio": 0.6,
#     "height_ratio": 0.5,
#     "offset_x_ratio": -0.5,
#     "offset_y_ratio": -1.0
# })
#
# COLLISION PARAMETER EXPLANATIONS:
# =================================
# - width_ratio: How wide the collision box is relative to sprite width (0.1 = 10% of sprite width)
# - height_ratio: How tall the collision box is relative to sprite height (0.2 = 20% of sprite height)  
# - offset_x_ratio: Horizontal positioning (-0.5 = center, -1.0 = left edge, 0.0 = right edge)
# - offset_y_ratio: Vertical positioning (-1.0 = bottom aligned, -0.5 = center, 0.0 = top aligned)


def populate_test_inventory():
    """Add one of each placeable item to the main inventory for testing purposes."""
    items_added = 0
    
    for item_name in placeable_size_settings.keys():
        item_data = next((itm for itm in items_list if itm["item_name"] == item_name), None)
        if not item_data:
            print(f"Warning: Item '{item_name}' not found in items_list")
            continue
        
        new_item = item_data.copy()
        new_item["quantity"] = 1
        
        target_slot = None
        for idx, slot in enumerate(inventory.inventory_list):
            if slot is None:
                target_slot = idx
                break
        
        if target_slot is not None:
            inventory.inventory_list[target_slot] = new_item
            items_added += 1
            print(f"Added {item_name} to inventory slot {target_slot}")
        else:
            print(f"Warning: No empty inventory slots available for {item_name}")
            break
    
    print(f"Successfully added {items_added} placeable items to inventory for testing")
    return items_added

def calculate_throw_trajectory(start_x, start_y, target_x, target_y, throw_power):
    delta_x = target_x - start_x
    delta_y = target_y - start_y
    distance_to_target = (delta_x**2 + delta_y**2) ** 0.5
    
    if distance_to_target == 0:
        # Throwing at player position, no direction
        return 0, 0, 0
    
    # Normalize direction
    dir_x = delta_x / distance_to_target
    dir_y = delta_y / distance_to_target
    
    # Max distance based on throw power (scales from min to max throw power)
    # throw_power ranges from 0 to 1
    max_distance = min_throw_power + (throw_power * (max_throw_power - min_throw_power))
    
    return dir_x, dir_y, max_distance

def spawn_thrown_item(x, y, vel_x, vel_y, item_data, is_cat=False, throw_power=1.0):
    # Load the item sprite
    sprite = None
    sprite_size = 64 if is_cat else 32  # Cats are 64x64, regular items are 32x32
    cache_key = f"{item_data.get('icon', 'unknown')}_{sprite_size}" if item_data else None
    
    if item_data and "icon" in item_data:
        icon_name = item_data["icon"]
        if cache_key not in loaded_item_sprites:
            try:
                # Handle both full paths (e.g., "assets/sprites/mobs/...") and filenames
                if icon_name.startswith("assets/"):
                    sprite_path = icon_name
                else:
                    sprite_path = f"assets/sprites/items/{icon_name}"
                loaded_sprite = pygame.image.load(sprite_path).convert_alpha()
                # Scale based on item type
                loaded_sprite = pygame.transform.scale(loaded_sprite, (sprite_size, sprite_size))
                loaded_item_sprites[cache_key] = loaded_sprite
            except:
                loaded_item_sprites[cache_key] = None
        sprite = loaded_item_sprites[cache_key]
    
    # Calculate speed (magnitude of velocity vector)
    speed = (vel_x**2 + vel_y**2) ** 0.5
    
    # Normalize direction
    if speed > 0:
        dir_x = vel_x / speed
        dir_y = vel_y / speed
    else:
        dir_x = 0
        dir_y = 0
    
    thrown_item = {
        "x": x,
        "y": y,
        "dir_x": dir_x,  # Normalized direction X
        "dir_y": dir_y,  # Normalized direction Y
        "speed": speed,  # How fast it travels per frame
        "distance_traveled": 0,  # Track distance traveled
        "max_distance": (min_throw_power + (throw_power * (max_throw_power - min_throw_power))) * 75,
        "item": item_data,
        "sprite": sprite,
        "sprite_size": sprite_size,
        "is_cat": is_cat,
        "cat_data": item_data if is_cat else None,
        "landed": False  # Track if item has landed
    }
    thrown_items.append(thrown_item)

def create_world_item_from_thrown(thrown_item):
    """Convert a thrown item to a world item and add it to the appropriate list"""
    if not thrown_item["item"]:
        return False
    
    item_name = thrown_item["item"].get("item_name", "")
    x = int(thrown_item["x"])
    y = int(thrown_item["y"])
    
    # Map item names to world item classes
    if item_name == "Sticks":
        sticks.append(Stick(x, y))
        return True
    elif item_name == "Stone":
        stones.append(Stone(x, y))
        return True
    elif item_name == "Mushroom":
        mushrooms.append(Mushroom(x, y))
        return True
    
    return False

def get_current_background(player_world_x, tiles):
    for tile_x, tile_image in tiles:
        if tile_x <= player_world_x < tile_x + BACKGROUND_SIZE:
            return tile_image
    return bg_grass

def get_footstep_sounds(background):
    grass_backgrounds = [bg_grass, bg_compact]
    dirt_backgrounds = [bg_dirt, bg_duskstone, bg_wasteland, bg_blackstone, bg_redrock, bg_lavastone]
    sand_backgrounds = [bg_sand, bg_savannah]

    if background in grass_backgrounds:
        return [f"footstep_grass{i}" for i in range(1, 7)]
    elif background in dirt_backgrounds:
        return [f"footstep_dirt{i}" for i in range(1, 7)]
    elif background in sand_backgrounds:
        return [f"footstep_sand{i}" for i in range(1, 7)]
    else:
        return [f"footstep_grass{i}" for i in range(1, 7)]

def calculate_temperature(current_background, time_of_day, player_swimming=False, player_in_lava=False, player_temp_resistance=0):
    if player_in_lava:
        return 120
    
    biome_temperatures = {
        bg_grass: {"5am": 50, "5pm": 70},
        bg_dirt: {"5am": 45, "5pm": 65},
        bg_compact: {"5am": 55, "5pm": 75},
        bg_sand: {"5am": 50, "5pm": 100},
        bg_savannah: {"5am": 55, "5pm": 80},
        bg_riverrock: {"5am": 40, "5pm": 60},
        bg_bigrock: {"5am": 40, "5pm": 60},
        bg_duskstone: {"5am": 30, "5pm": 60},
        bg_lavastone: {"5am": 100, "5pm": 120},
        bg_blackstone: {"5am": 35, "5pm": 65},
        bg_redrock: {"5am": 50, "5pm": 70},
        bg_snow: {"5am": 0, "5pm": 20},
    }
    
    if current_background == bg_lavastone:
        return 110 + (5 * math.sin(time_of_day * math.pi / 12))
    
    if current_background == bg_wasteland:
        wasteland_base_seed = int(total_elapsed_time / 100.0)
        random.seed(wasteland_base_seed)
        base_wasteland_temp = random.randint(10, 110)
        wasteland_fluctuation = 40 * math.sin((total_elapsed_time / 200.0) * math.pi)
        temp = base_wasteland_temp + wasteland_fluctuation
        temp = max(10, min(110, temp))
        if player_swimming:
            temp -= 30
    else:
        if current_background in biome_temperatures:
            temp_data = biome_temperatures[current_background]
            am_temp = temp_data["5am"]
            pm_temp = temp_data["5pm"]
        else:
            am_temp = 55
            pm_temp = 65
        
        hour_normalized = (time_of_day % 24)
        
        if 5 <= hour_normalized < 17:
            progress = (hour_normalized - 5) / 12
            temp = am_temp + (pm_temp - am_temp) * progress
        else:
            if hour_normalized >= 17:
                hours_into_cooling = hour_normalized - 17
            else:
                hours_into_cooling = (24 - 17) + hour_normalized
            progress = hours_into_cooling / 12
            temp = pm_temp + (am_temp - pm_temp) * progress
        
        if player_swimming:
            temp -= 30
    
    shift_amount = player_temp_resistance * 2
    if temp > 60:
        temp = max(60, temp - shift_amount)
    elif temp < 60:
        temp = min(60, temp + shift_amount)
    
    return max(0, min(120, temp))

def get_temperature_gauge_index(temperature):
    gauge_index = int((temperature / 120) * 7)
    return max(0, min(6, gauge_index))

def draw_temperature_gauge(screen, current_temperature, gauge_index):
    from buttons import temperature_gauges
    gauge_image = temperature_gauges[gauge_index]
    screen.blit(gauge_image, (20, height - 84))

def apply_temperature_effects(player, gauge_index, dt):
    if gauge_index == 0 or gauge_index == 6:
        player.extreme_temp_timer += dt
        
        if player.extreme_temp_timer >= 180:
            player.speed = int(100 * player.speed_leveler * (2/3))
        
        if gauge_index == 0:
            player.health -= dt * 1
            player.hunger -= dt * 0.5
            if player.stamina_timer <= 0 and player.stamina < player.max_stamina:
                if player.thirst == player.max_thirst:
                    player.stamina += dt * 8
                elif player.thirst > player.max_thirst * 0.7:
                    player.stamina += dt * 5
                elif player.thirst > player.max_thirst * 0.4:
                    player.stamina += dt * 3
                elif player.thirst > player.max_thirst * 0.1:
                    player.stamina += dt * 1
        else:
            player.health -= dt * 1
            player.thirst -= dt * 0.5
            if player.stamina_timer <= 0 and player.stamina < player.max_stamina:
                if player.thirst == player.max_thirst:
                    player.stamina += dt * 8
                elif player.thirst > player.max_thirst * 0.7:
                    player.stamina += dt * 5
                elif player.thirst > player.max_thirst * 0.4:
                    player.stamina += dt * 3
                elif player.thirst > player.max_thirst * 0.1:
                    player.stamina += dt * 1
    else:
        if player.extreme_temp_timer > 0:
            player.extreme_temp_timer -= dt
            if player.extreme_temp_timer <= 0:
                player.extreme_temp_timer = 0
                player.speed = int(100 * player.speed_leveler)
        
        if gauge_index == 1:
            player.hunger -= dt * 0.05
        elif gauge_index == 5:
            player.thirst -= dt * 0.05

# Placement system functions
def start_placement(item_data):
    """Start placement mode for a placeable item"""
    global placement_mode, placement_item, placement_position

    if not item_data or not item_data.get("placeable", False):
        return False

    placement_mode = True
    placement_item = item_data
    # Start placement in front of player
    placement_distance = 50
    if player.last_direction == "right":
        placement_position = (player_world_x + placement_distance, player_world_y)
    elif player.last_direction == "left":
        placement_position = (player_world_x - placement_distance, player_world_y)
    elif player.last_direction == "up":
        placement_position = (player_world_x, player_world_y - placement_distance)
    else:  # "down"
        placement_position = (player_world_x, player_world_y + placement_distance)

    return True

def cancel_placement():
    """Cancel placement mode"""
    global placement_mode, placement_item, placement_position
    placement_mode = False
    placement_item = None
    placement_position = (0, 0)

def check_placement_collision(x, y, item_data):
    """Check if placement position collides with world objects or mobs"""
    # Define collision bounds based on item sizing
    _, collision_size = get_placeable_sizes(item_data)
    
    # Handle both old format (width, height) and new format (x_offset, y_offset, width, height)
    if len(collision_size) == 4:
        collision_x_offset, collision_y_offset, collision_width, collision_height = collision_size
    else:
        # Fallback for old format - center the collision box
        collision_width, collision_height = collision_size
        collision_x_offset = -collision_width // 2
        collision_y_offset = -collision_height // 2

    collision_rect = pygame.Rect(x + collision_x_offset, y + collision_y_offset, collision_width, collision_height)

    # Check collision with world objects
    from world import rocks, boulders, trees, berry_bushes, ponds, lavas, dead_bushes, grasses, sticks, stones, savannah_grasses, mushrooms, fruit_plants, ferns

    # Check rocks (use their actual collision rect in world space)
    for rock in rocks:
        if hasattr(rock, 'rect'):
            rock_collision = pygame.Rect(
                rock.rect.x + 10,
                rock.rect.y + (rock.rect.height * 0.22),
                rock.rect.width - 20,
                rock.rect.height - 50
            )
            if rock_collision.colliderect(collision_rect):
                return True

    # Check boulders (use their actual collision rect in world space)
    for boulder in boulders:
        if hasattr(boulder, 'rect'):
            boulder_collision = pygame.Rect(
                boulder.rect.x + 10,
                boulder.rect.y + (boulder.rect.height * 0.22),
                boulder.rect.width - 20,
                boulder.rect.height - 50
            )
            if boulder_collision.colliderect(collision_rect):
                return True

    # Check trees
    for tree in trees:
        if hasattr(tree, 'rect') and tree.rect.colliderect(collision_rect):
            return True

    # Check berry bushes
    for bush in berry_bushes:
        if hasattr(bush, 'rect') and bush.rect.colliderect(collision_rect):
            return True

    # Check ponds
    for pond in ponds:
        if hasattr(pond, 'rect') and pond.rect.colliderect(collision_rect):
            return True

    # Check lavas
    for lava in lavas:
        if hasattr(lava, 'rect') and lava.rect.colliderect(collision_rect):
            return True

    # Check mobs
    from mob_placement import cats, squirrels, cows, chickens, crawlers, pocks, deers, black_bears, brown_bears, gilas, crows, duskwretches, fire_dragons, ice_dragons, electric_dragons, poison_dragons, dusk_dragons

    all_mobs = cats + squirrels + cows + chickens + crawlers + pocks + deers + black_bears + brown_bears + gilas + crows + duskwretches + fire_dragons + ice_dragons + electric_dragons + poison_dragons + dusk_dragons

    for mob in all_mobs:
        if hasattr(mob, 'rect') and mob.rect.colliderect(collision_rect):
            return True

    # Check already placed structures
    for structure in placed_structures:
        if structure['rect'].colliderect(collision_rect):
            return True

    return False

def place_structure(x, y, item_data):
    """Place a structure at the given position"""
    global placed_structures

    sprite_size, collision_size = get_placeable_sizes(item_data)
    
    # Handle both old format (width, height) and new format (x_offset, y_offset, width, height)
    if len(collision_size) == 4:
        collision_x_offset, collision_y_offset, collision_width, collision_height = collision_size
    else:
        # Fallback for old format - center the collision box
        collision_width, collision_height = collision_size
        collision_x_offset = -collision_width // 2
        collision_y_offset = -collision_height // 2

    # Create structure data
    structure = {
        'item_name': item_data['item_name'],
        'icon': item_data['icon'],
        'x': x,
        'y': y,
        'placed_time': pygame.time.get_ticks(),
        'sprite_size': sprite_size,
        'collision_size': collision_size,
        'rect': pygame.Rect(x + collision_x_offset, y + collision_y_offset, collision_width, collision_height)
    }

    placed_structures.append(structure)

    # Remove item from inventory
    selected_slot = inventory.hotbar_slots[inventory.selected_hotbar_slot]
    if selected_slot and selected_slot['quantity'] > 0:
        selected_slot['quantity'] -= 1
        if selected_slot['quantity'] <= 0:
            inventory.hotbar_slots[inventory.selected_hotbar_slot] = None

    return True

def update_placement_position():
    """Update placement position to stay in front of the player"""
    global placement_position

    if not placement_mode:
        return

    # Keep item in front of player based on their facing direction
    placement_distance = 50
    if player.last_direction == "right":
        placement_position = (player_world_x + placement_distance, player_world_y)
    elif player.last_direction == "left":
        placement_position = (player_world_x - placement_distance, player_world_y)
    elif player.last_direction == "up":
        placement_position = (player_world_x, player_world_y - placement_distance)
    else:  # "down"
        placement_position = (player_world_x, player_world_y + placement_distance)

def group_resources_by_type(resource_list):
    resource_counts = {}
    for resource in resource_list:
        if resource in resource_counts:
            resource_counts[resource] += 1
        else:
            resource_counts[resource] = 1
    return resource_counts

def add_collection_message(resource_name, count):
    text_surface = font.render(f"Collected {count} {resource_name}", True, (20, 255, 20))
    bg_surface = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 10), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 100))
    rect = pygame.Rect(20, 20, text_surface.get_width(), text_surface.get_height())
    
    collection_messages.insert(0, [text_surface, bg_surface, rect, 3.0, 3.0])

def get_selected_hotbar_item():
    """Return the item currently selected in the hotbar, if any."""
    selected_slot = inventory.selected_hotbar_slot
    if 0 <= selected_slot < len(inventory.hotbar_slots):
        return inventory.hotbar_slots[selected_slot]
    return None

def is_pickaxe_item(item):
    """Check if the given inventory item is any type of pickaxe."""
    if not item:
        return False
    item_name = item.get("item_name", "").lower()
    tags = item.get("tags", [])
    return "pickaxe" in item_name or ("mining" in tags)

def is_axe_item(item):
    """Check if the given inventory item is any type of axe (not pickaxe)."""
    if not item:
        return False
    item_name = item.get("item_name", "").lower()
    return "axe" in item_name and "pickaxe" not in item_name

def get_tool_tier(item):
    """Return a normalized tier name for resource multipliers."""
    if not item:
        return None
    name = item.get("item_name", "").lower()
    if "dragon" in name:
        return "dragon"
    if "obsidian" in name:
        return "obsidian"
    if "metal" in name:
        return "metal"
    if "gold" in name:
        return "gold"
    if "stone" in name:
        return "stone"
    if "wood" in name:
        return "wood"
    if "bone" in name:
        return "bone"
    return None

tool_multipliers = {
    "wood": {"normal": 1, "special": 1},
    "stone": {"normal": 2, "special": 2},
    "metal": {"normal": 3, "special": 3},
    "gold": {"normal": 1, "special": 6},
    "bone": {"normal": 6, "special": 1},
    "obsidian": {"normal": 4, "special": 4},
    "dragon": {"normal": 8, "special": 8},
}

special_resources = {"Flint", "Raw Metal", "Raw Gold"}
mining_resources = {"Stone", "Flint", "Raw Metal", "Raw Gold"}

def is_wood_resource(resource_name):
    lower_name = resource_name.lower()
    return "wood" in lower_name or resource_name == "Sticks"

def adjust_resources_with_tool(resources, tool_item):
    """Apply resource multipliers based on the equipped pickaxe/axe."""
    if not resources or not tool_item:
        return resources
    tier = get_tool_tier(tool_item)
    if not tier or tier not in tool_multipliers:
        return resources
    is_pickaxe = is_pickaxe_item(tool_item)
    is_axe = is_axe_item(tool_item)
    if not (is_pickaxe or is_axe):
        return resources

    adjusted = []
    for res in resources:
        res_name = res if isinstance(res, str) else str(res)
        # Enforce tool applicability by resource family.
        if is_pickaxe and res_name not in mining_resources:
            adjusted.append(res_name)
            continue
        if is_axe and not is_wood_resource(res_name):
            adjusted.append(res_name)
            continue

        is_special = res_name in special_resources
        mult = tool_multipliers.get(tier, {"normal": 1, "special": 1})
        factor = mult["special"] if is_special else mult["normal"]
        adjusted.extend([res_name] * max(1, factor))
    return adjusted

def calculate_held_item_offset(base_offset, frame_index, num_frames, direction, is_attacking, is_moving):
    if is_attacking:
        return calculate_attack_arc_offset(base_offset, frame_index, num_frames, direction)
    elif is_moving:
        return calculate_movement_offset(base_offset, frame_index, num_frames, direction)
    else:
        return base_offset

def calculate_attack_arc_offset(base_offset, frame_index, num_frames, direction):
    progress = frame_index / num_frames
    
    x_offset, y_offset = base_offset
    
    if direction == "right":
        arc_x = 20 * math.sin(progress * math.pi)
        arc_y = -25 * math.sin(progress * math.pi)
        return (x_offset + arc_x, y_offset + arc_y)
    elif direction == "left":
        arc_x = -20 * math.sin(progress * math.pi)
        arc_y = -25 * math.sin(progress * math.pi)
        return (x_offset + arc_x, y_offset + arc_y)
    elif direction == "down":
        arc_x = 0
        arc_y = 20 * math.sin(progress * math.pi)
        return (x_offset + arc_x, y_offset + arc_y)
    elif direction == "up":
        arc_x = 0
        arc_y = -20 * math.sin(progress * math.pi)
        return (x_offset + arc_x, y_offset + arc_y)
    
    return base_offset

def calculate_movement_offset(base_offset, frame_index, num_frames, direction):
    progress = frame_index / num_frames
    
    x_offset, y_offset = base_offset
    
    if direction == "right":
        pendulum_x = 8 * math.sin(progress * math.pi * 2)
        return (x_offset + pendulum_x, y_offset)
    elif direction == "left":
        pendulum_x = -8 * math.sin(progress * math.pi * 2)
        return (x_offset + pendulum_x, y_offset)
    elif direction == "down":
        bob_y = 6 * math.sin(progress * math.pi * 2)
        return (x_offset, y_offset + bob_y)
    elif direction == "up":
        bob_y = 6 * math.sin(progress * math.pi * 2)
        return (x_offset, y_offset + bob_y)
    
    return base_offset

def calculate_movement_rotation(frame_index, num_frames, direction, pendulum_offset):
    if direction in ["right", "left"]:
        rotation = (pendulum_offset / 8.0) * debug_movement_rotation
        return rotation
    
    return 0

def handle_debug_rotation_input(event):
    global debug_movement_rotation
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
            debug_movement_rotation += 1
            print(f"Movement rotation: {debug_movement_rotation}°")
        elif event.key == pygame.K_MINUS:
            debug_movement_rotation -= 1
            print(f"Movement rotation: {debug_movement_rotation}°")

def handle_debug_step_input(event):
    global debug_step_mode, debug_should_step_frame
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_h:
            debug_step_mode = not debug_step_mode
            if debug_step_mode:
                print("DEBUG: Frame step mode ENABLED - Press SPACE to advance one frame")
            else:
                print("DEBUG: Frame step mode DISABLED")
        elif event.key == pygame.K_SPACE and debug_step_mode:
            debug_should_step_frame = True
            print("DEBUG: Stepping one frame")

while running:
    if state != previous_state:
        if state == "menu":
            sound_manager.stop_music()
            sound_manager.play_music("assets/music/Settler's End.wav")
        elif state == "game":
            sound_manager.stop_music()
            sound_manager.play_random_ambient_music(min_delay=200, max_delay=800, volume=0.2, fade_in=4000)
        previous_state = state
    
    if state == "menu":
        menu_image = bg_grass
        menu_screen = pygame.Rect(0, 0, width, height)
        screen.blit(menu_image, (0, 0), menu_screen)

        collectibles = sticks + stones + grasses + savannah_grasses + mushrooms 
        all_objects = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants + ponds + lavas

        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -1000 and col.rect.y - cam_x < width + 1000]
        all_objects_no_liquids = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants
        visible_objects = [obj for obj in all_objects_no_liquids if obj.rect.x - cam_x > -1000 and obj.rect.x - cam_x < width + 1000]
        
        visible_liquids = [obj for obj in (ponds + lavas) if obj.rect.x - cam_x > -1000 and obj.rect.x - cam_x < width + 1000]
        
        visible_objects.extend(visible_collectibles)

        player_drawn = False

        for tile_x, tile_image in tiles:
            screen_x = tile_x - cam_x
            if -BACKGROUND_SIZE < screen_x < width:
                screen.blit(tile_image, (screen_x, floor_y))

        for obj in visible_liquids:
            obj.update_animation(dt)
            obj.draw(screen, cam_x)
        
        for obj in visible_objects:
            object_mid_y = obj.rect.y + obj.rect.height / 2
            obj.draw(screen, cam_x)

        catrun_title = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/catrun_title.png").convert_alpha(), (800, 200))
        screen.blit(catrun_title, (width/2 - catrun_title.get_width()/2, 100))
        new_game_button.draw(screen)
        load_button.draw(screen)
        menu_settings_button.draw(screen)
        menu_quit_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if new_game_button.is_clicked(event):
                state = "game"
                game_just_started = True
            elif load_button.is_clicked(event):
                pass
            elif menu_settings_button.is_clicked(event):
                pass
            elif menu_quit_button.is_clicked(event):
                running = False
        
        cam_x += .5
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    elif state == "game":
        should_process_frame = not debug_step_mode or debug_should_step_frame
        if debug_should_step_frame:
            debug_should_step_frame = False
        
        if should_process_frame:
            dungeon_depth = absolute_cam_x
            total_elapsed_time += dt
            time_of_day = (12 + (total_elapsed_time / 60)) % 24
            # Update crafting flash
            inventory.update_flash(dt)
            if smelter and smelter_in_use:
                smelter.update(dt)
            # Update placement position if in placement mode
            update_placement_position()
        else:
            dt = 0

        
        if game_just_started:
            generate_world()
            cats.clear()
            squirrels.clear()
            cows.clear()
            chickens.clear()
            crawlers.clear()
            pocks.clear()
            deers.clear()
            black_bears.clear()
            brown_bears.clear()
            gilas.clear()
            crows.clear()
            duskwretches.clear()
            fire_dragons.clear()
            ice_dragons.clear()
            electric_dragons.clear()
            poison_dragons.clear()
            dusk_dragons.clear()

            for _ in range(num_cats):
                tile_x, tile_image = random.choice(weighted_cat_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                cats.append(Cat(x, y, "Cat"))

            for _ in range(num_squirrels):
                tile_x, tile_image = random.choice(weighted_squirrel_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                squirrels.append(Squirrel(x, y, "Squirrel"))

            for _ in range(num_cows):
                tile_x, tile_image = random.choice(weighted_cow_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                cows.append(Cow(x, y, "Cow"))

            for _ in range(num_chickens):
                tile_x, tile_image = random.choice(weighted_chicken_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                chickens.append(Chicken(x, y, "Chicken"))

            for _ in range(num_crawlers):
                tile_x, tile_image = random.choice(weighted_crawler_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                crawlers.append(Crawler(x, y, "Crawler"))

            for _ in range(num_pocks):
                tile_x, tile_image = random.choice(weighted_pock_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                pocks.append(Pock(x, y, "Pock"))

            for _ in range(num_deers):
                tile_x, tile_image = random.choice(weighted_deer_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                deers.append(Deer(x, y, "Deer"))

            for _ in range(num_black_bears):
                tile_x, tile_image = random.choice(weighted_black_bear_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                black_bears.append(BlackBear(x, y, "Black Bear"))

            for _ in range(num_brown_bears):
                tile_x, tile_image = random.choice(weighted_brown_bear_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                brown_bears.append(BrownBear(x, y, "Brown Bear"))

            for _ in range(num_gilas):
                tile_x, tile_image = random.choice(weighted_gila_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                gilas.append(Gila(x, y, "Gila"))

            for _ in range(num_crows):
                tile_x, tile_image = random.choice(weighted_crow_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                crows.append(Crow(x, y, "Crow"))

            for _ in range(num_duskwretches):
                tile_x, tile_image = random.choice(weighted_duskwretch_tiles)
                x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                y = random.randint(0, height - 64)
                duskwretches.append(Duskwretch(x, y, "Duskwretch"))

            for _ in range(num_fire_dragons):
                if weighted_fire_dragon_tiles:
                    tile_x, tile_image = random.choice(weighted_fire_dragon_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    fire_dragons.append(Dragon(x, y, "Fire Dragon", "fire", random.randint(1, 100)))

            for _ in range(num_ice_dragons):
                if weighted_ice_dragon_tiles:
                    tile_x, tile_image = random.choice(weighted_ice_dragon_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    ice_dragons.append(Dragon(x, y, "Ice Dragon", "ice", random.randint(1, 100)))

            for _ in range(num_electric_dragons):
                if weighted_electric_dragon_tiles:
                    tile_x, tile_image = random.choice(weighted_electric_dragon_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    electric_dragons.append(Dragon(x, y, "Electric Dragon", "electric", random.randint(1, 100)))

            for _ in range(num_poison_dragons):
                if weighted_poison_dragon_tiles:
                    tile_x, tile_image = random.choice(weighted_poison_dragon_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    poison_dragons.append(Dragon(x, y, "Poison Dragon", "poison", random.randint(1, 100)))

            for _ in range(num_dusk_dragons):
                if weighted_dusk_dragon_tiles:
                    tile_x, tile_image = random.choice(weighted_dusk_dragon_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    dusk_dragons.append(Dragon(x, y, "Dusk Dragon", "dusk", random.randint(1, 100)))

            lavastone_start = 180 * BACKGROUND_SIZE
            debug_fire = Dragon(lavastone_start + 500, height // 2, "Fire Dragon", "fire", random.randint(1, 100))
            fire_dragons.append(debug_fire)
            
            snow_start = 24 * BACKGROUND_SIZE
            debug_ice = Dragon(snow_start + 500, height // 2, "Ice Dragon", "ice", random.randint(1, 100))
            ice_dragons.append(debug_ice)
            
            duskstone_start = 132 * BACKGROUND_SIZE
            debug_electric = Dragon(duskstone_start + 500, height // 2, "Electric Dragon", "electric", random.randint(1, 100))
            electric_dragons.append(debug_electric)
            
            wasteland_start = 108 * BACKGROUND_SIZE
            debug_poison = Dragon(wasteland_start + 500, height // 2, "Poison Dragon", "poison", random.randint(1, 100))
            poison_dragons.append(debug_poison)

            dungeon_depth = 0
            dungeon_depth_high = 0
            cam_x = 0
            absolute_cam_x = 0.0
            player_pos.x = width / 2
            player_pos.y = height / 2
       
            player.health = player.max_health
            player.stamina = player.max_stamina
            player.hunger = player.max_hunger
            player.thirst = player.max_thirst
            player.dead = False

            player.experience = 0
            player.exp_total = 0
            player.level = 1
            player.next_level_exp = 100
            player.level_up_timer = 0
            player.temp_weight_increase = 1

            player.health_leveler = 1
            player.stamina_leveler = 1
            player.hunger_leveler = 1
            player.thirst_leveler = 1
            player.warmth_leveler = 1
            player.weather_resistance_leveler = 1
            player.weight_leveler = 1
            player.strength_leveler = 1
            player.strength_level_gain = 3
            player.speed_leveler = 1
            player.defense_leveler = 1
            player.resilience_leveler = 1
            player.max_health = int(round(100 * player.health_leveler))
            player.max_stamina = int(round(100 * player.stamina_leveler))
            player.max_hunger = int(round(100 * player.hunger_leveler))
            player.max_thirst = int(round(100 * player.thirst_leveler))
            player.max_warmth = 100
            player.max_heat_resistance = int(round(100 * player.weather_resistance_leveler))
            player.max_cold_resistance = int(round(100 * player.weather_resistance_leveler))
            player.max_weight = int(round(100 * player.weight_leveler * player.temp_weight_increase))
            player.attack = int(round(player.damage + (player.strength_leveler - 1) * player.strength_level_gain))
            player.speed = int(round(100 * player.speed_leveler))
            player.defense = int(round(100 * player.defense_leveler))
            player.resilience = 100 * player.resilience_leveler

            player.damage = 5
            player.base_speed = 275
            player.unspent_stat_points = 0

            player.inventory = []
            player.score = 0
            
            inventory.inventory_list = [None] * inventory.capacity
            inventory.hotbar_slots = [None] * inventory.hotbar_size
            
            globals()['crafting_bench'] = CraftingBench(inventory)
            globals()['smelter'] = Smelter(inventory)
            
            populate_test_inventory()

            inventory_resources = []
            collection_messages = []
            thrown_items = []

            inventory.state = "inventory"

            game_just_started = False 
        
        player_world_x = player_pos.x + cam_x
        player_world_y = player_pos.y
        
        player_speed = player.get_speed()
        if player.swimming:
            player_speed *= 0.5
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            handle_debug_rotation_input(event)
            handle_debug_step_input(event)
            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if naming_cat is not None:
                    if event.key == pygame.K_RETURN:
                        if cat_name_input.strip():
                            naming_cat.cat_name = cat_name_input.strip()
                        naming_cat = None
                        cat_name_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        cat_name_input = cat_name_input[:-1]
                    elif event.unicode.isprintable() and len(cat_name_input) < 20:
                        cat_name_input += event.unicode
                    continue
                
                if event.key == pygame.K_ESCAPE:
                    if crafting_bench_in_use:
                        crafting_bench.close()
                        crafting_bench_in_use = False
                    elif not inventory_in_use:
                        if placement_mode:
                            cancel_placement()
                        else:
                            paused = not paused
                    elif inventory_in_use:
                        inventory_in_use = False
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None
                
                inventory.handle_keydown_hotbar(event, screen=None, use_on_press=False)
                
                if crafting_bench_in_use:
                    crafting_bench.handle_key_event(event)

                if event.key == pygame.K_f and not inventory_in_use and not crafting_bench_in_use and player.is_alive:
                    success, tags = inventory.consume_item()
                    if success:
                        if "food" in tags:
                            sound_manager.play_sound(random.choice([f"consume_item{i}" for i in range(1, 7)]))
                        elif any(tag in tags for tag in ["liquid", "consumable"]):
                            sound_manager.play_sound(random.choice([f"consume_water{i}" for i in range(1, 5)]))

                if event.key == pygame.K_q and not crafting_bench_in_use:
                    inventory_in_use = not inventory_in_use
                    if not inventory_in_use:
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None
                
                if inventory_in_use and player.is_alive:
                    if event.key == pygame.K_ESCAPE:
                        inventory_in_use = False
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None

            # Placement system - toggle placement mode with right-click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and player.is_alive and not crafting_bench_in_use:
                if placement_mode:
                    # Cancel placement mode
                    cancel_placement()
                else:
                    # Check if selected hotbar item is placeable
                    selected_item = inventory.get_selected_item()
                    if selected_item and selected_item.get("placeable", False):
                        start_placement(selected_item)
                    else:
                        # Fall back to throw mechanic
                        throw_charge_start = pygame.time.get_ticks()



            # Throw mechanic - release and throw
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and player.is_alive and not placement_mode:
                if throw_charge_start is not None:
                    charge_duration = (pygame.time.get_ticks() - throw_charge_start) / 1000.0
                    throw_power = min(charge_duration / max_throw_charge, 1.0)
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Quick click (< min_throw_hold_time): try to place cat from inventory or pick up nearby cat
                    if charge_duration < min_throw_hold_time:
                        # Check only the selected hotbar slot for a cat
                        cat_in_inventory = None
                        cat_slot_index = None
                        cat_is_hotbar = False
                        
                        # Check ONLY the selected hotbar slot
                        selected_hotbar = inventory.hotbar_slots[inventory.selected_hotbar_slot]
                        if selected_hotbar:
                            cat_object_candidate = selected_hotbar.get("cat_object")
                            if cat_object_candidate:
                                cat_in_inventory = selected_hotbar
                                cat_slot_index = inventory.selected_hotbar_slot
                                cat_is_hotbar = True
                        
                        # If cat found in selected hotbar slot, place it
                        if cat_in_inventory:
                            cat_object = cat_in_inventory["cat_object"]
                            
                            # Place cat in front of player based on facing direction
                            placement_distance = 50
                            if player.last_direction == "right":
                                place_x = player_world_x + placement_distance
                                place_y = player_world_y
                            elif player.last_direction == "left":
                                place_x = player_world_x - placement_distance
                                place_y = player_world_y
                            elif player.last_direction == "up":
                                place_x = player_world_x
                                place_y = player_world_y - placement_distance
                            else:  # "down"
                                place_x = player_world_x
                                place_y = player_world_y + placement_distance
                            
                            # Update cat position
                            cat_object.rect.centerx = place_x
                            cat_object.rect.centery = place_y
                            # Prevent immediate pickup on next frame
                            cat_object.placement_time = pygame.time.get_ticks()
                            
                            # Add cat back to world
                            cats.append(cat_object)
                            
                            # Remove cat from inventory
                            if cat_is_hotbar:
                                inventory.hotbar_slots[cat_slot_index] = None
                            else:
                                inventory.inventory_list[cat_slot_index] = None
                            
                            sound_manager.play_sound(random.choice(["cat_meow1", "cat_meow2", "cat_meow3"]))
                        
                        # Otherwise, try to pick up a nearby tamed cat into inventory
                        else:
                            closest_cat = None
                            closest_distance = 150  # Pickup range in pixels
                            
                            for cat in cats:
                                if cat.tame >= 50:  # Only tamed cats
                                    # Skip cats that were just placed (prevent immediate re-pickup)
                                    if hasattr(cat, 'placement_time'):
                                        time_since_placement = pygame.time.get_ticks() - cat.placement_time
                                        if time_since_placement < 500:  # 500ms cooldown after placement
                                            continue
                                    
                                    dist_x = abs(cat.rect.centerx - player_world_x)
                                    dist_y = abs(cat.rect.centery - player_world_y)
                                    distance = (dist_x**2 + dist_y**2) ** 0.5
                                    if distance < closest_distance:
                                        closest_distance = distance
                                        closest_cat = cat
                            
                            # Pick up the closest cat into inventory
                            if closest_cat:
                                cat_item_data = closest_cat.get_item_data()
                                # Try to add to hotbar first
                                added_to_hotbar = False
                                for i in range(inventory.hotbar_size):
                                    if inventory.hotbar_slots[i] is None:
                                        inventory.hotbar_slots[i] = cat_item_data
                                        added_to_hotbar = True
                                        break
                                
                                # If hotbar full, try main inventory
                                if not added_to_hotbar:
                                    for i in range(inventory.capacity):
                                        if inventory.inventory_list[i] is None:
                                            inventory.inventory_list[i] = cat_item_data
                                            break
                                
                                # Remove cat from world
                                cats.remove(closest_cat)
                                sound_manager.play_sound(random.choice(["cat_meow1", "cat_meow2", "cat_meow3"]))
                    
                    # Held click (>= min_throw_hold_time): throw toward mouse
                    elif charge_duration >= min_throw_hold_time:
                        # Calculate trajectory toward mouse
                        mouse_world_x = mouse_pos[0] + cam_x
                        mouse_world_y = mouse_pos[1]
                        
                        # Check only the selected hotbar slot for a cat to throw
                        cat_in_inventory = None
                        cat_slot_index = None
                        cat_is_hotbar = False
                        
                        # Check ONLY the selected hotbar slot
                        selected_hotbar = inventory.hotbar_slots[inventory.selected_hotbar_slot]
                        if selected_hotbar:
                            cat_object_candidate = selected_hotbar.get("cat_object")
                            if cat_object_candidate:
                                cat_in_inventory = selected_hotbar
                                cat_slot_index = inventory.selected_hotbar_slot
                                cat_is_hotbar = True
                        
                        # If cat in selected hotbar slot, throw it
                        if cat_in_inventory:
                            cat_object = cat_in_inventory["cat_object"]
                            # Throw from player position, not from cat's stored position
                            start_x = player_world_x
                            start_y = player_world_y
                            
                            # Calculate direction to mouse
                            delta_x = mouse_world_x - start_x
                            delta_y = mouse_world_y - start_y
                            distance = (delta_x**2 + delta_y**2) ** 0.5
                            
                            if distance > 0:
                                # Normalize and apply velocity in straight line to mouse
                                velocity = min_throw_power + (throw_power * (max_throw_power - min_throw_power))
                                vel_x = (delta_x / distance) * velocity * 4
                                vel_y = (delta_y / distance) * velocity * 4
                            else:
                                vel_x = 0
                                vel_y = 0
                            
                            spawn_thrown_item(start_x, start_y, vel_x, vel_y, 
                                        cat_object.get_item_data(), is_cat=True, throw_power=throw_power)
                            
                            # Remove cat from inventory and world
                            if cat_is_hotbar:
                                inventory.hotbar_slots[cat_slot_index] = None
                            else:
                                inventory.inventory_list[cat_slot_index] = None
                            if cat_object in cats:
                                cats.remove(cat_object)
                            
                            sound_manager.play_sound(random.choice(["cat_thrown1"]))
                        
                        else:
                            # Throw selected inventory item toward mouse
                            item = inventory.get_selected_item()
                            if item:
                                success, tags = inventory.throw_item()
                                if success:
                                    # Calculate direction to mouse
                                    start_x = player_world_x
                                    start_y = player_world_y
                                    delta_x = mouse_world_x - start_x
                                    delta_y = mouse_world_y - start_y
                                    distance = (delta_x**2 + delta_y**2) ** 0.5
                                    
                                    if distance > 0:
                                        velocity = min_throw_power + (throw_power * (max_throw_power - min_throw_power))
                                        vel_x = (delta_x / distance) * velocity * 4
                                        vel_y = (delta_y / distance) * velocity * 4
                                    else:
                                        # Fallback to direction-based throw 
                                        velocity = min_throw_power + (throw_power * (max_throw_power - min_throw_power))
                                        direction = 1 if player.last_direction in ["right", "down"] else -1
                                        vel_x = velocity * direction * 4
                                        vel_y = 0  # Straight horizontal throw
                                    
                                    is_cat_item = "cat_type" in item if item else False
                                    spawn_thrown_item(start_x, start_y, vel_x, vel_y, item, is_cat=is_cat_item, throw_power=throw_power)
                                    
                                    if "food" in tags:
                                        sound_manager.play_sound(random.choice([f"consume_item{i}" for i in range(1, 7)]))
                                    elif any(tag in tags for tag in ["liquid", "consumable"]):
                                        sound_manager.play_sound(random.choice([f"consume_water{i}" for i in range(1, 5)]))
                    
                    throw_charge_start = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                slot_index, is_hotbar = inventory.get_slot_at_mouse(mouse_pos, screen)
                if is_hotbar:
                    inventory.handle_selection_click(mouse_pos, screen)
                    inventory.start_drag(slot_index, is_hotbar)

                elif inventory_in_use and player.is_alive:
                    if inventory.state == "crafting":
                        import time
                        crafting_time = time.time()
                        inventory.handle_crafting_click(mouse_pos, crafting_time)
                    else:
                        inventory.handle_selection_click(mouse_pos, screen)
                        if slot_index is not None:
                            inventory.start_drag(slot_index, is_hotbar)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if placement_mode:
                    # Try to place the item
                    x, y = placement_position
                    if not check_placement_collision(x, y, placement_item):
                        place_structure(x, y, placement_item)
                        cancel_placement()  # Exit placement mode after successful placement
                    # If collision detected, don't place but stay in placement mode
                elif inventory.dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_index, is_hotbar = inventory.get_slot_at_mouse(mouse_pos, screen)

                    if slot_index is not None:
                        inventory.end_drag(slot_index, is_hotbar, screen)
                    else:
                        inventory.cancel_drag()



            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                if crafting_bench_in_use:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 4:
                        crafting_bench.handle_mouse_scroll(1)
                    else:
                        crafting_bench.handle_mouse_scroll(-1)
                else:
                    if event.button == 4:
                        inventory.selected_hotbar_slot = (inventory.selected_hotbar_slot - 1) % inventory.hotbar_size
                    elif event.button == 5:
                        inventory.selected_hotbar_slot = (inventory.selected_hotbar_slot + 1) % inventory.hotbar_size
                    inventory.selection_mode = "hotbar"
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                if crafting_bench_in_use:
                    mouse_pos = pygame.mouse.get_pos()
                    crafting_bench.handle_mouse_click(mouse_pos, event.button, screen)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if crafting_bench_in_use:
                    crafting_bench.close()
                    crafting_bench_in_use = False
                elif smelter_in_use:
                    smelter.close()
                    smelter_in_use = False
                else:
                    for structure in nearby_structures:
                        if structure['item_name'] == 'Workbench':
                            struct_collision = structure['rect']
                            horizontal_dist = abs(struct_collision.centerx - player_world_x)
                            vertical_dist = abs(struct_collision.centery - player_world_y)
                            workbench_reach = 40
                            horizontal_range = (struct_collision.width / 2) + workbench_reach
                            vertical_range = (struct_collision.height / 2) + workbench_reach
                            
                            facing_object = False
                            if player.last_direction == "right" and struct_collision.centerx > player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                                facing_object = True
                            elif player.last_direction == "left" and struct_collision.centerx < player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                                facing_object = True
                            elif player.last_direction == "up" and struct_collision.centery < player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                                facing_object = True
                            elif player.last_direction == "down" and struct_collision.centery > player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                                facing_object = True
                            
                            if facing_object:
                                crafting_bench.open((structure['x'], structure['y']))
                                crafting_bench_in_use = True
                                break
                    
                    if not crafting_bench_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Smelter':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                smelter_reach = 40
                                horizontal_range = (struct_collision.width / 2) + smelter_reach
                                vertical_range = (struct_collision.height / 2) + smelter_reach
                                
                                facing_object = False
                                if player.last_direction == "right" and struct_collision.centerx > player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                                    facing_object = True
                                elif player.last_direction == "left" and struct_collision.centerx < player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                                    facing_object = True
                                elif player.last_direction == "up" and struct_collision.centery < player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                                    facing_object = True
                                elif player.last_direction == "down" and struct_collision.centery > player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                                    facing_object = True
                                
                                if facing_object:
                                    smelter.open((structure['x'], structure['y']))
                                    smelter_in_use = True
                                    break
                
                if not crafting_bench_in_use:
                    for obj in visible_objects:
                        if hasattr(obj, 'collect') and not obj.destroyed:
                            if hasattr(obj, 'is_empty') and obj.is_empty:
                                continue
                            
                            obj_collision = obj.get_collision_rect(0)
                            horizontal_dist = abs(obj_collision.centerx - player_world_x)
                            vertical_dist = abs(obj_collision.centery - player_world_y)
                            collect_reach = 25
                            horizontal_range = (obj_collision.width / 2) + collect_reach
                            vertical_range = (obj_collision.height / 2) + collect_reach
                            facing_object = False
                            if player.last_direction == "right" and obj_collision.centerx > player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                                facing_object = True
                            elif player.last_direction == "left" and obj_collision.centerx < player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                                facing_object = True
                            elif player.last_direction == "up" and obj_collision.centery < player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                                facing_object = True
                            elif player.last_direction == "down" and obj_collision.centery > player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                                facing_object = True
                            if facing_object:
                                resource = obj.collect(player)
                                if resource:
                                    if hasattr(obj, 'berry'):
                                        collected_item = obj.berry
                                    elif hasattr(obj, 'fruit'):
                                        collected_item = obj.fruit
                                    elif hasattr(obj, 'resource'):
                                        collected_item = obj.resource
                                    else:
                                        collected_item = "Items"
                                    
                                    if inventory.add(resource):
                                        if hasattr(obj, 'berry') or hasattr(obj, 'fruit'):
                                            sound_manager.play_sound(random.choice([f"pick_berry{i}" for i in range(1,5)]))
                                        elif hasattr(obj, 'resource'):
                                            if obj.resource == "Sticks":
                                                sound_manager.play_sound("pickup_stick")
                                            elif obj.resource == "Stone":
                                                sound_manager.play_sound(random.choice(["collect_stone1", "collect_stone2"]))
                                            elif obj.resource == "Fiber":
                                                sound_manager.play_sound(random.choice(["pickup_grass1", "pickup_grass2", "pickup_grass3"]))
                                            elif obj.resource == "Mushroom" or obj.resource == "Poisonous Mushroom" or obj.resource == "Duskshroom" or obj.resource == "Dawnshroom":
                                                sound_manager.play_sound(random.choice([f"pick_berry{i}" for i in range(1,5)]))
                                        
                                        resource_counts = group_resources_by_type(resource)
                                        for resource_name, count in resource_counts.items():
                                            add_collection_message(resource_name, count)
                                    else:
                                        if hasattr(obj, 'is_empty'):
                                            obj.is_empty = False
                                        obj.destroyed = False
                                    
                                    collect_cooldown = current_time
                                    break
                
                for obj in visible_liquids:
                    if hasattr(obj, 'collect_from_pond') and hasattr(obj, 'destroyed') and not obj.destroyed:
                        obj_collision = obj.get_collision_rect(0)
                        horizontal_dist = abs(obj_collision.centerx - player_world_x)
                        vertical_dist = abs(obj_collision.centery - player_world_y)
                        collect_reach = 40
                        horizontal_range = (obj_collision.width / 2) + collect_reach
                        vertical_range = (obj_collision.height / 2) + collect_reach
                        
                        facing_object = False
                        if player.last_direction == "right" and obj_collision.centerx > player_world_x - 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "left" and obj_collision.centerx < player_world_x + 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "up" and obj_collision.centery < player_world_y + 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        elif player.last_direction == "down" and obj_collision.centery > player_world_y - 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        
                        if facing_object:
                            held_item = None
                            selected_slot = inventory.selected_hotbar_slot
                            if inventory.hotbar_slots[selected_slot] is not None:
                                held_item = inventory.hotbar_slots[selected_slot]
                            
                            if held_item:
                                resources = obj.collect_from_pond(player, held_item)
                                if resources:
                                    sound_manager.play_sound("consume_water1")
                                    held_item["quantity"] -= 1
                                    if held_item["quantity"] <= 0:
                                        inventory.hotbar_slots[selected_slot] = None
                                    
                                    if inventory.add(resources):
                                        water_type = resources[0]
                                        add_collection_message(water_type, len(resources))
                                    if obj.destroyed:
                                        if obj in visible_liquids:
                                            visible_liquids.remove(obj)
                                    harvest_cooldown = current_time
                                    break
                    
                    if hasattr(obj, 'collect_from_lava') and hasattr(obj, 'destroyed') and not obj.destroyed:
                        obj_collision = obj.get_collision_rect(0)
                        horizontal_dist = abs(obj_collision.centerx - player_world_x)
                        vertical_dist = abs(obj_collision.centery - player_world_y)
                        collect_reach = 40
                        horizontal_range = (obj_collision.width / 2) + collect_reach
                        vertical_range = (obj_collision.height / 2) + collect_reach
                        
                        facing_object = False
                        if player.last_direction == "right" and obj_collision.centerx > player_world_x - 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "left" and obj_collision.centerx < player_world_x + 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "up" and obj_collision.centery < player_world_y + 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        elif player.last_direction == "down" and obj_collision.centery > player_world_y - 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        
                        if facing_object:
                            held_item = None
                            selected_slot = inventory.selected_hotbar_slot
                            if inventory.hotbar_slots[selected_slot] is not None:
                                held_item = inventory.hotbar_slots[selected_slot]
                            
                            if held_item:
                                resources = obj.collect_from_lava(player, held_item)
                                if resources:
                                    sound_manager.play_sound("fire")
                                    held_item["quantity"] -= 1
                                    if held_item["quantity"] <= 0:
                                        inventory.hotbar_slots[selected_slot] = None
                                    
                                    if inventory.add(resources):
                                        add_collection_message("Lava", len(resources))
                                    if obj.destroyed:
                                        if obj in visible_liquids:
                                            visible_liquids.remove(obj)
                                    harvest_cooldown = current_time
                                    break

            if paused:
                if resume_button.is_clicked(event):
                    paused = False
                if quit_button.is_clicked(event):
                    state = "menu"
                    paused = False
    
        if not paused and not inventory_in_use and not smelter_in_use and not crafting_bench_in_use and naming_cat is None and pygame.mouse.get_pressed()[0] and not player.exhausted:
            if current_time - harvest_cooldown > harvest_delay:
                held_item = get_selected_hotbar_item()
                has_pickaxe_equipped = is_pickaxe_item(held_item)
                for obj in visible_objects:
                    if hasattr(obj, 'harvest') and hasattr(obj, 'destroyed') and not obj.destroyed:
                        
                        obj_collision = obj.get_collision_rect(0)
                        
                        horizontal_dist = abs(obj_collision.centerx - player_world_x)
                        vertical_dist = abs(obj_collision.centery - player_world_y)
                        
                        harvest_reach = 25
                        horizontal_range = (obj_collision.width / 2) + harvest_reach
                        vertical_range = (obj_collision.height / 2) + harvest_reach
                        
                        facing_object = False
                        if player.last_direction == "right" and obj_collision.centerx > player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "left" and obj_collision.centerx < player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "up" and obj_collision.centery < player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        elif player.last_direction == "down" and obj_collision.centery > player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                            
                        if facing_object:
                            if getattr(obj, "resource", None) == "Stone" and not has_pickaxe_equipped:
                                continue
                            resource = obj.harvest(player)
                            resource = adjust_resources_with_tool(resource, held_item)
                            if resource:
                                if hasattr(obj, 'resource'):
                                    if obj.resource == "Stone":
                                        sound_manager.play_sound(random.choice([f"harvest_stone{i}" for i in range(1, 7)]))
                                    elif obj.resource in ["Apple Wood", "Dusk Wood", "Fir Wood", "Oak Wood", "Orange Wood", "Olive Wood", "Willow Wood", "Palm Wood"]:
                                        sound_manager.play_sound(random.choice(["gather_wood1", "gather_wood2", "gather_wood3"]))
                                    elif obj.resource == "Sticks":
                                        sound_manager.play_sound(random.choice(["break_bush1", "break_bush2"]))
                                
                                if inventory.add(resource):
                                    resource_counts = group_resources_by_type(resource)
                                    for resource_name, count in resource_counts.items():
                                        add_collection_message(resource_name, count)

                                if obj.destroyed:
                                    visible_objects.remove(obj)
                                
                                harvest_cooldown = current_time
                                break
                    
        # Update thrown items physics - straight line movement with collision detection
        for thrown in thrown_items[:]:
            if not thrown["landed"]:
                # Move item along its direction vector
                step_distance = thrown["speed"]
                next_x = thrown["x"] + thrown["dir_x"] * step_distance
                next_y = thrown["y"] + thrown["dir_y"] * step_distance
                distance_this_frame = ((next_x - thrown["x"])**2 + (next_y - thrown["y"])**2) ** 0.5
                thrown["distance_traveled"] += distance_this_frame
                
                # Check for collisions with world objects and mobs
                item_rect = pygame.Rect(next_x - thrown["sprite_size"]//2, 
                                       next_y - thrown["sprite_size"]//2,
                                       thrown["sprite_size"], thrown["sprite_size"])
                
                collision_detected = False
                collision_objects = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants + ponds + lavas
                collision_mobs = cats + squirrels + cows + chickens + crawlers + pocks + deers + black_bears + brown_bears + gilas + crows + duskwretches
                
                for obj in collision_objects:
                    obj_rect = obj.get_collision_rect(0) if hasattr(obj, 'get_collision_rect') else obj.rect
                    if item_rect.colliderect(obj_rect):
                        collision_detected = True
                        break
                
                # Check for collisions with mobs
                if not collision_detected:
                    for mob in collision_mobs:
                        if item_rect.colliderect(mob.rect):
                            collision_detected = True
                            break
                
                # Check if item has traveled its max distance or hit an object
                if thrown["distance_traveled"] >= thrown["max_distance"] or collision_detected:
                    # Item has landed - keep current position (don't use next_x, next_y to stay before collision)
                    thrown["landed"] = True
                    
                    # If it's a cat, add it back to the world
                    if thrown["is_cat"]:
                        cat_data = thrown["cat_data"]
                        if cat_data and "cat_object" in cat_data:
                            cat_obj = cat_data["cat_object"]
                            cat_obj.rect.centerx = int(thrown["x"])
                            cat_obj.rect.centery = int(thrown["y"])
                            cat_obj.destroyed = False
                            cats.append(cat_obj)
                        thrown_items.remove(thrown)
                    # For regular items, convert to world item
                    else:
                        create_world_item_from_thrown(thrown)
                        thrown_items.remove(thrown)
                else:
                    # No collision, continue moving
                    thrown["x"] = next_x
                    thrown["y"] = next_y
                    
        dead_bushes = [db for db in dead_bushes if not db.destroyed]
        mushrooms = [m for m in mushrooms if not m.destroyed]
        savannah_grasses = [sgrass for sgrass in savannah_grasses if not sgrass.destroyed]
        grasses = [grass for grass in grasses if not grass.destroyed]
        stones = [stone for stone in stones if not stone.destroyed]
        sticks = [s for s in sticks if not s.destroyed]
        rocks = [r for r in rocks if not r.destroyed]
        trees = [t for t in trees if not t.destroyed]
        boulders = [b for b in boulders if not b.destroyed]
        berry_bushes = [bush for bush in berry_bushes if not bush.destroyed]
        ferns = [f for f in ferns if not f.destroyed]
        fruit_plants = [fp for fp in fruit_plants if not fp.destroyed]
        ponds = [pond for pond in ponds if not pond.destroyed]
        lavas = [lava for lava in lavas if not lava.destroyed]

        cats = [cat for cat in cats if not cat.destroyed]
        squirrels = [squirrel for squirrel in squirrels if not squirrel.destroyed]
        cows = [cow for cow in cows if not cow.destroyed]
        chickens = [chicken for chicken in chickens if not chicken.destroyed]
        crawlers = [crawler for crawler in crawlers if not crawler.destroyed]
        duskwretches = [duskwretch for duskwretch in duskwretches if not duskwretch.destroyed]
        pocks = [pock for pock in pocks if not pock.destroyed]
        deers = [deer for deer in deers if not deer.destroyed]
        black_bears = [black_bear for black_bear in black_bears if not black_bear.destroyed]
        brown_bears = [brown_bear for brown_bear in brown_bears if not brown_bear.destroyed]
        gilas = [gila for gila in gilas if not gila.destroyed]
        crows = [crow for crow in crows if not crow.destroyed]
        fire_dragons = [dragon for dragon in fire_dragons if not dragon.destroyed]
        ice_dragons = [dragon for dragon in ice_dragons if not dragon.destroyed]
        electric_dragons = [dragon for dragon in electric_dragons if not dragon.destroyed]
        poison_dragons = [dragon for dragon in poison_dragons if not dragon.destroyed]
        dusk_dragons = [dragon for dragon in dusk_dragons if not dragon.destroyed]

        for tile_x, tile_image in tiles:
            screen_x = tile_x - cam_x
            if -BACKGROUND_SIZE < screen_x < width:
                screen.blit(tile_image, (screen_x, floor_y))

        keys = pygame.key.get_pressed()

        collectibles = sticks + stones + grasses + savannah_grasses + mushrooms
        all_objects_no_liquids = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants
        all_objects = all_objects_no_liquids + ponds + lavas
        mobs = cats + squirrels + cows + chickens + crawlers + duskwretches + pocks + deers + black_bears + brown_bears + gilas + crows + fire_dragons + ice_dragons + electric_dragons + poison_dragons + dusk_dragons
        all_mobs = mobs

        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -256 and col.rect.x - cam_x < width + 256]
        visible_liquids = [obj for obj in (ponds + lavas) if obj.rect.x - cam_x > -256 and obj.rect.x - cam_x < width + 256 and obj.rect.y > -256 and obj.rect.y < height + 256]
        visible_objects = [obj for obj in all_objects_no_liquids if obj.rect.x - cam_x > -256 and obj.rect.x - cam_x < width + 256 and obj.rect.y > -256 and obj.rect.y < height + 256]
        visible_mobs = [mob for mob in mobs if mob.rect.x - cam_x > -256 and mob.rect.x - cam_x < width + 256 and mob.rect.y > -256 and mob.rect.y < height + 256]

        # Add visible placed structures
        visible_structures = []
        for structure in placed_structures:
            struct_x = structure['x']
            struct_y = structure['y']
            if struct_x - cam_x > -256 and struct_x - cam_x < width + 256 and struct_y > -256 and struct_y < height + 256:
                visible_structures.append(structure)
        
        for mob in visible_mobs:
            if isinstance(mob, Cat) and random.random() < 0.001:
                sound_manager.play_sound(random.choice([f"cat_meow{i}" for i in range(1,7)]))
            if isinstance(mob, Squirrel) and random.random() < 0.001:
                sound_manager.play_sound(random.choice([f"squirrel_chirp{i}" for i in range(1,4)]))
            elif isinstance(mob, Chicken) and random.random() < 0.001:
                sound_manager.play_sound(random.choice([f"chicken_cluck{i}" for i in range(1,7)]))
            elif isinstance(mob, Cow) and random.random() < 0.0005:
                sound_manager.play_sound(random.choice(["cow_moo1", "cow_moo2"]))
            elif isinstance(mob, Crow) and random.random() < 0.001:
                sound_manager.play_sound(random.choice([f"crow_caw{i}" for i in range(1,4)]))
            elif isinstance(mob, Duskwretch) and random.random() < 0.001 and not mob.chasing and not mob.attacking:
                sound_manager.play_sound("duskwretch_growl")
            elif isinstance(mob, (BlackBear, BrownBear)) and random.random() < 0.001:
                sound_manager.play_sound("animal_breath")
        
        visible_objects.extend(visible_mobs)
        visible_objects.extend(visible_collectibles)
        visible_objects.extend(visible_structures)
        visible_objects.sort(key=lambda obj: (obj.rect.y + obj.rect.height) if hasattr(obj, 'rect') else obj['y'] + 32)

        for mob in list(visible_mobs):
            if mob.destroyed:
                visible_mobs.remove(mob)
                mobs.remove(mob)
            if hasattr(mob, "death_experience"):
                mob.give_experience(player)

        for col in list(visible_collectibles):
            if col.destroyed and col in collectibles:
                collectibles.remove(col)

        player_drawn = False
        player_redraw_image = None
        player_redraw_x = 0
        player_redraw_y = 0

        for obj in visible_liquids:
            obj.update_animation(dt)
            obj.draw(screen, cam_x)

        def draw_held_item():
            current_hotbar_slot = inventory.hotbar_slots[inventory.selected_hotbar_slot]
            if current_hotbar_slot is not None:
                for item in items_list:
                    if item["item_name"] == current_hotbar_slot["item_name"] and "held_item_images" in item:
                        # disable attacking while smelter UI is open
                        is_attacking = pygame.mouse.get_pressed()[0] and not player.exhausted and not smelter_in_use
                        held_image = item["held_item_images"].get(player.last_direction)
                        
                        if held_image and is_attacking:
                            is_moving = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]
                            
                            if is_moving:
                                if player.last_direction == "down":
                                    num_frames = len(player_walk_down_attack_images)
                                elif player.last_direction == "up":
                                    num_frames = len(player_walk_up_attack_images)
                                elif player.last_direction == "left":
                                    num_frames = len(player_walk_left_attack_images)
                                elif player.last_direction == "right":
                                    num_frames = len(player_walk_right_attack_images)
                                else:
                                    num_frames = 3
                            else:
                                num_frames = 4
                            
                            frame_index = int(player_frame_index) % num_frames
                            attack_frame_data = item.get("attack_frame_data", {}).get(player.last_direction)
                            
                            if attack_frame_data and len(attack_frame_data) > 0:
                                attack_frame_index = frame_index % len(attack_frame_data)
                                frame_info = attack_frame_data[attack_frame_index]
                                swing_offset = frame_info["offset"]
                                rotation_angle = frame_info["rotation"]
                            else:
                                rotation_angle = (player_frame_index / num_frames) * 180 - 90
                                base_offset = item.get("held_item_offset", {}).get(player.last_direction, (0, 0))
                                swing_offset = calculate_held_item_offset(base_offset, player_frame_index, num_frames, player.last_direction, is_attacking=True, is_moving=is_moving)
                            
                            rotated_image = pygame.transform.rotate(held_image, rotation_angle)
                            
                            if player.last_direction == "left":
                                rotated_image = pygame.transform.flip(rotated_image, True, False)
                            
                            scale_factor = 0.65
                            scaled_size = (int(rotated_image.get_width() * scale_factor), int(rotated_image.get_height() * scale_factor))
                            rotated_image = pygame.transform.scale(rotated_image, scaled_size)
                            
                            held_x = player_pos.x - size/2 + swing_offset[0]
                            held_y = player_pos.y - size/2 + swing_offset[1]
                            
                            screen.blit(rotated_image, (held_x, held_y))
                        elif held_image:
                            is_moving = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]
                            base_offset = item.get("held_item_offset", {}).get(player.last_direction, (0, 0))
                            
                            movement_rotation = 0
                            vertical_bob = 0
                            if is_moving:
                                if player.last_direction == "down":
                                    num_frames = len(player_walk_down_images)
                                elif player.last_direction == "up":
                                    num_frames = len(player_walk_up_images)
                                elif player.last_direction == "left":
                                    num_frames = len(player_walk_left_images)
                                elif player.last_direction == "right":
                                    num_frames = len(player_walk_right_images)
                                else:
                                    num_frames = 3
                                
                                frame_index = int(player_frame_index) % num_frames
                                movement_frame_data = item.get("movement_frame_data", {}).get(player.last_direction)
                                
                                if movement_frame_data and frame_index < len(movement_frame_data):
                                    frame_info = movement_frame_data[frame_index]
                                    offset = frame_info["offset"]
                                    movement_rotation = frame_info["rotation"]
                                else:
                                    offset = calculate_held_item_offset(base_offset, player_frame_index, num_frames, player.last_direction, is_attacking=False, is_moving=True)
                                    pendulum_offset = offset[0] - base_offset[0]
                                    movement_rotation = calculate_movement_rotation(player_frame_index, num_frames, player.last_direction, pendulum_offset)
                                    
                                    progress = player_frame_index / num_frames
                                    vertical_bob = -4 * math.sin(progress * math.pi * 2)
                                    offset = (offset[0], offset[1] + vertical_bob)
                            else:
                                offset = base_offset
                            
                            held_x = player_pos.x - size/2 + offset[0]
                            held_y = player_pos.y - size/2 + offset[1]
                            
                            if player.last_direction == "left":
                                held_image = pygame.transform.flip(held_image, True, False)
                            
                            scale_factor = 0.65
                            scaled_size = (int(held_image.get_width() * scale_factor), int(held_image.get_height() * scale_factor))
                            held_image = pygame.transform.scale(held_image, scaled_size)
                            
                            if movement_rotation != 0:
                                held_image = pygame.transform.rotate(held_image, movement_rotation)
                            
                            screen.blit(held_image, (held_x, held_y))
                        break

        for obj in visible_objects:
            # Handle both regular objects with rect and placed structures (dictionaries)
            if isinstance(obj, dict) and 'y' in obj:
                object_mid_y = obj['y']
            else:
                object_mid_y = obj.rect.y + obj.rect.height / 2

            if not player_drawn and (player.rect.centery + 20) <= object_mid_y:
                # Draw axe first for left/up directions (behind the player)
                if player.last_direction in ["left", "up"]:
                    draw_held_item()
                
                # Draw player
                if player.swimming and player.current_liquid:
                    liquid_center_x = player.current_liquid.rect.centerx
                    liquid_center_y = player.current_liquid.rect.centery
                    liquid_width = player.current_liquid.rect.width
                    liquid_height = player.current_liquid.rect.height
                    
                    distance_x = abs((player_pos.x + cam_x) - liquid_center_x)
                    distance_y = abs(player_pos.y - liquid_center_y)
                    max_distance_x = liquid_width / 2
                    max_distance_y = liquid_height / 2
                    
                    normalized_x = min(1, distance_x / max_distance_x) if max_distance_x > 0 else 0
                    normalized_y = min(1, distance_y / max_distance_y) if max_distance_y > 0 else 0
                    
                    sinking_ratio = max(0, 1 - max(normalized_x, normalized_y))
                    
                    clip_height = int(player_current_image.get_height() * (1 - sinking_ratio * 0.5))
                    clip_rect = pygame.Rect(0, 0, player_current_image.get_width(), clip_height)
                    clipped_image = player_current_image.subsurface(clip_rect)
                    
                    y_offset = sinking_ratio * 4
                    screen.blit(clipped_image, (player_pos.x - size/2, player_pos.y - size/2 + y_offset))
                else:
                    screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))
                
                # Draw axe after for right/down directions (in front of the player)
                if player.last_direction in ["right", "down"]:
                    draw_held_item()
                
                player_drawn = True

            # Handle drawing of placed structures (dictionaries)
            if isinstance(obj, dict) and 'item_name' in obj:
                # Draw placed structure
                struct_sprite = None
                sprite_width, sprite_height = obj.get('sprite_size', default_placeable_sprite_size)
                try:
                    icon_path = f"assets/sprites/items/{obj['icon']}"
                    struct_sprite = pygame.image.load(icon_path).convert_alpha()
                    struct_sprite = pygame.transform.scale(struct_sprite, (sprite_width, sprite_height))
                except:
                    # Fallback to colored rectangle
                    struct_sprite = pygame.Surface((sprite_width, sprite_height))
                    struct_sprite.fill((100, 100, 100))

                screen_x = obj['x'] - cam_x - sprite_width // 2
                screen_y = obj['y'] - sprite_height // 2
                screen.blit(struct_sprite, (screen_x, screen_y))
            else:
                obj.draw(screen, cam_x)

            if hasattr(obj, 'breath_image') and obj.breath_image:
                screen.blit(obj.breath_image, (obj.breath_image_x - cam_x, obj.breath_image_y))
        
        if not player_drawn:
            if player.last_direction in ["left", "up"]:
                draw_held_item()
            
            if player.swimming and player.current_liquid:
                liquid_center_x = player.current_liquid.rect.centerx
                liquid_center_y = player.current_liquid.rect.centery
                liquid_width = player.current_liquid.rect.width
                liquid_height = player.current_liquid.rect.height
                
                distance_x = abs((player_pos.x + cam_x) - liquid_center_x)
                distance_y = abs(player_pos.y - liquid_center_y)
                max_distance_x = liquid_width / 2
                max_distance_y = liquid_height / 2
                
                normalized_x = min(1, distance_x / max_distance_x) if max_distance_x > 0 else 0
                normalized_y = min(1, distance_y / max_distance_y) if max_distance_y > 0 else 0
                
                sinking_ratio = max(0, 1 - max(normalized_x, normalized_y))
                
                clip_height = int(player_current_image.get_height() * (1 - sinking_ratio * 0.5))
                clip_rect = pygame.Rect(0, 0, player_current_image.get_width(), clip_height)
                clipped_image = player_current_image.subsurface(clip_rect)
                
                y_offset = sinking_ratio * 4
                screen.blit(clipped_image, (player_pos.x - size/2, player_pos.y - size/2 + y_offset))
            else:
                screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))
            
            if player.last_direction in ["right", "down"]:
                draw_held_item()

        # Draw thrown items
        for thrown in thrown_items:
            item_screen_x = int(thrown["x"] - cam_x)
            item_screen_y = int(thrown["y"])
            offset = thrown["sprite_size"] // 2

            if thrown["sprite"]:
                # Draw the item sprite
                screen.blit(thrown["sprite"], (item_screen_x - offset, item_screen_y - offset))
            else:
                # Fallback to circle if sprite not found
                pygame.draw.circle(screen, (255, 200, 100), (item_screen_x, item_screen_y), 5)

        # Draw placement preview
        if placement_mode and placement_item:
            preview_x = placement_position[0] - cam_x
            preview_y = placement_position[1]

            # Load item sprite for preview
            item_sprite = None
            sprite_size, _ = get_placeable_sizes(placement_item)
            sprite_width, sprite_height = sprite_size
            try:
                icon_path = f"assets/sprites/items/{placement_item['icon']}"
                item_sprite = pygame.image.load(icon_path).convert_alpha()
                item_sprite = pygame.transform.scale(item_sprite, (sprite_width, sprite_height))
            except:
                # Fallback to colored rectangle
                item_sprite = pygame.Surface((sprite_width, sprite_height))
                item_sprite.fill((150, 150, 150))

            # Check for collision and tint accordingly
            has_collision = check_placement_collision(placement_position[0], placement_position[1], placement_item)

            if not has_collision:
                # Apply green tint for valid placement
                green_tint = pygame.Surface(item_sprite.get_size())
                green_tint.fill((0, 255, 0))
                item_sprite.blit(green_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                # Make it semi-transparent
                item_sprite.set_alpha(180)

            # Draw the preview
            screen.blit(item_sprite, (preview_x - sprite_width // 2, preview_y - sprite_height // 2))

        # Draw charge indicator (only show after holding for min_throw_hold_time)
        if throw_charge_start is not None:
            charge_duration = (pygame.time.get_ticks() - throw_charge_start) / 1000.0
            # Only display charge bar after minimum hold time
            if charge_duration >= min_throw_hold_time:
                charge_percent = min(charge_duration / max_throw_charge, 1.0)
                
                bar_width = 50
                bar_height = 5
                pygame.draw.rect(screen, (100, 100, 100), 
                                (player_pos.x - bar_width//2, player_pos.y - size//2 - 15, bar_width, bar_height))
                pygame.draw.rect(screen, (255, 255, 0), 
                                (player_pos.x - bar_width//2, player_pos.y - size//2 - 15, int(bar_width * charge_percent), bar_height))

        player.rect.center = (player_pos.x, player_pos.y)
            
        # Get nearby placed structures
        nearby_structures = [structure for structure in placed_structures
                           if abs(structure['rect'].x - (player_pos.x + cam_x)) < 1500
                           and abs(structure['rect'].y - player_pos.y) < 800]

        nearby_objects = [obj for obj in all_objects
                    if abs(obj.rect.x - (player_pos.x + cam_x)) < 1500
                    and abs(obj.rect.y - player_pos.y) < 800]

        # Add nearby structures to nearby_objects for mob collision detection
        nearby_objects.extend(nearby_structures)

        nearby_mobs = [mob for mob in mobs
                    if abs(mob.rect.x - (player_pos.x + cam_x)) < 3000
                    and abs(mob.rect.y - player_pos.y) < 800]        

        def lerp(a, b, t):
            """Linear interpolation between a and b for t in [0,1]."""
            return a + (b - a) * max(0, min(1, t))

        # Default color/alpha
        R_value = G_value = B_value = A_value = 0

        # ---- Sunset (18 → 19) ----
        if 18.0 <= time_of_day < 19.0:
            t = (time_of_day - 18.0) / 1.0
            R_value = int(lerp(0, 120, t))
            B_value = int(lerp(0, 0, t))
            A_value = int(lerp(0, 90, t))

        # ---- Evening → Night (19 → 22) ----
        elif 19.0 <= time_of_day < 22.0:
            t = (time_of_day - 19.0) / 3.0
            R_value = int(lerp(120, 40, t))
            B_value = int(lerp(0, 20, t))
            A_value = int(lerp(90, 200, t))    

        # ---- Full Night (22 → 5) ----
        elif 22.0 <= time_of_day or time_of_day < 5.0:
            if time_of_day >= 22.0:
                t = (time_of_day - 22.0) / 5.0
            else:
                t = ((time_of_day + 24) - 22.0) / 5.0

            R_value = int(lerp(40, 0, t))
            B_value = int(lerp(20, 20, t))
            A_value = int(lerp(200, 200, t))

        # ---- Dawn (5 → 7) ----
        elif 5.0 <= time_of_day < 7.0:
            t = (time_of_day - 5.0) / 2.0
            R_value = int(lerp(0, 0, t))
            B_value = int(lerp(20, 0, t))
            A_value = int(lerp(200, 0, t))

        # ---- Daytime (6 → 18) ----
        else:
            R_value = G_value = B_value = A_value = 0

        R_value = max(0, min(255, R_value))
        G_value = max(0, min(255, G_value))
        B_value = max(0, min(255, B_value))
        A_value = max(0, min(255, A_value))

        # Draw overlay
        day_night_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        day_night_overlay.fill((R_value, G_value, B_value, A_value))
        screen.blit(day_night_overlay, (0, 0))


        inventory.draw_hotbar(screen)


        if not paused and not inventory_in_use and player.dead == False:

            if keys[pygame.K_e] and current_time - collect_cooldown > collect_delay:
                for obj in visible_objects:
                    if hasattr(obj, 'collect') and not obj.destroyed:
                        if hasattr(obj, 'is_empty') and obj.is_empty:
                            continue
                        
                        obj_collision = obj.get_collision_rect(0)
                        horizontal_dist = abs(obj_collision.centerx - player_world_x)
                        vertical_dist = abs(obj_collision.centery - player_world_y)
                        collect_reach = 40
                        horizontal_range = (obj_collision.width / 2) + collect_reach
                        vertical_range = (obj_collision.height / 2) + collect_reach
                        facing_object = False
                        if player.last_direction == "right" and obj_collision.centerx > player_world_x - 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "left" and obj_collision.centerx < player_world_x + 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                            facing_object = True
                        elif player.last_direction == "up" and obj_collision.centery < player_world_y + 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        elif player.last_direction == "down" and obj_collision.centery > player_world_y - 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                            facing_object = True
                        if facing_object:
                            resource = obj.collect(player)
                            if resource:
                                if hasattr(obj, 'berry'):
                                    collected_item = obj.berry
                                elif hasattr(obj, 'fruit'):
                                    collected_item = obj.fruit
                                elif hasattr(obj, 'resource'):
                                    collected_item = obj.resource
                                else:
                                    collected_item = "Items"
                                
                                if inventory.add(resource):
                                    if hasattr(obj, 'berry') or hasattr(obj, 'fruit'):
                                        sound_manager.play_sound(random.choice([f"pick_berry{i}" for i in range(1,5)]))
                                    elif hasattr(obj, 'resource'):
                                        if obj.resource == "Sticks":
                                            sound_manager.play_sound("pickup_stick")
                                        elif obj.resource == "Stone":
                                            sound_manager.play_sound(random.choice(["collect_stone1", "collect_stone2"]))
                                        elif obj.resource == "Fiber":
                                            sound_manager.play_sound(random.choice(["pickup_grass1", "pickup_grass2", "pickup_grass3"]))
                                        elif obj.resource == "Mushroom" or obj.resource == "Poisonous Mushroom" or obj.resource == "Duskshroom" or obj.resource == "Dawnshroom":
                                            sound_manager.play_sound(random.choice([f"pick_berry{i}" for i in range(1,5)]))
                                    
                                    resource_counts = group_resources_by_type(resource)
                                    for resource_name, count in resource_counts.items():
                                        add_collection_message(resource_name, count)
                                else:
                                    if hasattr(obj, 'is_empty'):
                                        obj.is_empty = False
                                    obj.destroyed = False
                                
                                collect_cooldown = current_time
                                break
                
                # Try to feed cats
                for mob in nearby_mobs:
                    if mob.__class__.__name__ == "Cat" and not mob.is_alive:
                        continue
                    if mob.__class__.__name__ != "Cat":
                        continue
                    
                    mob_collision = mob.rect
                    horizontal_dist = abs(mob_collision.centerx - player_world_x)
                    vertical_dist = abs(mob_collision.centery - player_world_y)
                    feed_reach = 40
                    horizontal_range = (mob_collision.width / 2) + feed_reach
                    vertical_range = (mob_collision.height / 2) + feed_reach
                    facing_mob = False
                    
                    if player.last_direction == "right" and mob_collision.centerx > player_world_x - 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                        facing_mob = True
                    elif player.last_direction == "left" and mob_collision.centerx < player_world_x + 10 and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                        facing_mob = True
                    elif player.last_direction == "up" and mob_collision.centery < player_world_y + 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                        facing_mob = True
                    elif player.last_direction == "down" and mob_collision.centery > player_world_y - 10 and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                        facing_mob = True
                    
                    if facing_mob:
                        # Get current hotbar item
                        current_slot = inventory.hotbar_slots[inventory.selected_hotbar_slot]
                        if current_slot is not None:
                            item_name = current_slot["item_name"]
                            # Feed the cat
                            tame_increase = mob.feed_cat(item_name)
                            if tame_increase > 0 or item_name == "Poisonous Mushroom":
                                # Check if cat was just tamed
                                if hasattr(mob, 'just_tamed') and mob.just_tamed and naming_cat is None:
                                    naming_cat = mob
                                    cat_name_input = ""
                                    mob.just_tamed = False
                                
                                # Remove item from hotbar
                                current_slot["quantity"] -= 1
                                if current_slot["quantity"] <= 0:
                                    inventory.hotbar_slots[inventory.selected_hotbar_slot] = None
                                collect_cooldown = current_time
                                break

            for bush in berry_bushes:
                bush.update(dt)
            
            for tree in trees:
                tree.update(dt)
            
            for plant in fruit_plants:
                plant.update(dt)

            visible_mob_set = set(visible_mobs)
            for mob in nearby_mobs:
                mob.is_visible = mob in visible_mob_set

            for mob in nearby_mobs:
                def get_obj_rect(obj):
                    if isinstance(obj, dict) and 'rect' in obj:
                        return obj['rect']
                    else:
                        return obj.rect

                mob_nearby_objects = [obj for obj in nearby_objects
                                    if abs(get_obj_rect(obj).x - mob.rect.x) < 100
                                    and abs(get_obj_rect(obj).y - mob.rect.y) < 100]
                
                
                
                if abs(player_world_x - mob.rect.x) < 200 and abs(player_world_y - mob.rect.y) < 200:
                    
                    temp_player = TempPlayerCollision(player_world_x, player_world_y, player.rect.width, player.rect.height)
                    mob_nearby_objects.append(temp_player)
                
                mob_nearby_mobs = [m for m in nearby_mobs 
                                if m is not mob 
                                and abs(m.rect.x - mob.rect.x) < 100 
                                and abs(m.rect.y - mob.rect.y) < 100]
                
            
                if hasattr(mob, "enemy"):
                    mob.handle_player_proximity(dt, player_world_x, player_world_y, player=None,
                                                nearby_objects=None, nearby_mobs=None)
                    mob.attack(player_world_x, player_world_y, player)

                    
            
                mob.update(dt, None, mob_nearby_objects, mob_nearby_mobs)
                mob.keep_in_screen(height)
            player_world_x = player_pos.x + cam_x
            player_world_y = player_pos.y
            player.attacking(nearby_mobs, player_world_x, player_world_y)
            for mob in nearby_mobs:
                mob.handle_health(screen, cam_x, dt)
                mob.handle_lava_damage(dt)
                mob.flee(player_world_x, player_world_y, dt)
                
                # Liquid collision for mobs
                mob_in_liquid = False
                for liquid in nearby_objects:
                    if hasattr(liquid, 'liquid_type'):
                        if mob.rect.colliderect(liquid.get_collision_rect(0)):
                            mob.enter_liquid(liquid.liquid_type, liquid)
                            mob_in_liquid = True
                            break
                if not mob_in_liquid:
                    mob.exit_liquid()


            
            inventory.add(inventory_resources)
            inventory_resources = []

            for index, message in enumerate(collection_messages[:]):
                text, bg, rect, timer, total_time = message
                
                spacing = 27
                rect.y = 500 + spacing * index
                
                alpha = int(255 * (timer / total_time))
                text.set_alpha(alpha)
                bg.set_alpha(alpha)
                
                if message[3] < 2:
                    text.set_alpha(alpha)
                    bg.set_alpha(alpha)

                screen.blit(bg, (rect.x, rect.y))
                screen.blit(text, (rect.x + 5, rect.y + 5))
                message[3] -= dt
                if message[3] <= 0:
                    collection_messages.remove(message)



            left_player_check = pygame.Rect(player.rect.left - 1, player.rect.top + 5, 1, player.rect.height - 12)
            right_player_check = pygame.Rect(player.rect.right, player.rect.top + 5, 1, player.rect.height - 12)
            top_player_check = pygame.Rect(player.rect.left + 5, player.rect.top - 1, player.rect.width - 12, 1)
            bottom_player_check = pygame.Rect(player.rect.left + 5, player.rect.bottom, player.rect.width - 12, 1)

            for mob in mobs:
                mob.collision_rect = mob.rect.inflate(-15, -15)

            # Exclude liquids from collision detection so player can enter them
            all_nearby_solid = [obj for obj in (nearby_objects + nearby_mobs)
                               if not hasattr(obj, 'liquid_type')]

            # Add placed structures to collision detection
            all_collision_objects = all_nearby_solid + nearby_structures

            def get_obj_collision_rect(obj, cam_x):
                if hasattr(obj, 'get_collision_rect'):
                    return obj.get_collision_rect(cam_x)
                elif isinstance(obj, dict) and 'rect' in obj:
                    # Convert structure rect from world to screen coordinates
                    rect = obj['rect']
                    return pygame.Rect(rect.x - cam_x, rect.y, rect.width, rect.height)
                else:
                    return obj.rect

            left_collision = any(
                left_player_check.colliderect(get_obj_collision_rect(obj, cam_x))
                for obj in all_collision_objects
            )

            right_collision = any(
                right_player_check.colliderect(get_obj_collision_rect(obj, cam_x))
                for obj in all_collision_objects
            )

            up_collision = any(
                top_player_check.colliderect(get_obj_collision_rect(obj, cam_x))
                for obj in all_collision_objects
            )

            down_collision = any(
                bottom_player_check.colliderect(get_obj_collision_rect(obj, cam_x))
                for obj in all_collision_objects
            )

            # Liquid collision detection - use bottom center point of player
            player_feet_rect = pygame.Rect(player.rect.centerx - 5, player.rect.bottom - 5, 10, 10)
            in_liquid = False
            for pond in nearby_objects:
                if hasattr(pond, 'liquid_type') and pond.liquid_type == "water":
                    if player_feet_rect.colliderect(pond.get_collision_rect(cam_x)):
                        player.enter_liquid("water", pond)
                        in_liquid = True
                        break
            for lava in nearby_objects:
                if hasattr(lava, 'liquid_type') and lava.liquid_type == "lava":
                    if player_feet_rect.colliderect(lava.get_collision_rect(cam_x)):
                        player.enter_liquid("lava", lava)
                        in_liquid = True
                        break
            
            if not in_liquid:
                player.exit_liquid()

            if not inventory_in_use and not smelter_in_use and not crafting_bench_in_use and naming_cat is None:

                if (((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])) or pygame.mouse.get_pressed()[0]) and not player.exhausted:
                    if player.lose_stamina(screen, dt):
                        stamina_depleted_message_timer = 2.0
                    player.stamina_speed()

                is_moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
                is_running = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and is_moving
                
                if is_moving:
                    base_delay = 0.4
                    
                    actual_speed = player_speed * shift_multiplier
                    base_speed = player.base_speed * player.speed
                    speed_ratio = actual_speed / base_speed if base_speed > 0 else 1.0
                    
                    current_step_delay = base_delay / speed_ratio
                    
                    step_sound_timer += dt
                    if step_sound_timer >= current_step_delay:
                        current_bg = get_current_background(player_world_x, tiles)
                        current_footsteps = get_footstep_sounds(current_bg)
                        sound_manager.play_sound(random.choice(current_footsteps))
                        step_sound_timer = 0
                else:
                    step_sound_timer = 0

                if not is_moving:
                    if player.last_direction == "down":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted and not smelter_in_use:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_down_images)
                                player_current_image = player_stand_attack_down_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_animation_timer += dt
                            if player_animation_timer > .2:
                                player_frame_index = (player_frame_index + 1) % len(player_idle_down_images)
                                player_current_image = player_idle_down_images[player_frame_index]
                                player_animation_timer = 0
                    elif player.last_direction == "up":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted and not smelter_in_use:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_up_images)
                                player_current_image = player_stand_attack_up_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_animation_timer += dt
                            if player_animation_timer > .2:
                                player_frame_index = (player_frame_index + 1) % len(player_idle_up_images)
                                player_current_image = player_idle_up_images[player_frame_index]
                                player_animation_timer = 0
                    elif player.last_direction == "left":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted and not smelter_in_use:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_left_images)
                                player_current_image = player_stand_attack_left_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_animation_timer += dt
                            if player_animation_timer > .2:
                                player_frame_index = (player_frame_index + 1) % len(player_idle_left_images)
                                player_current_image = player_idle_left_images[player_frame_index]
                                player_animation_timer = 0
                    elif player.last_direction == "right":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted and not smelter_in_use:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_right_images)
                                player_current_image = player_stand_attack_right_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_animation_timer += dt
                            if player_animation_timer > .2:
                                player_frame_index = (player_frame_index + 1) % len(player_idle_right_images)
                                player_current_image = player_idle_right_images[player_frame_index]
                                player_animation_timer = 0
                
                if not crafting_bench_in_use:
                    if keys[pygame.K_w] and (player_pos.y - (size/2)) >= 0:
                        if not up_collision:
                            player_pos.y -= player_speed * dt * shift_multiplier
                    
                    
                    if keys[pygame.K_s] and (player_pos.y + (size/2)) <= height:
                        if not down_collision:
                            player_pos.y += player_speed * dt * shift_multiplier

                    
                    if keys[pygame.K_a]:
                        if not left_collision:
                            absolute_cam_x -= player_speed * dt * shift_multiplier
                            dungeon_depth = max(0, dungeon_depth - dungeon_traversal_speed * shift_multiplier)

                    
                    if keys[pygame.K_d]:
                        if not right_collision:
                            absolute_cam_x += player_speed * dt * shift_multiplier
                            dungeon_depth += dungeon_traversal_speed * shift_multiplier

                cam_x = int(absolute_cam_x)

                if not crafting_bench_in_use and (keys[pygame.K_d] and pygame.mouse.get_pressed()[0] and not player.exhausted):
                    player.last_direction = "right"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_right_attack_images)
                            player_current_image = player_walk_right_attack_images[player_frame_index]
                            player_animation_timer = 0

                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_right_attack_images)
                            player_current_image = player_walk_right_attack_images[player_frame_index]
                            player_animation_timer = 0

                elif not crafting_bench_in_use and keys[pygame.K_d]:
                    player.last_direction = "right"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_right_images)
                            player_current_image = player_walk_right_images[player_frame_index]
                            player_animation_timer = 0
                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_right_images)
                            player_current_image = player_walk_right_images[player_frame_index]
                            player_animation_timer = 0
                

                elif not crafting_bench_in_use and (keys[pygame.K_a] and pygame.mouse.get_pressed()[0] and not player.exhausted):
                    player.last_direction = "left"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_left_attack_images)
                            player_current_image = player_walk_left_attack_images[player_frame_index]
                            player_animation_timer = 0

                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_left_attack_images)
                            player_current_image = player_walk_left_attack_images[player_frame_index]
                            player_animation_timer = 0

                elif not crafting_bench_in_use and keys[pygame.K_a]:
                    player.last_direction = "left"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_left_images)
                            player_current_image = player_walk_left_images[player_frame_index]
                            player_animation_timer = 0

                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_left_images)
                            player_current_image = player_walk_left_images[player_frame_index]
                            player_animation_timer = 0


                elif not crafting_bench_in_use and (keys[pygame.K_w] and pygame.mouse.get_pressed()[0] and not player.exhausted):
                    player.last_direction = "up"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_up_attack_images)
                            player_current_image = player_walk_up_attack_images[player_frame_index]
                            player_animation_timer = 0

                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_up_attack_images)
                            player_current_image = player_walk_up_attack_images[player_frame_index]
                            player_animation_timer = 0

                elif not crafting_bench_in_use and keys[pygame.K_w]:
                    player.last_direction = "up"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_up_images)
                            player_current_image = player_walk_up_images[player_frame_index]
                            player_animation_timer = 0
                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_up_images)
                            player_current_image = player_walk_up_images[player_frame_index]
                            player_animation_timer = 0
                
                

                elif not crafting_bench_in_use and (keys[pygame.K_s] and pygame.mouse.get_pressed()[0] and not player.exhausted):
                    player.last_direction = "down"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_down_attack_images)
                            player_current_image = player_walk_down_attack_images[player_frame_index]
                            player_animation_timer = 0

                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_down_attack_images)
                            player_current_image = player_walk_down_attack_images[player_frame_index]
                            player_animation_timer = 0

                elif not crafting_bench_in_use and keys[pygame.K_s]:
                    player.last_direction = "down"
                    player_animation_timer += dt
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if player_animation_timer > .04:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_down_images)
                            player_current_image = player_walk_down_images[player_frame_index]
                            player_animation_timer = 0
                    else:
                        if player_animation_timer > .07:
                            player_frame_index = (player_frame_index + 1) % len(player_walk_down_images)
                            player_current_image = player_walk_down_images[player_frame_index]
                            player_animation_timer = 0

                


                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    shift_multiplier = 1.5
                    
                else:
                    shift_multiplier = 1

                step_sound_timer += dt
                if step_sound_timer >= step_sound_delay and (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                    sound_manager.play_sound(random.choice(grass_steps))
                    step_sound_timer = 0


        player.health_bar(screen)
        player.stamina_bar(screen)
        player.hunger_bar(screen)
        player.exp_bar(screen)
        player.thirst_bar(screen)
        screen.blit(stat_holder_image, (20, 50))
        player.handle_exp(screen, dt)
        player.status_effects(dt)
        player.handle_swimming(dt)
        player.handle_lava_damage(dt)
        player.regain_health(dt)
        player.lose_hunger(dt)
        player.lose_thirst(dt)
        player.clamp_stats()
    
        
        if dungeon_depth >= dungeon_depth_high:
            dungeon_depth_high = dungeon_depth

        player.determine_score(dungeon_depth_high)
        player.print_score(screen, dungeon_depth_high)
        player.is_dead(screen, dungeon_depth_high)

        if (not ((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])) and not pygame.mouse.get_pressed()[0]) or player.exhausted:
            player.regain_stamina(dt, screen)
            player.stamina_speed()
            player.lose_thirst(dt)
            
        if stamina_depleted_message_timer > 0:
            tired_text = font.render("Too tired. Rest to regain stamina", True, (40, 255, 20))
            x = screen.get_width()//2 - tired_text.get_width()//2
            y = 20
            temp_surface = pygame.Surface((tired_text.get_width() + 10, tired_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 20))
            screen.blit(temp_surface, (x - 5, y - 5))
            screen.blit(tired_text, (x, y))
            stamina_depleted_message_timer -= dt
        if inventory.inventory_full_message_timer > 0:
            full_text = font.render("Inventory Full! Cannot pick up items.", True, (255, 50, 50))
            x = screen.get_width()//2 - full_text.get_width()//2
            y = 50
            temp_surface = pygame.Surface((full_text.get_width() + 10, full_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 150))
            screen.blit(temp_surface, (x - 5, y - 5))
            screen.blit(full_text, (x, y))
            inventory.inventory_full_message_timer -= dt



        if smelter_in_use:
            smelter.render(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                slot_info = smelter.get_slot_at_mouse(mouse_pos, screen)
                slot_index, slot_type = slot_info
                
                if hasattr(smelter, 'button_rect') and smelter.button_rect.collidepoint(mouse_pos):
                    if smelter.fire_lit:
                        smelter.put_out_fire()
                    else:
                        smelter.light_fire()
                elif slot_index is not None:
                    if smelter.dragging:
                        smelter.end_drag(slot_info)
                    else:
                        smelter.start_drag(slot_info)
            elif event.type == pygame.MOUSEBUTTONUP:
                if smelter.dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_info = smelter.get_slot_at_mouse(mouse_pos, screen)
                    slot_index, slot_type = slot_info
                    if slot_index is not None:
                        smelter.end_drag(slot_info)
                    else:
                        smelter.cancel_drag()

        if inventory_in_use:

            inventory.draw_inventory(screen)
            if inventory.state == "inventory":
                inventory.draw_items(screen)
                inventory.draw_hotbar(screen)
            inventory.draw_dragged_item(screen)
            if inventory_tab_unused.is_clicked(event):
                inventory.state = "inventory"
            elif crafting_tab_unused.is_clicked(event):
                inventory.state = "crafting"
            elif level_up_tab_unused.is_clicked(event):
                inventory.state = "level_up"
            elif cats_tab_unused.is_clicked(event):
                inventory.state = "cats"
            if inventory.state == "level_up":
                inventory.handle_level_up_event(event)

        if paused:
            screen.blit(temp_pause_surface, pause_menu_rect.topleft)
            screen.blit(pause_menu_image, (((width - pause_menu_image.get_width())//2), ((height - pause_menu_image.get_height())//2)))
            resume_button.draw(screen)
            quit_button.draw(screen)

        depth_text = font.render(f"Dungeon Depth: {dungeon_depth:.1f}", True, (255, 255, 255))
        depth_rect = pygame.Rect(20, 20, depth_text.get_width(), depth_text.get_height())
        temp_surface = pygame.Surface((depth_rect.width + 10, depth_rect.height + 10), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 100))
        screen.blit(temp_surface, (depth_rect.x, depth_rect.y))
        screen.blit(depth_text, (depth_rect.x + 5, depth_rect.y + 5))

        time_text = font.render(f"Time: {time_of_day:.0f}", True, (255, 255, 255))
        time_rect = pygame.Rect(width - time_text.get_width() - 30, 20, time_text.get_width(), time_text.get_height())
        time_surface = pygame.Surface((time_rect.width + 10, time_rect.height + 10), pygame.SRCALPHA)
        time_surface.fill((0, 0, 0, 100))
        screen.blit(time_surface, (time_rect.x + 8, time_rect.y + 22))
        screen.blit(time_text, (time_rect.x + 13, time_rect.y + 27))

        if player.extreme_temp_timer >= 180:
            fatigue_color = (255, 150, 100)
            fatigue_text = font.render(f"FATIGUED ({player.extreme_temp_timer:.0f}s)", True, fatigue_color)
            fatigue_rect = pygame.Rect(width - fatigue_text.get_width() - 30, 60, fatigue_text.get_width(), fatigue_text.get_height())
            fatigue_surface = pygame.Surface((fatigue_rect.width + 10, fatigue_rect.height + 10), pygame.SRCALPHA)
            fatigue_surface.fill((0, 0, 0, 100))
            screen.blit(fatigue_surface, (fatigue_rect.x + 8, fatigue_rect.y + 22))
            screen.blit(fatigue_text, (fatigue_rect.x + 13, fatigue_rect.y + 27))

        current_bg = get_current_background(player_world_x, tiles)
        current_temperature = calculate_temperature(current_bg, time_of_day, player.swimming, player.in_lava, player.temperature_resistance_leveler)
        gauge_idx = get_temperature_gauge_index(current_temperature)
        draw_temperature_gauge(screen, current_temperature, gauge_idx)
        apply_temperature_effects(player, gauge_idx, dt)

        if crafting_bench_in_use:
            crafting_bench.draw(screen)

        if not paused and not inventory_in_use and naming_cat is None and not crafting_bench_in_use:
            if keys[pygame.K_o]:
                dungeon_depth -= 500
                absolute_cam_x -= 500
                player_pos.x = width / 2

            if keys[pygame.K_p]:
                dungeon_depth += 500
                absolute_cam_x += 500
                player_pos.x = width / 2

        # Draw cat naming prompt
        if naming_cat is not None:
            # Semi-transparent overlay
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            # Naming box
            box_width = 400
            box_height = 150
            box_x = width // 2 - box_width // 2
            box_y = height // 2 - box_height // 2
            
            # Draw box background
            pygame.draw.rect(screen, (40, 40, 60), pygame.Rect(box_x, box_y, box_width, box_height), border_radius=10)
            # Draw border
            pygame.draw.rect(screen, (200, 150, 100), pygame.Rect(box_x, box_y, box_width, box_height), width=3, border_radius=10)
            
            # Draw text
            title_font = pygame.font.SysFont(None, 28)
            input_font = pygame.font.SysFont(None, 24)
            
            title_text = title_font.render("Enter Cat's Name:", True, (255, 255, 200))
            title_rect = title_text.get_rect(center=(width // 2, box_y + 30))
            screen.blit(title_text, title_rect)
            
            # Draw input text with cursor
            input_display = cat_name_input + "|"
            input_text = input_font.render(input_display, True, (200, 200, 255))
            input_rect = input_text.get_rect(center=(width // 2, box_y + 70))
            screen.blit(input_text, input_rect)
            
            # Draw instruction text
            instruction_font = pygame.font.SysFont(None, 20)
            instruction_text = instruction_font.render("Press ENTER to confirm or BACKSPACE to delete", True, (200, 200, 200))
            instruction_rect = instruction_text.get_rect(center=(width // 2, box_y + 120))
            screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
pygame.quit()
