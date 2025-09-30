import pygame
import random


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


