# Compute next_level_exp per level for the provided leveling rule.
# Start next_level_exp at 100, req_multiplier at 0.5. Apply bracketed decrements.
import pygame
pygame.font.init()

font = pygame.font.Font("assets\Fonts\GFSDidot-Regular.ttf", 16)
font_path = "assets\Fonts\GFSDidot-Regular.ttf"


# next_level_exp = 100.0
# req_multiplier = 0.5
# levels = []
# for lvl in range(1, 100):
#     next_level_exp = next_level_exp + next_level_exp * req_multiplier
#     levels.append((lvl, next_level_exp))
#     if lvl <= 10:
#         req_multiplier -= 0.034
#     elif lvl <= 20:
#         req_multiplier -= 0.012
#     elif lvl <= 30:
#         req_multiplier -= 0.0005
#     elif lvl <= 40:
#         req_multiplier -= 0.0004
#     elif lvl <= 50:
#         req_multiplier -= 0.00019
#     elif lvl <= 60:
#         req_multiplier -= 0.00009
#     elif lvl <= 70:
#         req_multiplier -= 0.00008
#     elif lvl <= 80:
#         req_multiplier -= 0.00007
#     elif lvl < 100:
#         req_multiplier -= 0.00003

# for lvl, exp in levels[:50]:
#     print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))
# print('...')
# for lvl, exp in levels[50:60]:
#     print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))
# print('...')
# for lvl, exp in levels[60:90]:
#     print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))
# print('...')
# for lvl, exp in levels[90:99]:
#     print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))