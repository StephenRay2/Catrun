import pygame
pygame.init()
from world import *
from buttons import *
from mob_placement import *


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
inventory = Inventory(64)
stamina_depleted_message_timer = 0

collection_message = None
collection_timer = 0
collection_messages = []
collection_message_num = 0

paused = False
inventory_in_use = False

stat_holder_image = pygame.image.load("assets/sprites/buttons/stat_holder.png").convert_alpha()
stat_holder_image = pygame.transform.scale(stat_holder_image, (50, 100))

hotbar_image = pygame.image.load("assets/sprites/buttons/hotbar.png").convert_alpha()
hotbar_image = pygame.transform.scale(hotbar_image, (800, 74))

quit_image = pygame.image.load("assets/sprites/buttons/quit_button.png").convert_alpha()
resume_image = pygame.image.load("assets/sprites/buttons/resume_button.png").convert_alpha()

quit_image = pygame.transform.scale(quit_image, (400, 150))
resume_image = pygame.transform.scale(resume_image, (600, 150))

resume_button = Button(width//2 - resume_image.get_width()//2, height//2 - 225, resume_image)
quit_button   = Button(width//2 - quit_image.get_width()//2, height//2 + 50, quit_image)

pause_menu_image = pygame.image.load("assets/sprites/buttons/pause_menu.png").convert_alpha()
pause_menu_image = pygame.transform.scale(pause_menu_image, (800, 650))

pause_menu_rect = pygame.Rect(0, 0, width, height)
temp_pause_surface = pygame.Surface((pause_menu_rect.width, pause_menu_rect.height), pygame.SRCALPHA)
temp_pause_surface.fill((0, 0, 0, 100))

harvest_cooldown = 0
harvest_delay = 300
inventory_resources = []

######################### GAME LOOP ################################

while running:
    player_speed = player.get_speed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused

        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            inventory_in_use = not inventory_in_use

        if paused:
            if resume_button.is_clicked(event):
                paused = False
            if quit_button.is_clicked(event):
                running = False

    current_time = pygame.time.get_ticks()
        
    if not paused and pygame.mouse.get_pressed()[0] and not player.exhausted:
        if current_time - harvest_cooldown > harvest_delay:
            harvest_cooldown = current_time
            for obj in visible_objects:
                if hasattr(obj, 'harvest') and hasattr(obj, 'destroyed') and not obj.destroyed:
                    facing_object = False
                    
                    horizontal_dist = abs(obj.rect.centerx - player_world_x)
                    vertical_dist = abs(obj.rect.centery - player_world_y)
                    
                    if player.last_direction == "right" and obj.rect.centerx > player_world_x and horizontal_dist < 50 and vertical_dist < 40:
                        facing_object = True
                    elif player.last_direction == "left" and obj.rect.centerx < player_world_x and horizontal_dist < 50 and vertical_dist < 40:
                        facing_object = True
                    elif player.last_direction == "up" and obj.rect.centery < player_world_y and vertical_dist < 50 and horizontal_dist < 40:
                        facing_object = True
                    elif player.last_direction == "down" and obj.rect.centery > player_world_y and vertical_dist < 50 and horizontal_dist < 40:
                        facing_object = True
                    
                    if facing_object:
                        resource = obj.harvest(player)
                        if resource:
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

    
            
    rocks = [r for r in rocks if not r.destroyed]
    trees = [t for t in trees if not t.destroyed]
    boulders = [b for b in boulders if not b.destroyed]
    berry_bushes = [bush for bush in berry_bushes if not bush.destroyed]

    cats = [cat for cat in cats if not cat.destroyed]
    squirrels = [squirrel for squirrel in squirrels if not squirrel.destroyed]
    crawlers = [crawler for crawler in crawlers if not crawler.destroyed]

        
    for tile_x, tile_image in tiles:
        screen_x = tile_x - cam_x
        if -BACKGROUND_SIZE < screen_x < width:
            screen.blit(tile_image, (screen_x, floor_y))

    keys = pygame.key.get_pressed()

    all_objects = rocks + trees + boulders + berry_bushes
    mobs = cats + squirrels + crawlers

    visible_objects = [obj for obj in all_objects if obj.rect.x - cam_x > -1000 and obj.rect.x - cam_x < width + 1000]
    visible_mobs = [mob for mob in mobs if mob.rect.x - cam_x > -1000 and mob.rect.x - cam_x < width + 1000]
    visible_objects.extend(visible_mobs)
    visible_objects.sort(key=lambda obj: obj.rect.y + obj.rect.height)

    for mob in visible_objects:
        if mob.destroyed:
            visible_mobs.remove(obj)

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
                if abs(obj.rect.x - (player_pos.x + cam_x)) < 1500 
                and abs(obj.rect.y - player_pos.y) < 800]
    nearby_mobs = [mob for mob in mobs
                if abs(mob.rect.x - (player_pos.x + cam_x)) < 1500 
                and abs(mob.rect.y - player_pos.y) < 800]
    
    screen.blit(hotbar_image, (width//2 - hotbar_image.get_width()//2, height - 100))
    


    if not paused and player.dead == False:

        for bush in berry_bushes:
            if player.rect.colliderect(
                pygame.Rect(bush.rect.x - cam_x, bush.rect.y, bush.rect.width, bush.rect.height)
            ) and keys[pygame.K_e]:
                berries = bush.collect(player)
                
                if berries:
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
            if player.rect.colliderect(
                pygame.Rect(tree.rect.x - cam_x, tree.rect.y, tree.rect.width, tree.rect.height)
            ) and keys[pygame.K_e]:
                fruit = tree.collect(player)
                
                if fruit:
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
            
            player_world_x = player_pos.x + cam_x
            player_world_y = player_pos.y
            
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
        player_world_x = player_pos.x + cam_x
        player_world_y = player_pos.y
        player.attacking(nearby_mobs, player_world_x, player_world_y)
        for mob in nearby_mobs:
            mob.handle_health(screen, cam_x, dt)


################# NOT INVENTORY IN USE #################

        if not inventory_in_use:

            if (((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and keys[pygame.K_LSHIFT]) or pygame.mouse.get_pressed()[0]) and not player.exhausted:
                if player.lose_stamina(screen, dt):
                    stamina_depleted_message_timer = 2.0
                player.stamina_speed()

            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
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
                if keys[pygame.K_LSHIFT]:
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
            

            elif keys[pygame.K_a] and pygame.mouse.get_pressed()[0] and not player.exhausted:
                player.last_direction = "left"
                player_animation_timer += dt
                if keys[pygame.K_LSHIFT]:
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


            elif keys[pygame.K_w] and pygame.mouse.get_pressed()[0] and not player.exhausted:
                player.last_direction = "up"
                player_animation_timer += dt
                if keys[pygame.K_LSHIFT]:
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
            
            

            elif keys[pygame.K_s] and pygame.mouse.get_pressed()[0] and not player.exhausted:
                player.last_direction = "down"
                player_animation_timer += dt
                if keys[pygame.K_LSHIFT]:
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

            


            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                shift_multiplier = 1.5
                
            else:
                shift_multiplier = 1

    

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

    if (not ((keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and keys[pygame.K_LSHIFT]) and not pygame.mouse.get_pressed()[0]) or player.exhausted:
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
        inventory.draw_items(screen)
        screen.blit(hotbar_image, (width//2 - hotbar_image.get_width()//2, height - 100))

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
        dungeon_depth = 2000
        cam_x = 100000
        player_pos.x = width / 2

    if keys[pygame.K_l]:
        dungeon_depth = 6300
        cam_x = 315000
        player_pos.x = width / 2

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
pygame.quit()