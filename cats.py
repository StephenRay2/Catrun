import pygame
import random
import os
from world import screen
from sounds import sound_manager
from debug import font_path, font
from mobs import Mob
from player import Player

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


cat_types = [
    {"type":"black", "walk_right_image1" : "assets/sprites/mobs/BlackCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/BlackCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/BlackCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/BlackCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/BlackCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/BlackCatRightStanding.png", "dead_image": "assets/sprites/mobs/BlackCatDead.png", "caged1": "black_cat_caged_left", "caged2": "black_cat_caged_right"}, 
    {"type":"salt_and_pepper", "walk_right_image1" : "assets/sprites/mobs/SandPCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandPCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandPCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandPCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandPCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandPCatRightStanding.png", "dead_image": "assets/sprites/mobs/SandPCatDead.png", "caged1": "SandP_cat_caged_left", "caged2": "SandP_cat_caged_right"},
    {"type":"white", "walk_right_image1" : "assets/sprites/mobs/WhiteCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WhiteCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WhiteCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WhiteCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WhiteCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WhiteCatRightStanding.png", "dead_image": "assets/sprites/mobs/WhiteCatDead.png", "caged1": "white_cat_caged_left", "caged2": "white_cat_caged_right"}, 
    {"type":"white_and_black", "walk_right_image1" : "assets/sprites/mobs/WandBCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WandBCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WandBCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WandBCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WandBCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WandBCatRightStanding.png", "dead_image": "assets/sprites/mobs/WandBCatDead.png", "caged1": "WandB_cat_caged_left", "caged2": "WandB_cat_caged_right"}, 
    {"type":"sandy", "walk_right_image1" : "assets/sprites/mobs/SandyCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandyCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandyCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandyCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandyCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandyCatRightStanding.png", "dead_image": "assets/sprites/mobs/SandyCatDead.png", "caged1": "sandy_cat_caged_left", "caged2": "sandy_cat_caged_right"}, 
    {"type":"orange", "walk_right_image1" : "assets/sprites/mobs/OrangeCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/OrangeCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/OrangeCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/OrangeCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/OrangeCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/OrangeCatRightStanding.png", "dead_image": "assets/sprites/mobs/OrangeCatDead.png", "caged1": "orange_cat_caged_left", "caged2": "orange_cat_caged_right"}, 
    {"type":"calico", "walk_right_image1" : "assets/sprites/mobs/CalicoCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/CalicoCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/CalicoCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/CalicoCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/CalicoCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/CalicoCatRightStanding.png", "dead_image": "assets/sprites/mobs/CalicoCatDead.png", "caged1": "calico_cat_caged_left", "caged2": "calico_cat_caged_right"}, 
    {"type":"gray", "walk_right_image1" : "assets/sprites/mobs/GrayCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/GrayCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/GrayCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/GrayCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/GrayCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/GrayCatRightStanding.png", "dead_image": "assets/sprites/mobs/GrayCatDead.png", "caged1": "gray_cat_caged_left", "caged2": "gray_cat_caged_right"}, 
    {"type":"white_and_orange", "walk_right_image1" : "assets/sprites/mobs/WandOCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WandOCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WandOCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WandOCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WandOCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WandOCatRightStanding.png", "dead_image": "assets/sprites/mobs/WandOCatDead.png", "caged1": "WandO_cat_caged_left", "caged2": "WandO_cat_caged_right"}]


def _load_cat_attack_paths(prefix):
    """Load all right-facing attack frame paths for a cat sprite prefix.
    Each cat can have a different number of attack frames; detect them dynamically.
    """
    paths = []
    index = 1
    while True:
        path = f"assets/sprites/mobs/{prefix}RightAttack{index}.png"
        if not os.path.exists(path):
            break
        paths.append(path)
        index += 1
    return paths


CAT_ATTACK_IMAGE_PATHS = {
    "black": _load_cat_attack_paths("BlackCat"),
    "salt_and_pepper": _load_cat_attack_paths("SandPCat"),
    "white": _load_cat_attack_paths("WhiteCat"),
    "white_and_black": _load_cat_attack_paths("WandBCat"),
    "sandy": _load_cat_attack_paths("SandyCat"),
    "orange": _load_cat_attack_paths("OrangeCat"),
    "calico": _load_cat_attack_paths("CalicoCat"),
    "gray": _load_cat_attack_paths("GrayCat"),
    "white_and_orange": _load_cat_attack_paths("WandOCat"),
}


class Cat(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.cat_type = random.choice(cat_types)

        self.walk_right_images = [pygame.image.load(self.cat_type[f"walk_right_image{i}"]).convert_alpha() for i in range(1, 6)]
        self.stand_right_image = pygame.image.load(self.cat_type[f"stand_right_image"]).convert_alpha()

        type_key = self.cat_type.get("type")
        attack_paths = CAT_ATTACK_IMAGE_PATHS.get(type_key, [])
        self.attack_right_images = [pygame.image.load(path).convert_alpha() for path in attack_paths]
        self.attack_left_images = [pygame.transform.flip(img, True, False) for img in self.attack_right_images]

        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center = (x, y))

        self.frame_index = 0
        self.animation_speed = 0.25
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 

        self.tame_max = 100 * (1 + (self.level * 0.05))
        self.tame = 0
        self.tamed = False
        self.just_tamed = False
        self.cat_name = None
        self.poison = False
        self.poison_time = 0
        self.poison_strength = 0
        self.poison_damage_timer = 0
        self.poison_damage_rate = 1.5
        self.death_experience = int(200  * (1 + (self.level * 0.05)))
        self.level = 1
        self.experience = 0
        self.next_level_exp = 100
        self.unspent_stat_points = 0
        self.tamed_boost = 1.1
        self.meat_resource = "Raw Small Meat"
        self.special_drops = [{'item': 'Fur', 'chance': 0.1, 'min': 1, 'max': 2}]

        self.health_leveler = 1.0
        self.attack_leveler = 1.0
        self.speed_leveler = 1.0
        self.defense_leveler = 1.0
        self.hunger_leveler = 1.0

        self.full_health = 100 + (random.randint(3, 7) * self.level) * self.tamed_boost * self.health_leveler
        self.health = self.full_health
        self.max_health = self.full_health
        self.max_hunger = int(100 * self.hunger_leveler)
        self.hunger = self.max_hunger
        self.untamed_base_speed = 150
        self.tamed_base_speed = 275
        self.base_speed = self.untamed_base_speed
        self.speed_stat = 100
        self.speed = self.speed_stat / 100.0
        self.attack = max(5, int(self.level * 4 * self.attack_leveler))
        self.defense = max(5, int(self.level * 5 * self.defense_leveler))

        self._exp_time_accumulator = 0.0

        self.attacking = False
        self.attack_timer = 0.0
        if self.attack_right_images:
            self.attack_duration = max(0.5, 0.12 * len(self.attack_right_images))
        else:
            self.attack_duration = 0.5
        self.attack_has_hit = False

        self.dead_cat_right_image = pygame.image.load(self.cat_type["dead_image"]).convert_alpha()
        self.dead_cat_left_image = pygame.transform.flip(self.dead_cat_right_image, True, False)
        
        self.tame_bar_timer = 0
        self.tame_bar_display_time = 2.0
        
        self.follow_player = True
        self.sit = False
        self.wander = False
        self.passive = False
        self.follow_radius = 140
        self.target_enemy = None

    def _apply_tame_speed(self):
        """Update base speed based on whether the cat is tamed."""
        self.base_speed = self.tamed_base_speed if self.tamed else self.untamed_base_speed

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        from mobs import Redmite, Squirrel
        from player import Player
        
        if self.tame_bar_timer > 0:
            self.tame_bar_timer -= dt

        if self.is_alive:
            self._exp_time_accumulator += dt
            while self._exp_time_accumulator >= 1.0:
                self._exp_time_accumulator -= 1.0
                self.gain_experience(0.5)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_cat_right_image
            else:
                self.image = self.dead_cat_left_image
            return

        if self.attacking:
            self._update_attack_animation(dt)
            return

        if nearby_mobs:
            threats = [
                m for m in nearby_mobs
                if m is not self
                and getattr(m, "is_alive", True)
                and (
                    getattr(m, "target", None) is self
                    or (hasattr(m, "attackers") and self in getattr(m, "attackers", set()))
                    or (hasattr(self, "attackers") and m in getattr(self, "attackers", set()))
                )
            ]
            if threats:
                self.target_enemy = min(
                    threats,
                    key=lambda m: (m.rect.centerx - self.rect.centerx) ** 2 + (m.rect.centery - self.rect.centery) ** 2,
                )

        if not self.tamed:
            if not self.target_enemy or not getattr(self.target_enemy, "is_alive", True):
                prey = [m for m in (nearby_mobs or []) if isinstance(m, (Redmite, Squirrel)) and getattr(m, "is_alive", True)]
                if prey:
                    nearest = min(prey, key=lambda m: (m.rect.centerx - self.rect.centerx) ** 2 + (m.rect.centery - self.rect.centery) ** 2)
                    self.target_enemy = nearest
                else:
                    self.target_enemy = None

            if self.target_enemy and getattr(self.target_enemy, "is_alive", True):
                enemy_dx = self.target_enemy.rect.centerx - self.rect.centerx
                enemy_dy = self.target_enemy.rect.centery - self.rect.centery
                enemy_distance = (enemy_dx**2 + enemy_dy**2) ** 0.5

                if enemy_distance > 80:
                    if enemy_distance > 0:
                        enemy_direction = pygame.Vector2(enemy_dx, enemy_dy).normalize()
                        self.direction = enemy_direction
                        self.speed = 1.2
                    self.move_timer = 0
                else:
                    if not self.attacking:
                        self.attacking = True
                        self.attack_timer = self.attack_duration
                        self.attack_has_hit = False
                        self.frame_index = 0.0
                        self.last_direction = "right" if enemy_dx >= 0 else "left"
                        self.direction = pygame.Vector2(0, 0)
                        return

        if self.tamed and player and self.follow_player:
            player_world_x = getattr(player, "world_x", player.rect.centerx)
            player_world_y = getattr(player, "world_y", player.rect.centery)

            if nearby_mobs:
                preferred_targets = [m for m in nearby_mobs if isinstance(m, (Redmite, Squirrel)) and getattr(m, "is_alive", True)]
                if preferred_targets:
                    nearest = min(preferred_targets, key=lambda m: (m.rect.centerx - self.rect.centerx) ** 2 + (m.rect.centery - self.rect.centery) ** 2)
                    self.target_enemy = nearest
                for mob in nearby_mobs:
                    if mob is self or not getattr(mob, "is_alive", True):
                        continue
                    if hasattr(mob, 'target') and mob.target == player:
                        self.target_enemy = mob
                        break
                    if hasattr(player, 'attacking_target') and player.attacking_target == mob:
                        self.target_enemy = mob
                        break

            if self.target_enemy and getattr(self.target_enemy, "is_alive", True):
                enemy_dx = self.target_enemy.rect.centerx - self.rect.centerx
                enemy_dy = self.target_enemy.rect.centery - self.rect.centery
                enemy_distance = (enemy_dx**2 + enemy_dy**2) ** 0.5

                if enemy_distance > 80:
                    if enemy_distance > 0:
                        enemy_direction = pygame.Vector2(enemy_dx, enemy_dy).normalize()
                        self.direction = enemy_direction
                        self.speed = 1.5
                    self.move_timer = 0
                else:
                    if not self.attacking:
                        self.attacking = True
                        self.attack_timer = self.attack_duration
                        self.attack_has_hit = False
                        self.frame_index = 0.0
                        self.last_direction = "right" if enemy_dx >= 0 else "left"
                        self.direction = pygame.Vector2(0, 0)
                        return
            else:
                if self.target_enemy and not getattr(self.target_enemy, "is_alive", False):
                    self.target_enemy = None

                dx = player_world_x - self.rect.centerx
                dy = player_world_y - self.rect.centery
                distance = (dx**2 + dy**2) ** 0.5

                if distance > self.follow_radius:
                    if distance > 0:
                        direction = pygame.Vector2(dx, dy).normalize()
                        extra_mult = min(1.5, max(0.0, (distance - self.follow_radius) / 300.0))
                        self.speed = 1.0 + extra_mult
                        self.direction = direction
                    else:
                        self.direction = pygame.Vector2(0, 0)
                        self.speed = 1.0
                else:
                    if self.wander and distance > 40:
                        if self.move_timer <= 0:
                            self.direction = pygame.Vector2(random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)]))
                            self.move_timer = random.randint(60, 180)
                            self.speed = 0.7
                        self.move_timer -= 1
                    else:
                        self.direction = pygame.Vector2(0, 0)
                        self.speed = 1.0

        Mob.update(self, dt, player, nearby_objects, nearby_mobs, player_sleeping)

    def get_collision_rect(self, cam_x):
        """Smaller collision box near the bottom-center of the cat sprite."""
        rect = self.rect
        width = int(rect.width * 0.4)
        height = int(rect.height * 0.35)
        x_offset = (rect.width - width) // 2
        y_offset = rect.height - height
        return pygame.Rect(rect.x - cam_x + x_offset, rect.y + y_offset, width, height)

    def _update_attack_animation(self, dt):
        """Play the cat's attack animation and apply damage to its target."""
        from player import Player
        
        if self.last_direction == "right":
            frames = getattr(self, "attack_right_images", [])
        else:
            frames = getattr(self, "attack_left_images", [])

        if frames:
            effective_speed = self.animation_speed * 0.4
            self.frame_index = (self.frame_index + effective_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
        else:
            self.image = self.stand_right_image if self.last_direction == "right" else self.stand_left_image

        if self.target_enemy and getattr(self.target_enemy, "is_alive", True):
            if not self.attack_has_hit and self.attack_timer <= self.attack_duration * 0.5:
                if isinstance(self.target_enemy, Player):
                    self.attacking = False
                    self.target_enemy = None
                    return
                self.target_enemy.health -= self.attack
                if hasattr(self.target_enemy, "register_attack"):
                    self.target_enemy.register_attack(self)
                if self.target_enemy.health <= 0:
                    self.target_enemy.health = 0
                    if hasattr(self.target_enemy, "is_alive"):
                        self.target_enemy.is_alive = False
                self.attack_has_hit = True

        self.attack_timer -= dt
        if (self.attack_timer <= 0 or
                not self.target_enemy or
                not getattr(self.target_enemy, "is_alive", False)):
            self.attacking = False
            self.frame_index = 0.0
            self.attack_has_hit = False

    def feed_cat(self, item_name):
        """Feed the cat with food item. Returns the tame increase amount."""
        tame_increase = 0
        health_increase = 0
        
        if item_name in ["Fish", "Raw Venison", "Raw Lizard Meat", "Raw Beef", "Raw Chicken", "Raw Small Meat", "Raw Bear Meat"]:
            tame_increase = 20
            health_increase = 15
        elif item_name in ["Cooked Fish", "Cooked Venison", "Cooked Lizard Meat", "Cooked Beef", "Cooked Chicken", "Cooked Small Meat", "Cooked Bear Meat"]:
            tame_increase = 15
            health_increase = 15
        elif item_name =="Small Milk":
            tame_increase = 30
            health_increase = 25
        elif item_name == "Medium Glass Milk":
            tame_increase = 60
            health_increase = 50
        elif item_name == "Large Metal Milk":
            tame_increase = 150
            health_increase = 100
        elif item_name == "Poisonous Mushroom":
            tame_increase = -50
            self.poison = True
            self.poison_time = 30
            self.poison_strength = 1
            return 0
        elif item_name in ["Apples", "Oranges", "Coconuts", "Pineapple", "Watermelon", "Mushroom", "Blood Berries", "Dawn Berries", "Dusk Berries", "Sun Berries", "Teal Berries", "Twilight Drupes", "Vio Berries"]:
            tame_increase = 1
            health_increase = 5
        
        if tame_increase > 0:
            self.tame = min(self.tame + tame_increase, self.tame_max)
            self.health = min(self.health + health_increase, self.max_health)
            
            if self.tame >= self.tame_max and not self.tamed:
                self.tamed = True
                self.just_tamed = True
                self._apply_tame_speed()
                self.disable_autonomous_movement = True
            
            sound_manager.play_sound(random.choice(["cat_purr1", "cat_purr2"]))
            self.tame_bar_timer = self.tame_bar_display_time
        
        return tame_increase
    
    def draw_tame_bar(self, screen, cam_x):
        """Draw the taming bar above the cat."""
        if self.tame_bar_timer <= 0:
            return
        
        bar_width = 50
        bar_height = 8
        x = self.rect.centerx - cam_x - bar_width // 2
        y = self.rect.top + 5
        
        pygame.draw.rect(screen, (60, 20, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
        
        tame_ratio = self.tame / self.tame_max
        tame_width = int(bar_width * tame_ratio)
        pygame.draw.rect(screen, (200, 100, 200), pygame.Rect(x, y, tame_width, bar_height), border_radius=2)
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
    
    def draw_cat_name(self, screen, cam_x):
        """Draw the cat's name above its head if it has one."""
        if self.cat_name:
            font = pygame.font.Font(font_path, 12)
            name_text = font.render(str(self.cat_name) + " Lvl " + str(self.level), True, (255, 255, 200))
            text_x = self.rect.centerx - cam_x - name_text.get_width() // 2
            text_y = self.rect.top - 10
            draw_text_with_background(screen, name_text, text_x, text_y)
        
    def draw(self, screen, cam_x):
        self.draw_tame_bar(screen, cam_x)
        self.draw_cat_name(screen, cam_x)
        super().draw(screen, cam_x)

    def get_item_data(self):
        """Create inventory item data for this cat."""
        cat_type = self.cat_type["type"]
        
        cat_type_to_mapping = {
            "black": ("Tamed Black Cat", "assets/sprites/mobs/BlackCatRightStanding.png"),
            "salt_and_pepper": ("Tamed Salt and Pepper Cat", "assets/sprites/mobs/SandPCatRightStanding.png"),
            "white": ("Tamed White Cat", "assets/sprites/mobs/WhiteCatRightStanding.png"),
            "white_and_black": ("Tamed Black and White Cat", "assets/sprites/mobs/WandBCatRightStanding.png"),
            "sandy": ("Tamed Sandy Cat", "assets/sprites/mobs/SandyCatRightStanding.png"),
            "orange": ("Tamed Orange Cat", "assets/sprites/mobs/OrangeCatRightStanding.png"),
            "calico": ("Tamed Calico Cat", "assets/sprites/mobs/CalicoCatRightStanding.png"),
            "gray": ("Tamed Gray Cat", "assets/sprites/mobs/GrayCatRightStanding.png"),
            "white_and_orange": ("Tamed Orange and White Cat", "assets/sprites/mobs/WandOCatRightStanding.png")
        }
        
        item_name, icon = cat_type_to_mapping.get(cat_type, ("Tamed Black Cat", "assets/sprites/mobs/BlackCatRightStanding.png"))
        
        return {
            "item_name": item_name,
            "icon": icon,
            "quantity": 1,
            "cat_object": self,
            "cat_type": cat_type,
            "cat_tame": self.tame,
            "cat_health": self.health,
            "cat_level": self.level,
            "cat_name": self.cat_name
        }

    def level_up(self):
        self.level += 1
        self.unspent_stat_points += 1
        self.next_level_exp = int(100 + (self.level * 120))
        self.experience = 0

    def gain_experience(self, amount):
        """Increase this cat's experience and handle level-ups."""
        if amount <= 0:
            return
        self.experience += amount
        while self.experience >= self.next_level_exp:
            self.experience -= self.next_level_exp
            self.level_up()

    def apply_stat_upgrade(self, stat_key):
        if self.unspent_stat_points <= 0:
            return False

        upgraded = False

        if stat_key == "health":
            self.max_health += 10
            self.health = min(self.health + 10, self.max_health)
            upgraded = True
        elif stat_key == "attack":
            if self.attack < 5:
                self.attack = 5
            self.attack += 2
            upgraded = True
        elif stat_key == "defense":
            if self.defense < 5:
                self.defense = 5
            self.defense += 2
            upgraded = True
        elif stat_key == "hunger":
            self.max_hunger += 10
            self.hunger = min(self.hunger + 10, self.max_hunger)
            upgraded = True

        if not upgraded:
            return False

        self.unspent_stat_points -= 1
        return True
