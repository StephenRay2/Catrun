import pygame
from world import *


class Button:
    def __init__(self, x, y, image, hover_color=(255, 255, 255, 20)):
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hover_color = hover_color  

    def draw(self, screen):
        if self.is_hovered():
            hover_img = self.image.copy()
            hover_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            hover_surface.fill(self.hover_color)
            hover_img.blit(hover_surface, (0, 0))
            screen.blit(hover_img, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN 
            and event.button == 1 
            and self.rect.collidepoint(event.pos)
        )

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


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

load_button = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/LoadGameButton.png").convert_alpha(), (350, 82))
menu_quit_button = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/MenuQuitButton.png").convert_alpha(), (350, 82))
menu_settings_button = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/MenuSettingsButton.png").convert_alpha(), (350, 82))
new_game_button = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/NewGameButton.png").convert_alpha(), (350, 82))

new_game_button = Button(width//2 - new_game_button.get_width()//2, height//2 - 50, new_game_button)
load_button = Button(width//2 - load_button.get_width()//2, height//2 + 50, load_button)
menu_settings_button = Button(width//2 - menu_settings_button.get_width()//2, height//2 + 150, menu_settings_button)
menu_quit_button = Button(width//2 - menu_quit_button.get_width()//2, height//2 + 250, menu_quit_button)
