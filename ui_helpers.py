import pygame


def draw_close_button(screen, panel_rect, size=24, margin=6):
    if panel_rect is None:
        return None

    x = int(panel_rect.right - size - margin)
    y = int(panel_rect.top - size - margin)
    x = max(4, min(x, screen.get_width() - size - 4))
    y = max(4, min(y, screen.get_height() - size - 4))

    rect = pygame.Rect(x, y, size, size)
    hover = rect.collidepoint(pygame.mouse.get_pos())

    bg_alpha = 180 if not hover else 210
    bg_color = (20, 20, 25, bg_alpha)
    border_color = (190, 190, 200, 200)
    line_color = (210, 210, 220) if not hover else (235, 235, 235)

    box = pygame.Surface((size, size), pygame.SRCALPHA)
    box.fill(bg_color)
    pygame.draw.rect(box, border_color, box.get_rect(), 1, border_radius=4)

    pad = max(5, size // 4)
    pygame.draw.line(box, line_color, (pad, pad), (size - pad, size - pad), 2)
    pygame.draw.line(box, line_color, (pad, size - pad), (size - pad, pad), 2)

    screen.blit(box, rect.topleft)
    return rect
