import pygame
import random


cat_types = [
    {"type":"black", "walk_right_image1" : "assets/sprites/mobs/BlackCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/BlackCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/BlackCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/BlackCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/BlackCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/BlackCatRightStanding.png"}, 
    {"type":"salt_and_pepper", "walk_right_image1" : "assets/sprites/mobs/SandPCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandPCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandPCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandPCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandPCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandPCatRightStanding.png"},
    {"type":"white", "walk_right_image1" : "assets/sprites/mobs/WhiteCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WhiteCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WhiteCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WhiteCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WhiteCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WhiteCatRightStanding.png"}]


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

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y

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

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    def update(self, dt):
        if self.move_timer <= 0:
            if random.randint(0, 100) < 2:  # chance to move
                self.direction.x = random.choice([-1, 0, 1])
                self.direction.y = random.choice([-1, 0, 1])
                self.move_timer = random.randint(30, 120)
            else:
                self.direction.x = 0
                self.direction.y = 0
        else:
            self.move_timer -= 1

        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        if self.direction.x > 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_right_frames):
                self.frame_index = 0
            self.image = self.walk_right_frames[int(self.frame_index)]

        elif self.direction.x < 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_left_frames):
                self.frame_index = 0
            self.image = self.walk_left_frames[int(self.frame_index)]

        else:
            if self.direction.y >= 0:
                self.image = self.stand_right_image
            else:
                self.image = self.stand_left_image
