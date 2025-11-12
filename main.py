import pygame
pygame.init()
from buttons import *
from mob_placement import *
from sounds import *

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
        visible_objects.sort(key=lambda obj: obj.rect.y + obj.rect.height)

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
        dungeon_depth = absolute_cam_x
        total_elapsed_time += dt
        time_of_day = (12 + (total_elapsed_time / 60)) % 24

        
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

            player.health_leveler = 1
            player.stamina_leveler = 1
            player.hunger_leveler = 1
            player.thirst_leveler = 1
            player.warmth_leveler = 1
            player.max_health = 100 * player.health_leveler
            player.max_stamina = 100 * player.stamina_leveler
            player.max_hunger = 100 * player.hunger_leveler
            player.max_thirst = 100 * player.thirst_leveler
            player.max_warmth = 100

            player.damage = 50
            player.attack = 1
            player.base_speed = 275
            player.speed = 1
            player.defense = 1

            player.inventory = []
            player.score = 0
            
            inventory.inventory_list = [None] * inventory.capacity
            inventory.hotbar_slots = [None] * inventory.hotbar_size

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
                
                if event.key == pygame.K_ESCAPE and not inventory_in_use:
                    paused = not paused
                
                inventory.handle_keydown_hotbar(event, screen=None, use_on_press=False)

                if event.key == pygame.K_f and not inventory_in_use and player.is_alive:
                    success, tags = inventory.consume_item()
                    if success:
                        if "food" in tags:
                            sound_manager.play_sound(random.choice([f"consume_item{i}" for i in range(1, 7)]))
                        elif any(tag in tags for tag in ["liquid", "consumable"]):
                            sound_manager.play_sound(random.choice([f"consume_water{i}" for i in range(1, 5)]))

                if event.key == pygame.K_q:
                    inventory_in_use = not inventory_in_use
                    if not inventory_in_use:
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None
                
                if inventory_in_use and player.is_alive:
                    if event.key == pygame.K_ESCAPE:
                        inventory_in_use = False
                        inventory.selection_mode = "hotbar"
                        inventory.selected_inventory_slot = None

            # Throw mechanic - start charging
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and player.is_alive:
                throw_charge_start = pygame.time.get_ticks()

            # Throw mechanic - release and throw
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and player.is_alive:
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
                        if selected_hotbar and "cat_object" in selected_hotbar:
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
                        if selected_hotbar and "cat_object" in selected_hotbar:
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
                if inventory.dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    slot_index, is_hotbar = inventory.get_slot_at_mouse(mouse_pos, screen)
                    
                    if slot_index is not None:
                        inventory.end_drag(slot_index, is_hotbar, screen)
                    else:
                        inventory.cancel_drag()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                if event.button == 4:
                    inventory.selected_hotbar_slot = (inventory.selected_hotbar_slot - 1) % inventory.hotbar_size
                elif event.button == 5:
                    inventory.selected_hotbar_slot = (inventory.selected_hotbar_slot + 1) % inventory.hotbar_size
                inventory.selection_mode = "hotbar"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
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
    
        if not paused and not inventory_in_use and naming_cat is None and pygame.mouse.get_pressed()[0] and not player.exhausted:
            if current_time - harvest_cooldown > harvest_delay:
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
                            resource = obj.harvest(player)
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

        for tile_x, tile_image in tiles:
            screen_x = tile_x - cam_x
            if -BACKGROUND_SIZE < screen_x < width:
                screen.blit(tile_image, (screen_x, floor_y))

        keys = pygame.key.get_pressed()

        collectibles = sticks + stones + grasses + savannah_grasses + mushrooms
        all_objects_no_liquids = rocks + trees + boulders + berry_bushes + dead_bushes + ferns + fruit_plants
        all_objects = all_objects_no_liquids + ponds + lavas
        mobs = cats + squirrels + cows + chickens + crawlers + duskwretches + pocks + deers + black_bears + brown_bears + gilas + crows
        all_mobs = mobs

        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -256 and col.rect.x - cam_x < width + 256]
        visible_liquids = [obj for obj in (ponds + lavas) if obj.rect.x - cam_x > -256 and obj.rect.x - cam_x < width + 256 and obj.rect.y > -256 and obj.rect.y < height + 256]
        visible_objects = [obj for obj in all_objects_no_liquids if obj.rect.x - cam_x > -256 and obj.rect.x - cam_x < width + 256 and obj.rect.y > -256 and obj.rect.y < height + 256]
        visible_mobs = [mob for mob in mobs if mob.rect.x - cam_x > -256 and mob.rect.x - cam_x < width + 256 and mob.rect.y > -256 and mob.rect.y < height + 256]
        
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
        visible_objects.sort(key=lambda obj: obj.rect.y + obj.rect.height)

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

        for obj in visible_liquids:
            obj.update_animation(dt)
            obj.draw(screen, cam_x)

        for obj in visible_objects:
            object_mid_y = obj.rect.y + obj.rect.height / 2
            if not player_drawn and (player.rect.centery + 20) <= object_mid_y:
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
                player_drawn = True
            obj.draw(screen, cam_x)

        if not player_drawn:
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
            
        nearby_objects = [obj for obj in all_objects 
                    if abs(obj.rect.x - (player_pos.x + cam_x)) < 1500 
                    and abs(obj.rect.y - player_pos.y) < 800]
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
                mob_nearby_objects = [obj for obj in nearby_objects 
                                    if abs(obj.rect.x - mob.rect.x) < 100 
                                    and abs(obj.rect.y - mob.rect.y) < 100]
                
                
                
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

            left_collision = any(
                left_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby_solid
            )

            right_collision = any(
                right_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby_solid
            )

            up_collision = any(
                top_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby_solid
            )

            down_collision = any(
                bottom_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby_solid
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

            if not inventory_in_use and naming_cat is None:

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
                        if pygame.mouse.get_pressed()[0] and not player.exhausted:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_down_images)
                                player_current_image = player_stand_attack_down_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_current_image = player_stand_image
                    elif player.last_direction == "up":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_up_images)
                                player_current_image = player_stand_attack_up_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_current_image = player_stand_up
                    elif player.last_direction == "left":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_left_images)
                                player_current_image = player_stand_attack_left_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_current_image = player_stand_left
                    elif player.last_direction == "right":
                        if pygame.mouse.get_pressed()[0] and not player.exhausted:
                            player_animation_timer += dt
                            if player_animation_timer > .07:
                                player_frame_index = (player_frame_index + 1) % len(player_stand_attack_right_images)
                                player_current_image = player_stand_attack_right_images[player_frame_index]
                                player_animation_timer = 0
                        else:
                            player_current_image = player_stand_right
                
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

                if keys[pygame.K_d] and pygame.mouse.get_pressed()[0] and not player.exhausted:
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

                elif keys[pygame.K_d]:
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
                

                elif keys[pygame.K_a] and pygame.mouse.get_pressed()[0] and not player.exhausted:
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

                elif keys[pygame.K_a]:
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


                elif keys[pygame.K_w] and pygame.mouse.get_pressed()[0] and not player.exhausted:
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

                elif keys[pygame.K_w]:
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
                
                

                elif keys[pygame.K_s] and pygame.mouse.get_pressed()[0] and not player.exhausted:
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

                elif keys[pygame.K_s]:
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

        if not paused and not inventory_in_use and naming_cat is None:
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