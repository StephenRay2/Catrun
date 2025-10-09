import pygame
import random


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
        self.image = pygame.Surface((48, 48))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(center=(x, y)).inflate(-10, -20)

        self.max_health = 100
        self.health = 100
        self.max_stamina = 100
        self.stamina = 100
        self.max_hunger = 100
        self.hunger = 100
        self.max_warmth = 100
        self.warmth = 100
        self.attack = 100
        self.speed = 100
        self.defense = 100
        self.level = 1
        self.experience = 0

        self.inventory = []
        self.is_alive = True
        self.is_attacking = False
        self.direction = pygame.Vector2(0, 0)

    def feed_cat(self, cat):
        pass


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

    