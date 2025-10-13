import pygame
import random

font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 40)
xl_font = pygame.font.Font(None, 100)
class TempPlayerCollision:
                    def __init__(self, x, y, width, height):
                        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)

cat_types = [
    {"type":"black", "walk_right_image1" : "assets/sprites/mobs/BlackCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/BlackCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/BlackCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/BlackCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/BlackCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/BlackCatRightStanding.png"}, 
    {"type":"salt_and_pepper", "walk_right_image1" : "assets/sprites/mobs/SandPCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandPCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandPCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandPCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandPCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandPCatRightStanding.png"},
    {"type":"white", "walk_right_image1" : "assets/sprites/mobs/WhiteCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WhiteCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WhiteCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WhiteCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WhiteCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WhiteCatRightStanding.png"}, {"type":"white_and_black", "walk_right_image1" : "assets/sprites/mobs/WandBCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WandBCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WandBCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WandBCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WandBCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WandBCatRightStanding.png"}, {"type":"sandy", "walk_right_image1" : "assets/sprites/mobs/SandyCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandyCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandyCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandyCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandyCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandyCatRightStanding.png"}, {"type":"orange", "walk_right_image1" : "assets/sprites/mobs/OrangeCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/OrangeCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/OrangeCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/OrangeCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/OrangeCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/OrangeCatRightStanding.png"}, {"type":"calico", "walk_right_image1" : "assets/sprites/mobs/CalicoCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/CalicoCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/CalicoCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/CalicoCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/CalicoCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/CalicoCatRightStanding.png"}]


squirrel_move_images = ["assets/sprites/mobs/SquirrelMove1.png", "assets/sprites/mobs/SquirrelMove2.png", "assets/sprites/mobs/SquirrelMove3.png", "assets/sprites/mobs/SquirrelMove4.png", "assets/sprites/mobs/SquirrelMove5.png", "assets/sprites/mobs/SquirrelMove6.png"]

squirrel_stand_image = "assets/sprites/mobs/SquirrelStand1.png"

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
        self.max_health = 100 * self.health_leveler
        self.health = 10
        self.stamina_leveler = 1
        self.max_stamina = 100 * self.stamina_leveler
        self.stamina = 10
        self.hunger_leveler = 1
        self.max_hunger = 100 * self.hunger_leveler
        self.hunger = 0
        self.full_timer = 60
        self.water_leveler = 1
        self.max_water = 100 * self.water_leveler
        self.water = 100
        self.water_full_timer = 60
        self.warmth_leveler = 1
        self.max_warmth = 100
        self.warmth = 100
        self.attack = 1
        self.base_speed = 350
        self.speed = 1
        self.defense = 1
        self.level = 1
        self.experience = 0
        self.exp_total = 0
        self.next_level_exp = 100
        self.level_up_timer = 0

        self.inventory = []
        self.is_alive = True
        self.is_attacking = False
        self.direction = pygame.Vector2(0, 0)

        self.dead = False
        self.score = 0

    def determine_score(self, dungeon_depth):
        return int(self.exp_total / 100) + int(dungeon_depth)

    def print_score(self, screen, dungeon_depth):
        score_text = font.render(f"Score: {self.determine_score(dungeon_depth)}", True, (255, 255, 255))
        x = screen.get_width() - score_text.get_width() - 20
        y = 20
        temp_surface = pygame.Surface((score_text.get_width() + 10, score_text.get_height() + 10), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 100))
        screen.blit(temp_surface, (x - 5, y - 5))
        screen.blit(score_text, (x, y))
        
    def is_dead(self, screen, dungeon_depth):
        game_over_text =xl_font.render("YOU DIED. GAME OVER.", True, (255, 20, 20))
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

    def get_speed(self):
        return self.base_speed * self.speed

    def regain_health(self, dt):
        if 0 < self.health < self.max_health:
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

    def regain_stamina(self, dt):
        if self.stamina < self.max_stamina:
            if self.water == self.max_water:
                self.stamina += dt * 16
            elif self.water > self.max_water * .7:
                self.stamina += dt * 10
            elif self.water > self.max_water * .4:
                self.stamina += dt * 6
            elif self.water > self.max_water * .1:
                self.stamina += dt * 2
            else:
                self.stamina -= dt / 12
                self.health -= dt / 12
            if self.water == 100:
                self.water_full_timer -= dt
                if self.water_full_timer <= 0:
                    self.water -= dt/100
            else:
                if self.water > 0:
                    self.water -= dt / 30

        if self.stamina > 10 and self.speed < 1:
                self.speed = 1


    def lose_stamina(self, dt):
        if self.stamina > 0:
            self.stamina -= dt * 6
        

    def stamina_speed(self):
        if self.stamina <= 10: 
            self.speed = .4
        elif self.stamina <= 20: 
            self.speed = .6
        else:
            self.speed = 1

    def lose_hunger(self, dt):
        if self.hunger > 0:
            if self.hunger == 100:
                self.full_timer -= dt
                if self.full_timer <= 0:
                    self.hunger -= dt/100
            else:
                self.hunger -= dt / 100
                self.full_timer = 60
            

    def lose_water(self, dt):
        if self.water > 0:
            if self.water == 100:
                self.water_full_timer -= dt
                if self.water_full_timer <= 0:
                    self.water -= dt/100
            else:
                self.water -= dt / 100
                self.water_full_timer = 60

    def level_up(self, screen):
            self.level += 1
            self.exp_total += self.next_level_exp
            if self.level <= 10:
                self.next_level_exp = int(100 + (self.exp_total * 0.3))
            elif self.level <= 30:
                self.next_level_exp = int(200 + (self.exp_total * 0.122))
            elif self.level <= 50:
                self.next_level_exp = int(500 + (self.exp_total * 0.045))
            elif self.level <= 70:
                self.next_level_exp = int(1000 + (self.exp_total * 0.01))
            elif self.level <= 100:
                self.next_level_exp = int(1500 + (self.exp_total * 0.007))
            self.level_up_timer = 10

        

    def show_level_up_message(self, screen):
        level_up_text = large_font.render(
            f"Corynn leveled up to level {self.level}! Upgrade stats in inventory!",
            True, (20, 255, 20)
        )
        screen.blit(level_up_text, (
            screen.get_width() // 2 - level_up_text.get_width() // 2,
            20
        ))



    def feed_cat(self, cat):
        pass

    def health_bar(self, screen):
        max_health = self.max_health
        health = self.health
        bar_width = self.max_health * 2
        bar_height = 18
        x = 43
        y = 64

        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if health_ratio > .4:
            pygame.draw.rect(screen, (200, 40, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (255, 80, 60), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        health_text = f"{int(health)} / {max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))

    def stamina_bar(self, screen):
        max_stamina = self.max_stamina
        stamina = self.stamina
        bar_width = max_stamina * 2
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
        text_surface = font.render(stamina_text, True, (255, 255, 255))
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))


    def hunger_bar(self, screen):
        max_hunger = self.max_hunger
        hunger = self.hunger
        bar_width = max_hunger * 2
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
        text_surface = font.render(hunger_text, True, (255, 255, 255))
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))

    def water_bar(self, screen):
        max_water = self.max_water
        water = self.water
        bar_width = self.max_water * 2
        bar_height = 18
        x = 43
        y = 118

        water_ratio = water / max_water
        water_width = int(bar_width * water_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if water_ratio > .4:
            pygame.draw.rect(screen, (0, 40, 255), pygame.Rect(x, y, water_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (100, 100, 255), pygame.Rect(x, y, water_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        water_text = f"{int(water)} / {max_water}"
        text_surface = font.render(water_text, True, (255, 255, 255))
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))

    def exp_bar(self, screen):
        next_level_exp = self.next_level_exp
        experience = self.experience
        bar_width = 800
        bar_height = 5
        x = screen.get_width()//2 - 400
        y = screen.get_height() - 105

        experience_ratio = experience / next_level_exp
        experience_width = int(bar_width * experience_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if experience_ratio < .97:
            pygame.draw.rect(screen, (20, 255, 20), pygame.Rect(x, y, experience_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (160, 120, 255), pygame.Rect(x, y, experience_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)



class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.collision_rect = None
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.frame_index = 0
        self.animation_speed = 0.15
        self.last_direction = "right"

    def get_collision_rect(self, cam_x):
        rect = self.collision_rect or self.rect
        return pygame.Rect(rect.x - cam_x, rect.y, rect.width, rect.height)

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.move_timer <= 0:
            if random.random() < 0.02:
                self.direction.xy = random.choice([(-1,0), (1,0), (0,-1), (0,1), (0,0)])
                self.move_timer = random.randint(30, 120)
            else:
                self.direction.xy = (0, 0)
        else:
            self.move_timer -= 1

        if self.direction.length_squared() == 0:
            self.animate_stand()
            return

        test_rect = self.rect.move(self.direction.x, self.direction.y)
        collision = any(self.check_collision(test_rect, obj.rect) for obj in (nearby_objects or []))
        if not collision:
            collision = any(self.check_collision(test_rect, mob.get_collision_rect(0)) 
                            for mob in (nearby_mobs or []) if mob is not self)

        if not collision:
            self.rect = test_rect

        self.animate_walk()

    def check_collision(self, test_rect, other_rect):
        if not test_rect.colliderect(other_rect):
            return False
        current_dist = self.distance(self.rect.center, other_rect.center)
        new_dist = self.distance(test_rect.center, other_rect.center)
        return new_dist < current_dist

    def distance(self, a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

    def animate_walk(self):
        if self.direction.x > 0:
            self.animate_frames("right")
        elif self.direction.x < 0:
            self.animate_frames("left")
        elif self.direction.y != 0:
            self.animate_frames(self.last_direction)
        else:
            self.animate_stand()

    def animate_frames(self, direction):
        self.last_direction = direction
        self.frame_index = (self.frame_index + self.animation_speed) % len(self.walk_right_frames)
        frames = self.walk_right_frames if direction == "right" else self.walk_left_frames
        self.image = frames[int(self.frame_index)]

    def animate_stand(self):
        self.image = self.stand_right_image if self.last_direction == "right" else self.stand_left_image

class Cat(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.cat_type = random.choice(cat_types)

        self.walk_right_frames = [pygame.image.load(self.cat_type[f"walk_right_image{i}"]).convert_alpha() for i in range(1, 6)]
        self.stand_right_image = pygame.image.load(self.cat_type[f"stand_right_image"]).convert_alpha()

        self.walk_left_frames = [pygame.transform.flip(img, True, False) for img in self.walk_right_frames]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center = (x, y))

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 

        self.tame_max = 100
        self.tame = 0
        self.tamed = False

        self.max_health = 100
        self.health = 100
        self.max_hunger = 100
        self.hunger = 100

    def tame_cat(self):
        pass

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))


class Squirrel(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)

        self.walk_right_frames = [pygame.image.load(img).convert_alpha() for img in squirrel_move_images]
        self.stand_right_image = pygame.image.load(squirrel_stand_image).convert_alpha()

        self.walk_left_frames = [pygame.transform.flip(img, True, False) for img in self.walk_right_frames]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    