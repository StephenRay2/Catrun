import pygame
import random

rock_images = ["/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock1.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock2.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock3.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock4.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/Rock6.png"]

tree_images = ["/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/AppleTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/BareAppleTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/DuskwoodTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/FirTree.png", "/Users/stephenray/CodeProjects/Catrun/assets/sprites/biomes/grassland/OakTree.png"]

class Rock():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
        chosen_image = random.choice(rock_images)
        self.image = pygame.image.load(chosen_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = (x, y))


    def draw(self, screen, cam_x, cam_y=0):
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        screen.blit(self.image, (screen_x, screen_y))


class Tree():
    def __init__(self, x, y):
        self.x = x
        self.y = y


        chosen_image = random.choice(tree_images)
        self.image = pygame.image.load(chosen_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 128))
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self, screen, cam_x, cam_y=0):
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        screen.blit(self.image, (screen_x, screen_y))
