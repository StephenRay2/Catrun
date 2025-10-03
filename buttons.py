import pygame


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
