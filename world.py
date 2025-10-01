import pygame
import random

rock_images = ["/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock1.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock2.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock3.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock4.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock6.png"]

tree_images = ["/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/AppleTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/BareAppleTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/DuskwoodTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/FirTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/OakTree.png"]

class Solid(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(), size
        )
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))


class Rock(Solid):
    def __init__(self, x, y):
        img = random.choice(rock_images)
        super().__init__(img, x, y, (64, 64))


class Tree(Solid):
    def __init__(self, x, y):
        img = random.choice(tree_images)
        super().__init__(img, x, y, (64, 128))
        self.image_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y + 64, 64, 64)
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.image_rect.x - cam_x, self.image_rect.y))