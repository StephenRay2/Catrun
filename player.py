import pygame
import random
import math
from world import screen
from sounds import grass_steps, sound_manager
from debug import font_path, font

hud_font = pygame.font.Font(font_path, 14)
font = pygame.font.Font(font_path, 18)
large_font = pygame.font.Font(font_path, 28)
xl_font = pygame.font.Font(font_path, 72)
size = 64


def draw_text_with_background(screen, text_surface, x, y, padding=4):
    bg_rect = text_surface.get_rect(topleft=(x, y)).inflate(padding * 2, padding)
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 150))
    screen.blit(bg_surface, bg_rect.topleft)
    screen.blit(text_surface, (x, y))

player_stand_image = pygame.image.load("assets/sprites/player/GlenjaminFrontIdle1.png")
player_stand_image_back = pygame.image.load("assets/sprites/player/GlenjaminUpIdle1.png")
player_stand_left = pygame.transform.flip(pygame.image.load("assets/sprites/player/GlenjaminRightIdle1.png"), True, False)
player_stand_right = pygame.image.load("assets/sprites/player/GlenjaminRightIdle1.png")
player_walk_down_images = [pygame.image.load(f"assets/sprites/player/GlenjaminDownWalk{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_up_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpWalk{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_left_images = [pygame.transform.flip(pygame.image.load(f"assets/sprites/player/GlenjaminRightWalk{i}.png"), True, False).convert_alpha() for i in range(1, 9)]
player_stand_attack_down_images = [pygame.image.load(f"assets/sprites/player/GlenjaminDownAttack{i}.png").convert_alpha() for i in range(1, 5)]
player_stand_attack_up_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpAttack{i}.png").convert_alpha() for i in range(1, 5)]
player_stand_attack_left_images = [pygame.image.load(f"assets/sprites/player/GlenjaminLeftAttack{i}.png").convert_alpha() for i in range(1, 5)]
player_walk_down_attack_images = [pygame.image.load(f"assets/sprites/player/GlenjaminDownWalkAttack{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_up_attack_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpWalkAttack{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_left_attack_images = [pygame.image.load(f"assets/sprites/player/GlenjaminLeftWalkAttack{i}.png").convert_alpha() for i in range(1, 9)]
player_idle_down_images = [pygame.image.load(f"assets/sprites/player/GlenjaminFrontIdle{i}.png").convert_alpha() for i in range(1, 4)]
player_idle_up_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpIdle{i}.png").convert_alpha() for i in range(1, 4)]
player_idle_left_images = [pygame.transform.flip(pygame.image.load(f"assets/sprites/player/GlenjaminRightIdle{i}.png"), True, False).convert_alpha() for i in range(1, 4)]

player_stand_image = pygame.transform.scale(player_stand_image, (size, size))
player_stand_up = pygame.transform.scale(player_stand_image_back, (size, size))
player_stand_left = pygame.transform.scale(player_stand_left, (size, size))
player_stand_right = pygame.transform.scale(player_stand_right, (size, size))
player_walk_down_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_down_images]
player_walk_up_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_up_images]
player_walk_left_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_left_images]
player_walk_right_images = [pygame.transform.flip(img, True, False) for img in player_walk_left_images]
player_stand_attack_down_images = [pygame.transform.scale(img, (size, size)) for img in player_stand_attack_down_images]
player_stand_attack_up_images = [pygame.transform.scale(img, (size, size)) for img in player_stand_attack_up_images]
player_stand_attack_left_images = [pygame.transform.scale(img, (size, size)) for img in player_stand_attack_left_images]
player_stand_attack_right_images = [pygame.transform.flip(img, True, False) for img in player_stand_attack_left_images]
player_walk_down_attack_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_down_attack_images]
player_walk_up_attack_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_up_attack_images]
player_walk_left_attack_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_left_attack_images]
player_walk_right_attack_images = [pygame.transform.flip(img, True, False) for img in player_walk_left_attack_images]
player_idle_down_images = [pygame.transform.scale(img, (size, size)) for img in player_idle_down_images]
player_idle_up_images = [pygame.transform.scale(img, (size, size)) for img in player_idle_up_images]
player_idle_left_images = [pygame.transform.scale(img, (size, size)) for img in player_idle_left_images]
player_idle_right_images = [pygame.transform.flip(img, True, False) for img in player_idle_left_images]

player_frame_index = 0
player_animation_timer = 0
player_current_image = player_stand_image
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
cam_x = 0
cam_y = 0


class TempPlayerCollision:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)

    def get_collision_rect(self, cam_x):
        return pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.width, self.rect.height)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.image = pygame.Surface((48, 48))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(center=(x, y)).inflate(-10, -20)

        self.health_leveler = 1
        self.max_health = int(round(100 * self.health_leveler))
        self.health = self.max_health
        self.stamina_leveler = 1
        self.max_stamina = int(round(100 * self.stamina_leveler))
        self.stamina = self.max_stamina
        self.hunger_leveler = 1
        self.max_hunger = int(round(100 * self.hunger_leveler))
        self.hunger = self.max_hunger
        self.full_timer = 60
        self.thirst_leveler = 1
        self.max_thirst = int(round(100 * self.thirst_leveler))
        self.thirst = self.max_thirst
        self.thirst_full_timer = 60
        self.weather_resistance_leveler = 1
        self.max_heat_resistance = 100 * self.weather_resistance_leveler
        self.temp_heat_resistance_increase = 1
        self.temp_heat_resistance_timer = 0
        self.heat_resistance = 100 * self.temp_heat_resistance_increase
        self.max_cold_resistance = 100 * self.weather_resistance_leveler
        self.temp_cold_resistance_increase = 1
        self.temp_cold_resistance_timer = 0
        self.cold_resistance = 100 * self.temp_cold_resistance_increase
        self.max_torpidity = 100
        self.torpidity = 0
        self.extreme_temp_timer = 0
        self.temp_weight_increase = 1
        self.weight_leveler = 1
        self.max_weight = 100 * self.weight_leveler * self.temp_weight_increase
        self.weight = 0
        self.glow = False
        self.glow_time = 0
        self.poison = False
        self.poison_time = 0
        self.damage = 5
        self.poison_strength = 1
        self.strength_leveler = 1
        self.strength_level_gain = 1
        self.attack = int(self.damage + (self.strength_leveler - 1) * self.strength_level_gain)
        self.temp_attack_boost = 1
        self.base_speed = 275
        self.speed_leveler = 1
        self.speed = 100 * self.speed_leveler
        self.defense_leveler = 1
        self.defense = 100 * self.defense_leveler
        self.resilience_leveler = 1
        self.resilience = 100 * self.resilience_leveler
        self.temperature_resistance_leveler = 0
        self.level = 1
        self.experience = 0
        self.exp_total = 0
        self.req_multiplier = .5
        self.next_level_exp = 100
        self.level_up_timer = 0
        self.stamina_timer = 0
        self.stamina_message_timer = 0
        self.unspent_stat_points = 0
        self.health_bar_color = ()
        self.poisoned_health_color = ()

        self.inventory = []
        self.is_alive = True
        self.is_attacking = False
        self.direction = pygame.Vector2(0, 0)
        self.step_sound = random.choice(grass_steps)
        self.spawn_protection_center = pygame.Vector2(x, y)
        self.spawn_protection_radius = 900
        self.spawn_protection_radius_sq = self.spawn_protection_radius * self.spawn_protection_radius

        self.exhausted = False
        self.dead = False
        self.score = 0
        self.last_direction = "down"
        self.attack_cooldown = pygame.time.get_ticks()
        self.attack_delay = 300
        self.mob_noise_delay = 3
        self.redmite_slots = [None, None, None, None]
        
        self.swimming = False
        self.in_lava = False
        self.swim_stamina_drain = 0.3
        self.lava_damage_rate = 40
        self.lava_damage_timer = 0
        self.current_liquid = None
        self.ground_slow_factor = 1.0

    def is_in_spawn_protection(self):
        return False

    def status_effects(self, dt):
        if self.poison == True:
            self.poison_time -= dt
            self.health -= dt * self.poison_strength
            if self.health < 0:
                self.health = 0
            if self.poison_time <= 0:
                self.poison = False
                self.poison_time = 0
                self.poison_strength = 1
    
    def handle_swimming(self, dt, liquid_collision=None):
        if self.swimming:
            self.stamina -= self.swim_stamina_drain * dt
            
            if self.stamina < 0:
                self.stamina = 0
                if not self.in_lava:
                    self.health -= 5 * dt
                    if self.health < 0:
                        self.health = 0
                        self.is_alive = False
                        self.dead = True
    
    def handle_lava_damage(self, dt):
        if self.in_lava:
            self.lava_damage_timer += dt
            if self.lava_damage_timer >= 0.1:
                self.health -= self.lava_damage_rate * (self.lava_damage_timer / 1.0)
                self.lava_damage_timer = 0
                if self.health < 0:
                    self.health = 0
                    self.is_alive = False
                    self.dead = True
    
    def enter_liquid(self, liquid_type, liquid_obj=None):
        if liquid_type == "water":
            self.swimming = True
            self.in_lava = False
        elif liquid_type == "lava":
            self.swimming = True
            self.in_lava = True
        self.current_liquid = liquid_obj
    
    def exit_liquid(self):
        self.swimming = False
        self.in_lava = False
        self.lava_damage_timer = 0
        self.current_liquid = None

    def attacking(self, nearby_mobs, player_world_x, player_world_y, mouse_over_hotbar=False):
        from mobs import Cat, Redmite
        if pygame.mouse.get_pressed()[0] and not self.exhausted and not mouse_over_hotbar:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_cooldown > self.attack_delay:
                self.attack_cooldown = current_time
                self.attacking_target = None

                for mob in nearby_mobs:
                    if isinstance(mob, Cat) and getattr(mob, "tamed", False):
                        continue

                    mob_collision = mob.get_collision_rect(0)

                    horizontal_dist = abs(mob_collision.centerx - player_world_x)
                    vertical_dist = abs(mob_collision.centery - player_world_y)

                    attack_reach = 25
                    horizontal_range = (mob_collision.width / 2) + attack_reach
                    vertical_range = (mob_collision.height / 2) + attack_reach

                    facing_object = False
                    if self.last_direction == "right" and mob_collision.centerx > player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                        facing_object = True
                    elif self.last_direction == "left" and mob_collision.centerx < player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                        facing_object = True
                    elif self.last_direction == "up" and mob_collision.centery < player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                        facing_object = True
                    elif self.last_direction == "down" and mob_collision.centery > player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                        facing_object = True

                    if facing_object and 1 <= mob.health:
                        if isinstance(mob, Redmite) and getattr(mob, "latched_to_player", False):
                            continue
                        self.attacking_target = mob
                        old_health = mob.health
                        mob.health -= self.attack
                        if hasattr(mob, "register_attack"):
                            mob.register_attack(self)
                        if mob.health < 0:
                            mob.health = 0
                        try:
                            from inventory import inventory as player_inventory
                            player_inventory.decrement_durability(player_inventory.selected_hotbar_slot, True, 1)
                        except Exception:
                            pass

                        if not hasattr(mob, "last_hit_sound_time"):
                            mob.last_hit_sound_time = 0

                        hit_sound_cooldown = 6000
                        if current_time - mob.last_hit_sound_time > hit_sound_cooldown:
                            mob.last_hit_sound_time = current_time
                            if mob.__class__.__name__ in ["BlackBear", "BrownBear"]:
                                sound_manager.play_sound("bear_get_hit")
                            elif mob.__class__.__name__ == "Deer":
                                if hasattr(mob, 'is_buck') and mob.is_buck:
                                    sound_manager.play_sound("buck_get_hit")
                                else:
                                    sound_manager.play_sound("deer_get_hit")
                            elif mob.__class__.__name__ == "Chicken":
                                sound_manager.play_sound(random.choice([f"chicken_get_hit{i}" for i in range(1,4)]))
                            elif mob.__class__.__name__ == "Cat":
                                sound_manager.play_sound("cat_get_hit1")
                            elif mob.__class__.__name__ == "Cow":
                                sound_manager.play_sound(random.choice(["cow_moo1", "cow_moo2"]))
                            elif mob.__class__.__name__ == "Squirrel":
                                sound_manager.play_sound("squirrel_get_hit")
                            elif mob.__class__.__name__ == "Crow":
                                sound_manager.play_sound(random.choice(["crow_caw1", "crow_caw2", "crow_caw"]))

    def determine_score(self, dungeon_depth):
        return int(self.exp_total / 100) + int(dungeon_depth)

    def print_score(self, screen, dungeon_depth):
        score_text = hud_font.render(f"Score: {self.determine_score(dungeon_depth)}", True, (255, 255, 255))
        x = screen.get_width() - score_text.get_width() - 20
        y = 30
        temp_surface = pygame.Surface((score_text.get_width() + 10, score_text.get_height() + 10), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 100))
        screen.blit(temp_surface, (x - 5, y - 5))
        screen.blit(score_text, (x, y))
        
    def is_dead(self, screen, dungeon_depth):
        game_over_text = xl_font.render("YOU DIED. GAME OVER.", True, (255, 20, 20))
        score_text = large_font.render(f"Score: {self.determine_score(dungeon_depth)}", True, (255, 255, 255))
        go_x = screen.get_width()//2 - game_over_text.get_width()//2
        go_y = screen.get_height()//2 - game_over_text.get_height()//2 - 20
        score_x = screen.get_width()//2 - score_text.get_width()//2
        score_y = screen.get_height()//2 - score_text.get_height()//2 + 30
        if self.health < 1:
            self.dead = True
            pause_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(pause_surface, (0, 0, 0, 150), screen.get_rect())
            temp_surface = pygame.Surface((score_text.get_width() + 10, score_text.get_height() + 10), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 100))
            screen.blit(pause_surface, (0, 0))
            screen.blit(game_over_text, (go_x, go_y - 30))
            screen.blit(temp_surface, (score_x - 5, score_y - 5))
            screen.blit(score_text, (score_x, score_y))
            
    def handle_exp(self, screen, dt):
        if self.experience >= self.next_level_exp:
            self.experience -= self.next_level_exp
            self.level_up(screen)

        if self.level_up_timer > 0:
            self.show_level_up_message(screen)
            self.level_up_timer -= dt

    def level_up(self, screen):
        lvl = self.level
        self.level += 1
        self.exp_total += self.next_level_exp
        if self.level > 0:
            self.next_level_exp += (self.next_level_exp * self.req_multiplier)
            if lvl <= 10:
                self.req_multiplier -= 0.034
            elif lvl <= 20:
                self.req_multiplier -= 0.012
            elif lvl <= 30:
                self.req_multiplier -= 0.0005
            elif lvl <= 40:
                self.req_multiplier -= 0.0004
            elif lvl <= 50:
                self.req_multiplier -= 0.00019
            elif lvl <= 60:
                self.req_multiplier -= 0.00009
            elif lvl <= 70:
                self.req_multiplier -= 0.00008
            elif lvl <= 80:
                self.req_multiplier -= 0.00007
            elif lvl < 100:
                self.req_multiplier -= 0.00003
        self.level_up_timer = 10
        self.unspent_stat_points += 1
        sound_manager.play_sound("level_up")

    def apply_stat_upgrade(self, stat_key):
        if self.unspent_stat_points <= 0:
            return False

        upgraded = False
        if stat_key == "health":
            self.health_leveler = round(self.health_leveler + 0.1, 4)
            self.max_health = int(100 * self.health_leveler)
            self.health = self.max_health
            upgraded = True
        elif stat_key == "stamina":
            self.stamina_leveler = round(self.stamina_leveler + 0.1, 4)
            self.max_stamina = int(100 * self.stamina_leveler)
            self.stamina = self.max_stamina
            upgraded = True
        elif stat_key == "hunger":
            self.hunger_leveler = round(self.hunger_leveler + 0.1, 4)
            self.max_hunger = int(100 * self.hunger_leveler)
            self.hunger = self.max_hunger
            upgraded = True
        elif stat_key == "thirst":
            self.thirst_leveler = round(self.thirst_leveler + 0.1, 4)
            self.max_thirst = int(100 * self.thirst_leveler)
            self.thirst = self.max_thirst
            upgraded = True
        elif stat_key == "weather":
            self.weather_resistance_leveler = round(self.weather_resistance_leveler + 0.1, 4)
            self.max_heat_resistance = int(100 * self.weather_resistance_leveler)
            self.max_cold_resistance = int(100 * self.weather_resistance_leveler)
            self.heat_resistance = self.max_heat_resistance
            self.cold_resistance = self.max_cold_resistance
            upgraded = True
        elif stat_key == "weight":
            self.weight_leveler = round(self.weight_leveler + 0.1, 4)
            self.max_weight = int(100 * self.weight_leveler * self.temp_weight_increase)
            upgraded = True
        elif stat_key == "strength":
            self.strength_leveler = round(self.strength_leveler + 1, 4)
            self.attack = int(self.damage + (self.strength_leveler - 1) * self.strength_level_gain)
            upgraded = True
        elif stat_key == "speed":
            self.speed_leveler = round(self.speed_leveler + 0.05, 4)
            self.speed = int(100 * self.speed_leveler)
            upgraded = True
        elif stat_key == "defense":
            self.defense_leveler = round(self.defense_leveler + 0.1, 4)
            self.defense = int(100 * self.defense_leveler)
            upgraded = True
        elif stat_key == "resilience":
            self.resilience_leveler = round(self.resilience_leveler + 0.1, 4)
            self.resilience = int(100 * self.resilience_leveler)
            upgraded = True

        if upgraded:
            self.unspent_stat_points -= 1
            return True
        return False

    def show_level_up_message(self, screen):
        level_up_text = large_font.render(
            f"You leveled up to level {self.level}! Upgrade stats in inventory!",
            True, (20, 255, 20)
        )
        screen.blit(level_up_text, (
            screen.get_width() // 2 - level_up_text.get_width() // 2,
            20
        ))

    def get_speed(self):
        speed = self.base_speed * (self.speed / 100)
        weight_ratio = self.weight / self.max_weight if self.max_weight > 0 else 0
        if weight_ratio >= 1:
            weight_multiplier = 0
        elif weight_ratio >= 0.95:
            weight_multiplier = 0.25
        elif weight_ratio >= 0.9:
            weight_multiplier = 0.5
        else:
            weight_multiplier = 1
        speed = speed * weight_multiplier
        speed *= getattr(self, "ground_slow_factor", 1.0)
        return speed

    def regain_health(self, dt):
        if 1 <= self.health <= self.max_health:
            if not self.poison:
                if self.hunger == self.max_hunger:
                    self.health += dt / 2
                elif self.hunger > self.max_hunger * .7:
                    self.health += dt / 4
                elif self.hunger > self.max_hunger * .4:
                    self.health += dt / 8
                elif self.hunger > self.max_hunger * .1:
                    self.health += dt / 12
                else:
                    self.health -= dt / 8
            if self.hunger == 100:
                self.full_timer -= dt
                if self.full_timer <= 0:
                    self.hunger -= dt/100
            else:
                if self.hunger > 0:
                    self.hunger -= dt / 30
        if self.health < 0:
            self.health = 0
        if self.hunger < 0:
            self.hunger = 0

    def regain_stamina(self, dt, screen):
        if self.stamina_timer > 0:
            self.stamina_timer -= dt
            return
        
        if self.stamina < self.max_stamina:
            if self.thirst == self.max_thirst:
                self.stamina += dt * 16
            elif self.thirst > self.max_thirst * 0.7:
                self.stamina += dt * 10
            elif self.thirst > self.max_thirst * 0.4:
                self.stamina += dt * 6
            elif self.thirst > self.max_thirst * 0.1:
                self.stamina += dt * 2
            else:
                self.stamina -= dt / 12
                self.health -= dt / 12

        if self.thirst == 100:
            self.thirst_full_timer -= dt
            if self.thirst_full_timer <= 0:
                self.thirst -= dt / 100
        elif self.thirst > 0:
            self.thirst -= dt / 40

        if self.stamina > 10 and self.speed < 100:
            self.speed = 100
        
        if self.stamina < 0:
            self.stamina = 0
        if self.health < 0:
            self.health = 0
        if self.thirst < 0:
            self.thirst = 0

    def lose_stamina(self, screen, dt):
        stamina_depleted = False
        if self.stamina > 0:
            self.stamina -= dt * 6
            if self.stamina <= 0:
                self.stamina = 0
                stamina_depleted = True
                self.stamina_timer = 2.0
        return stamina_depleted

    def stamina_speed(self):
        if self.stamina <= 0:
            self.speed = 30
            self.exhausted = True
        elif self.stamina <= 10: 
            self.speed = 40
            self.exhausted = False
        elif self.stamina <= 20: 
            self.speed = 60
            self.exhausted = False
        else:
            self.speed = 100
            self.exhausted = False

    def lose_hunger(self, dt):
        if self.hunger > 0:
            if self.hunger == 100:
                self.full_timer -= dt
                if self.full_timer <= 0:
                    self.hunger -= dt/100
            else:
                self.hunger -= dt / 100
                self.full_timer = 60
        if self.hunger < 0:
            self.hunger = 0
            

    def lose_thirst(self, dt):
        if self.thirst > 0:
            if self.thirst == 100:
                self.thirst_full_timer -= dt
                if self.thirst_full_timer <= 0:
                    self.thirst -= dt/100
            else:
                self.thirst -= dt / 100
                self.thirst_full_timer = 60
        if self.thirst < 0:
            self.thirst = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1,5)]))

    def clamp_stats(self):
        if self.health < 0:
            self.health = 0
        if self.health > self.max_health:
            self.health = self.max_health
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger > self.max_hunger:
            self.hunger = self.max_hunger
        if self.stamina < 0:
            self.stamina = 0
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina
        if self.thirst < 0:
            self.thirst = 0
        if self.thirst > self.max_thirst:
            self.thirst = self.max_thirst

    def feed_cat(self, cat):
        pass

    def health_bar(self, screen):
        max_health = self.max_health
        health = self.health
        bar_width = self.max_health * .5
        bar_height = 18
        x = 43
        y = 64

        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if self.poison:
            pygame.draw.rect(screen, (150, 80, 200), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        else:
            if health_ratio > .4:
                pygame.draw.rect(screen, (200, 40, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
            else:
                pygame.draw.rect(screen, (255, 80, 60), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        health_text = f"{int(health)} / {max_health}"
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(health_text, True, (255, 255, 255))
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def stamina_bar(self, screen):
        max_stamina = self.max_stamina
        stamina = self.stamina
        bar_width = max_stamina * .5
        bar_height = 18
        x = 43
        y = 82

        stamina_ratio = stamina / max_stamina
        stamina_width = int(bar_width * stamina_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if stamina_ratio > .4:
            pygame.draw.rect(screen, (140, 230, 100), pygame.Rect(x, y, stamina_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (90, 180, 60), pygame.Rect(x, y, stamina_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        stamina_text = f"{int(stamina)} / {max_stamina}"
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(stamina_text, True, (255, 255, 255))
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def hunger_bar(self, screen):
        max_hunger = self.max_hunger
        hunger = self.hunger
        bar_width = max_hunger * .5
        bar_height = 18
        x = 43
        y = 100

        hunger_ratio = hunger / max_hunger
        hunger_width = int(bar_width * hunger_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if hunger_ratio > .4:
            pygame.draw.rect(screen, (240, 128, 0), pygame.Rect(x, y, hunger_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (200, 100, 40), pygame.Rect(x, y, hunger_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        hunger_text = f"{int(hunger)} / {max_hunger}"
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(hunger_text, True, (255, 255, 255))
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def thirst_bar(self, screen):
        max_thirst = self.max_thirst
        thirst = self.thirst
        bar_width = self.max_thirst * .5
        bar_height = 18
        x = 43
        y = 118

        thirst_ratio = thirst / max_thirst
        thirst_width = int(bar_width * thirst_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if thirst_ratio > .4:
            pygame.draw.rect(screen, (0, 40, 255), pygame.Rect(x, y, thirst_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (100, 100, 255), pygame.Rect(x, y, thirst_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        thirst_text = f"{int(thirst)} / {max_thirst}"
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(thirst_text, True, (255, 255, 255))
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def exp_bar(self, screen):
        from inventory import hotbar_image
        next_level_exp = self.next_level_exp
        experience = self.experience
        bar_width = hotbar_image.get_width()
        bar_height = 5
        x = screen.get_width()//2 - bar_width // 2
        y = screen.get_height() - 75

        safe_next = next_level_exp if next_level_exp > 0 else 1
        experience_ratio = experience / safe_next
        if not math.isfinite(experience_ratio):
            experience_ratio = 1
        experience_ratio = max(0, min(experience_ratio, 1))
        experience_width = int(bar_width * experience_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if experience_ratio < .97:
            pygame.draw.rect(screen, (20, 255, 20), pygame.Rect(x, y, experience_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (160, 120, 255), pygame.Rect(x, y, experience_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

    def get_collision_rect(self, cam_x):
        return pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.width, self.rect.height)
