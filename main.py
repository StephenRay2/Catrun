import pygame
import math
import random
pygame.init()
from buttons import *
from mob_placement import *
from sounds import *
from crafting_bench import CraftingBench
from arcane_crafter import ArcaneCrafter
from smelter import Smelter
from campfire import Campfire
from mortar_pestle import MortarPestle
from chest import ChestUI
from alchemy_bench import AlchemyBench
from world import DroppedItem, dropped_items, Bank, banks
from debug import font_path, font
from mobs import hud_font

clock = pygame.time.Clock()
from inventory import *
running = True
dt = 0
time_speed_multiplier = 1.0
size = 64
world_x = 0.0
absolute_cam_x = 0.0
floor_y = 0
shift_multiplier = 1
dungeon_depth = absolute_cam_x
dungeon_depth_high = 0
scroll = 0
dungeon_traversal_speed = .1
time_of_day = 4.00
total_elapsed_time = 00.00
time_of_day_start = time_of_day
stamina_depleted_message_timer = 0
need_pickaxe_message_timer = 0
need_shovel_message_timer = 0
player_world_x = player_pos.x + cam_x
player_world_y = player_pos.y

collection_messages = []

# Cat naming system
naming_cat = None
cat_name_input = ""

paused = False
inventory_in_use = False
mouse_attack_blocked = False
mouse_attack_block_expires = 0
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
min_throw_hold_time = 0.2  # Minimum hold time (in seconds) to trigger throw instead of pickup
thrown_items = []
loaded_item_sprites = {}  # Cache for loaded item sprites
placeable_animation_cache = {}  # Cache for animated placeable sprites (keyed by name and size)
light_mask_cache = {}  # Cache for radial light masks
LIGHT_THROW_ITEMS = {"Feathers", "Phoenix Feather"}
STONE_THROW_ITEMS = {"Stone", "Redrock Stone", "Snowy Stone"}
BREAK_ON_HIT_ITEMS = {"Throwing Star", "Throwing Knife", "Snowball"}

# Light flicker variables
light_flicker_timer = 0
light_flicker_speed = 0.05

# Default placeable sizing
default_placeable_sprite_size = (64, 64)

# Placement system variables
placement_mode = False
placement_item = None
placement_position = (0, 0)
placed_structures = []
tent_menu_active = False
tent_menu_tent = None
tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
tent_hold_threshold = 0.6
fast_travel_menu_active = False
sleeping_in_tent = False
sleeping_tent_x = 0
sleeping_tent_y = 0
sleeping_tent_height = default_placeable_sprite_size[1]
tent_hide_active = False
tent_exit_offset = 20
tent_hover_highlight_surface = None
tent_hover_highlight_rect = None
current_tent_hover_option = None

def place_player_below_tent():
    tent_bottom_y = sleeping_tent_y + (sleeping_tent_height // 2)
    base_screen_y = tent_bottom_y + tent_exit_offset
    base_screen_x = sleeping_tent_x - cam_x

    def player_collides_at(screen_x, screen_y):
        if not hasattr(player, "rect"):
            return False
        player_rect = player.rect.copy()
        player_rect.center = (screen_x, screen_y)
        world_rect = player_rect.copy()
        world_rect.x += cam_x
        return world_rect_collides(world_rect)

    min_y = size / 2
    max_y = height - size / 2
    min_x = size / 2
    max_x = width - size / 2
    y_steps = [0, 10, 20, 30, 40, 60, 80, 100, 130, 160]
    x_offsets = [0, -20, 20, -40, 40, -60, 60]

    for y_offset in y_steps:
        target_y = max(min_y, min(base_screen_y + y_offset, max_y))
        for x_offset in x_offsets:
            target_x = max(min_x, min(base_screen_x + x_offset, max_x))
            if not player_collides_at(target_x, target_y):
                player_pos.x = target_x
                player_pos.y = target_y
                if hasattr(player, "rect"):
                    player.rect.center = (player_pos.x, player_pos.y)
                return

    # Fallback to base position even if colliding, but keep within bounds
    player_pos.x = max(min_x, min(base_screen_x, max_x))
    player_pos.y = max(min_y, min(base_screen_y, max_y))
    if hasattr(player, "rect"):
        player.rect.center = (player_pos.x, player_pos.y)

# Crafting bench variables
crafting_bench = None
crafting_bench_in_use = False
arcane_crafter = None
arcane_crafter_in_use = False
smelter = None
smelter_in_use = False
campfire = None
campfire_in_use = False
mortar_pestle = None
mortar_pestle_in_use = False
alchemy_bench = None
alchemy_bench_in_use = False
chest_ui = None
chest_in_use = False

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
    "Alchemy Bench": {
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
            # Heavier base so it can't be placed through solids
            "width_ratio": 0.7,
            "height_ratio": 0.35,
            "offset_x_ratio": -0.5,
            "offset_y_ratio": -1.0
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
            # Wide, shallow ground footprint; aligned to base
            "width_ratio": 0.95,
            "height_ratio": 0.33,
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

        new_item = inventory.create_item_instance(item_data, 1)
        
        target_slot = None
        for idx, slot in enumerate(inventory.inventory_list):
            if slot is None:
                target_slot = idx
                break
        
        if target_slot is not None:
            inventory.inventory_list[target_slot] = new_item
            items_added += 1
        else:
            break
    
    print(f"Successfully added {items_added} placeable items to inventory for testing")
    return items_added


def set_starting_loadout():
    """Populate starting inventory with one of each weapon and clear everything else."""
    loadout_items = [
        # Clubs
        "Wooden Club", "Spiked Wooden Club",
        # Swords
        "Wooden Sword", "Stone Sword", "Metal Sword", "Gold Sword", "Bone Sword", "Obsidian Sword",
        "Dusk Dragon Scale Sword", "Electric Dragon Scale Sword", "Fire Dragon Scale Sword", "Ice Dragon Scale Sword", "Poison Dragon Scale Sword",
        # Spears
        "Wooden Spear", "Stone Spear", "Metal Spear", "Gold Spear", "Bone Spear", "Obsidian Spear",
        "Dusk Dragon Scale Spear", "Electric Dragon Scale Spear", "Fire Dragon Scale Spear", "Ice Dragon Scale Spear", "Poison Dragon Scale Spear",
        # Axes (weapons)
        "Wooden Axe", "Stone Axe", "Metal Axe", "Gold Axe", "Bone Axe", "Obsidian Axe",
        "Dusk Dragon Scale Axe", "Electric Dragon Scale Axe", "Fire Dragon Scale Axe", "Ice Dragon Scale Axe", "Poison Dragon Scale Axe",
        # Pickaxes (included as weapons/tools)
        "Wooden Pickaxe", "Stone Pickaxe", "Metal Pickaxe", "Gold Pickaxe", "Bone Pickaxe", "Obsidian Pickaxe",
        "Dusk Dragon Scale Pickaxe", "Electric Dragon Scale Pickaxe", "Fire Dragon Scale Pickaxe", "Ice Dragon Scale Pickaxe", "Poison Dragon Scale Pickaxe",
    ]

    next_slot = 0
    for item_name in loadout_items:
        item_data = next((itm for itm in items_list if itm["item_name"] == item_name), None)
        if not item_data:
            print(f"Warning: starting item '{item_name}' not found.")
            continue
        new_item = inventory.create_item_instance(item_data, 1)
        while next_slot < inventory.capacity and inventory.inventory_list[next_slot] is not None:
            next_slot += 1
        if next_slot < inventory.capacity:
            inventory.inventory_list[next_slot] = new_item
            next_slot += 1
    # Add torches stack
    torch_data = next((itm for itm in items_list if itm["item_name"] == "Torch"), None)
    if torch_data:
        torch_stack = inventory.create_item_instance(torch_data, 50)
        while next_slot < inventory.capacity and inventory.inventory_list[next_slot] is not None:
            next_slot += 1
        if next_slot < inventory.capacity:
            inventory.inventory_list[next_slot] = torch_stack
            next_slot += 1

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
    cat_payload = dict(item_data) if is_cat and item_data else None

    break_on_hit = False
    preserve_instance = False
    if item_data and not is_cat:
        preserve_instance = should_preserve_item_instance(item_data)
        item_name = item_data.get("item_name", "")
        lower_name = item_name.lower()
        if item_name in BREAK_ON_HIT_ITEMS:
            break_on_hit = True
        elif is_regular_weapon_item(item_data):
            preserve_instance = True
            apply_flat_durability_cost(item_data, 31)
    
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
        "cat_data": cat_payload if is_cat else None,
        "landed": False,  # Track if item has landed
        "break_on_hit": break_on_hit,
        "preserve_instance": preserve_instance
    }
    thrown_items.append(thrown_item)

def should_preserve_item_instance(item_data):
    if not item_data:
        return False
    return item_data.get("durability") is not None

def apply_fractional_durability_cost(item_data, fraction):
    if not item_data or not fraction:
        return False
    durability = item_data.get("durability")
    max_durability = item_data.get("max_durability", durability)
    if durability is None or max_durability in (None, 0):
        return False
    cost = max(1, int(math.ceil(max_durability * fraction)))
    item_data["durability"] = max(0, durability - cost)
    return item_data["durability"] <= 0

def apply_flat_durability_cost(item_data, amount):
    if not item_data or amount is None:
        return False
    durability = item_data.get("durability")
    if durability is None:
        return False
    item_data["durability"] = max(0, durability - amount)
    return item_data["durability"] <= 0

def is_regular_weapon_item(item_data):
    if not item_data:
        return False
    item_name = item_data.get("item_name", "").lower()
    if item_name in ("throwing star", "throwing knife"):
        return False
    tags = item_data.get("tags", [])
    if "weapon" in tags:
        return True
    weapon_keywords = ["sword", "spear", "club", "axe", "shovel", "dagger", "mace", "knife"]
    for keyword in weapon_keywords:
        if keyword == "axe" and "pickaxe" in item_name:
            continue
        if keyword in item_name:
            return True
    return False

def calculate_thrown_damage(item_data, base_attack):
    if not item_data:
        return 0
    item_name = item_data.get("item_name", "")
    lower_name = item_name.lower()
    if "snowball" in lower_name:
        return 1
    if item_name in LIGHT_THROW_ITEMS:
        return 0
    if item_name in STONE_THROW_ITEMS:
        return random.randint(4, 8)
    if "throwing star" in lower_name:
        return random.randint(20, 25)
    if "throwing knife" in lower_name:
        return random.randint(15, 20)
    if is_regular_weapon_item(item_data):
        return compute_weapon_attack(base_attack, item_data) + 20
    return 0

def apply_snowball_slow_effect(mob, stack_duration=1.5, max_duration=7.5, max_stacks=5):
    if not hasattr(mob, "snowball_slow_stacks"):
        mob.snowball_slow_stacks = 0
        mob.snowball_slow_timer = 0.0
    mob.snowball_slow_stacks = min(max_stacks, getattr(mob, "snowball_slow_stacks", 0) + 1)
    current_timer = getattr(mob, "snowball_slow_timer", 0.0)
    mob.snowball_slow_timer = min(max_duration, current_timer + stack_duration)

def handle_thrown_hit(thrown_item, mob, base_attack):
    if not thrown_item or thrown_item.get("is_cat"):
        return
    item_data = thrown_item.get("item")
    if not item_data:
        return
    damage = calculate_thrown_damage(item_data, base_attack)
    if damage > 0:
        mob.health = max(0, mob.health - damage)
        if item_data.get("item_name", "").lower() == "snowball":
            apply_snowball_slow_effect(mob)
    break_on_hit = thrown_item.get("break_on_hit", False)
    should_drop = not break_on_hit
    durability = item_data.get("durability")
    if durability is not None and durability <= 0:
        should_drop = False
    if should_drop:
        create_world_item_from_thrown(thrown_item)

def build_cat_from_item(cat_data, x, y):
    """Recreate a cat mob from inventory item data when the cat object is missing."""
    cat_type_key = cat_data.get("cat_type")
    cat_type_data = next((ct for ct in cat_types if ct.get("type") == cat_type_key), random.choice(cat_types))
    
    cat = Cat(x, y, "Cat")
    
    if cat_type_data and cat.cat_type != cat_type_data:
        cat.cat_type = cat_type_data
        cat.walk_right_images = [pygame.image.load(cat.cat_type[f"walk_right_image{i}"]).convert_alpha() for i in range(1, 6)]
        cat.stand_right_image = pygame.image.load(cat.cat_type["stand_right_image"]).convert_alpha()
        cat.walk_left_images = [pygame.transform.flip(img, True, False) for img in cat.walk_right_images]
        cat.stand_left_image = pygame.transform.flip(cat.stand_right_image, True, False)
        cat.dead_cat_right_image = pygame.image.load(cat.cat_type["dead_image"]).convert_alpha()
        cat.dead_cat_left_image = pygame.transform.flip(cat.dead_cat_right_image, True, False)
        cat.image = cat.stand_right_image
        cat.rect = cat.image.get_rect(center=(x, y))
    else:
        cat.rect.center = (x, y)
    
    cat.cat_name = cat_data.get("cat_name")
    cat.tame = cat_data.get("cat_tame", cat.tame)
    cat.tamed = True
    # Recreated cats are already tamed companions, so let them
    # use their custom follow/attack movement logic.
    cat.disable_autonomous_movement = True
    cat.just_tamed = False
    cat.level = cat_data.get("cat_level", cat.level)
    cat.health = min(cat_data.get("cat_health", cat.health), cat.max_health)
    return cat

def resolve_item_icon_path(item_data):
    if not item_data:
        return None
    icon = item_data.get("icon")
    if not icon:
        return None
    if icon.startswith("assets/"):
        return icon
    return f"assets/sprites/items/{icon}"

def spawn_dropped_collectible(item_data, quantity=1, drop_x=None, drop_y=None, item_instance=None):
    payload = item_instance or item_data
    if not payload or quantity is None or quantity <= 0:
        return False
    icon_path = resolve_item_icon_path(payload)
    x = player_world_x if drop_x is None else drop_x
    y = player_world_y if drop_y is None else drop_y
    # Offset so the item centers near the player position
    icon_size = getattr(DroppedItem, "ICON_SIZE", 16)
    half = icon_size // 2
    dropped_items.append(
        DroppedItem(
            int(x - half),
            int(y - half),
            payload.get("item_name", ""),
            icon_path,
            amount=quantity,
            item_instance=item_instance
        )
    )
    return True

def process_drop_result(drop_result, drop_x=None, drop_y=None):
    if not drop_result:
        return False
    item_data = drop_result.get("item_data")
    amount = drop_result.get("amount", 0)
    if not item_data or amount <= 0:
        return False
    return spawn_dropped_collectible(item_data, amount, drop_x, drop_y)

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
    
    # Fallback: spawn a generic dropped collectible that can be picked back up
    item_instance = None
    if thrown_item.get("preserve_instance"):
        item_instance = thrown_item["item"]
        if item_instance.get("durability") is not None and item_instance["durability"] <= 0:
            return False
    spawn_dropped_collectible(
        thrown_item["item"],
        thrown_item.get("quantity", 1),
        x,
        y,
        item_instance=item_instance
    )
    return True

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

def world_rect_collides(collision_rect):
    """Return True if the provided world-space rect hits any blocking object.

    Convert both sides to screen space (via cam_x) so placement uses the same
    collision shapes as movement. Collectibles remain ignored.
    """
    from world import (
        rocks,
        boulders,
        trees,
        berry_bushes,
        ponds,
        lavas,
        dead_bushes,
        fruit_plants,
        ferns,
        gemstone_rocks,
        metal_ore_rocks,
        metal_vein_rocks,
        gold_ore_rocks,
        gold_vein_rocks,
        banks,
    )

    global cam_x
    cam_offset = int(cam_x) if "cam_x" in globals() else 0

    # Candidate rect in screen space
    test_rect = pygame.Rect(
        collision_rect.x - cam_offset,
        collision_rect.y,
        collision_rect.width,
        collision_rect.height,
    )

    def make_rock_collision(rect):
        if rect is None:
            return None
        return pygame.Rect(
            rect.x - cam_offset + 10,
            rect.y + int(rect.height * 0.22),
            max(1, rect.width - 20),
            max(1, rect.height - 50),
        )

    # Rocks and boulders (including special ore/gem rocks)
    for rock in rocks:
        if getattr(rock, "destroyed", False):
            continue
        rock_rect = make_rock_collision(getattr(rock, "rect", None))
        if rock_rect and rock_rect.colliderect(test_rect):
            return True

    for gem in gemstone_rocks:
        if getattr(gem, "destroyed", False):
            continue
        gem_rect = make_rock_collision(getattr(gem, "rect", None))
        if gem_rect and gem_rect.colliderect(test_rect):
            return True

    for ore in metal_ore_rocks + metal_vein_rocks + gold_ore_rocks + gold_vein_rocks:
        if getattr(ore, "destroyed", False):
            continue
        ore_rect = make_rock_collision(getattr(ore, "rect", None))
        if ore_rect and ore_rect.colliderect(test_rect):
            return True

    for boulder in boulders:
        if getattr(boulder, "destroyed", False):
            continue
        boulder_rect = make_rock_collision(getattr(boulder, "rect", None))
        if boulder_rect and boulder_rect.colliderect(test_rect):
            return True

    def rect_to_screen(obj):
        r = getattr(obj, "rect", None)
        if r is None:
            return None
        return pygame.Rect(r.x - cam_offset, r.y, r.width, r.height)

    for tree in trees:
        if getattr(tree, "destroyed", False):
            continue
        r = rect_to_screen(tree)
        if r and r.colliderect(test_rect):
            return True

    for bush in berry_bushes:
        if getattr(bush, "destroyed", False):
            continue
        r = rect_to_screen(bush)
        if r and r.colliderect(test_rect):
            return True

    for bush in dead_bushes:
        if getattr(bush, "destroyed", False):
            continue
        r = rect_to_screen(bush)
        if r and r.colliderect(test_rect):
            return True

    for plant in fruit_plants:
        if getattr(plant, "destroyed", False):
            continue
        r = rect_to_screen(plant)
        if r and r.colliderect(test_rect):
            return True

    for fern in ferns:
        if getattr(fern, "destroyed", False):
            continue
        r = rect_to_screen(fern)
        if r and r.colliderect(test_rect):
            return True

    for bank in banks:
        if getattr(bank, "destroyed", False):
            continue
        r = rect_to_screen(bank)
        if r and r.colliderect(test_rect):
            return True

    for pond in ponds:
        if getattr(pond, "destroyed", False):
            continue
        if hasattr(pond, "get_collision_rect") and pond.get_collision_rect(cam_offset).colliderect(test_rect):
            return True

    for lava in lavas:
        if getattr(lava, "destroyed", False):
            continue
        if hasattr(lava, "get_collision_rect") and lava.get_collision_rect(cam_offset).colliderect(test_rect):
            return True

    from mob_placement import (
        cats,
        squirrels,
        cows,
        chickens,
        crawlers,
        ashhounds,
        pocks,
        deers,
        black_bears,
        brown_bears,
        gilas,
        crows,
        duskwretches,
        fire_dragons,
        ice_dragons,
        electric_dragons,
        poison_dragons,
        dusk_dragons,
        glowbirds,
    )

    all_mobs = (
        cats
        + squirrels
        + cows
        + chickens
        + crawlers
        + ashhounds
        + pocks
        + deers
        + black_bears
        + brown_bears
        + gilas
        + crows
        + glowbirds
        + duskwretches
        + fire_dragons
        + ice_dragons
        + electric_dragons
        + poison_dragons
        + dusk_dragons
    )

    for mob in all_mobs:
        rect = getattr(mob, "rect", None)
        if rect is not None:
            mob_rect = pygame.Rect(rect.x - cam_offset, rect.y, rect.width, rect.height)
            if mob_rect.colliderect(test_rect):
                return True

    for structure in placed_structures:
        rect = structure.get("rect")
        if rect:
            struct_rect = pygame.Rect(rect.x - cam_offset, rect.y, rect.width, rect.height)
            if struct_rect.colliderect(test_rect):
                return True

    return False

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

    return world_rect_collides(collision_rect)

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

    if item_data['item_name'] == 'Chest':
        structure['storage'] = [None] * 36

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
        if isinstance(resource, dict) and "__full_item__" in resource:
            item_name = resource["__full_item__"].get("item_name", "Item")
        else:
            item_name = resource
        resource_counts[item_name] = resource_counts.get(item_name, 0) + 1
    return resource_counts

def add_collection_message(resource_name, count):
    message_font = pygame.font.Font(font_path, 13)
    text_surface = message_font.render(f"Collected {count} {resource_name}", True, (20, 255, 20))
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

def is_shovel_item(item):
    """Return True if the item is a digging tool."""
    if not item:
        return False
    item_name = item.get("item_name", "").lower()
    tags = item.get("tags", [])
    return "shovel" in item_name or "digging" in tags

def get_harvest_power(tool_item, resource_name):
    """Return how many resources a single harvest hit should yield based on the held tool."""
    base_power = 1
    if not tool_item or not resource_name:
        return base_power

    tier = get_tool_tier(tool_item)
    if not tier or tier not in tool_multipliers:
        return base_power

    is_pickaxe = is_pickaxe_item(tool_item)
    is_axe = is_axe_item(tool_item)
    is_shovel = is_shovel_item(tool_item)
    is_special = resource_name in special_resources

    if is_pickaxe and resource_name in mining_resources:
        mult = tool_multipliers.get(tier, {"normal": 1, "special": 1})
        return max(base_power, mult["special"] if is_special else mult["normal"])

    if is_axe and is_wood_resource(resource_name):
        mult = tool_multipliers.get(tier, {"normal": 1})
        return max(base_power, mult.get("normal", 1))

    if is_shovel and resource_name in shovel_resources:
        mult = tool_multipliers.get(tier, {"normal": 1, "special": 1})
        return max(base_power, mult.get("normal", 1))

    # Future: shovel support for dirt/sand/etc.
    return base_power

def get_special_drop_multiplier(tool_item):
    """Bonus chance for special drops from mining resources based on pickaxe tier."""
    if not tool_item or not is_pickaxe_item(tool_item):
        return 1.0
    tier = get_tool_tier(tool_item)
    return SPECIAL_DROP_MULTS.get(tier, 1.0)

def get_special_yield_multiplier(tool_item):
    """Bonus yield for special mining drops from pickaxe tier."""
    if not tool_item or not is_pickaxe_item(tool_item):
        return 1.0
    tier = get_tool_tier(tool_item)
    mults = HARVEST_TOOL_MULTS.get(tier, {"special": 1})
    return mults.get("special", 1)

def get_weapon_tier_from_name(name):
    tiers = ["dragon", "obsidian", "metal", "gold", "bone", "stone", "wood"]
    for tier in tiers:
        if tier in name:
            return tier
    return None

def compute_weapon_attack(base_attack, held_item):
    """Return effective attack after weapon multipliers/flat bonuses."""
    if not held_item:
        return base_attack

    name = held_item.get("item_name", "").lower()
    tier = get_weapon_tier_from_name(name)

    if "throwing knife" in name:
        return max(1, int(base_attack + 15))

    if "shovel" in name:
        shovel_bonus = {
            "wood": 5,
            "stone": 7,
            "metal": 12,
            "bone": 12,
            "gold": 12,
            "obsidian": 15,
            "dragon": 20
        }
        bonus = shovel_bonus.get(tier, 0)
        if bonus > 0:
            return max(1, int(base_attack + bonus))

    sword_mults = {
        "wood": (1.1, 5),
        "stone": (1.3, 9),
        "metal": (1.4, 13),
        "bone": (2.1, 2),
        "obsidian": (1.4, 25),
        "dragon": (2.2, 20),
    }
    spear_flats = {
        "wood": 9,
        "stone": 15,
        "metal": 22,
        "bone": 19,
        "obsidian": 40,
        "dragon": 55,
    }

    # Clubs
    if "spiked wooden club" in name:
        return max(1, int(math.floor(base_attack * 1.5) + 12))
    if "wooden club" in name:
        return max(1, int(math.floor(base_attack * 1.3) + 4))

    # Swords
    if "sword" in name and tier in sword_mults:
        mult, flat = sword_mults[tier]
        return max(1, int(math.floor(base_attack * mult) + flat))

    # Axes (not pickaxes): same as sword multipliers, but lower base damage
    if "axe" in name and "pickaxe" not in name and tier in sword_mults:
        mult, flat = sword_mults[tier]
        reduced_base = base_attack // 1.5
        return max(1, int(math.floor(reduced_base * mult) + flat))

    # Pickaxes: similar scaling to axes but using one-third base damage
    if "pickaxe" in name and tier in sword_mults:
        mult, flat = sword_mults[tier]
        reduced_base = base_attack // 3
        return max(1, int(math.floor(reduced_base * mult) + flat))

    # Spears: flat bonuses only
    if "spear" in name and tier in spear_flats:
        return max(1, int(base_attack + spear_flats[tier]))

    return base_attack

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

# Use the shared tool multiplier table from inventory/tooltips
tool_multipliers = HARVEST_TOOL_MULTS

special_resources = {"Flint", "Raw Metal", "Raw Gold"}
mining_resources = {"Stone", "Flint", "Raw Metal", "Raw Gold"}
shovel_resources = {"Salt", "Clay", "Sand", "Snow"}

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
    is_shovel = is_shovel_item(tool_item)
    if not (is_pickaxe or is_axe or is_shovel):
        return resources

    adjusted = []
    for res in resources:
        res_name = res if isinstance(res, str) else str(res)
        if is_shovel and res_name in shovel_resources:
            mult = tool_multipliers.get(tier, {"normal": 1, "special": 1})
            factor = mult.get("normal", 1)
            adjusted.extend([res_name] * max(1, factor))
            continue
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

        rocks = [rock for rock in rocks if not rock.destroyed]
        boulders = [boulder for boulder in boulders if not boulder.destroyed]
        trees = [tree for tree in trees if not tree.destroyed]
        berry_bushes = [bush for bush in berry_bushes if not bush.destroyed]
        dead_bushes = [bush for bush in dead_bushes if not bush.destroyed]
        ferns = [fern for fern in ferns if not fern.destroyed]
        fruit_plants = [plant for plant in fruit_plants if not plant.destroyed]
        gemstone_rocks = [gr for gr in gemstone_rocks if not gr.destroyed]
        metal_ore_rocks = [ore for ore in metal_ore_rocks if not ore.destroyed]
        metal_vein_rocks = [vein for vein in metal_vein_rocks if not vein.destroyed]
        gold_ore_rocks = [ore for ore in gold_ore_rocks if not ore.destroyed]
        gold_vein_rocks = [vein for vein in gold_vein_rocks if not vein.destroyed]
        banks = [bank for bank in banks if not bank.destroyed]
        
        collectibles = sticks + stones + grasses + savannah_grasses + mushrooms + dropped_items 
        all_objects = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants + ponds + lavas + banks

        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -1000 and col.rect.y - cam_x < width + 1000]
        all_objects_no_liquids = rocks + trees + boulders + gemstone_rocks + metal_ore_rocks + metal_vein_rocks + gold_ore_rocks + gold_vein_rocks + berry_bushes + dead_bushes + ferns + fruit_plants + banks
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
            prev_time_of_day = time_of_day
            time_dt = dt * time_speed_multiplier
            total_elapsed_time += time_dt
            time_of_day = (time_of_day_start + (total_elapsed_time / 60)) % 24
            light_flicker_timer += dt
            if sleeping_in_tent or tent_hide_active:
                absolute_cam_x = sleeping_tent_x - width // 2
            if sleeping_in_tent and time_of_day >= 6 and time_of_day < 18:
                sleeping_in_tent = False
                time_speed_multiplier = 1.0
                absolute_cam_x = player_world_x - width // 2
                place_player_below_tent()
            # Update crafting flash
            inventory.update_flash(dt)
            for dropped in list(dropped_items):
                dropped.update_lifetime(time_dt)
            if smelter:
                smelter.update(time_dt)
            if campfire:
                campfire.update(time_dt)
            # Update placement position if in placement mode
            update_placement_position()
        else:
            dt = 0

        
        if game_just_started:
            generate_world()
            total_elapsed_time = 0
            time_of_day = time_of_day_start
            sleeping_in_tent = False
            tent_hide_active = False
            time_speed_multiplier = 1.0
            stamina_depleted_message_timer = 0
            need_pickaxe_message_timer = 0
            player.full_timer = 60
            player.thirst_full_timer = 60
            cats.clear()
            squirrels.clear()
            cows.clear()
            chickens.clear()
            crawlers.clear()
            ashhounds.clear()
            pocks.clear()
            deers.clear()
            black_bears.clear()
            brown_bears.clear()
            gilas.clear()
            crows.clear()
            glowbirds.clear()
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

            for _ in range(num_ashhounds):
                if weighted_ashhound_tiles:
                    tile_x, tile_image = random.choice(weighted_ashhound_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    ashhounds.append(Ashhound(x, y, "Ashhound"))

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

            for _ in range(num_glowbirds):
                if weighted_glowbird_tiles:
                    tile_x, tile_image = random.choice(weighted_glowbird_tiles)
                    x = random.randint(tile_x, tile_x + BACKGROUND_SIZE - 64)
                    y = random.randint(0, height - 64)
                    glowbirds.append(Glowbird(x, y, "Glowbird"))

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
            player.max_weight = int(round(400 * player.weight_leveler * player.temp_weight_increase))
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
            globals()['arcane_crafter'] = ArcaneCrafter(inventory)
            globals()['smelter'] = Smelter(inventory)
            globals()['campfire'] = Campfire(inventory)
            globals()['mortar_pestle'] = MortarPestle(inventory)
            globals()['alchemy_bench'] = AlchemyBench(inventory)
            globals()['chest_ui'] = ChestUI(inventory)

            inventory_resources = []
            collection_messages = []
            thrown_items = []

            inventory.state = "inventory"
            starter_items = [
                "Arcane Crafter",
                "Smelter",
                "Workbench",
                "Mortar And Pestle",
                "Tent",
                "Fire Dragon Scale Sword",
                "Fire Dragon Scale Pickaxe",
                "Chest",
                "Chest"
            ]
            # Add 20 torches (will stack) plus other starter items
            torch_stack = ["Torch"] * 10
            beef_stack = ["Raw Beef"] * 20
            inventory.add(torch_stack + starter_items + beef_stack)
            
            from world import gemstone_rocks, GemstoneRock
            gemstone_rocks.append(GemstoneRock(int(player_pos.x + cam_x + 100), int(player_pos.y + 50)))

            game_just_started = False 
        
        if sleeping_in_tent or tent_hide_active:
            # During sleep/hide, use tent position as world center for mob AI
            player_world_x = sleeping_tent_x
            player_world_y = player_pos.y
        else:
            player_world_x = player_pos.x + cam_x
            player_world_y = player_pos.y
        inventory.ui_open = inventory_in_use or campfire_in_use or smelter_in_use or crafting_bench_in_use or mortar_pestle_in_use or alchemy_bench_in_use or chest_in_use or inventory.drop_menu_active or tent_menu_active or fast_travel_menu_active
        
        player_speed = player.get_speed()
        if player.swimming:
            player_speed *= 0.5
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEWHEEL:
                if inventory_in_use and inventory.state == "cats":
                    inventory.handle_cat_scroll(-event.y)
                    continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                if inventory_in_use and inventory.state == "cats":
                    direction = 1 if event.button == 5 else -1
                    inventory.handle_cat_scroll(direction)
                    continue
            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Exit hide/sleep states with E
                if tent_hide_active and event.key == pygame.K_e:
                    tent_hide_active = False
                    place_player_below_tent()
                    continue
                if sleeping_in_tent and event.key == pygame.K_e:
                    sleeping_in_tent = False
                    time_speed_multiplier = 1.0
                    place_player_below_tent()
                    continue
                if tent_menu_active and event.key == pygame.K_e:
                    tent_menu_active = False
                    tent_menu_tent = None
                    continue
                if fast_travel_menu_active and event.key == pygame.K_e:
                    fast_travel_menu_active = False
                    continue

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

                if inventory.drop_menu_active and inventory.awaiting_drop_amount:
                    drop_result = inventory.handle_drop_amount_key(event)
                    if drop_result:
                        process_drop_result(drop_result)
                    continue
                
                if event.key == pygame.K_ESCAPE:
                    if crafting_bench_in_use:
                        crafting_bench.close()
                        crafting_bench_in_use = False
                    elif arcane_crafter_in_use:
                        arcane_crafter.close()
                        arcane_crafter_in_use = False
                    elif campfire_in_use:
                        campfire.close()
                        campfire_in_use = False
                    elif smelter_in_use:
                        smelter.close()
                        smelter_in_use = False
                    elif mortar_pestle_in_use:
                        mortar_pestle.close()
                        mortar_pestle_in_use = False
                    elif alchemy_bench_in_use:
                        alchemy_bench.close()
                        alchemy_bench_in_use = False
                    elif chest_in_use:
                        chest_ui.close()
                        chest_in_use = False
                    elif not inventory_in_use:
                        if placement_mode:
                            cancel_placement()
                        else:
                            paused = not paused
                    elif inventory_in_use:
                        inventory_in_use = False
                        inventory.ui_open = False
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None
                        inventory.close_drop_menu()

                # Disable hotbar key switching while placing a structure
                if not placement_mode:
                    inventory.handle_keydown_hotbar(event, screen=None, use_on_press=False)
                
                if crafting_bench_in_use:
                    crafting_bench.handle_key_event(event)
                elif arcane_crafter_in_use:
                    arcane_crafter.handle_key_event(event)
                elif alchemy_bench_in_use:
                    alchemy_bench.handle_key_event(event)
                elif mortar_pestle_in_use:
                    mortar_pestle.handle_key_event(event)
                # Allow exiting smelter/campfire with E or ESC even while UI is open
                if (smelter_in_use or campfire_in_use or mortar_pestle_in_use or alchemy_bench_in_use or chest_in_use) and event.key not in (pygame.K_e, pygame.K_ESCAPE):
                    continue

            if inventory_in_use:
                tab_clicked = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if inventory_tab_unused.is_clicked(event):
                        inventory.state = "inventory"
                        inventory.close_drop_menu()
                        tab_clicked = True
                    elif crafting_tab_unused.is_clicked(event):
                        inventory.state = "crafting"
                        inventory.close_drop_menu()
                        tab_clicked = True
                    elif level_up_tab_unused.is_clicked(event):
                        inventory.state = "level_up"
                        inventory.close_drop_menu()
                        tab_clicked = True
                    elif cats_tab_unused.is_clicked(event):
                        inventory.state = "cats"
                        inventory.close_drop_menu()
                        tab_clicked = True
                if tab_clicked:
                    continue
                inventory.handle_level_up_event(event)
                inventory.handle_cats_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f and not inventory_in_use and not crafting_bench_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use and player.is_alive:
                consumed_item = False
                success, tags = inventory.consume_item()
                if success:
                    consumed_item = True
                    if "food" in tags:
                        sound_manager.play_sound(random.choice([f"consume_item{i}" for i in range(1, 7)]))
                    elif any(tag in tags for tag in ["liquid", "consumable"]):
                        sound_manager.play_sound(random.choice([f"consume_water{i}" for i in range(1, 5)]))
                if not consumed_item and player.swimming and player.current_liquid and not player.in_lava:
                    if getattr(player.current_liquid, "liquid_type", "") == "water":
                        player.thirst = player.max_thirst
                        player.thirst_full_timer = getattr(player, "thirst_full_timer", 60)
                        sound_manager.play_sound(random.choice([f"consume_water{i}" for i in range(1, 5)]))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q and not crafting_bench_in_use and not smelter_in_use and not campfire_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use and not arcane_crafter_in_use:
                inventory_in_use = not inventory_in_use
                inventory.ui_open = inventory_in_use
                if not inventory_in_use:
                    inventory.selection_mode = "hotbar"
                    inventory.selected_inventory_slot = None
                    inventory.close_drop_menu()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and player.is_alive:
                selected_slot = None
                selected_index = None
                slot_is_hotbar = False
                if inventory.selection_mode == "hotbar":
                    selected_index = inventory.selected_hotbar_slot
                    selected_slot = inventory.hotbar_slots[selected_index]
                    slot_is_hotbar = True
                elif inventory.selection_mode == "inventory" and inventory.selected_inventory_slot is not None:
                    selected_index = inventory.selected_inventory_slot
                    selected_slot = inventory.inventory_list[selected_index]
                
                is_cat_slot = selected_slot is not None and ("cat_object" in selected_slot or "cat_type" in selected_slot)
                if is_cat_slot and selected_index is not None:
                    cat_obj = selected_slot.get("cat_object")
                    if cat_obj is None and "cat_type" in selected_slot:
                        cat_obj = build_cat_from_item(selected_slot, player_world_x, player_world_y)
                        selected_slot["cat_object"] = cat_obj
                    if cat_obj:
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
                        else:
                            place_x = player_world_x
                            place_y = player_world_y + placement_distance

                            cat_obj.rect.centerx = place_x
                            cat_obj.rect.centery = place_y
                            cat_obj.placement_time = pygame.time.get_ticks()
                            cat_obj.destroyed = False
                            if cat_obj not in cats:
                                cats.append(cat_obj)

                            if "quantity" in selected_slot:
                                selected_slot["quantity"] -= 1
                                if selected_slot["quantity"] <= 0:
                                    if slot_is_hotbar:
                                        inventory.hotbar_slots[selected_index] = None
                                    else:
                                        inventory.inventory_list[selected_index] = None
                            else:
                                if slot_is_hotbar:
                                    inventory.hotbar_slots[selected_index] = None
                                else:
                                    inventory.inventory_list[selected_index] = None
                            inventory.recalc_weight()
                            sound_manager.play_sound(random.choice(["cat_meow1", "cat_meow2", "cat_meow3"]))
                    else:
                        drop_result = inventory.remove_selected_quantity(1)
                        if drop_result:
                            process_drop_result(drop_result)
                    inventory.close_drop_menu()
                
                if inventory_in_use and player.is_alive:
                    if event.key == pygame.K_ESCAPE:
                        inventory_in_use = False
                        inventory.ui_open = False
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None
                        inventory.close_drop_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and inventory.drop_menu_active:
                drop_result = inventory.handle_drop_menu_click(pygame.mouse.get_pos())
                if drop_result:
                    process_drop_result(drop_result)
                    continue
                if inventory.drop_menu_active:
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                ui_context_open = (
                    inventory_in_use
                    or campfire_in_use
                    or smelter_in_use
                    or crafting_bench_in_use
                    or arcane_crafter_in_use
                    or mortar_pestle_in_use
                    or alchemy_bench_in_use
                    or chest_in_use
                )
                if ui_context_open:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if inventory_in_use:
                        slot_index, is_hotbar = inventory.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None and inventory.handle_drop_right_click(mouse_pos, screen):
                            continue
                    elif smelter_in_use:
                        slot_info = smelter.get_slot_at_mouse(mouse_pos, screen)
                        slot_index, slot_type = slot_info
                        if slot_index is not None:
                            if slot_type in ["inventory", "hotbar"]:
                                is_hotbar = (slot_type == "hotbar")
                                if inventory.open_drop_menu(slot_index, is_hotbar, mouse_pos):
                                    continue
                            elif smelter.open_drop_menu(slot_index, slot_type, mouse_pos):
                                continue
                    elif campfire_in_use:
                        slot_info = campfire.get_slot_at_mouse(mouse_pos, screen)
                        slot_index, slot_type = slot_info
                        if slot_index is not None:
                            if slot_type in ["inventory", "hotbar"]:
                                is_hotbar = (slot_type == "hotbar")
                                if inventory.open_drop_menu(slot_index, is_hotbar, mouse_pos):
                                    continue
                            elif campfire.open_drop_menu(slot_index, slot_type, mouse_pos):
                                continue
                    elif crafting_bench_in_use:
                        slot_index, is_hotbar = crafting_bench.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            if crafting_bench.open_drop_menu(slot_index, is_hotbar, mouse_pos):
                                continue
                    elif arcane_crafter_in_use:
                        slot_index, slot_type = arcane_crafter.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            if slot_type in ["inventory", "hotbar"]:
                                is_hotbar = (slot_type == "hotbar")
                                if inventory.open_drop_menu(slot_index, is_hotbar, mouse_pos):
                                    continue
                            elif arcane_crafter.open_drop_menu(slot_index, slot_type, mouse_pos):
                                continue
                    elif alchemy_bench_in_use:
                        slot_index, is_hotbar = alchemy_bench.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            if alchemy_bench.open_drop_menu(slot_index, is_hotbar, mouse_pos):
                                continue
                    elif chest_in_use:
                        slot_index, slot_type = chest_ui.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            if chest_ui.open_drop_menu(slot_index, slot_type, mouse_pos):
                                continue
                    
                    inventory.close_drop_menu()
                    continue

            # Placement system - toggle placement mode with right-click
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 3
                and player.is_alive
                and not crafting_bench_in_use
                and not arcane_crafter_in_use
                and not smelter_in_use
                and not campfire_in_use
                and not mortar_pestle_in_use
                and not alchemy_bench_in_use
                and not chest_in_use
                and not inventory_in_use
            ):
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
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and player.is_alive and not placement_mode and not inventory_in_use:
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
                                success, tags, thrown_instance = inventory.throw_item()
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
                                    
                                    thrown_payload = thrown_instance or item
                                    is_cat_item = "cat_type" in thrown_payload if thrown_payload else False
                                    spawn_thrown_item(start_x, start_y, vel_x, vel_y, thrown_payload, is_cat=is_cat_item, throw_power=throw_power)
                                    
                                    if "food" in tags:
                                        sound_manager.play_sound(random.choice([f"consume_item{i}" for i in range(1, 7)]))
                                    elif any(tag in tags for tag in ["liquid", "consumable"]):
                                        sound_manager.play_sound(random.choice([f"consume_water{i}" for i in range(1, 5)]))
                
                throw_charge_start = None

            # Campfire UI drag handling
            if campfire_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_info = campfire.get_slot_at_mouse(mouse_pos, screen)
                    slot_index, slot_type = slot_info
                    
                    if hasattr(campfire, 'button_rect') and campfire.button_rect.collidepoint(mouse_pos):
                        campfire.toggle_fire()
                    elif slot_index is not None:
                        if campfire.dragging:
                            campfire.end_drag(slot_info)
                        else:
                            campfire.start_drag(slot_info)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if campfire.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_info = campfire.get_slot_at_mouse(mouse_pos, screen)
                        slot_index, slot_type = slot_info
                        if slot_index is not None:
                            campfire.end_drag(slot_info)
                        else:
                            campfire.cancel_drag()

            # Smelter UI drag handling
            if smelter_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_info = smelter.get_slot_at_mouse(mouse_pos, screen)
                    slot_index, slot_type = slot_info
                    
                    if hasattr(smelter, 'button_rect') and smelter.button_rect.collidepoint(mouse_pos):
                        smelter.toggle_fire()
                    elif slot_index is not None:
                        if smelter.dragging:
                            smelter.end_drag(slot_info)
                        else:
                            smelter.start_drag(slot_info)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if smelter.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_info = smelter.get_slot_at_mouse(mouse_pos, screen)
                        slot_index, slot_type = slot_info
                        if slot_index is not None:
                            smelter.end_drag(slot_info)
                        else:
                            smelter.cancel_drag()

            # Crafting bench drag handling
            if crafting_bench_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_index, is_hotbar = crafting_bench.get_slot_at_mouse(mouse_pos, screen)
                    if slot_index is not None:
                        if crafting_bench.dragging:
                            crafting_bench.end_drag(slot_index, is_hotbar)
                        else:
                            crafting_bench.start_drag(slot_index, is_hotbar)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if crafting_bench.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_index, is_hotbar = crafting_bench.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            crafting_bench.end_drag(slot_index, is_hotbar)
                        else:
                            crafting_bench.cancel_drag()

            # Arcane crafter drag handling (same as workbench for now)
            if arcane_crafter_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_info = arcane_crafter.get_slot_at_mouse(mouse_pos, screen)
                    slot_index, slot_type = slot_info
                    if slot_index is not None:
                        if arcane_crafter.dragging:
                            arcane_crafter.end_drag(slot_info)
                        else:
                            arcane_crafter.start_drag(slot_info)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if arcane_crafter.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_info = arcane_crafter.get_slot_at_mouse(mouse_pos, screen)
                        slot_index, slot_type = slot_info
                        if slot_index is not None:
                            arcane_crafter.end_drag(slot_info)
                        else:
                            arcane_crafter.cancel_drag()

            # Chest drag handling
            if chest_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_index, slot_type = chest_ui.get_slot_at_mouse(mouse_pos, screen)
                    if slot_index is not None:
                        if chest_ui.dragging:
                            chest_ui.end_drag(slot_index, slot_type)
                        else:
                            chest_ui.start_drag(slot_index, slot_type)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if chest_ui.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_index, slot_type = chest_ui.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            chest_ui.end_drag(slot_index, slot_type)
                        else:
                            chest_ui.cancel_drag()

            # Alchemy bench drag handling
            if alchemy_bench_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_index, is_hotbar = alchemy_bench.get_slot_at_mouse(mouse_pos, screen)
                    if slot_index is not None:
                        if alchemy_bench.dragging:
                            alchemy_bench.end_drag(slot_index, is_hotbar)
                        else:
                            alchemy_bench.start_drag(slot_index, is_hotbar)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if alchemy_bench.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_index, is_hotbar = alchemy_bench.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            alchemy_bench.end_drag(slot_index, is_hotbar)
                        else:
                            alchemy_bench.cancel_drag()

            # Mortar and Pestle drag handling
            if mortar_pestle_in_use:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_index, is_hotbar = mortar_pestle.get_slot_at_mouse(mouse_pos, screen)
                    if slot_index is not None:
                        if mortar_pestle.dragging:
                            mortar_pestle.end_drag(slot_index, is_hotbar)
                        else:
                            mortar_pestle.start_drag(slot_index, is_hotbar)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if mortar_pestle.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        slot_index, is_hotbar = mortar_pestle.get_slot_at_mouse(mouse_pos, screen)
                        if slot_index is not None:
                            mortar_pestle.end_drag(slot_index, is_hotbar)
                        else:
                            mortar_pestle.cancel_drag()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not smelter_in_use and not campfire_in_use and not crafting_bench_in_use and not arcane_crafter_in_use and not alchemy_bench_in_use and not chest_in_use and not mortar_pestle_in_use:
                mouse_pos = pygame.mouse.get_pos()

                slot_index, is_hotbar = inventory.get_slot_at_mouse(mouse_pos, screen)
                if is_hotbar and not placement_mode:
                    mouse_attack_blocked = True
                    mouse_attack_block_expires = pygame.time.get_ticks() + 200
                    inventory.handle_selection_click(mouse_pos, screen)
                    inventory.start_drag(slot_index, is_hotbar)

                elif inventory_in_use and player.is_alive:
                    if inventory.state == "crafting":
                        import time
                        crafting_time = time.time()
                        inventory.handle_crafting_click(mouse_pos, crafting_time)
                    else:
                        if slot_index is not None:
                            mouse_attack_blocked = True
                            mouse_attack_block_expires = pygame.time.get_ticks() + 200
                        inventory.handle_selection_click(mouse_pos, screen)
                        if slot_index is not None:
                            allow_drag = is_hotbar or inventory.state == "inventory"
                            if allow_drag:
                                inventory.start_drag(slot_index, is_hotbar)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not smelter_in_use and not campfire_in_use and not crafting_bench_in_use and not alchemy_bench_in_use and not chest_in_use and not mortar_pestle_in_use:
                mouse_attack_blocked = False
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
                scroll_target = None
                if crafting_bench_in_use:
                    scroll_target = crafting_bench
                elif arcane_crafter_in_use:
                    scroll_target = arcane_crafter
                elif alchemy_bench_in_use:
                    scroll_target = alchemy_bench
                elif mortar_pestle_in_use:
                    scroll_target = mortar_pestle

                if scroll_target is not None:
                    if event.button == 4:
                        scroll_target.handle_mouse_scroll(1)
                    else:
                        scroll_target.handle_mouse_scroll(-1)
                elif not placement_mode:
                    if event.button == 4:
                        inventory.selected_hotbar_slot = (inventory.selected_hotbar_slot - 1) % inventory.hotbar_size
                    elif event.button == 5:
                        inventory.selected_hotbar_slot = (inventory.selected_hotbar_slot + 1) % inventory.hotbar_size
                    inventory.selection_mode = "hotbar"
                    inventory.show_selected_hotbar_name()

            if tent_menu_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                menu_rect = pygame.Rect(width // 2 - 180, height // 2 - 90, 360, 180)
                option = get_tent_menu_option(event.pos, menu_rect)
                if option == "sleep":
                    if time_of_day >= 18 or time_of_day < 6:
                        sleeping_in_tent = True
                        tent_hide_active = False
                        time_speed_multiplier = 30.0
                        sleeping_tent_x = tent_menu_tent['x']
                        sleeping_tent_y = tent_menu_tent['y']
                        sprite_size = tent_menu_tent.get('sprite_size', default_placeable_sprite_size)
                        sleeping_tent_height = sprite_size[1] if sprite_size else default_placeable_sprite_size[1]
                        tent_menu_active = False
                        tent_menu_tent = None
                        tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
                elif option == "hide":
                    tent_hide_active = True
                    sleeping_tent_x = tent_menu_tent['x']
                    sleeping_tent_y = tent_menu_tent['y']
                    sprite_size = tent_menu_tent.get('sprite_size', default_placeable_sprite_size)
                    sleeping_tent_height = sprite_size[1] if sprite_size else default_placeable_sprite_size[1]
                    time_speed_multiplier = 1.0
                    tent_menu_active = False
                    tent_menu_tent = None
                    tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
                elif option == "pickup":
                    if tent_hover_timers.get("pickup", 0.0) >= tent_hold_threshold:
                        if tent_menu_tent in placed_structures:
                            placed_structures.remove(tent_menu_tent)
                        inventory.add(["Tent"])
                        tent_menu_active = False
                        tent_menu_tent = None
                        tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
                elif option == "demolish":
                    if tent_hover_timers.get("demolish", 0.0) >= tent_hold_threshold:
                        if tent_menu_tent in placed_structures:
                            placed_structures.remove(tent_menu_tent)
                        tent_menu_active = False
                        tent_menu_tent = None
                        tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
                elif option == "fast_travel":
                    fast_travel_menu_active = True
                    tent_menu_active = False
                elif option == "cancel":
                    tent_menu_active = False
                    tent_menu_tent = None
                    tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
                continue

            if fast_travel_menu_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                box_rect = pygame.Rect(width // 2 - 210, height // 2 - 110, 420, 220)
                close_rect = pygame.Rect(box_rect.x + box_rect.width//2 - 60, box_rect.y + box_rect.height - 60, 120, 34)
                if close_rect.collidepoint(event.pos):
                    fast_travel_menu_active = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                if crafting_bench_in_use:
                    mouse_pos = pygame.mouse.get_pos()
                    crafting_bench.handle_mouse_click(mouse_pos, event.button, screen)
                elif arcane_crafter_in_use:
                    mouse_pos = pygame.mouse.get_pos()
                    arcane_crafter.handle_mouse_click(mouse_pos, event.button, screen)
                elif alchemy_bench_in_use:
                    mouse_pos = pygame.mouse.get_pos()
                    alchemy_bench.handle_mouse_click(mouse_pos, event.button, screen)
                elif mortar_pestle_in_use:
                    mouse_pos = pygame.mouse.get_pos()
                    mortar_pestle.handle_mouse_click(mouse_pos, event.button, screen)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if crafting_bench_in_use:
                    crafting_bench.close()
                    crafting_bench_in_use = False
                elif arcane_crafter_in_use:
                    arcane_crafter.close()
                    arcane_crafter_in_use = False
                elif campfire_in_use:
                    campfire.close()
                    campfire_in_use = False
                elif smelter_in_use:
                    smelter.close()
                    smelter_in_use = False
                elif mortar_pestle_in_use:
                    mortar_pestle.close()
                    mortar_pestle_in_use = False
                elif alchemy_bench_in_use:
                    alchemy_bench.close()
                    alchemy_bench_in_use = False
                elif chest_in_use:
                    chest_ui.close()
                    chest_in_use = False
                elif fast_travel_menu_active:
                    fast_travel_menu_active = False
                elif tent_menu_active:
                    tent_menu_active = False
                    tent_menu_tent = None
                else:
                    for structure in nearby_structures:
                        if structure['item_name'] == 'Workbench':
                            struct_collision = structure['rect']
                            horizontal_dist = abs(struct_collision.centerx - player_world_x)
                            vertical_dist = abs(struct_collision.centery - player_world_y)
                            workbench_reach = 20
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
                    
                    if not crafting_bench_in_use and not arcane_crafter_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Arcane Crafter':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                reach = 20
                                horizontal_range = (struct_collision.width / 2) + reach
                                vertical_range = (struct_collision.height / 2) + reach
                                
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
                                    arcane_crafter.open((structure['x'], structure['y']))
                                    arcane_crafter_in_use = True
                                    break
                    
                    if not crafting_bench_in_use and not arcane_crafter_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Smelter':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                smelter_reach = 20
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
                    
                    if not crafting_bench_in_use and not smelter_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Campfire':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                campfire_reach = 20
                                horizontal_range = (struct_collision.width / 2) + campfire_reach
                                vertical_range = (struct_collision.height / 2) + campfire_reach
                                
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
                                    campfire.open((structure['x'], structure['y']))
                                    campfire_in_use = True
                                    break

                    if not crafting_bench_in_use and not smelter_in_use and not campfire_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Mortar And Pestle':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                mortar_pestle_reach = 20
                                horizontal_range = (struct_collision.width / 2) + mortar_pestle_reach
                                vertical_range = (struct_collision.height / 2) + mortar_pestle_reach
                                
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
                                    mortar_pestle.open((structure['x'], structure['y']))
                                    mortar_pestle_in_use = True
                                    break

                    if not crafting_bench_in_use and not smelter_in_use and not campfire_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Alchemy Bench':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                alchemy_reach = 20
                                horizontal_range = (struct_collision.width / 2) + alchemy_reach
                                vertical_range = (struct_collision.height / 2) + alchemy_reach

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
                                    alchemy_bench.open((structure['x'], structure['y']))
                                    alchemy_bench_in_use = True
                                    break

                    if not crafting_bench_in_use and not smelter_in_use and not campfire_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use:
                        for structure in nearby_structures:
                            if structure['item_name'] == 'Chest':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                chest_reach = 20
                                horizontal_range = (struct_collision.width / 2) + chest_reach
                                vertical_range = (struct_collision.height / 2) + chest_reach

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
                                    chest_ui.open(structure)
                                    chest_in_use = True
                                    break
                    
                    if not crafting_bench_in_use and not smelter_in_use and not campfire_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use:
                        for structure in nearby_structures:
                            if structure.get('item_name') == 'Tent':
                                struct_collision = structure['rect']
                                horizontal_dist = abs(struct_collision.centerx - player_world_x)
                                vertical_dist = abs(struct_collision.centery - player_world_y)
                                tent_reach = 50
                                horizontal_range = (struct_collision.width / 2) + tent_reach
                                vertical_range = (struct_collision.height / 2) + tent_reach
                                
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
                                    tent_menu_active = True
                                    tent_menu_tent = structure
                                    tent_hover_timers = {"pickup": 0.0, "demolish": 0.0}
                                    break
                    
                if not crafting_bench_in_use and not tent_menu_active and not fast_travel_menu_active and not sleeping_in_tent and not tent_hide_active:
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
                        if player.swimming and player.current_liquid == obj:
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
    
        mouse_pos = pygame.mouse.get_pos()
        hotbar_rect = pygame.Rect(width/2 - 257, height - 70, 514, 55)
        mouse_over_hotbar = hotbar_rect.collidepoint(mouse_pos) if hotbar_rect else False
        
        if not paused and not inventory_in_use and not smelter_in_use and not campfire_in_use and not crafting_bench_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use and naming_cat is None and pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not mouse_over_hotbar:
            if current_time - harvest_cooldown > harvest_delay:
                held_item = get_selected_hotbar_item()
                base_attack_val = int(round(player.damage + (player.strength_leveler - 1) * player.strength_level_gain))
                player.attack = compute_weapon_attack(base_attack_val, held_item)
                has_pickaxe_equipped = is_pickaxe_item(held_item)
                has_shovel_equipped = is_shovel_item(held_item)
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
                            from world import GemstoneRock, MetalOreRock, MetalVeinRock, GoldOreRock, GoldVeinRock
                            is_gemstone_rock = isinstance(obj, GemstoneRock)
                            is_ore_or_vein = isinstance(obj, (MetalOreRock, MetalVeinRock, GoldOreRock, GoldVeinRock))
                            is_bank = isinstance(obj, Bank)
                            if (getattr(obj, "resource", None) == "Stone" or is_gemstone_rock or is_ore_or_vein) and not has_pickaxe_equipped:
                                need_pickaxe_message_timer = 1.5
                                continue
                            if is_bank and not has_shovel_equipped:
                                need_shovel_message_timer = 1.5
                                continue
                            current_tool_resource = getattr(obj, "resource", None)
                            if is_gemstone_rock or is_ore_or_vein:
                                current_tool_resource = "Stone"
                            harvest_power = get_harvest_power(held_item, current_tool_resource)
                            special_chance_mult = get_special_drop_multiplier(held_item)
                            special_yield_mult = get_special_yield_multiplier(held_item)
                            resource = obj.harvest(player, harvest_power, special_chance_mult, special_yield_mult)
                            
                            if is_gemstone_rock or is_ore_or_vein:
                                sound_manager.play_sound(random.choice([f"harvest_stone{i}" for i in range(1, 7)]))
                                inventory.decrement_durability(inventory.selected_hotbar_slot, True, 1)
                            
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
                                
                                if not is_gemstone_rock and not is_ore_or_vein:
                                    inventory.decrement_durability(inventory.selected_hotbar_slot, True, 1)
                            
                            if obj.destroyed:
                                visible_objects.remove(obj)
                                
                            harvest_cooldown = current_time
                            break
                    
        base_throw_attack = int(round(player.damage + (player.strength_leveler - 1) * player.strength_level_gain))
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
                collision_objects = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants + ponds + lavas + banks
                collision_mobs = cats + squirrels + cows + chickens + crawlers + ashhounds + pocks + deers + black_bears + brown_bears + gilas + crows + glowbirds + duskwretches
                
                for obj in collision_objects:
                    obj_rect = obj.get_collision_rect(0) if hasattr(obj, 'get_collision_rect') else obj.rect
                    if item_rect.colliderect(obj_rect):
                        collision_detected = True
                        break
                
                # Check for collisions with mobs
                removed_due_to_hit = False
                if not collision_detected:
                    for mob in collision_mobs:
                        if item_rect.colliderect(mob.rect):
                            if thrown.get("is_cat"):
                                # Thrown cats deal damage using player base attack
                                # (no weapon) plus the cat's own base attack, and
                                # count as an attack on this mob.
                                # Avoid harming tamed cats.
                                from mobs import Cat  # local import to avoid cycles
                                if not (isinstance(mob, Cat) and getattr(mob, "tamed", False)):
                                    cat_data = thrown.get("cat_data") or {}
                                    cat_obj = cat_data.get("cat_object")
                                    if cat_obj is not None:
                                        cat_attack = getattr(cat_obj, "attack", 0)
                                    else:
                                        cat_level = cat_data.get("cat_level", 1)
                                        cat_attack = max(5, int(cat_level * 4))
                                    damage = max(0, int(base_throw_attack + cat_attack))
                                    if damage > 0:
                                        mob.health = max(0, mob.health - damage)
                                        # Let mob AI and other cats treat this
                                        # as a player attack on this target.
                                        setattr(player, "attacking_target", mob)
                                # Cat still "lands" via the landing logic below.
                            else:
                                handle_thrown_hit(thrown, mob, base_throw_attack)
                                if thrown in thrown_items:
                                    thrown_items.remove(thrown)
                                removed_due_to_hit = True
                            collision_detected = True
                            break
                if removed_due_to_hit:
                    continue
                
                # Check if item has traveled its max distance or hit an object
                if thrown["distance_traveled"] >= thrown["max_distance"] or collision_detected:
                    # Item has landed - keep current position (don't use next_x, next_y to stay before collision)
                    thrown["landed"] = True
                    
                    # If it's a cat, add it back to the world
                    if thrown["is_cat"]:
                        cat_data = thrown["cat_data"]
                        if cat_data:
                            cat_obj = cat_data.get("cat_object")
                            if cat_obj is None:
                                cat_obj = build_cat_from_item(cat_data, int(thrown["x"]), int(thrown["y"]))
                                cat_data["cat_object"] = cat_obj
                            if cat_obj:
                                cat_obj.rect.centerx = int(thrown["x"])
                                cat_obj.rect.centery = int(thrown["y"])
                                cat_obj.destroyed = False
                                cat_obj.placement_time = pygame.time.get_ticks()
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
                    
        dead_bushes[:] = [db for db in dead_bushes if not db.destroyed]
        mushrooms[:] = [m for m in mushrooms if not m.destroyed]
        savannah_grasses[:] = [sgrass for sgrass in savannah_grasses if not sgrass.destroyed]
        grasses[:] = [grass for grass in grasses if not grass.destroyed]
        stones[:] = [stone for stone in stones if not stone.destroyed]
        sticks[:] = [s for s in sticks if not s.destroyed]
        dropped_items[:] = [d for d in dropped_items if not d.destroyed]
        rocks[:] = [r for r in rocks if not r.destroyed]
        trees[:] = [t for t in trees if not t.destroyed]
        boulders[:] = [b for b in boulders if not b.destroyed]
        berry_bushes[:] = [bush for bush in berry_bushes if not bush.destroyed]
        ferns[:] = [f for f in ferns if not f.destroyed]
        fruit_plants[:] = [fp for fp in fruit_plants if not fp.destroyed]
        ponds[:] = [pond for pond in ponds if not pond.destroyed]
        lavas[:] = [lava for lava in lavas if not lava.destroyed]
        banks[:] = [bank for bank in banks if not bank.destroyed]

        cats[:] = [cat for cat in cats if not cat.destroyed]
        squirrels[:] = [squirrel for squirrel in squirrels if not squirrel.destroyed]
        cows[:] = [cow for cow in cows if not cow.destroyed]
        chickens[:] = [chicken for chicken in chickens if not chicken.destroyed]
        crawlers[:] = [crawler for crawler in crawlers if not crawler.destroyed]
        ashhounds[:] = [ashhound for ashhound in ashhounds if not ashhound.destroyed]
        duskwretches[:] = [duskwretch for duskwretch in duskwretches if not duskwretch.destroyed]
        pocks[:] = [pock for pock in pocks if not pock.destroyed]
        deers[:] = [deer for deer in deers if not deer.destroyed]
        black_bears[:] = [black_bear for black_bear in black_bears if not black_bear.destroyed]
        brown_bears[:] = [brown_bear for brown_bear in brown_bears if not brown_bear.destroyed]
        gilas[:] = [gila for gila in gilas if not gila.destroyed]
        crows[:] = [crow for crow in crows if not crow.destroyed]
        glowbirds[:] = [glowbird for glowbird in glowbirds if not glowbird.destroyed]
        fire_dragons[:] = [dragon for dragon in fire_dragons if not dragon.destroyed]
        ice_dragons[:] = [dragon for dragon in ice_dragons if not dragon.destroyed]
        electric_dragons[:] = [dragon for dragon in electric_dragons if not dragon.destroyed]
        poison_dragons[:] = [dragon for dragon in poison_dragons if not dragon.destroyed]
        dusk_dragons[:] = [dragon for dragon in dusk_dragons if not dragon.destroyed]

        for tile_x, tile_image in tiles:
            screen_x = tile_x - cam_x
            if -BACKGROUND_SIZE < screen_x < width:
                screen.blit(tile_image, (screen_x, floor_y))

        keys = pygame.key.get_pressed()

        rocks[:] = [rock for rock in rocks if not rock.destroyed]
        boulders[:] = [boulder for boulder in boulders if not boulder.destroyed]
        trees[:] = [tree for tree in trees if not tree.destroyed]
        berry_bushes[:] = [bush for bush in berry_bushes if not bush.destroyed]
        dead_bushes[:] = [bush for bush in dead_bushes if not bush.destroyed]
        ferns[:] = [fern for fern in ferns if not fern.destroyed]
        fruit_plants[:] = [plant for plant in fruit_plants if not plant.destroyed]
        gemstone_rocks[:] = [gr for gr in gemstone_rocks if not gr.destroyed]
        metal_ore_rocks[:] = [ore for ore in metal_ore_rocks if not ore.destroyed]
        metal_vein_rocks[:] = [vein for vein in metal_vein_rocks if not vein.destroyed]
        gold_ore_rocks[:] = [ore for ore in gold_ore_rocks if not ore.destroyed]
        gold_vein_rocks[:] = [vein for vein in gold_vein_rocks if not vein.destroyed]
        
        collectibles = sticks + stones + grasses + savannah_grasses + mushrooms + dropped_items + marsh_reeds
        all_objects_no_liquids = rocks + trees + boulders + gemstone_rocks + metal_ore_rocks + metal_vein_rocks + gold_ore_rocks + gold_vein_rocks + berry_bushes + dead_bushes + ferns + fruit_plants + banks
        all_objects = all_objects_no_liquids + ponds + lavas
        mobs = cats + squirrels + cows + chickens + crawlers + ashhounds + duskwretches + pocks + deers + black_bears + brown_bears + gilas + crows + glowbirds + fire_dragons + ice_dragons + electric_dragons + poison_dragons + dusk_dragons
        all_mobs = mobs

        visibility_cam_x = sleeping_tent_x if (sleeping_in_tent or tent_hide_active) else cam_x
        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -256 and col.rect.x - cam_x < width + 256]
        visible_liquids = [obj for obj in (ponds + lavas) if obj.rect.x - cam_x > -256 and obj.rect.x - cam_x < width + 256 and obj.rect.y > -256 and obj.rect.y < height + 256]
        visible_objects = [obj for obj in all_objects_no_liquids if obj.rect.x - cam_x > -256 and obj.rect.x - cam_x < width + 256 and obj.rect.y > -256 and obj.rect.y < height + 256]
        visible_mobs = [mob for mob in mobs if mob.rect.x - visibility_cam_x > -256 and mob.rect.x - visibility_cam_x < width + 256 and mob.rect.y > -256 and mob.rect.y < height + 256]

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
            elif isinstance(mob, (Crow, Glowbird)) and random.random() < 0.001:
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
                def get_held_frame(image_entry, item_data):
                    """Return the current frame for a held item (supports animated lists)."""
                    if isinstance(image_entry, list):
                        valid_frames = [frame for frame in image_entry if frame]
                        if not valid_frames:
                            return None
                        frame_duration = max(0.01, item_data.get("held_item_frame_duration", 0.12))
                        frame_idx = int(pygame.time.get_ticks() / (frame_duration * 1000)) % len(valid_frames)
                        return valid_frames[frame_idx]
                    return image_entry

                for item in items_list:
                    if item["item_name"] == current_hotbar_slot["item_name"] and "held_item_images" in item:
                        # disable attacking while smelter UI is open
                        is_attacking = pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not smelter_in_use and not campfire_in_use and not mouse_over_hotbar
                        held_image = get_held_frame(item["held_item_images"].get(player.last_direction), item)
                        
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
                            
                            base_anchor_y = player_pos.y - size + 20
                            held_x = player_pos.x - size/2 + swing_offset[0]
                            held_y = base_anchor_y + swing_offset[1]
                            
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
                            
                            base_anchor_y = player_pos.y - size + 20
                            held_x = player_pos.x - size/2 + offset[0]
                            held_y = base_anchor_y + offset[1]
                            
                            if player.last_direction == "left":
                                held_image = pygame.transform.flip(held_image, True, False)
                            
                            scale_factor = 0.65
                            scaled_size = (int(held_image.get_width() * scale_factor), int(held_image.get_height() * scale_factor))
                            held_image = pygame.transform.scale(held_image, scaled_size)
                            
                            if movement_rotation != 0:
                                held_image = pygame.transform.rotate(held_image, movement_rotation)
                            
                            screen.blit(held_image, (held_x, held_y))
                        break

        def draw_shadow_for_obj(obj):
            rect = None
            if isinstance(obj, dict) and 'rect' in obj:
                rect = obj['rect']
            elif hasattr(obj, 'rect'):
                rect = obj.rect
            if rect is None:
                return
            # Skip drawing shadow for destroyed objects
            if hasattr(obj, 'destroyed') and obj.destroyed:
                return
            is_player_obj = obj is player
            name = getattr(obj, "__class__", type("x", (), {})).__name__ if not isinstance(obj, dict) else obj.get("item_name", "")
            alpha = 40
            width_mult = 0.8
            height_mult = 0.25
            y_offset = 0
            # Tweak by type
            if name == "SavannahGrass":
                width_mult = 0.55
                height_mult = 0.25
            elif name in ("Grass", "Stick", "DroppedItem", "Mushroom", "MarshReed"):
                width_mult = 0.4
                height_mult = 0.2
            elif name == "Torch":
                y_offset = rect.height * 0.05
            if name in ("Rock", "RedrockRock", "SnowyRock", "MetalOreRock", "MetalVeinRock", "GoldOreRock", "GoldVeinRock", "GemstoneRock"):
                y_offset = 0
            if name in ("Boulder","RedrockBoulder", "SnowyBoulder"):
                y_offset = -25
            if name in ("Squirrel",):
                width_mult = 0.45
                height_mult = 0.18
            if hasattr(obj, "resource") and getattr(obj, "resource", "") == "Willow Wood":
                y_offset = -rect.height * 0.08
            if name in ("Crow", "Glowbird", "Bird", "Duck"):
                width_mult = 0.35
                height_mult = 0.18
            if is_player_obj:
                y_offset += rect.height * 0.16
            shadow_width = max(8, int(rect.width * width_mult))
            shadow_height = max(4, int(rect.height * height_mult))
            shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, alpha), shadow_surface.get_rect())
            # Player rect is in screen space; other objects need camera offset applied.
            shadow_x = rect.centerx - shadow_width // 2
            if not is_player_obj:
                shadow_x -= cam_x
            screen.blit(shadow_surface, (shadow_x, rect.bottom - shadow_height // 2 + y_offset))

        def get_tent_menu_option(mouse_pos, rect):
            if not rect.collidepoint(mouse_pos):
                return None
            rel_x = mouse_pos[0] - rect.x
            rel_y = mouse_pos[1] - rect.y
            col = int(rel_x / (rect.width / 3))
            row = int(rel_y / (rect.height / 2))
            col = max(0, min(2, col))
            row = max(0, min(1, row))
            options = [
                ["sleep", "hide", "pickup"],
                ["fast_travel", "demolish", "cancel"],
            ]
            return options[row][col]

        def draw_tent_menu(screen, dt_local):
            global tent_hover_timers, tent_hover_highlight_surface, tent_hover_highlight_rect, current_tent_hover_option
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            menu_w, menu_h = 360, 180
            menu_x = width // 2 - menu_w // 2
            menu_y = height // 2 - menu_h // 2
            rect = pygame.Rect(menu_x, menu_y, menu_w, menu_h)
            pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=8)
            pygame.draw.rect(screen, (200, 200, 220), rect, 2, border_radius=8)
            # grid lines
            pygame.draw.line(screen, (120, 120, 140), (menu_x + menu_w // 3, menu_y), (menu_x + menu_w // 3, menu_y + menu_h), 2)
            pygame.draw.line(screen, (120, 120, 140), (menu_x + 2 * menu_w // 3, menu_y), (menu_x + 2 * menu_w // 3, menu_y + menu_h), 2)
            pygame.draw.line(screen, (120, 120, 140), (menu_x, menu_y + menu_h // 2), (menu_x + menu_w, menu_y + menu_h // 2), 2)

            options_grid = [
                ["sleep", "hide", "pickup"],
                ["fast_travel", "demolish", "cancel"],
            ]
            option_rects = {}
            for row in range(2):
                for col in range(3):
                    cell_rect = pygame.Rect(
                        menu_x + col * (menu_w // 3),
                        menu_y + row * (menu_h // 2),
                        menu_w // 3,
                        menu_h // 2,
                    )
                    option_rects[options_grid[row][col]] = cell_rect

            labels = {
                "sleep": "Sleep",
                "hide": "Hide",
                "pickup": "Pick Up",
                "fast_travel": "Fast Travel",
                "demolish": "Demolish",
                "cancel": "Cancel",
            }
            mouse_pos = pygame.mouse.get_pos()
            hovered_option = get_tent_menu_option(mouse_pos, rect)

            if hovered_option != current_tent_hover_option:
                current_tent_hover_option = hovered_option
                if hovered_option:
                    highlight_rect = option_rects.get(hovered_option)
                    if highlight_rect:
                        tent_hover_highlight_surface = pygame.Surface(highlight_rect.size, pygame.SRCALPHA)
                        tent_hover_highlight_surface.fill((255, 255, 255, 50))
                        tent_hover_highlight_rect = highlight_rect.copy()
                    else:
                        tent_hover_highlight_surface = None
                        tent_hover_highlight_rect = None
                else:
                    tent_hover_highlight_surface = None
                    tent_hover_highlight_rect = None

            for key in tent_hover_timers.keys():
                if hovered_option != key:
                    tent_hover_timers[key] = 0.0

            for row in range(2):
                for col in range(3):
                    option = options_grid[row][col]
                    cell_rect = option_rects[option]
                    if option == current_tent_hover_option and tent_hover_highlight_surface and tent_hover_highlight_rect:
                        screen.blit(tent_hover_highlight_surface, cell_rect.topleft)
                        if option in tent_hover_timers:
                            tent_hover_timers[option] += dt_local
                    text_surface = pygame.font.Font(font_path, 18).render(labels[option], True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    screen.blit(text_surface, text_rect)
                    if option in ("pickup", "demolish"):
                        progress = min(1.0, tent_hover_timers.get(option, 0.0) / tent_hold_threshold)
                        bar_w = cell_rect.width * 0.6
                        bar_h = 6
                        bar_x = cell_rect.centerx - bar_w / 2
                        bar_y = cell_rect.bottom - 16
                        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
                        pygame.draw.rect(screen, (200, 120, 40), (bar_x, bar_y, bar_w * progress, bar_h))

            return rect

        def draw_fast_travel_placeholder(screen):
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            box_w, box_h = 420, 220
            box_x = width // 2 - box_w // 2
            box_y = height // 2 - box_h // 2
            box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
            pygame.draw.rect(screen, (30, 40, 60), box_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 220), box_rect, 2, border_radius=10)
            title = pygame.font.Font(font_path, 22).render("Fast Travel (Coming Soon)", True, (255, 255, 255))
            body = pygame.font.Font(font_path, 18).render("Fast travel destinations will appear here.", True, (220, 220, 220))
            button_rect = pygame.Rect(box_x + box_w//2 - 60, box_y + box_h - 60, 120, 34)
            pygame.draw.rect(screen, (80, 120, 180), button_rect, border_radius=6)
            pygame.draw.rect(screen, (220, 220, 240), button_rect, 1, border_radius=6)
            button_text = pygame.font.Font(font_path, 18).render("Close", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(box_rect.centerx, box_y + 50)))
            screen.blit(body, body.get_rect(center=(box_rect.centerx, box_y + 95)))
            screen.blit(button_text, button_text.get_rect(center=button_rect.center))
            return button_rect

        for obj in visible_objects:
            # Handle both regular objects with rect and placed structures (dictionaries)
            if isinstance(obj, dict) and 'y' in obj:
                object_mid_y = obj['y']
            else:
                object_mid_y = obj.rect.y + obj.rect.height / 2

            if not player_drawn and (player.rect.centery + 20) <= object_mid_y and not (sleeping_in_tent or tent_hide_active):
                # Draw axe first for left/up directions (behind the player)
                if player.last_direction in ["left", "up"]:
                    draw_held_item()

                # Draw player (with shadow)
                draw_shadow_for_obj(player)
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
                    screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size + 20))

                # Draw axe after for right/down directions (in front of the player)
                if player.last_direction in ["right", "down"]:
                    draw_held_item()

                player_drawn = True

            draw_shadow_for_obj(obj)

            # Handle drawing of placed structures (dictionaries)
            if isinstance(obj, dict) and 'item_name' in obj:
                # Draw placed structure
                struct_sprite = None
                sprite_width, sprite_height = obj.get('sprite_size', default_placeable_sprite_size)
                if obj.get('item_name') == 'Smelter' and smelter is not None:
                    lit_sprite = smelter.get_world_sprite((sprite_width, sprite_height))
                    if lit_sprite:
                        struct_sprite = lit_sprite
                if obj.get('item_name') == 'Campfire' and campfire is not None:
                    cf_sprite = campfire.get_world_sprite((sprite_width, sprite_height))
                    if cf_sprite:
                        struct_sprite = cf_sprite
                if obj.get('item_name') == 'Torch':
                    key = ('Torch', sprite_width, sprite_height)
                    if key not in placeable_animation_cache:
                        frames = []
                        for i in range(1, 5):
                            try:
                                frame = pygame.image.load(f"assets/sprites/itemFrames/Torch{i}.png").convert_alpha()
                                frame = pygame.transform.scale(frame, (sprite_width, sprite_height))
                                frames.append(frame)
                            except:
                                continue
                        placeable_animation_cache[key] = frames
                    frames = placeable_animation_cache.get(key, [])
                    if frames:
                        elapsed = pygame.time.get_ticks() - obj.get('placed_time', 0)
                        frame_idx = int(elapsed / 150) % len(frames)
                        struct_sprite = frames[frame_idx]
                try:
                    if struct_sprite is None:
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
        
        if not player_drawn and not (sleeping_in_tent or tent_hide_active):
            if player.last_direction in ["left", "up"]:
                draw_held_item()

            draw_shadow_for_obj(player)
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

        mob_reference_x = sleeping_tent_x if (sleeping_in_tent or tent_hide_active) else player_pos.x + cam_x
        mob_reference_radius = 10000 if (sleeping_in_tent or tent_hide_active) else 3000
        nearby_mobs = [mob for mob in mobs
                    if abs(mob.rect.x - mob_reference_x) < mob_reference_radius
                    and abs(mob.rect.y - player_pos.y) < 800]

        def lerp(a, b, t):
            """Linear interpolation between a and b for t in [0,1]."""
            return a + (b - a) * max(0, min(1, t))

        def get_light_mask(radius, max_alpha, tint_color=(0, 0, 0)):
            """Return a cached radial gradient mask used to subtract darkness."""
            key = (radius, max_alpha, tint_color)
            if key in light_mask_cache:
                return light_mask_cache[key]

            size = radius * 4
            surf = pygame.Surface((size, size), pygame.SRCALPHA)

            center = (size // 2, size // 2)

            ring_radii = [1.65, 1.6, 1.55, 1.5, 1.45, 1.4, 1.35, 1.3, 1.25, 1.2]
            ring_alphas = [0.03, 0.07, 0.11, 0.16, 0.22, 0.32, 0.5, 0.7, 0.85, .95]

            for r_scale, a_scale in zip(ring_radii, ring_alphas):
                r = max(1, int(radius * r_scale))
                alpha = int(max_alpha * a_scale)
                pygame.draw.circle(surf, (tint_color[0], tint_color[1], tint_color[2], alpha), center, r)

            light_mask_cache[key] = surf
            return surf


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

        # Draw overlay with local light falloff
        day_night_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        day_night_overlay.fill((R_value, G_value, B_value, A_value))

        if A_value > 0:
            lights = []
            # Placed torches
            for struct in placed_structures:
                if struct.get("item_name") == "Torch":
                    lights.append((struct["x"] - cam_x, struct["y"], 220, None))
                elif struct.get("item_name") == "Campfire" and campfire and getattr(campfire, "fire_lit", False):
                    lights.append((struct["x"] - cam_x, struct["y"], 260, None))
                elif struct.get("item_name") == "Smelter" and smelter and getattr(smelter, "fire_lit", False):
                    lights.append((struct["x"] - cam_x, struct["y"], 260, None))
            # Held torch (player light)
            player_torch = None
            sel_slot = inventory.selected_hotbar_slot
            if 0 <= sel_slot < len(inventory.hotbar_slots):
                player_torch = inventory.hotbar_slots[sel_slot]
            if player_torch and player_torch.get("item_name") == "Torch":
                lights.append((player_pos.x, player_pos.y, 220, None))
            # Lava pools give off strong light
            for lava in lavas:
                if getattr(lava, "destroyed", False):
                    continue
                lights.append((lava.rect.centerx - cam_x, lava.rect.centery, 320, (25, 10, 0)))
            # Fire ferns glow softly
            for fern in ferns:
                if getattr(fern, "destroyed", False):
                    continue
                if getattr(fern, "biome", "") == "lavastone":
                    lights.append((fern.rect.centerx - cam_x, fern.rect.centery, 140, (40, 15, 0)))
            # Glowbirds emit a smaller, cool-tinted light
            for glowbird in glowbirds:
                if getattr(glowbird, "is_alive", False) and not getattr(glowbird, "destroyed", False):
                    lights.append(
                        (
                            glowbird.rect.centerx - cam_x,
                            glowbird.rect.centery,
                            getattr(glowbird, "light_radius", 110),
                            getattr(glowbird, "light_tint", (10, 40, 120)),
                        )
                    )

            for lx, ly, radius, tint_override in lights:
                flicker_seed = int(lx * 1000 + ly * 1000 + light_flicker_timer * 10)
                random.seed(flicker_seed)
                
                radius_flicker = random.uniform(-3, 3)
                flickered_radius = int(radius + radius_flicker)
                
                tint_choice = tint_override if tint_override is not None else random.choice([
                    (0, 0, 0),
                    (5, 3, 0),
                    (3, 2, 0),
                    (4, 1, 0)
                ])
                
                mask = get_light_mask(flickered_radius, A_value, tint_choice)
                mask_rect = mask.get_rect(center=(int(lx), int(ly)))
                day_night_overlay.blit(mask, mask_rect.topleft, special_flags=pygame.BLEND_RGBA_SUB)
                
                random.seed()

        screen.blit(day_night_overlay, (0, 0))


        inventory.draw_hotbar(screen)


        if not paused and not inventory_in_use and not smelter_in_use and not campfire_in_use and not crafting_bench_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use and not tent_menu_active and not fast_travel_menu_active and not tent_hide_active and player.dead == False:

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
                bush.update(time_dt)
            
            for tree in trees:
                tree.update(time_dt)
            
            for plant in fruit_plants:
                plant.update(time_dt)

            # Expose player's world position on the player object so that
            # follower pets (like tamed cats) can use consistent coordinates.
            player.world_x = player_world_x
            player.world_y = player_world_y

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
                    # Pick nearest target between player and any tamed cats
                    potential_targets = [
                        (player_world_x, player_world_y, player)
                    ]
                    for cat in cats:
                        if getattr(cat, "tamed", False) and not getattr(cat, "destroyed", False) and getattr(cat, "is_alive", True):
                            potential_targets.append((cat.rect.centerx, cat.rect.centery, cat))
                    target_world_x, target_world_y, target_entity = min(
                        potential_targets,
                        key=lambda t: (t[0] - mob.rect.centerx) ** 2 + (t[1] - mob.rect.centery) ** 2
                    )

                    mob.handle_player_proximity(dt, target_world_x, target_world_y, target_entity,
                                                nearby_objects=None, nearby_mobs=None)
                    mob.attack(target_world_x, target_world_y, target_entity)

                    
            
                # Pass the real player object so pets (like tamed cats)
                # can follow and assist the player correctly.
                mob.update(time_dt, player, mob_nearby_objects, mob_nearby_mobs, sleeping_in_tent or tent_hide_active)
                mob.keep_in_screen(height)
            if sleeping_in_tent or tent_hide_active:
                player_world_x = sleeping_tent_x
                player_world_y = player_pos.y
            else:
                player_world_x = player_pos.x + cam_x
                player_world_y = player_pos.y
            player.attacking(nearby_mobs, player_world_x, player_world_y, mouse_over_hotbar)
            for mob in nearby_mobs:
                mob.handle_health(screen, cam_x, dt, sleeping_in_tent or tent_hide_active)
                mob.handle_lava_damage(dt)
                mob.flee(player_world_x, player_world_y, dt, sleeping_in_tent or tent_hide_active)
                
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

            if not inventory_in_use and not smelter_in_use and not campfire_in_use and not crafting_bench_in_use and not mortar_pestle_in_use and not alchemy_bench_in_use and not chest_in_use and naming_cat is None:

                if (((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])) or (pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not mouse_over_hotbar)) and not player.exhausted:
                    if player.lose_stamina(screen, dt):
                        stamina_depleted_message_timer = 2.0
                    player.stamina_speed()

                is_moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
                is_running = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and is_moving
                
                if is_moving:
                    base_delay = 0.4
                    
                    actual_speed = player_speed * shift_multiplier
                    base_speed = player.base_speed * player.speed
                    speed_ratio = actual_speed / base_speed if base_speed > 0 else 0
                    
                    if speed_ratio > 0:
                        current_step_delay = base_delay / speed_ratio
                        
                        step_sound_timer += dt
                        if step_sound_timer >= current_step_delay:
                            current_bg = get_current_background(player_world_x, tiles)
                            current_footsteps = get_footstep_sounds(current_bg)
                            sound_manager.play_sound(random.choice(current_footsteps))
                            step_sound_timer = 0
                    else:
                        step_sound_timer = 0
                else:
                    step_sound_timer = 0

                if not is_moving:
                    if player.last_direction == "down":
                        if pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not smelter_in_use and not campfire_in_use and not mouse_over_hotbar:
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
                        if pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not smelter_in_use and not campfire_in_use and not mouse_over_hotbar:
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
                        if pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not smelter_in_use and not campfire_in_use and not mouse_over_hotbar:
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
                        if pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not smelter_in_use and not campfire_in_use and not mouse_over_hotbar:
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

                if not crafting_bench_in_use and (keys[pygame.K_d] and pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not mouse_over_hotbar):
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
                

                elif not crafting_bench_in_use and (keys[pygame.K_a] and pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not mouse_over_hotbar):
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


                elif not crafting_bench_in_use and (keys[pygame.K_w] and pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not mouse_over_hotbar):
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
                
                

                elif not crafting_bench_in_use and (keys[pygame.K_s] and pygame.mouse.get_pressed()[0] and not mouse_attack_blocked and pygame.time.get_ticks() >= mouse_attack_block_expires and not player.exhausted and not mouse_over_hotbar):
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

        if (not ((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])) and ((not pygame.mouse.get_pressed()[0]) or mouse_attack_blocked or pygame.time.get_ticks() < mouse_attack_block_expires)) or player.exhausted:
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
        if need_pickaxe_message_timer > 0:
            pickaxe_text = font.render("Use a pickaxe to harvest this.", True, (255, 220, 80))
            x = screen.get_width()//2 - pickaxe_text.get_width()//2
            y = 80
            temp_surface = pygame.Surface((pickaxe_text.get_width() + 10, pickaxe_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 120))
            screen.blit(temp_surface, (x - 5, y - 5))
            screen.blit(pickaxe_text, (x, y))
            need_pickaxe_message_timer -= dt
        if need_shovel_message_timer > 0:
            shovel_text = font.render("Use a shovel to harvest this.", True, (180, 220, 255))
            x = screen.get_width()//2 - shovel_text.get_width()//2
            y = 110
            temp_surface = pygame.Surface((shovel_text.get_width() + 10, shovel_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 120))
            screen.blit(temp_surface, (x - 5, y - 5))
            screen.blit(shovel_text, (x, y))
            need_shovel_message_timer -= dt
        if inventory.inventory_full_message_timer > 0:
            full_text = font.render("Inventory Full! Cannot pick up items.", True, (255, 50, 50))
            x = screen.get_width()//2 - full_text.get_width()//2
            y = 50
            temp_surface = pygame.Surface((full_text.get_width() + 10, full_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 150))
            screen.blit(temp_surface, (x - 5, y - 5))
            screen.blit(full_text, (x, y))
            inventory.inventory_full_message_timer -= dt

        if inventory_in_use or campfire_in_use or smelter_in_use or crafting_bench_in_use or arcane_crafter_in_use or mortar_pestle_in_use or alchemy_bench_in_use or chest_in_use:
            inventory.begin_hover_pass()
        else:
            inventory.clear_hover_state()

        if campfire_in_use:
            campfire.render(screen)

        if smelter_in_use:
            smelter.render(screen)

        if inventory_in_use:
            if inventory.state != "inventory":
                inventory.close_drop_menu()
            inventory.draw_inventory(screen)
            if inventory.state == "inventory":
                inventory.draw_items(screen)
                inventory.draw_hotbar(screen)
                inventory.draw_drop_menu(screen)
            inventory.draw_dragged_item(screen)
        elif (campfire_in_use or smelter_in_use) and inventory.drop_menu_active:
            inventory.draw_drop_menu(screen)
            inventory.draw_dragged_item(screen)

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

        time_text = hud_font.render(f"Time: {time_of_day:.0f}", True, (255, 255, 255))
        time_rect = pygame.Rect(width - time_text.get_width() - 33, 31, time_text.get_width(), time_text.get_height())
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
        # store on player for UI display
        player.current_temperature = current_temperature
        # Warm up near active light sources
        light_sources = []
        for struct in placed_structures:
            if struct.get("item_name") == "Torch":
                light_sources.append((struct["x"], struct["y"], 220, 6))
            elif struct.get("item_name") == "Campfire" and campfire and getattr(campfire, "fire_lit", False):
                light_sources.append((struct["x"], struct["y"], 260, 10))
            elif struct.get("item_name") == "Smelter" and smelter and getattr(smelter, "fire_lit", False):
                light_sources.append((struct["x"], struct["y"], 260, 12))
        # Held torch warmth
        sel_slot = inventory.selected_hotbar_slot
        if 0 <= sel_slot < len(inventory.hotbar_slots):
            held_item = inventory.hotbar_slots[sel_slot]
            if held_item and held_item.get("item_name") == "Torch":
                light_sources.append((player_world_x, player_world_y, 220, 6))
        warm_bonus = 0
        for lx, ly, radius, bonus in light_sources:
            dist = math.hypot(lx - player_world_x, ly - player_world_y)
            if dist < radius:
                factor = 1 - (dist / radius)
                warm_bonus += bonus * factor
        if warm_bonus > 0:
            current_temperature = min(120, current_temperature + min(warm_bonus, 25))
        gauge_idx = get_temperature_gauge_index(current_temperature)
        draw_temperature_gauge(screen, current_temperature, gauge_idx)
        apply_temperature_effects(player, gauge_idx, dt)

        if tent_menu_active:
            draw_tent_menu(screen, dt)
        if fast_travel_menu_active:
            draw_fast_travel_placeholder(screen)

        if crafting_bench_in_use:
            crafting_bench.draw(screen)
            if inventory.drop_menu_active:
                inventory.draw_drop_menu(screen)
                inventory.draw_dragged_item(screen)

        if arcane_crafter_in_use:
            arcane_crafter.draw(screen)
            if inventory.drop_menu_active:
                inventory.draw_drop_menu(screen)
                inventory.draw_dragged_item(screen)

        if chest_in_use:
            chest_ui.draw(screen)
            if inventory.drop_menu_active:
                inventory.draw_drop_menu(screen)
                inventory.draw_dragged_item(screen)

        if alchemy_bench_in_use:
            alchemy_bench.draw(screen)
            if inventory.drop_menu_active:
                inventory.draw_drop_menu(screen)
                inventory.draw_dragged_item(screen)

        if mortar_pestle_in_use:
            mortar_pestle.draw(screen)
            if inventory.drop_menu_active:
                inventory.draw_drop_menu(screen)
                inventory.draw_dragged_item(screen)

        inventory.draw_hover_tooltip(screen)

        if not paused and not inventory_in_use and naming_cat is None and not crafting_bench_in_use and not arcane_crafter_in_use and not alchemy_bench_in_use and not chest_in_use and not mortar_pestle_in_use:
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
            title_font = pygame.font.Font(font_path, 22)
            input_font = pygame.font.Font(font_path, 18)
            
            title_text = title_font.render("Enter Cat's Name:", True, (255, 255, 200))
            title_rect = title_text.get_rect(center=(width // 2, box_y + 30))
            screen.blit(title_text, title_rect)
            
            # Draw input text with cursor
            input_display = cat_name_input + "|"
            input_text = input_font.render(input_display, True, (200, 200, 255))
            input_rect = input_text.get_rect(center=(width // 2, box_y + 70))
            screen.blit(input_text, input_rect)
            
            # Draw instruction text
            instruction_font = pygame.font.Font(font_path, 16)
            instruction_text = instruction_font.render("Press ENTER to confirm or BACKSPACE to delete", True, (200, 200, 200))
            instruction_rect = instruction_text.get_rect(center=(width // 2, box_y + 120))
            screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
pygame.quit()
