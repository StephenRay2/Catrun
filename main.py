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
floor_y = 0
shift_multiplier = 1
dungeon_depth = 0
dungeon_depth_high = 0
font = pygame.font.SysFont(None, 24)
scroll = 0
dungeon_traversal_speed = .1

stamina_depleted_message_timer = 0
player_world_x = player_pos.x + cam_x
player_world_y = player_pos.y

collection_message = None
collection_timer = 0
collection_messages = []
collection_message_num = 0

paused = False
inventory_in_use = False

step_sound_timer = 0
step_sound_delay = 0.3
collect_cooldown = 0
collect_delay = 300
harvest_cooldown = 0
harvest_delay = 300
inventory_resources = []
state = "menu"
generate_world()
previous_state = state
sound_manager.play_music("assets/music/Settler's End.wav")
######################### GAME LOOP ################################

while running:
    if state != previous_state:
        if state == "menu":
            sound_manager.stop_music()
            sound_manager.play_music("assets/music/Settler's End.wav")
        elif state == "game":
            sound_manager.stop_music()
            sound_manager.play_random_ambient_music(min_delay=100, max_delay=500, volume=0.2, fade_in=5000)
        previous_state = state
    if state == "menu":
        menu_image = bg_grass
        menu_screen = pygame.Rect(0, 0, width, height)
        screen.blit(menu_image, (0, 0), menu_screen)

        
        collectibles = sticks + stones + grasses + savannah_grasses + mushrooms
        all_objects = rocks + trees + boulders + berry_bushes + dead_bushes

        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -1000 and col.rect.y - cam_x < width + 1000]
        visible_objects = [obj for obj in all_objects if obj.rect.x - cam_x > -1000 and obj.rect.x - cam_x < width + 1000]
        visible_objects.extend(visible_collectibles)
        visible_objects.sort(key=lambda obj: obj.rect.y + obj.rect.height)

        player_drawn = False

        for tile_x, tile_image in tiles:
            screen_x = tile_x - cam_x
            if -BACKGROUND_SIZE < screen_x < width:
                screen.blit(tile_image, (screen_x, floor_y))

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

            dungeon_depth = 0
            dungeon_depth_high = 0
            cam_x = 0
            player_pos.x = width / 2
            player_pos.y = height / 2
       
            player.health = player.max_health
            player.stamina = player.max_stamina
            player.hunger = player.max_hunger
            player.water = player.max_water
            player.dead = False

            player.experience = 0
            player.exp_total = 0
            player.level = 1
            player.next_level_exp = 100
            player.level_up_timer = 0

            player.health_leveler = 1
            player.stamina_leveler = 1
            player.hunger_leveler = 1
            player.water_leveler = 1
            player.warmth_leveler = 1
            player.max_health = 100 * player.health_leveler
            player.max_stamina = 100 * player.stamina_leveler
            player.max_hunger = 100 * player.hunger_leveler
            player.max_water = 100 * player.water_leveler
            player.max_warmth = 100

            player.damage = 5
            player.attack = 1
            player.base_speed = 275
            player.speed = 1
            player.defense = 1

            player.inventory = []
            player.score = 0

            inventory.inventory_list = []

            inventory_resources = []
            collection_messages = []

            game_just_started = False 
        
        player_world_x = player_pos.x + cam_x
        player_world_y = player_pos.y
        
        player_speed = player.get_speed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                inventory_in_use = not inventory_in_use

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if current_time - collect_cooldown > collect_delay:
                    collect_cooldown = current_time
                    for obj in visible_objects:
                        if hasattr(obj, 'collect') and hasattr(obj, 'is_empty') and not obj.destroyed and not obj.is_empty:
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
                                    sound_manager.play_sound(random.choice([f"pick_berry{i}" for i in range(1,5)]))
                                    inventory_resources.extend(resource)
                                    collection_messages.insert(0, [
                                        font.render(f"Collected {len(resource)} {obj.berry}", True, (20, 255, 20)),
                                        pygame.Surface((font.render(f"Collected {len(resource)} {obj.berry}", True, (20, 255, 20)).get_width() + 10, font.render(f"Collected {len(resource)} {obj.berry}", True, (20, 255, 20)).get_height() + 10), pygame.SRCALPHA),
                                        pygame.Rect(20, 500, font.render(f"Collected {len(resource)} {obj.berry}", True, (20, 255, 20)).get_width(), font.render(f"Collected {len(resource)} {obj.berry}", True, (20, 255, 20)).get_height()),
                                        3.0,
                                        1.0
                                    ])
                                    collection_messages[0][1].fill((0, 0, 0, 100))

            if paused:
                if resume_button.is_clicked(event):
                    paused = False
                if quit_button.is_clicked(event):
                    state = "menu"
                    paused = False
    
        current_time = pygame.time.get_ticks()


            
        if not paused and not inventory_in_use and pygame.mouse.get_pressed()[0] and not player.exhausted:
            if current_time - harvest_cooldown > harvest_delay:
                harvest_cooldown = current_time
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
                                    elif obj.resource in ["Apple Wood", "Dusk Wood", "Fir Wood", "Oak Wood", "Orange Wood"]:
                                        sound_manager.play_sound(random.choice(["gather_wood1", "gather_wood2", "gather_wood3"]))
                                    elif obj.resource == "Sticks":
                                        sound_manager.play_sound(random.choice(["break_bush1", "break_bush2"]))
                                inventory_resources.extend(resource)
                                resource_collect_text = font.render(f"Collected {len(resource)} {obj.resource}", True, (20, 255, 20))
                                collection_messages.insert(0, [
                                    resource_collect_text,
                                    pygame.Surface((resource_collect_text.get_width() + 10, resource_collect_text.get_height() + 10), pygame.SRCALPHA),
                                    pygame.Rect(20, 500, resource_collect_text.get_width(), resource_collect_text.get_height()),
                                    3.0,
                                    1.0
                                ])
                                collection_messages[0][1].fill((0, 0, 0, 100))
                            if obj.destroyed:
                                visible_objects.remove(obj)

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
        all_objects = rocks + trees + boulders + berry_bushes + dead_bushes
        mobs = cats + squirrels + cows + chickens + crawlers + duskwretches + pocks + deers + black_bears + brown_bears + gilas + crows

        visible_collectibles = [col for col in collectibles if col.rect.x- cam_x > -1000 and col.rect.y - cam_x < width + 1000]
        visible_objects = [obj for obj in all_objects if obj.rect.x - cam_x > -1000 and obj.rect.x - cam_x < width + 1000]
        visible_mobs = [mob for mob in mobs if mob.rect.x - cam_x > -1000 and mob.rect.x - cam_x < width + 1000]
        visible_objects.extend(visible_mobs)
        visible_objects.extend(visible_collectibles)
        visible_objects.sort(key=lambda obj: obj.rect.y + obj.rect.height)

        for mob in visible_objects:
            if mob.destroyed:
                visible_mobs.remove(obj)

        for col in visible_objects:
            if col.destroyed:
                collectibles.remove(col)

        player_drawn = False

        for obj in visible_objects:
            object_mid_y = obj.rect.y + obj.rect.height / 2
            if not player_drawn and (player.rect.centery + 20) <= object_mid_y:
                screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))
                player_drawn = True
            obj.draw(screen, cam_x)

        if not player_drawn:
            screen.blit(player_current_image, (player_pos.x - size/2, player_pos.y - size/2))

        player.rect.center = (player_pos.x, player_pos.y)
            
        nearby_objects = [obj for obj in all_objects 
                    if abs(obj.rect.x - (player_pos.x + cam_x)) < 1500 
                    and abs(obj.rect.y - player_pos.y) < 800]
        nearby_mobs = [mob for mob in mobs
                    if abs(mob.rect.x - (player_pos.x + cam_x)) < 1500 
                    and abs(mob.rect.y - player_pos.y) < 800]
        
        screen.blit(hotbar_image, (width//2 - hotbar_image.get_width()//2, height - 100))
        


        if not paused and not inventory_in_use and player.dead == False:

            for bush in berry_bushes:
                if current_time - collect_cooldown > collect_delay:
                    if player.rect.colliderect(
                        pygame.Rect(bush.rect.x - cam_x, bush.rect.y, bush.rect.width, bush.rect.height)
                    ) and keys[pygame.K_e]:
                        berries = bush.collect(player)
                        
                        if berries:
                            sound_manager.play_sound(random.choice([f"pick_berry{i}" for i in range(1, 5)]))
                            collect_cooldown = current_time
                            inventory_resources.extend(berries)
                            berry_collect_text = font.render(f"Collected {len(berries)} {bush.berry}", True, (20, 255, 20))
                            
                            collection_messages.insert(0, [
                                berry_collect_text,
                                pygame.Surface((berry_collect_text.get_width() + 10, berry_collect_text.get_height() + 10), pygame.SRCALPHA),
                                pygame.Rect(20, 500, berry_collect_text.get_width(), berry_collect_text.get_height()),
                                3.0,
                                1.0
                            ])
                            collection_messages[0][1].fill((0, 0, 0, 100))

            for tree in trees:
                if current_time - collect_cooldown > collect_delay:
                    if player.rect.colliderect(
                        pygame.Rect(tree.rect.x - cam_x, tree.rect.y, tree.rect.width, tree.rect.height)
                    ) and keys[pygame.K_e]:
                        fruit = tree.collect(player)
                        
                        if fruit:
                            collect_cooldown = current_time
                            fruit_collect_text = font.render(f"Collected {len(fruit)} {tree.fruit}", True, (20, 255, 20))
                            inventory_resources.extend(fruit)
                            collection_messages.insert(0, [
                                fruit_collect_text,
                                pygame.Surface((fruit_collect_text.get_width() + 10, fruit_collect_text.get_height() + 10), pygame.SRCALPHA),
                                pygame.Rect(20, 500, fruit_collect_text.get_width(), fruit_collect_text.get_height()),
                                3.0,
                                1.0
                            ])
                            collection_messages[0][1].fill((0, 0, 0, 100))

            for col in collectibles:
                if current_time - collect_cooldown > collect_delay:
                    if player.rect.colliderect(
                        pygame.Rect(col.rect.x - cam_x, col.rect.y, col.rect.width, col.rect.height)
                    ) and keys[pygame.K_e]:
                        resources = col.collect(player)
                        
                        if resources:
                            collect_cooldown = current_time
                            inventory_resources.extend(resources)
                            resource_collect_text = font.render(f"Collected {len(resources)} {col.resource}", True, (20, 255, 20))
                            
                            collection_messages.insert(0, [
                                resource_collect_text,
                                pygame.Surface((resource_collect_text.get_width() + 10, resource_collect_text.get_height() + 10), pygame.SRCALPHA),
                                pygame.Rect(20, 500, resource_collect_text.get_width(), resource_collect_text.get_height()),
                                3.0,
                                1.0
                            ])
                            collection_messages[0][1].fill((0, 0, 0, 100))
            
            inventory.add(inventory_resources)
            inventory_resources = []

            if collection_timer > 0:
                collection_timer -= dt
                if collection_message:
                    text, bg, rect = collection_message
                    screen.blit(bg, (rect.x, rect.y))
                    screen.blit(text, (rect.x + 5, rect.y + 5))
                collection_message_num -= 1

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

            all_nearby = nearby_objects + nearby_mobs

            left_collision = any(
                left_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby
            )

            right_collision = any(
                right_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby
            )

            up_collision = any(
                top_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby
            )

            down_collision = any(
                bottom_player_check.colliderect(obj.get_collision_rect(cam_x))
                for obj in all_nearby
            )

            for bush in berry_bushes:
                bush.update(dt)
            
            for tree in trees:
                tree.update(dt)


            for mob in mobs:
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
                mob.flee(player_world_x, player_world_y, dt)


    ################# NOT INVENTORY IN USE #################

            if not inventory_in_use:

                if (((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])) or pygame.mouse.get_pressed()[0]) and not player.exhausted:
                    if player.lose_stamina(screen, dt):
                        stamina_depleted_message_timer = 2.0
                    player.stamina_speed()

                # Check if player is moving in any direction
                is_moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
                is_running = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and is_moving
                
                # Play footstep sound if moving (only once per delay, regardless of direction)
                if is_moving:
                    # Calculate delay based on actual player speed (accounts for exhaustion and sprinting)
                    # player_speed is calculated from player.get_speed() which returns base_speed * speed
                    # shift_multiplier (1.5 when running, 1.0 when walking) affects actual movement
                    base_delay = 0.3  # Base walking speed delay
                    
                    # The actual speed being used includes shift_multiplier
                    actual_speed = player_speed * shift_multiplier
                    base_speed = player.base_speed * player.speed
                    speed_ratio = actual_speed / base_speed if base_speed > 0 else 1.0
                    
                    current_step_delay = base_delay / speed_ratio
                    
                    step_sound_timer += dt
                    if step_sound_timer >= current_step_delay:
                        sound_manager.play_sound(random.choice(grass_steps))
                        step_sound_timer = 0
                else:
                    # Reset timer when not moving
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



    ############# END NOT INVENTORY IN USE #################
    ############# END NOT PAUSED #################
        player.health_bar(screen)
        player.stamina_bar(screen)
        player.hunger_bar(screen)
        player.exp_bar(screen)
        player.water_bar(screen)
        screen.blit(stat_holder_image, (20, 50))
        player.handle_exp(screen, dt)
        player.regain_health(dt)
        player.lose_hunger(dt)
        player.lose_water(dt)
    
        
        if dungeon_depth >= dungeon_depth_high:
            dungeon_depth_high = dungeon_depth

        player.determine_score(dungeon_depth_high)
        player.print_score(screen, dungeon_depth_high)
        player.is_dead(screen, dungeon_depth_high)

        if (not ((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])) and not pygame.mouse.get_pressed()[0]) or player.exhausted:
            player.regain_stamina(dt, screen)
            player.stamina_speed()
            player.lose_water(dt)
            
        if stamina_depleted_message_timer > 0:
            tired_text = font.render("Too tired. Rest to regain stamina", True, (40, 255, 20))
            x = screen.get_width()//2 - tired_text.get_width()//2
            y = 20
            temp_surface = pygame.Surface((tired_text.get_width() + 10, tired_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 20))
            screen.blit(temp_surface, (x - 5, y - 5))
            screen.blit(tired_text, (x, y))
            stamina_depleted_message_timer -= dt



        if inventory_in_use:

            inventory.draw_inventory(screen)
            if inventory.state == "inventory":
                inventory.draw_items(screen)
            screen.blit(hotbar_image, (width//2 - hotbar_image.get_width()//2, height - 100))
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


        if keys[pygame.K_i]:
            dungeon_depth = 10000
            cam_x = 500000
            player_pos.x = width / 2

        if keys[pygame.K_o]:
            dungeon_depth = 5000
            cam_x = 250000
            player_pos.x = width / 2

        if keys[pygame.K_p]:
            dungeon_depth = 1600
            cam_x = 75000
            player_pos.x = width / 2

        if keys[pygame.K_l]:
            dungeon_depth = 6300
            cam_x = 315000
            player_pos.x = width / 2

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
pygame.quit()