import pygame
import random
import math
from world import *
from sounds import *
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 40)
xl_font = pygame.font.Font(None, 100)
size = 64

def draw_text_with_background(screen, text_surface, x, y, padding=4):
    """Draw text with a semi-transparent black background box."""
    bg_rect = text_surface.get_rect(topleft=(x, y)).inflate(padding * 2, padding)
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 150))
    screen.blit(bg_surface, bg_rect.topleft)
    screen.blit(text_surface, (x, y))

############ PLAYER IMAGES #################


player_stand_image = pygame.image.load("assets/sprites/player/GlenjaminFrontIdle1.png")
player_stand_image_back = pygame.image.load("assets/sprites/player/GlenjaminUpIdle1.png")
player_stand_left = pygame.transform.flip(pygame.image.load("assets/sprites/player/GlenjaminRightIdle1.png"), True, False)
player_stand_right = pygame.image.load("assets/sprites/player/GlenjaminRightIdle1.png")
player_walk_down_images = [pygame.image.load(f"assets/sprites/player/GlenjaminDownWalk{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_up_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpWalk{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_left_images = [pygame.transform.flip(pygame.image.load(f"assets/sprites/player/GlenjaminRightWalk{i}.png"), True, False).convert_alpha() for i in range(1, 9)]
player_stand_attack_down_images = [pygame.image.load(f"assets/sprites/player/GlenjaminDownAttack{i}.png").convert_alpha() for i in range(1, 5)]
player_stand_attack_up_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpAttack{i}.png").convert_alpha() for i in range(1, 5)]
player_stand_attack_left_images = [pygame.image.load(f"assets/sprites/player/GlenjaminLeftAttack{i}.png").convert_alpha() for i in range(1, 5)]
player_walk_down_attack_images = [pygame.image.load(f"assets/sprites/player/GlenjaminDownWalkAttack{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_up_attack_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpWalkAttack{i}.png").convert_alpha() for i in range(1, 9)]
player_walk_left_attack_images = [pygame.image.load(f"assets/sprites/player/GlenjaminLeftWalkAttack{i}.png").convert_alpha() for i in range(1, 9)]
player_idle_down_images = [pygame.image.load(f"assets/sprites/player/GlenjaminFrontIdle{i}.png").convert_alpha() for i in range(1, 4)]
player_idle_up_images = [pygame.image.load(f"assets/sprites/player/GlenjaminUpIdle{i}.png").convert_alpha() for i in range(1, 4)]
player_idle_left_images = [pygame.transform.flip(pygame.image.load(f"assets/sprites/player/GlenjaminRightIdle{i}.png"), True, False).convert_alpha() for i in range(1, 4)]

player_stand_image = pygame.transform.scale(player_stand_image, (size, size))
player_stand_up = pygame.transform.scale(player_stand_image_back, (size, size))
player_stand_left = pygame.transform.scale(player_stand_left, (size, size))
player_stand_right = pygame.transform.scale(player_stand_right, (size, size))
player_walk_down_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_down_images]
player_walk_up_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_up_images]
player_walk_left_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_left_images]
player_walk_right_images = [pygame.transform.flip(img, True, False) for img in player_walk_left_images]
player_stand_attack_down_images = [pygame.transform.scale(img, (size, size)) for img in player_stand_attack_down_images]
player_stand_attack_up_images  = [pygame.transform.scale(img, (size, size)) for img in player_stand_attack_up_images]
player_stand_attack_left_images  = [pygame.transform.scale(img, (size, size)) for img in player_stand_attack_left_images]
player_stand_attack_right_images = [pygame.transform.flip(img, True, False) for img in player_stand_attack_left_images]
player_walk_down_attack_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_down_attack_images]
player_walk_up_attack_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_up_attack_images]
player_walk_left_attack_images = [pygame.transform.scale(img, (size, size)) for img in player_walk_left_attack_images]
player_walk_right_attack_images = [pygame.transform.flip(img, True, False) for img in player_walk_left_attack_images]
player_idle_down_images = [pygame.transform.scale(img, (size, size)) for img in player_idle_down_images]
player_idle_up_images = [pygame.transform.scale(img, (size, size)) for img in player_idle_up_images]
player_idle_left_images = [pygame.transform.scale(img, (size, size)) for img in player_idle_left_images]
player_idle_right_images = [pygame.transform.flip(img, True, False) for img in player_idle_left_images]

player_frame_index = 0
player_animation_timer = 0
player_current_image = player_stand_image
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
cam_x = 0
cam_y = 0


class TempPlayerCollision:
                    def __init__(self, x, y, width, height):
                        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)

                    def get_collision_rect(self, cam_x):
                        return pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.width, self.rect.height)

cat_types = [
    {"type":"black", "walk_right_image1" : "assets/sprites/mobs/BlackCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/BlackCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/BlackCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/BlackCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/BlackCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/BlackCatRightStanding.png", "dead_image": "assets/sprites/mobs/BlackCatDead.png", "caged1": "black_cat_caged_left", "caged2": "black_cat_caged_right"}, 
    {"type":"salt_and_pepper", "walk_right_image1" : "assets/sprites/mobs/SandPCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandPCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandPCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandPCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandPCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandPCatRightStanding.png", "dead_image": "assets/sprites/mobs/SandPCatDead.png", "caged1": "SandP_cat_caged_left", "caged2": "SandP_cat_caged_right"},
    {"type":"white", "walk_right_image1" : "assets/sprites/mobs/WhiteCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WhiteCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WhiteCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WhiteCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WhiteCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WhiteCatRightStanding.png", "dead_image": "assets/sprites/mobs/WhiteCatDead.png", "caged1": "white_cat_caged_left", "caged2": "white_cat_caged_right"}, 
    {"type":"white_and_black", "walk_right_image1" : "assets/sprites/mobs/WandBCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WandBCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WandBCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WandBCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WandBCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WandBCatRightStanding.png", "dead_image": "assets/sprites/mobs/WandBCatDead.png", "caged1": "WandB_cat_caged_left", "caged2": "WandB_cat_caged_right"}, 
    {"type":"sandy", "walk_right_image1" : "assets/sprites/mobs/SandyCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/SandyCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/SandyCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/SandyCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/SandyCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/SandyCatRightStanding.png", "dead_image": "assets/sprites/mobs/SandyCatDead.png", "caged1": "sandy_cat_caged_left", "caged2": "sandy_cat_caged_right"}, 
    {"type":"orange", "walk_right_image1" : "assets/sprites/mobs/OrangeCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/OrangeCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/OrangeCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/OrangeCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/OrangeCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/OrangeCatRightStanding.png", "dead_image": "assets/sprites/mobs/OrangeCatDead.png", "caged1": "orange_cat_caged_left", "caged2": "orange_cat_caged_right"}, 
    {"type":"calico", "walk_right_image1" : "assets/sprites/mobs/CalicoCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/CalicoCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/CalicoCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/CalicoCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/CalicoCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/CalicoCatRightStanding.png", "dead_image": "assets/sprites/mobs/CalicoCatDead.png", "caged1": "calico_cat_caged_left", "caged2": "calico_cat_caged_right"}, 
    {"type":"gray", "walk_right_image1" : "assets/sprites/mobs/GrayCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/GrayCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/GrayCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/GrayCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/GrayCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/GrayCatRightStanding.png", "dead_image": "assets/sprites/mobs/GrayCatDead.png", "caged1": "gray_cat_caged_left", "caged2": "gray_cat_caged_right"}, 
    {"type":"white_and_orange", "walk_right_image1" : "assets/sprites/mobs/WandOCatRightMove1.png", "walk_right_image2" : "assets/sprites/mobs/WandOCatRightMove2.png", "walk_right_image3" : "assets/sprites/mobs/WandOCatRightMove3.png", "walk_right_image4" : "assets/sprites/mobs/WandOCatRightMove4.png", "walk_right_image5" : "assets/sprites/mobs/WandOCatRightMove5.png", "stand_right_image" : "assets/sprites/mobs/WandOCatRightStanding.png", "dead_image": "assets/sprites/mobs/WandOCatDead.png", "caged1": "WandO_cat_caged_left", "caged2": "WandO_cat_caged_right"}]


squirrel_move_images = ["assets/sprites/mobs/SquirrelMove1.png", "assets/sprites/mobs/SquirrelMove2.png", "assets/sprites/mobs/SquirrelMove3.png", "assets/sprites/mobs/SquirrelMove4.png", "assets/sprites/mobs/SquirrelMove5.png", "assets/sprites/mobs/SquirrelMove6.png"]
squirrel_stand_image = "assets/sprites/mobs/SquirrelStand1.png"
squirrel_dead_image = "assets/sprites/mobs/SquirrelDead.png"

cow_types = [
    {"type":"black", "walk_right_image1" : "assets/sprites/mobs/BlackCowRightWalk1.png", "walk_right_image2" : "assets/sprites/mobs/BlackCowRightWalk2.png", "walk_right_image3" : "assets/sprites/mobs/BlackCowRightWalk3.png", "walk_right_image4" : "assets/sprites/mobs/BlackCowRightWalk4.png", "walk_right_image5" : "assets/sprites/mobs/BlackCowRightWalk5.png", "stand_right_image" : "assets/sprites/mobs/BlackCowRightStanding.png", "dead_image": "assets/sprites/mobs/BlackCowDead.png"},
    {"type":"brown", "walk_right_image1" : "assets/sprites/mobs/BrownCowRightWalk1.png", "walk_right_image2" : "assets/sprites/mobs/BrownCowRightWalk2.png", "walk_right_image3" : "assets/sprites/mobs/BrownCowRightWalk3.png", "walk_right_image4" : "assets/sprites/mobs/BrownCowRightWalk4.png", "walk_right_image5" : "assets/sprites/mobs/BrownCowRightWalk5.png", "stand_right_image" : "assets/sprites/mobs/BrownCowRightStanding.png", "dead_image": "assets/sprites/mobs/BrownCowDead.png"}
]

chicken_move_images = ["assets/sprites/mobs/ChickenRightWalk1.png", "assets/sprites/mobs/ChickenRightWalk2.png", "assets/sprites/mobs/ChickenRightWalk3.png", "assets/sprites/mobs/ChickenRightWalk4.png", "assets/sprites/mobs/ChickenRightWalk5.png"]
chicken_stand_image = "assets/sprites/mobs/ChickenRightStanding.png"
chicken_dead_image = "assets/sprites/mobs/ChickenDead.png"

crawler_idle_images = ["assets/sprites/mobs/CrawlerIdle1.png", "assets/sprites/mobs/CrawlerIdle2.png"]
crawler_move_left_images = ["assets/sprites/mobs/CrawlerLeftWalk1.png", "assets/sprites/mobs/CrawlerLeftWalk2.png", "assets/sprites/mobs/CrawlerLeftWalk3.png", "assets/sprites/mobs/CrawlerLeftWalk4.png"]
crawler_attack_left_images = ["assets/sprites/mobs/CrawlerAttack1.png", "assets/sprites/mobs/CrawlerAttack2.png", "assets/sprites/mobs/CrawlerAttack3.png", "assets/sprites/mobs/CrawlerAttack4.png"]
crawler_dead_image_left = pygame.transform.scale(
    pygame.image.load("assets/sprites/mobs/CrawlerDead.png").convert_alpha(), (size, size))
crawler_dead_image_right = pygame.transform.flip(crawler_dead_image_left, True, False)

duskwretch_idle_images = ["assets/sprites/mobs/DuskwretchLeftStand1.png", "assets/sprites/mobs/DuskwretchLeftStand2.png", "assets/sprites/mobs/DuskwretchLeftStand3.png"]
duskwretch_start_move_left_images = ["assets/sprites/mobs/DuskwretchStartLeftWalk1.png", "assets/sprites/mobs/DuskwretchStartLeftWalk2.png"]
duskwretch_end_move_left_images = ["assets/sprites/mobs/DuskwretchStartLeftWalk2.png", "assets/sprites/mobs/DuskwretchStartLeftWalk1.png"]
duskwretch_move_left_images = ["assets/sprites/mobs/DuskwretchLeftWalk1.png", "assets/sprites/mobs/DuskwretchLeftWalk2.png", "assets/sprites/mobs/DuskwretchLeftWalk3.png", "assets/sprites/mobs/DuskwretchLeftWalk4.png"]
duskwretch_chase_left_images = ["assets/sprites/mobs/DuskwretchChaseLeft1.png", "assets/sprites/mobs/DuskwretchChaseLeft2.png", "assets/sprites/mobs/DuskwretchChaseLeft4.png", "assets/sprites/mobs/DuskwretchChaseLeft3.png", "assets/sprites/mobs/DuskwretchChaseLeft5.png"]
duskwretch_attack_left_images = ["assets/sprites/mobs/DuskwretchLeftAttack1.png", "assets/sprites/mobs/DuskwretchLeftAttack2.png", "assets/sprites/mobs/DuskwretchLeftAttack3.png"]
duskwretch_dead_image_left = pygame.image.load("assets/sprites/mobs/DuskwretchDead.png").convert_alpha()
duskwretch_dead_image_right = pygame.transform.flip(duskwretch_dead_image_left, True, False)

pock_idle_images = ["assets/sprites/mobs/PockIdle1.png", "assets/sprites/mobs/PockIdle2.png"]
pock_move_right_images = ["assets/sprites/mobs/PockMoveRight1.png", "assets/sprites/mobs/PockMoveRight2.png", "assets/sprites/mobs/PockMoveRight3.png", "assets/sprites/mobs/PockMoveRight4.png"]
pock_throw_right_images = ["assets/sprites/mobs/PockThrowRight1.png", "assets/sprites/mobs/PockThrowRight2.png", "assets/sprites/mobs/PockThrowRight3.png", "assets/sprites/mobs/PockThrowRight4.png"]
pock_dead_image_left = pygame.image.load("assets/sprites/mobs/PockDead.png").convert_alpha()
pock_dead_image_right = pygame.transform.flip(pock_dead_image_left, True, False)


deer_idle_images = ["assets/sprites/mobs/DeerIdle1.png", "assets/sprites/mobs/DeerIdle2.png", "assets/sprites/mobs/DeerIdle3.png", "assets/sprites/mobs/DeerIdle4.png", "assets/sprites/mobs/DeerIdle5.png", "assets/sprites/mobs/DeerIdle6.png", "assets/sprites/mobs/DeerIdle7.png", "assets/sprites/mobs/DeerIdle8.png"]
deer_walk_left_images = ["assets/sprites/mobs/DeerWalkLeft1.png", "assets/sprites/mobs/DeerWalkLeft2.png", "assets/sprites/mobs/DeerWalkLeft3.png", "assets/sprites/mobs/DeerWalkLeft4.png", "assets/sprites/mobs/DeerWalkLeft5.png", "assets/sprites/mobs/DeerWalkLeft6.png", "assets/sprites/mobs/DeerWalkLeft7.png", "assets/sprites/mobs/DeerWalkLeft8.png"]
buck_idle_images = ["assets/sprites/mobs/BuckIdle1.png", "assets/sprites/mobs/BuckIdle2.png", "assets/sprites/mobs/BuckIdle3.png", "assets/sprites/mobs/BuckIdle4.png", "assets/sprites/mobs/BuckIdle5.png", "assets/sprites/mobs/BuckIdle6.png", "assets/sprites/mobs/BuckIdle7.png", "assets/sprites/mobs/BuckIdle8.png"]
buck_walk_left_images = ["assets/sprites/mobs/BuckWalkLeft1.png", "assets/sprites/mobs/BuckWalkLeft2.png", "assets/sprites/mobs/BuckWalkLeft3.png", "assets/sprites/mobs/BuckWalkLeft4.png", "assets/sprites/mobs/BuckWalkLeft5.png", "assets/sprites/mobs/BuckWalkLeft6.png", "assets/sprites/mobs/BuckWalkLeft7.png", "assets/sprites/mobs/BuckWalkLeft8.png"]
buck_attack_left_images = ["assets/sprites/mobs/BuckAttack1.png", "assets/sprites/mobs/BuckAttack2.png", "assets/sprites/mobs/BuckAttack3.png"]
deer_dead_image = pygame.image.load("assets/sprites/mobs/DeerDead.png").convert_alpha()
buck_dead_image = pygame.image.load("assets/sprites/mobs/BuckDead.png").convert_alpha()

black_bear_idle_images = ["assets/sprites/mobs/BlackBearIdle1.png", "assets/sprites/mobs/BlackBearIdle2.png", "assets/sprites/mobs/BlackBearIdle3.png", "assets/sprites/mobs/BlackBearIdle4.png"]
black_bear_walk_left_images = ["assets/sprites/mobs/BlackBearWalkLeft1.png", "assets/sprites/mobs/BlackBearWalkLeft2.png", "assets/sprites/mobs/BlackBearWalkLeft3.png", "assets/sprites/mobs/BlackBearWalkLeft4.png", "assets/sprites/mobs/BlackBearWalkLeft5.png", "assets/sprites/mobs/BlackBearWalkLeft6.png"]
brown_bear_idle_images = ["assets/sprites/mobs/BrownBearIdle1.png", "assets/sprites/mobs/BrownBearIdle2.png", "assets/sprites/mobs/BrownBearIdle3.png", "assets/sprites/mobs/BrownBearIdle4.png"]
brown_bear_attack_left_images = ["assets/sprites/mobs/BrownBearAttack1.png", "assets/sprites/mobs/BrownBearAttack2.png", "assets/sprites/mobs/BrownBearAttack3.png"]
brown_bear_walk_left_images = ["assets/sprites/mobs/BrownBearWalkLeft1.png", "assets/sprites/mobs/BrownBearWalkLeft2.png", "assets/sprites/mobs/BrownBearWalkLeft3.png", "assets/sprites/mobs/BrownBearWalkLeft4.png", "assets/sprites/mobs/BrownBearWalkLeft5.png", "assets/sprites/mobs/BrownBearWalkLeft6.png"]
black_bear_attack_left_images = ["assets/sprites/mobs/BlackBearAttack1.png", "assets/sprites/mobs/BlackBearAttack2.png", "assets/sprites/mobs/BlackBearAttack3.png"]
black_bear_dead_image = pygame.image.load("assets/sprites/mobs/BlackBearDead.png").convert_alpha()
brown_bear_dead_image = pygame.image.load("assets/sprites/mobs/BrownBearDead.png").convert_alpha()

gila_idle_images = ["assets/sprites/mobs/GilaIdle1.png", "assets/sprites/mobs/GilaIdle2.png"]
gila_walk_left_images = ["assets/sprites/mobs/GilaWalkLeft1.png", "assets/sprites/mobs/GilaWalkLeft2.png", "assets/sprites/mobs/GilaWalkLeft3.png"]
gila_attack_left_images = ["assets/sprites/mobs/GilaAttackLeft1.png", "assets/sprites/mobs/GilaAttackLeft2.png", "assets/sprites/mobs/GilaAttackLeft3.png"]
gila_dead_image = pygame.image.load("assets/sprites/mobs/GilaDead.png").convert_alpha()

crow_walk_left_images = ["assets/sprites/mobs/CrowWalkLeft1.png", "assets/sprites/mobs/CrowWalkLeft2.png", "assets/sprites/mobs/CrowWalkLeft3.png", "assets/sprites/mobs/CrowWalkLeft4.png", "assets/sprites/mobs/CrowWalkLeft5.png"]
crow_fly_left_images = ["assets/sprites/mobs/CrowFlyLeft1.png", "assets/sprites/mobs/CrowFlyLeft2.png", "assets/sprites/mobs/CrowFlyLeft3.png", "assets/sprites/mobs/CrowFlyLeft4.png"]
crow_start_fly_left_images = ["assets/sprites/mobs/CrowStartFlyLeft1.png", "assets/sprites/mobs/CrowStartFlyLeft2.png", "assets/sprites/mobs/CrowStartFlyLeft3.png", "assets/sprites/mobs/CrowStartFlyLeft4.png", "assets/sprites/mobs/CrowStartFlyLeft5.png", "assets/sprites/mobs/CrowStartFlyLeft6.png"]
crow_landing_left_images = ["assets/sprites/mobs/CrowLandingLeft1.png", "assets/sprites/mobs/CrowLandingLeft2.png", "assets/sprites/mobs/CrowLandingLeft3.png", "assets/sprites/mobs/CrowLandingLeft4.png", "assets/sprites/mobs/CrowLandingLeft5.png", "assets/sprites/mobs/CrowLandingLeft6.png", "assets/sprites/mobs/CrowLandingLeft7.png", "assets/sprites/mobs/CrowLandingLeft8.png"]
crow_dead_image = pygame.image.load("assets/sprites/mobs/CrowDead.png").convert_alpha()

dragon_types = [
    {"type": "fire", "rare_gems": [{"gem": "Ruby", "chance": 0.1}, {"gem": "Garnet", "chance": 0.1}]},
    {"type": "ice", "rare_gems": [{"gem": "Aquamarine", "chance": 0.1}, {"gem": "Sapphire", "chance": 0.1}]},
    {"type": "electric", "rare_gems": [{"gem": "Topaz", "chance": 0.1}, {"gem": "Opal", "chance": 0.1}]},
    {"type": "poison", "rare_gems": [{"gem": "Amethyst", "chance": 0.1}, {"gem": "Emerald", "chance": 0.1}]},
    {"type": "dusk", "rare_gems": [{"gem": "Diamond", "chance": 0.1}, {"gem": "Pearl", "chance": 0.1}]}
]

def create_dragon_images(dragon_type_name):
    prefix = f"{dragon_type_name.capitalize()}Dragon"
    breath_prefix = f"{dragon_type_name.capitalize()}Breath"
    walk_left = [f"assets/sprites/mobs/{prefix}LeftWalk{i}.png" for i in range(1, 7)]
    idle_left = [f"assets/sprites/mobs/{prefix}LeftIdle{i}.png" for i in range(1, 4)]
    start_fly_left = [f"assets/sprites/mobs/{prefix}LeftStartFly{i}.png" for i in range(1, 8)]
    fly_left = [f"assets/sprites/mobs/{prefix}LeftFly{i}.png" for i in range(1, 11)]
    end_fly_left = [f"assets/sprites/mobs/{prefix}LeftEndFly{i}.png" for i in range(1, 8)]
    bite_attack_left = [f"assets/sprites/mobs/{prefix}LeftBiteAttack{i}.png" for i in range(1, 4)]
    breath_attack_left = [f"assets/sprites/mobs/{prefix}LeftBreathAttack{i}.png" for i in range(1, 11)]
    breath_effect_left = [f"assets/sprites/mobs/{breath_prefix}Left{i}.png" for i in range(1, 11)]
    dead_left = f"assets/sprites/mobs/{prefix}LeftDead.png"
    
    return {
        "walk_left": walk_left,
        "idle_left": idle_left,
        "start_fly_left": start_fly_left,
        "fly_left": fly_left,
        "end_fly_left": end_fly_left,
        "bite_attack_left": bite_attack_left,
        "breath_attack_left": breath_attack_left,
        "breath_effect_left": breath_effect_left,
        "dead_left": dead_left
    }

fire_dragon_images = create_dragon_images("fire")
ice_dragon_images = create_dragon_images("ice")
electric_dragon_images = create_dragon_images("electric")
poison_dragon_images = create_dragon_images("poison")
dusk_dragon_images = create_dragon_images("dusk")


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
        self.max_health = int(round(100 * self.health_leveler))
        self.health = self.max_health
        self.stamina_leveler = 1
        self.max_stamina = int(round(100 * self.stamina_leveler))
        self.stamina = self.max_stamina
        self.hunger_leveler = 1
        self.max_hunger = int(round(100 * self.hunger_leveler))
        self.hunger = self.max_hunger
        self.full_timer = 60
        self.thirst_leveler = 1
        self.max_thirst = int(round(100 * self.thirst_leveler))
        self.thirst = self.max_thirst
        self.thirst_full_timer = 60
        self.weather_resistance_leveler = 1
        self.max_heat_resistance = 100 * self.weather_resistance_leveler
        self.temp_heat_resistance_increase = 1
        self.temp_heat_resistance_timer = 0
        self.heat_resistance = 100 * self.temp_heat_resistance_increase
        self.max_cold_resistance = 100 * self.weather_resistance_leveler
        self.temp_cold_resistance_increase = 1
        self.temp_cold_resistance_timer = 0
        self.cold_resistance = 100 * self.temp_cold_resistance_increase
        self.max_torpidity = 100
        self.torpidity = 0
        self.extreme_temp_timer = 0
        self.temp_weight_increase = 1
        self.weight_leveler = 1
        self.max_weight = 100 * self.weight_leveler * self.temp_weight_increase
        self.weight = 0
        self.glow = False
        self.glow_time = 0
        self.poison = False
        self.poison_time = 0
        self.damage = 5
        self.poison_strength = 1
        self.strength_leveler = 1
        self.strength_level_gain = 1
        self.attack = int(self.damage + (self.strength_leveler - 1) * self.strength_level_gain)
        self.temp_attack_boost = 1
        self.base_speed = 275
        self.speed_leveler = 1
        self.speed = 100 * self.speed_leveler
        self.defense_leveler = 1
        self.defense = 100 * self.defense_leveler
        self.resilience_leveler = 1
        self.resilience = 100 * self.resilience_leveler
        self.temperature_resistance_leveler = 0
        self.level = 1
        self.experience = 0
        self.exp_total = 0
        self.req_multiplier = .5
        self.next_level_exp = 100
        self.level_up_timer = 0
        self.stamina_timer = 0
        self.stamina_message_timer = 0
        self.unspent_stat_points = 0
        self.health_bar_color = ()
        self.poisoned_health_color = ()

        self.inventory = []
        self.is_alive = True
        self.is_attacking = False
        self.direction = pygame.Vector2(0, 0)
        self.step_sound = random.choice(grass_steps)

        self.exhausted = False
        self.dead = False
        self.score = 0
        self.last_direction = "down"
        self.attack_cooldown = pygame.time.get_ticks()
        self.attack_delay = 300
        self.mob_noise_delay = 3
        
        self.swimming = False
        self.in_lava = False
        self.swim_stamina_drain = 0.3
        self.lava_damage_rate = 40  # damage per second in lava
        self.lava_damage_timer = 0
        self.current_liquid = None

    def status_effects(self, dt):
        if self.poison == True:
            self.poison_time -= dt
            self.health -= dt * self.poison_strength
            if self.health < 0:
                self.health = 0
            if self.poison_time <= 0:
                self.poison = False
                self.poison_time = 0
                self.poison_strength = 1
    
    def handle_swimming(self, dt, liquid_collision=None):
        """Handle swimming mechanics - stamina drain and drowning"""
        if self.swimming:
            self.stamina -= self.swim_stamina_drain * dt
            
            if self.stamina < 0:
                self.stamina = 0
                if not self.in_lava:
                    self.health -= 5 * dt  # Drown damage
                    if self.health < 0:
                        self.health = 0
                        self.is_alive = False
                        self.dead = True
    
    def handle_lava_damage(self, dt):
        if self.in_lava:
            self.lava_damage_timer += dt
            if self.lava_damage_timer >= 0.1:
                self.health -= self.lava_damage_rate * (self.lava_damage_timer / 1.0)
                self.lava_damage_timer = 0
                if self.health < 0:
                    self.health = 0
                    self.is_alive = False
                    self.dead = True
    
    def enter_liquid(self, liquid_type, liquid_obj=None):
        if liquid_type == "water":
            self.swimming = True
            self.in_lava = False
        elif liquid_type == "lava":
            self.swimming = True
            self.in_lava = True
        self.current_liquid = liquid_obj
    
    def exit_liquid(self):
        """Exit a liquid"""
        self.swimming = False
        self.in_lava = False
        self.lava_damage_timer = 0
        self.current_liquid = None

    def attacking(self, nearby_mobs, player_world_x, player_world_y, mouse_over_hotbar=False):
        if pygame.mouse.get_pressed()[0] and not self.exhausted and not mouse_over_hotbar:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_cooldown > self.attack_delay:
                self.attack_cooldown = current_time
                for mob in nearby_mobs:
                    mob_collision = mob.get_collision_rect(0)

                    horizontal_dist = abs(mob_collision.centerx - player_world_x)
                    vertical_dist = abs(mob_collision.centery - player_world_y)

                    attack_reach = 25
                    horizontal_range = (mob_collision.width / 2) + attack_reach
                    vertical_range = (mob_collision.height / 2) + attack_reach

                    facing_object = False
                    if self.last_direction == "right" and mob_collision.centerx > player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                        facing_object = True
                    elif self.last_direction == "left" and mob_collision.centerx < player_world_x and horizontal_dist < horizontal_range and vertical_dist < vertical_range:
                        facing_object = True
                    elif self.last_direction == "up" and mob_collision.centery < player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                        facing_object = True
                    elif self.last_direction == "down" and mob_collision.centery > player_world_y and vertical_dist < vertical_range and horizontal_dist < horizontal_range:
                        facing_object = True

                    if facing_object and 1 <= mob.health:
                        old_health = mob.health
                        # Flat damage plus strength upgrades
                        mob.health -= self.attack
                        if mob.health < 0:
                            mob.health = 0
                        try:
                            from inventory import inventory as player_inventory
                            player_inventory.decrement_durability(player_inventory.selected_hotbar_slot, True, 1)
                        except Exception:
                            pass

                        if not hasattr(mob, "last_hit_sound_time"):
                            mob.last_hit_sound_time = 0

                        hit_sound_cooldown = 6000
                        if current_time - mob.last_hit_sound_time > hit_sound_cooldown:
                            mob.last_hit_sound_time = current_time
                            if mob.__class__.__name__ in ["BlackBear", "BrownBear"]:
                                sound_manager.play_sound("bear_get_hit")
                            elif mob.__class__.__name__ == "Deer":
                                if hasattr(mob, 'is_buck') and mob.is_buck:
                                    sound_manager.play_sound("buck_get_hit")
                                else:
                                    sound_manager.play_sound("deer_get_hit")
                            elif mob.__class__.__name__ == "Chicken":
                                sound_manager.play_sound(random.choice([f"chicken_get_hit{i}" for i in range(1,4)]))
                            elif mob.__class__.__name__ == "Cat":
                                sound_manager.play_sound("cat_get_hit1")
                            elif mob.__class__.__name__ == "Cow":
                                sound_manager.play_sound(random.choice(["cow_moo1", "cow_moo2"]))
                            elif mob.__class__.__name__ == "Squirrel":
                                sound_manager.play_sound("squirrel_get_hit")
                            elif mob.__class__.__name__ == "Crow":
                                sound_manager.play_sound(random.choice(["crow_caw1", "crow_caw2", "crow_caw"]))

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

    def level_up(self, screen):
        self.level += 1
        self.exp_total += self.next_level_exp
        if self.level > 0:
            self.next_level_exp += (self.next_level_exp * self.req_multiplier)
            if self.level <= 20:
                self.req_multiplier -= .022
            elif self.level <= 40:
                self.req_multiplier -= .0018
            elif self.level <= 60:
                self.req_multiplier -= .0008
            elif self.level <= 80:
                self.req_multiplier -= .00008
            elif self.level < 100:
                self.req_multiplier -= .00003
            if self.level >= 100:
                self.req_multiplier += 1
        self.level_up_timer = 10
        self.unspent_stat_points += 1
        sound_manager.play_sound("level_up")

    def apply_stat_upgrade(self, stat_key):
        if self.unspent_stat_points <= 0:
            return False

        upgraded = False
        if stat_key == "health":
            self.health_leveler = round(self.health_leveler + 0.1, 4)
            self.max_health = int(100 * self.health_leveler)
            self.health = self.max_health
            upgraded = True
        elif stat_key == "stamina":
            self.stamina_leveler = round(self.stamina_leveler + 0.1, 4)
            self.max_stamina = int(100 * self.stamina_leveler)
            self.stamina = self.max_stamina
            upgraded = True
        elif stat_key == "hunger":
            self.hunger_leveler = round(self.hunger_leveler + 0.1, 4)
            self.max_hunger = int(100 * self.hunger_leveler)
            self.hunger = self.max_hunger
            upgraded = True
        elif stat_key == "thirst":
            self.thirst_leveler = round(self.thirst_leveler + 0.1, 4)
            self.max_thirst = int(100 * self.thirst_leveler)
            self.thirst = self.max_thirst
            upgraded = True
        elif stat_key == "weather":
            self.weather_resistance_leveler = round(self.weather_resistance_leveler + 0.1, 4)
            self.max_heat_resistance = int(100 * self.weather_resistance_leveler)
            self.max_cold_resistance = int(100 * self.weather_resistance_leveler)
            self.heat_resistance = self.max_heat_resistance
            self.cold_resistance = self.max_cold_resistance
            upgraded = True
        elif stat_key == "weight":
            self.weight_leveler = round(self.weight_leveler + 0.1, 4)
            self.max_weight = int(100 * self.weight_leveler * self.temp_weight_increase)
            upgraded = True
        elif stat_key == "strength":
            self.strength_leveler = round(self.strength_leveler + 1, 4)
            self.attack = int(self.damage + (self.strength_leveler - 1) * self.strength_level_gain)
            upgraded = True
        elif stat_key == "speed":
            self.speed_leveler = round(self.speed_leveler + 0.05, 4)
            self.speed = int(100 * self.speed_leveler)
            upgraded = True
        elif stat_key == "defense":
            self.defense_leveler = round(self.defense_leveler + 0.1, 4)
            self.defense = int(100 * self.defense_leveler)
            upgraded = True
        elif stat_key == "resilience":
            self.resilience_leveler = round(self.resilience_leveler + 0.1, 4)
            self.resilience = int(100 * self.resilience_leveler)
            upgraded = True
        elif stat_key == "temperature_resistance":
            self.temperature_resistance_leveler += 1
            upgraded = True

        if upgraded:
            self.unspent_stat_points -= 1
            return True

        return False

    def show_level_up_message(self, screen):
        level_up_text = large_font.render(
            f"You leveled up to level {self.level}! Upgrade stats in inventory!",
            True, (20, 255, 20)
        )
        screen.blit(level_up_text, (
            screen.get_width() // 2 - level_up_text.get_width() // 2,
            20
        ))

    def get_speed(self):
        speed = self.base_speed * (self.speed / 100)
        weight_ratio = self.weight / self.max_weight if self.max_weight > 0 else 0
        if weight_ratio >= 1:
            weight_multiplier = 0
        elif weight_ratio >= 0.95:
            weight_multiplier = 0.25
        elif weight_ratio >= 0.9:
            weight_multiplier = 0.5
        else:
            weight_multiplier = 1
        return speed * weight_multiplier

    def regain_health(self, dt):
        if 1 <= self.health <= self.max_health:
            if not self.poison:
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
        if self.health < 0:
            self.health = 0
        if self.hunger < 0:
            self.hunger = 0

    def regain_stamina(self, dt, screen):
        if self.stamina_timer > 0:
            self.stamina_timer -= dt
            return
        
        if self.stamina < self.max_stamina:
            if self.thirst == self.max_thirst:
                self.stamina += dt * 16
            elif self.thirst > self.max_thirst * 0.7:
                self.stamina += dt * 10
            elif self.thirst > self.max_thirst * 0.4:
                self.stamina += dt * 6
            elif self.thirst > self.max_thirst * 0.1:
                self.stamina += dt * 2
            else:
                self.stamina -= dt / 12
                self.health -= dt / 12

        if self.thirst == 100:
            self.thirst_full_timer -= dt
            if self.thirst_full_timer <= 0:
                self.thirst -= dt / 100
        elif self.thirst > 0:
            self.thirst -= dt / 40

        if self.stamina > 10 and self.speed < 100:
            self.speed = 100
        
        if self.stamina < 0:
            self.stamina = 0
        if self.health < 0:
            self.health = 0
        if self.thirst < 0:
            self.thirst = 0

    def lose_stamina(self, screen, dt):
        stamina_depleted = False
        if self.stamina > 0:
            self.stamina -= dt * 6
            if self.stamina <= 0:
                self.stamina = 0
                stamina_depleted = True
                self.stamina_timer = 2.0
        return stamina_depleted

    def stamina_speed(self):
        if self.stamina <= 0:
            self.speed = 30
            self.exhausted = True
        elif self.stamina <= 10: 
            self.speed = 40
            self.exhausted = False
        elif self.stamina <= 20: 
            self.speed = 60
            self.exhausted = False
        else:
            self.speed = 100
            self.exhausted = False

    def lose_hunger(self, dt):
        if self.hunger > 0:
            if self.hunger == 100:
                self.full_timer -= dt
                if self.full_timer <= 0:
                    self.hunger -= dt/100
            else:
                self.hunger -= dt / 100
                self.full_timer = 60
        if self.hunger < 0:
            self.hunger = 0
            

    def lose_thirst(self, dt):
        if self.thirst > 0:
            if self.thirst == 100:
                self.thirst_full_timer -= dt
                if self.thirst_full_timer <= 0:
                    self.thirst -= dt/100
            else:
                self.thirst -= dt / 100
                self.thirst_full_timer = 60
        if self.thirst < 0:
            self.thirst = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1,5)]))

    def clamp_stats(self):
        if self.health < 0:
            self.health = 0
        if self.health > self.max_health:
            self.health = self.max_health
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger > self.max_hunger:
            self.hunger = self.max_hunger
        if self.stamina < 0:
            self.stamina = 0
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina
        if self.thirst < 0:
            self.thirst = 0
        if self.thirst > self.max_thirst:
            self.thirst = self.max_thirst

    def feed_cat(self, cat):
        pass

    def health_bar(self, screen):
        max_health = self.max_health
        health = self.health
        bar_width = self.max_health * .5
        bar_height = 18
        x = 43
        y = 64

        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if self.poison:
            pygame.draw.rect(screen, (150, 80, 200), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        else:
            if health_ratio > .4:
                pygame.draw.rect(screen, (200, 40, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
            else:
                pygame.draw.rect(screen, (255, 80, 60), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        health_text = f"{int(health)} / {max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def stamina_bar(self, screen):
        max_stamina = self.max_stamina
        stamina = self.stamina
        bar_width = max_stamina * .5
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
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def hunger_bar(self, screen):
        max_hunger = self.max_hunger
        hunger = self.hunger
        bar_width = max_hunger * .5
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
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def thirst_bar(self, screen):
        max_thirst = self.max_thirst
        thirst = self.thirst
        bar_width = self.max_thirst * .5
        bar_height = 18
        x = 43
        y = 118

        thirst_ratio = thirst / max_thirst
        thirst_width = int(bar_width * thirst_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if thirst_ratio > .4:
            pygame.draw.rect(screen, (0, 40, 255), pygame.Rect(x, y, thirst_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (100, 100, 255), pygame.Rect(x, y, thirst_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        thirst_text = f"{int(thirst)} / {max_thirst}"
        text_surface = font.render(thirst_text, True, (255, 255, 255))
        if bar_width < 100:
            text_x = x + bar_width + 8
        else:
            text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        if bar_width < 100:
            draw_text_with_background(screen, text_surface, text_x, text_y)
        else:
            screen.blit(text_surface, (text_x, text_y))

    def exp_bar(self, screen):
        from inventory import hotbar_image
        next_level_exp = self.next_level_exp
        experience = self.experience
        bar_width = hotbar_image.get_width()
        bar_height = 5
        x = screen.get_width()//2 - bar_width // 2
        y = screen.get_height() - 75

        safe_next = next_level_exp if next_level_exp > 0 else 1
        experience_ratio = experience / safe_next
        # Clamp ratio to [0, 1] and guard against non-finite values
        if not math.isfinite(experience_ratio):
            experience_ratio = 1
        experience_ratio = max(0, min(experience_ratio, 1))
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
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.frame_index = 0
        self.animation_speed = 0.15
        self.last_direction = "right"
        self.is_alive = True
        self.resource = None
        self.health = 100
        self.full_health = 100
        self.bar_timer = 0
        self.last_health = 0
        self.resource = "Hide"
        self.resource_amount = 3
        self.destroyed = False
        self.fleeing = False
        self.flee_timer = 0
        self.base_speed = 100
        self.speed = 1
        self.level = 1
        self.death_experience = 50
        self.death_time = None
        self.harvest_grace_ms = 200
        
        self.swimming = False
        self.in_lava = False
        self.lava_damage_rate = 50
        self.lava_damage_timer = 0
        self.immune_to_lava = False
        self.current_liquid = None


    def handle_lava_damage(self, dt):
        """Handle lava damage for mobs - only take damage if not immune"""
        if self.in_lava and not self.immune_to_lava:
            self.lava_damage_timer += dt
            if self.lava_damage_timer >= 0.1:  # Apply damage every 0.1 seconds
                self.health -= self.lava_damage_rate * (self.lava_damage_timer / 1.0)
                self.lava_damage_timer = 0
                if self.health < 0:
                    self.health = 0
                    self.is_alive = False
    
    def enter_liquid(self, liquid_type, liquid_obj=None):
        if liquid_type in ["water", "lava"]:
            self.swimming = True
            if liquid_type == "lava":
                self.in_lava = True
        self.current_liquid = liquid_obj
    
    def exit_liquid(self):
        self.swimming = False
        self.in_lava = False
        self.lava_damage_timer = 0
        self.current_liquid = None

    def give_experience(self, player):
        if self.health < 1:
            player.experience += self.death_experience
            player.exp_total += self.death_experience
            self.death_experience = 0

    def keep_in_screen(self, screen_height):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x, rect.y, rect.width, rect.height)

    def check_collision(self, direction, nearby_objects, nearby_mobs):
        solid_objects = [obj for obj in nearby_objects if not hasattr(obj, 'liquid_type')]
        all_nearby = solid_objects + nearby_mobs

        def get_obj_collision_rect(obj):
            if hasattr(obj, 'get_collision_rect'):
                return obj.get_collision_rect(0)
            elif isinstance(obj, dict) and 'rect' in obj:
                # Structure collision rect is already in world coordinates
                return obj['rect']
            else:
                return obj.rect

        collision_rect = self.get_collision_rect(0)

        left_check = pygame.Rect(collision_rect.left - 1, collision_rect.top + 5, 1, collision_rect.height - 10)
        right_check = pygame.Rect(collision_rect.right, collision_rect.top + 5, 1, collision_rect.height - 10)
        top_check = pygame.Rect(collision_rect.left + 5, collision_rect.top - 1, collision_rect.width - 10, 1)
        bottom_check = pygame.Rect(collision_rect.left + 5, collision_rect.bottom, collision_rect.width - 10, 1)

        left_collision = any(left_check.colliderect(get_obj_collision_rect(obj)) for obj in all_nearby)
        right_collision = any(right_check.colliderect(get_obj_collision_rect(obj)) for obj in all_nearby)
        up_collision = any(top_check.colliderect(get_obj_collision_rect(obj)) for obj in all_nearby)
        down_collision = any(bottom_check.colliderect(get_obj_collision_rect(obj)) for obj in all_nearby)

        can_move_x = not ((direction.x > 0 and right_collision) or (direction.x < 0 and left_collision))
        can_move_y = not ((direction.y > 0 and down_collision) or (direction.y < 0 and up_collision))

        return can_move_x, can_move_y

    def get_speed(self):
        speed = self.base_speed * self.speed
        if self.swimming:
            speed *= 0.5
        return speed

    def draw(self, screen, cam_x):
        if self.swimming:
            if hasattr(self, 'current_liquid') and self.current_liquid:
                liquid_center_x = self.current_liquid.rect.centerx
                liquid_center_y = self.current_liquid.rect.centery
                liquid_width = self.current_liquid.rect.width
                liquid_height = self.current_liquid.rect.height
                
                dist_x = abs(self.rect.centerx - liquid_center_x) / (liquid_width / 2)
                dist_y = abs(self.rect.centery - liquid_center_y) / (liquid_height / 2)
                
                sinking_ratio = max(0, 1 - max(dist_x, dist_y))
                
                # Clip image from bottom based on sinking depth
                clip_pixels = int(sinking_ratio * self.rect.height * 0.4)
                
                if clip_pixels > 0 and self.image:
                    clipped_image = self.image.subsurface(pygame.Rect(0, 0, self.image.get_width(), self.image.get_height() - clip_pixels))
                    screen.blit(clipped_image, (self.rect.x - cam_x, self.rect.y))
                else:
                    screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if not self.is_alive:
            self.direction.xy = (0, 0)
            return
        
        sleep_multiplier = 40 if player_sleeping else 1
        animation_speed_multiplier = sleep_multiplier  # Use same multiplier for animations
        
        if not hasattr(self, "cow") and self.move_timer <= 0 and self.is_alive and not self.fleeing:
            decision_chance = min(0.02 * sleep_multiplier, 1.0)
            if random.random() < decision_chance:
                self.direction.xy = random.choice([(-1,0), (1,0), (0,-1), (0,1), (0,0), (0,0), (0,0)])
                self.move_timer = random.randint(30, 120)
            else:
                self.direction.xy = (0, 0)
        else:
            self.move_timer -= 1

        if hasattr(self, "cow") and self.move_timer <= 0 and self.is_alive and not self.fleeing:
            decision_chance = min(0.02 * sleep_multiplier, 1.0)
            if random.random() < decision_chance:
                self.direction.xy = random.choice([(0,0), (-1,0), (1,0), (0,-1), (0,1), (0,0), (0,0)])
                self.move_timer = random.randint(30, 120)
            else:
                self.direction.xy = (0, 0)
        else:
            self.move_timer -= 1

        if self.direction.length_squared() > 0:
            can_move_x, can_move_y = self.check_collision(self.direction, nearby_objects or [], nearby_mobs or [])
            
            actual_speed = self.get_speed() * dt
            movement = self.direction * actual_speed
            
            new_x = self.rect.x + movement.x if can_move_x else self.rect.x
            new_y = self.rect.y + movement.y if can_move_y else self.rect.y
            self.rect.topleft = (new_x, new_y)

            self.animate_walk(animation_speed_multiplier)
        else:
            self.animate_stand(animation_speed_multiplier)

    def animate_walk(self, animation_speed_multiplier=1.0):
        if self.direction.x > 0:
            self.animate_frames("right", animation_speed_multiplier)
        elif self.direction.x < 0:
            self.animate_frames("left", animation_speed_multiplier)
        elif self.direction.y != 0:
            self.animate_frames(self.last_direction, animation_speed_multiplier)
        else:
            self.animate_stand(animation_speed_multiplier)

    def animate_frames(self, direction, animation_speed_multiplier=1.0):
        self.last_direction = direction
        effective_animation_speed = self.animation_speed * animation_speed_multiplier
        self.frame_index = (self.frame_index + effective_animation_speed) % len(self.walk_right_images)
        frames = self.walk_right_images if direction == "right" else self.walk_left_images
        self.image = frames[int(self.frame_index)]

    def animate_stand(self, animation_speed_multiplier=1.0):
        if self.last_direction == "right":
            stand_attr = getattr(self, "stand_right_image", None) or getattr(self, "stand_right_images", None)
        else:
            stand_attr = getattr(self, "stand_left_image", None) or getattr(self, "stand_left_images", None)

        if stand_attr is None:
            return

        if isinstance(stand_attr, pygame.Surface):
            self.image = stand_attr
        elif isinstance(stand_attr, (list, tuple)):
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = (self.frame_index + effective_animation_speed) % len(stand_attr)
            self.image = stand_attr[int(self.frame_index)]

    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 25
        bar_height = 4
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5

        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)

        if self.health < self.last_health:
            self.bar_timer = 5
            if not hasattr(self, 'enemy'):
                self.fleeing = True

        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt

        self.last_health = self.health

        if self.health <= 0:
            if self.is_alive:
                self.death_time = pygame.time.get_ticks()
            elif self.death_time is None:
                self.death_time = pygame.time.get_ticks()
            self.is_alive = False

    def harvest(self, player=None, harvest_power=1, special_chance_mult=1.0, special_yield_mult=1.0):
        if not self.destroyed and not self.is_alive:
            # Small buffer after death before harvesting is allowed
            if self.death_time is None:
                self.death_time = pygame.time.get_ticks()
            elapsed = pygame.time.get_ticks() - self.death_time
            if elapsed < self.harvest_grace_ms:
                return []

            resources = []

            # Get primary resource (hide/meat) - scale modestly with strength level, not raw attack damage
            harvest_rate = 1
            if player and hasattr(player, "strength_leveler"):
                harvest_rate = max(1, int(player.strength_leveler))
            resource_collected = min(self.resource_amount, harvest_rate)
            self.resource_amount -= resource_collected
            
            if resource_collected > 0:
                resources.extend([self.resource] * resource_collected)
            
            # Add meat/secondary resources based on mob type
            if hasattr(self, 'meat_resource'):
                meat_amount = random.randint(1, 3)
                resources.extend([self.meat_resource] * meat_amount)
            
            # Special drops for certain mobs
            if hasattr(self, 'special_drops'):
                for drop in self.special_drops:
                    if random.random() < drop['chance']:
                        amount = random.randint(drop['min'], drop['max'])
                        resources.extend([drop['item']] * amount)
            
            if self.resource_amount <= 0:
                self.destroyed = True
            
            if player and resources:
                player.experience += harvest_experience * len(resources)
                player.exp_total += harvest_experience * len(resources)
            
            return resources
        return []
    
    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive:
            if self.health < self.last_health and not hasattr(self, 'attacking'):
                self.fleeing = True
                self.flee_timer = 8
                self.move_timer = 0
                
            if self.fleeing and self.is_alive:
                if self.move_timer <= 0:
                    sleep_multiplier = 40 if player_sleeping else 1
                    decision_chance = min(0.02 * sleep_multiplier, 1.0)
                    if random.random() < decision_chance:
                        direction = pygame.Vector2(random.choice([(-1,0), (1,0), (0,-1), (0,1)]))
                    else:
                        direction = pygame.Vector2(-dx, -dy)
                        
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        
                    self.speed = 1.3
                    self.direction = direction
                    
                    self.move_timer = random.randint(30, 120)
                
                self.move_timer -= 1
                    
                if distance_sq > 400*400:
                    self.fleeing = False
                    self.speed = 1.0
                    
            if self.flee_timer > 0:
                self.flee_timer -= dt
            else:
                if distance_sq > 400*400:
                    self.fleeing = False
                    self.speed = 1.0 
class Cat(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.cat_type = random.choice(cat_types)

        self.walk_right_images = [pygame.image.load(self.cat_type[f"walk_right_image{i}"]).convert_alpha() for i in range(1, 6)]
        self.stand_right_image = pygame.image.load(self.cat_type[f"stand_right_image"]).convert_alpha()

        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center = (x, y))

        self.frame_index = 0
        self.animation_speed = 0.25
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 

        self.tame_max = 100 * (1 + (self.level * 0.05))
        self.tame = 0
        self.tamed = False
        self.just_tamed = False
        self.cat_name = None
        self.poison = False
        self.poison_time = 0
        self.poison_strength = 0
        self.poison_damage_timer = 0
        self.poison_damage_rate = 1.5
        self.death_experience = 200  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1
        self.tamed_boost = 1.1
        self.meat_resource = "Raw Small Meat"
        self.special_drops = [{'item': 'Fur', 'chance': 0.1, 'min': 1, 'max': 2}]

        self.full_health = 100 + (random.randint(5, 7) * self.level) * self.tamed_boost
        self.health = self.full_health
        self.max_health = self.full_health
        self.max_hunger = 100
        self.hunger = 100
        self.base_speed = 160
        self.speed = 1

        self.dead_cat_right_image = pygame.image.load(self.cat_type["dead_image"]).convert_alpha()
        self.dead_cat_left_image = pygame.transform.flip(self.dead_cat_right_image, True, False)
        
        # Taming bar display
        self.tame_bar_timer = 0
        self.tame_bar_display_time = 2.0  # Show bar for 2 seconds after feeding
        
        # Tamed cat behaviors
        self.follow_player = True
        self.sit = False
        self.wander = False
        self.passive = False
        self.follow_radius = 200  # Cats must stay within 500px of player
        self.target_enemy = None  # Enemy cat is attacking

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)
        
        # Update taming bar timer
        if self.tame_bar_timer > 0:
            self.tame_bar_timer -= dt
        
        # Tamed cat behavior - follow player and combat support
        if self.tamed and player and self.follow_player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            
            # Follow player if too far away
            if distance > self.follow_radius:
                if distance > 0:
                    direction = pygame.Vector2(dx, dy).normalize()
                    self.speed = 1.3  # Move faster when following
                else:
                    direction = pygame.Vector2(0, 0)
                    self.speed = 1.0
                self.direction = direction
            else:
                # Maintain position, slow wander if not in combat
                if self.wander and not self.target_enemy:
                    if self.move_timer <= 0:
                        self.direction = pygame.Vector2(random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)]))
                        self.move_timer = random.randint(60, 180)
                        self.speed = 0.7
                    self.move_timer -= 1
                else:
                    self.direction = pygame.Vector2(0, 0)
                    self.speed = 1.0
            
            # Target enemies that are attacking the player or that player is attacking
            if nearby_mobs:
                for mob in nearby_mobs:
                    # Attack if mob is attacking player or if player is attacking mob
                    if mob != self and mob.is_alive:
                        if hasattr(mob, 'target') and mob.target == player:
                            # This mob is attacking the player
                            self.target_enemy = mob
                            break
                        elif hasattr(player, 'attacking_target') and player.attacking_target == mob:
                            # Player is attacking this mob
                            self.target_enemy = mob
                            break
            
            # Attack target enemy if exists
            if self.target_enemy and self.target_enemy.is_alive:
                enemy_dx = self.target_enemy.rect.centerx - self.rect.centerx
                enemy_dy = self.target_enemy.rect.centery - self.rect.centery
                enemy_distance = (enemy_dx**2 + enemy_dy**2) ** 0.5
                
                # Move toward enemy if not in attack range
                if enemy_distance > 50:
                    if enemy_distance > 0:
                        enemy_direction = pygame.Vector2(enemy_dx, enemy_dy).normalize()
                        self.direction = enemy_direction
                        self.speed = 1.2
                    self.move_timer = 0
                else:
                    # Attack the enemy
                    self.attacking = True
                    self.attack_cooldown = 0.5
            else:
                # Clear target if it's dead or none found
                if self.target_enemy and not self.target_enemy.is_alive:
                    self.target_enemy = None

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_cat_right_image
            else:
                self.image = self.dead_cat_left_image

    def feed_cat(self, item_name):
        """Feed the cat with food item. Returns the tame increase amount."""
        tame_increase = 0
        health_increase = 0
        
        # Raw meats - +20 tame, +15 health
        if item_name in ["Fish", "Raw Venison", "Raw Lizard Meat", "Raw Beef", "Raw Chicken", "Raw Small Meat", "Raw Bear Meat"]:
            tame_increase = 20
            health_increase = 15
        # Cooked meats - +10 tame, +20 health
        elif item_name in ["Cooked Fish", "Cooked Venison", "Cooked Lizard Meat", "Cooked Beef", "Cooked Chicken", "Cooked Small Meat", "Cooked Bear Meat"]:
            tame_increase = 5
            health_increase = 20
        # Milk - +30 tame, +25 health
        elif item_name =="Small Milk":
            tame_increase = 30
            health_increase = 25
        elif item_name == "Medium Glass Milk":
            tame_increase = 60
            health_increase = 50
        elif item_name == "Large Metal Milk":
            tame_increase = 150
            health_increase = 100
        # Poisonous Mushroom - same as player (poison)
        elif item_name == "Poisonous Mushroom":
            tame_increase = -50
            self.poison = True
            self.poison_time = 30
            self.poison_strength = 1
            return 0
        # Other normal foods - +1 tame, +5 health
        elif item_name in ["Apples", "Oranges", "Coconuts", "Pineapple", "Watermelon", "Mushroom", "Blood Berries", "Dawn Berries", "Dusk Berries", "Sun Berries", "Teal Berries", "Twilight Drupes", "Vio Berries"]:
            tame_increase = 1
            health_increase = 5
        
        # Apply tame increase and health increase
        if tame_increase > 0:
            self.tame = min(self.tame + tame_increase, self.tame_max)
            # Increase health when feeding
            self.health = min(self.health + health_increase, self.max_health)
            
            # Check if just became tamed
            if self.tame >= self.tame_max and not self.tamed:
                self.tamed = True
                self.just_tamed = True
            
            # Play cat purr sound
            sound_manager.play_sound(random.choice(["cat_purr1", "cat_purr2"]))
            # Show taming bar
            self.tame_bar_timer = self.tame_bar_display_time
        
        return tame_increase
    
    def draw_tame_bar(self, screen, cam_x):
        """Draw the taming bar above the cat."""
        if self.tame_bar_timer <= 0:
            return
        
        bar_width = 50
        bar_height = 8
        x = self.rect.centerx - cam_x - bar_width // 2
        y = self.rect.top + 5
        
        # Draw background (dark purple)
        pygame.draw.rect(screen, (60, 20, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
        
        # Draw taming progress (bright purple)
        tame_ratio = self.tame / self.tame_max
        tame_width = int(bar_width * tame_ratio)
        pygame.draw.rect(screen, (200, 100, 200), pygame.Rect(x, y, tame_width, bar_height), border_radius=2)
        
        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
    
    def draw_cat_name(self, screen, cam_x):
        """Draw the cat's name above its head if it has one."""
        if self.cat_name:
            font = pygame.font.SysFont(None, 20)
            name_text = font.render(str(self.cat_name) + " Lvl " + str(self.level), True, (255, 255, 200))
            text_x = self.rect.centerx - cam_x - name_text.get_width() // 2
            text_y = self.rect.top + 5
            draw_text_with_background(screen, name_text, text_x, text_y)
        
    def draw(self, screen, cam_x):

        self.draw_tame_bar(screen, cam_x)
        self.draw_cat_name(screen, cam_x)
        super().draw(screen, cam_x)

    def get_item_data(self):
        """Create inventory item data for this cat."""
        cat_type = self.cat_type["type"]
        
        # Map cat type to item name and icon
        cat_type_to_mapping = {
            "black": ("Tamed Black Cat", "assets/sprites/mobs/BlackCatRightStanding.png"),
            "salt_and_pepper": ("Tamed Salt and Pepper Cat", "assets/sprites/mobs/SandPCatRightStanding.png"),
            "white": ("Tamed White Cat", "assets/sprites/mobs/WhiteCatRightStanding.png"),
            "white_and_black": ("Tamed Black and White Cat", "assets/sprites/mobs/WandBCatRightStanding.png"),
            "sandy": ("Tamed Sandy Cat", "assets/sprites/mobs/SandyCatRightStanding.png"),
            "orange": ("Tamed Orange Cat", "assets/sprites/mobs/OrangeCatRightStanding.png"),
            "calico": ("Tamed Calico Cat", "assets/sprites/mobs/CalicoCatRightStanding.png"),
            "gray": ("Tamed Gray Cat", "assets/sprites/mobs/GrayCatRightStanding.png"),
            "white_and_orange": ("Tamed Orange and White Cat", "assets/sprites/mobs/WandOCatRightStanding.png")
        }
        
        item_name, icon = cat_type_to_mapping.get(cat_type, ("Tamed Black Cat", "assets/sprites/mobs/BlackCatRightStanding.png"))
        
        return {
            "item_name": item_name,
            "icon": icon,
            "quantity": 1,
            "cat_object": self,
            "cat_type": cat_type,
            "cat_tame": self.tame,
            "cat_health": self.health,
            "cat_level": self.level,
            "cat_name": self.cat_name
        }


class Squirrel(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)

        self.walk_right_images = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (48, 48)) for img in squirrel_move_images]
        self.stand_right_image = pygame.transform.scale(pygame.image.load(squirrel_stand_image).convert_alpha(), (48, 48))

        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 150
        self.speed = 1
        self.full_health = 50 + (random.randint(5, 7) * self.level)
        self.health = self.full_health
        self.level = 1
        self.death_experience = 75 * (1 + (self.level * self.death_experience * .0001))
        self.resource = "Hide"
        self.meat_resource = "Raw Small Meat"
        self.special_drops = [{'item': 'Fur', 'chance': 0.1, 'min': 1, 'max': 2}]
        

        self.frame_index = 0
        self.animation_speed = 0.3
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 
        self.dead_squirrel_right_image = pygame.transform.scale(pygame.image.load(squirrel_dead_image).convert_alpha(), (48, 48))
        self.dead_squirrel_left_image = pygame.transform.flip(self.dead_squirrel_right_image, True, False)

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_squirrel_right_image
            else:
                self.image = self.dead_squirrel_left_image


class Cow(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.cow_type = random.choice(cow_types)

        self.walk_right_images = [pygame.transform.scale(pygame.image.load(self.cow_type[f"walk_right_image{i}"]).convert_alpha(), (size, size)) for i in range(1, 6)]
        self.stand_right_image = pygame.transform.scale(pygame.image.load(self.cow_type[f"stand_right_image"]).convert_alpha(), (size, size))

        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center = (x, y))

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right"

        self.full_health = 150 + (random.randint(5, 7) * self.level)
        self.health = self.full_health
        self.base_speed = 70
        self.speed = 1
        self.meat_resource = "Raw Beef"
        self.resource = "Hide"
        self.resource_amount = 5
        self.cow = "moo"
        self.death_experience = 100  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1

        self.dead_cow_right_image = pygame.transform.scale(pygame.image.load(self.cow_type["dead_image"]).convert_alpha(), (size, size))
        self.dead_cow_left_image = pygame.transform.flip(self.dead_cow_right_image, True, False)

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_cow_right_image
            else:
                self.image = self.dead_cow_left_image


class Chicken(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)

        self.walk_right_images = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (40, 40)) for img in chicken_move_images]
        self.stand_right_image = pygame.transform.scale(pygame.image.load(chicken_stand_image).convert_alpha(), (40, 40))

        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]
        self.stand_left_image = pygame.transform.flip(self.stand_right_image, True, False)

        self.image = self.stand_right_image
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 120
        self.speed = 1
        self.meat_resource = "Raw Chicken"
        self.special_drops = [{'item': 'Feathers', 'chance': 0.5, 'min': 1, 'max': 2}
]
        self.resource_amount = random.randint(3, 6)
        self.full_health = 80 + (random.randint(5, 7) * self.level)
        self.health = self.full_health
        self.death_experience = 70  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1

        self.frame_index = 0
        self.animation_speed = 0.3
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right"
        self.dead_chicken_right_image = pygame.transform.scale(pygame.image.load(chicken_dead_image).convert_alpha(), (40, 40))
        self.dead_chicken_left_image = pygame.transform.flip(self.dead_chicken_right_image, True, False)

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_chicken_right_image
            else:
                self.image = self.dead_chicken_left_image


class Enemy(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.chasing = False
        self.special_drops = [{'item': 'Bone', 'chance': 0.3, 'min': 1, 'max': 3}]
        self.enemy = True
        self.attacking = False
        self.death_experience = 500  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1

    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        if self.is_alive:
            if 50 * 50 < distance_sq < 200*200:
                self.chasing = True
            elif distance_sq > 400*400:
                self.chasing = False

            if self.chasing and not self.fleeing:
                direction = pygame.Vector2(dx, dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                self.direction = direction 

    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        if self.is_alive:
            if self.health < self.full_health*.2 and not hasattr(self, 'enemy'):
                self.fleeing = True
                self.flee_timer = 8
            
            if self.fleeing:
                direction = pygame.Vector2(-dx, -dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                speed = self.speed * 1.2
                self.direction = direction * speed

                if distance_sq > 600*600:
                    self.fleeing = False

            if self.flee_timer > 0:
                self.flee_timer -= dt
            
            if distance_sq > 600*600:
                self.fleeing = False

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.is_alive:
            if getattr(self, "attacking", False):
                return
            
            sleep_multiplier = 40 if player_sleeping else 1
            animation_speed_multiplier = sleep_multiplier  # Use same multiplier for animations
            
            if not self.chasing:
                if self.move_timer <= 0:
                    decision_chance = min(0.02 * sleep_multiplier, 1.0)
                    if random.random() < decision_chance:
                        self.direction.xy = random.choice([(-1,0), (1,0), (0,-1), (0,1), (0,0)])
                        self.move_timer = random.randint(30, 120)
                    else:
                        self.direction.xy = (0, 0)
                else:
                    self.move_timer -= 1

            if self.direction.length_squared() > 0:
                can_move_x, can_move_y = self.check_collision(self.direction, nearby_objects or [], nearby_mobs or [])
                
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                
                new_x = self.rect.x + movement.x if can_move_x else self.rect.x
                new_y = self.rect.y + movement.y if can_move_y else self.rect.y
                self.rect.topleft = (new_x, new_y)

                self.animate_walk(animation_speed_multiplier)
            else:
                self.animate_stand(animation_speed_multiplier)

class Crawler(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.name = name
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in crawler_move_left_images]
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in crawler_idle_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in crawler_attack_left_images]

        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]

        self.image = self.stand_right_images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 20

        self.attack_damage = 3
        self.base_speed = 100
        self.speed = 1
        self.health = self.full_health = 150 + (random.randint(5, 7) * self.level)
        self.health = self.full_health
        self.resource = "Hide"
        self.resource_amount = random.randint(4, 9)
        self.death_experience = 500  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1

    def attack(self, player_world_x, player_world_y, player):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        if self.chasing == True:
            self.speed = 1.5
        else:
            self.speed = 1

        if self.is_alive and (self.health / self.full_health) < 0.2:
            if not self.fleeing:
                self.fleeing = True
                self.flee_timer = 8
            self.attacking = False
            return

        if self.fleeing:
            self.attacking = False
            return

        if self.is_alive and distance_sq < (50 * 50):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0

        if self.attacking:
            frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

            self.attack_timer -= 1

            if self.attack_timer == self.attack_duration // 2 and distance_sq < (50 * 50):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if not self.is_alive:
            if self.last_direction == "left":
                self.image = crawler_dead_image_left
            else:
                self.image = crawler_dead_image_right

class Duskwretch(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.name = name
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in duskwretch_move_left_images]
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in duskwretch_idle_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in duskwretch_attack_left_images]
        self.start_walk_left_images = [pygame.image.load(img).convert_alpha() for img in duskwretch_start_move_left_images]
        self.end_walk_left_images = [pygame.image.load(img).convert_alpha() for img in duskwretch_end_move_left_images]
        self.chase_left_images = [pygame.image.load(img).convert_alpha() for img in duskwretch_chase_left_images]

        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        self.start_walk_right_images = [pygame.transform.flip(img, True, False) for img in self.start_walk_left_images]
        self.end_walk_right_images = [pygame.transform.flip(img, True, False) for img in self.end_walk_left_images]
        self.chase_right_images = [pygame.transform.flip(img, True, False) for img in self.chase_left_images]

        self.image = self.stand_right_images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.death_experience = 1200  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1

        self.last_direction = "right" 
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 20
        self.has_roared = False
        self.chase_steps_timer = 0

        self.attack_damage = 4
        self.base_speed = 150
        self.speed = 1
        self.full_health = 180 + (random.randint(15, 22) * self.level)
        self.health = self.full_health
        self.resource = "Hide"
        self.meat_resource = "Dusk Meat"
        self.special_drops.append({'item': 'Duskwretch Claws', 'chance': 0.4, 'min': 1, 'max': 2}
)
        self.resource_amount = random.randint(4, 9)

        self.state = "idle"
        self.was_moving = False
        self.is_moving = False
        self.transition_done = False

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 10, rect.y + 50, rect.width - 20, rect.height - 70)

    def attack(self, player_world_x, player_world_y, player):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy

        if self.is_alive and distance_sq < (70 * 70):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0

        if self.attacking:
            self.state = "attacking"
            self.animation_speed = .13
            frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

            self.attack_timer -= 2

            if self.attack_timer == self.attack_duration // 2 and distance_sq < (70 * 70):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.state = "idle"

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if self.attacking:
            return

        if not self.is_alive:
            self.direction.xy = (0, 0)
            self.image = duskwretch_dead_image_left if self.last_direction == "left" else duskwretch_dead_image_right
            return

        self.is_moving = self.direction.length_squared() > 0 and self.is_alive

        if self.is_moving and not self.was_moving:
            if self.chasing:
                sound_manager.play_sound(random.choice(["duskwretch_roar1", "duskwretch_roar2"]))
                self.state = "chase"
                self.speed = 2.2
            else:
                self.state = "start_walk"
                self.speed = 1.0
            self.frame_index = 0
            self.transition_done = False

        elif not self.is_moving and self.was_moving:
            self.state = "end_walk"
            self.speed = 1.0
            self.frame_index = 0
            self.transition_done = False

        elif self.is_moving and self.chasing and self.state != "chase":
            self.state = "chase"
            self.speed = 2.2
            self.frame_index = 0

        elif self.is_moving and not self.chasing and self.state == "chase":
            self.state = "walk"
            self.speed = 1.0
            self.frame_index = 0

        if self.chasing and self.is_moving:
            self.chase_steps_timer -= dt
            if self.chase_steps_timer <= 0:
                sound_manager.play_sound(random.choice([f"duskwretch_chase_steps{i}" for i in range(1, 6)]))
                self.chase_steps_timer = 0.3

        sleep_multiplier = 40 if player_sleeping else 1
        animation_speed_multiplier = sleep_multiplier
        
        self.animate_state(dt, animation_speed_multiplier)
        self.was_moving = self.is_moving


    def animate_state(self, dt, animation_speed_multiplier=1.0):
        if self.state == "attacking":
            return
            
        elif self.state == "start_walk":
            self.animation_speed = .1
            frames = self.start_walk_right_images if self.last_direction == "right" else self.start_walk_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index += effective_animation_speed
            if self.frame_index >= len(frames):
                if self.chasing:
                    self.state = "chase"
                else:
                    self.state = "walk"
                self.frame_index = 0
            else:
                self.image = frames[int(self.frame_index)]

        elif self.state == "walk":
            frames = self.walk_right_images if self.last_direction == "right" else self.walk_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

        elif self.state == "chase":
            self.animation_speed = .13
            frames = self.chase_right_images if self.last_direction == "right" else self.chase_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

        elif self.state == "end_walk":
            frames = self.end_walk_right_images if self.last_direction == "right" else self.end_walk_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index += effective_animation_speed
            if self.frame_index >= len(frames):
                self.state = "idle"
                self.frame_index = 0
            else:
                self.image = frames[int(self.frame_index)]

        elif self.state == "idle":
            frames = self.stand_right_images if self.last_direction == "right" else self.stand_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        return
    

class AggressiveMob(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.chasing = False
        self.aggressive = False
        self.attacking = False

    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        if not self.aggressive:
            return

        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        if self.is_alive:
            if 50 * 50 < distance_sq < 250*250:
                self.chasing = True
            elif distance_sq > 400*400:
                self.chasing = False

            if self.chasing and not self.fleeing:
                direction = pygame.Vector2(dx, dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                self.direction = direction

    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        if self.is_alive:
            if self.health < self.full_health*.2 and not hasattr(self, 'attacking'):
                self.fleeing = True
                self.flee_timer = 8
                self.move_timer = 0

            if self.fleeing and self.is_alive:
                if self.move_timer <= 0:
                    sleep_multiplier = 40 if player_sleeping else 1
                    decision_chance = min(0.02 * sleep_multiplier, 1.0)
                    if random.random() < decision_chance:
                        direction = pygame.Vector2(random.choice([(-1,0), (1,0), (0,-1), (0,1)]))
                    else:
                        direction = pygame.Vector2(-dx, -dy)

                    if direction.length_squared() > 0:
                        direction = direction.normalize()

                    self.speed = 1.5
                    self.direction = direction

                    self.move_timer = random.randint(30, 120)

                self.move_timer -= 1

                if distance_sq > 600*600:
                    self.fleeing = False
                    self.speed = 1.0

            if self.flee_timer > 0:
                self.flee_timer -= dt
            else:
                if distance_sq > 600*600:
                    self.fleeing = False
                    self.speed = 1.0

    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        super().handle_health(screen, cam_x, dt, player_sleeping)
        if self.health < self.last_health and not self.aggressive:
            self.aggressive = True
            self.enemy = True


class Pock(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.name = name
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in pock_idle_images]
        self.walk_right_images = [pygame.image.load(img).convert_alpha() for img in pock_move_right_images]
        self.throw_right_images = [pygame.image.load(img).convert_alpha() for img in pock_throw_right_images]

        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.throw_left_images = [pygame.transform.flip(img, True, False) for img in self.throw_right_images]
        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]

        self.image = self.stand_right_images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right"
        self.throwing = False
        self.throw_timer = 0
        self.throw_duration = 30

        self.attack_damage = 5
        self.base_speed = 120
        self.speed = 1
        self.full_health = 100 + (random.randint(12, 20) * self.level)
        self.health = self.full_health
        self.resource = "Hide"
        self.resource_amount = random.randint(2, 5)
        self.death_experience = 500  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1

    def attack(self, player_world_x, player_world_y, player):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy

        if self.is_alive and distance_sq < (100 * 100):
            if not self.throwing:
                self.throwing = True
                self.throw_timer = self.throw_duration
                self.frame_index = 0.0

        if self.throwing:
            frames = self.throw_right_images if self.last_direction == "right" else self.throw_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

            self.throw_timer -= 1

            if self.throw_timer == self.throw_duration // 2 and distance_sq < (100 * 100):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
                

            if self.throw_timer <= 0:
                self.throwing = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if not self.is_alive:
            if self.last_direction == "left":
                self.image = pock_dead_image_left
            else:
                self.image = pock_dead_image_right



class Deer(AggressiveMob):
    global player_world_x, player_world_y
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.is_buck = random.choice([True, False])
        if self.is_buck:
            self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in buck_idle_images]
            self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in buck_walk_left_images]
            self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in buck_attack_left_images]
            self.dead_image_left = buck_dead_image
        else:
            self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in deer_idle_images]
            self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in deer_walk_left_images]
            self.dead_image_left = deer_dead_image
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        
        if self.is_buck:
            self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
            self.attack_timer = 0
            self.attack_duration = 25
            self.attack_damage = 7
        
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 180
        self.speed = 1
        self.full_health = 150 + (random.randint(5, 7) * self.level)
        self.health = self.full_health
        self.meat_resource = "Raw Venison"
        if self.is_buck:
            self.special_drops = [
        {'item': 'Buck Antlers', 'chance': 0.1, 'min': 1, 'max': 2}]
        else:
            self.special_drops = []
        self.resource_amount = random.randint(4, 8)
        self.frame_index = 0
        self.animation_speed = 0.2
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        self.hoof_timer = 0
        self.is_moving = False
        self.level = 1

        if self.is_buck:

            self.death_experience = 300  * (1 + (self.level * self.death_experience * .0001))
            self.aggressive = False
            self.enemy = False
        else:

            self.death_experience = 150  * (1 + (self.level * self.death_experience * .0001))
            self.aggressive = False
            self.enemy = False


    def get_collision_rect(self, cam_x):
            if self.is_buck:
                rect = self.rect
                return pygame.Rect(rect.x - cam_x + 15, rect.y + 50, rect.width - 30, rect.height - 55)
            else:
                rect = self.rect
                return pygame.Rect(rect.x - cam_x + 5, rect.y + 20, rect.width - 20, rect.height - 35)

    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 25
        bar_height = 4
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5
        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)
        
        if self.health < self.last_health:
            self.bar_timer = 5
            if self.is_buck and not self.aggressive:
                self.aggressive = True
                self.enemy = True
            elif not self.is_buck:
                self.fleeing = True
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        if not self.is_buck:
            dx = player_world_x - self.rect.centerx
            dy = player_world_y - self.rect.centery
            distance_sq = dx*dx + dy*dy
            
            if self.is_alive and distance_sq < 300*300:
                self.fleeing = True
                self.flee_timer = 8
                
                if self.move_timer <= 0:
                    direction = pygame.Vector2(-dx, -dy)
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                    
                    self.speed = 1.5
                    self.direction = direction
                    self.move_timer = random.randint(30, 120)
                
                self.move_timer -= 1
                
                if distance_sq > 500*500:
                    self.fleeing = False
                    self.speed = 1.0
            
            if self.flee_timer > 0:
                self.flee_timer -= dt
            else:
                if distance_sq > 500*500:
                    self.fleeing = False
                    self.speed = 1.0
        else:
            self.fleeing = False
    
    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        if self.is_buck and self.aggressive:
            dx = player_world_x - self.rect.centerx
            dy = player_world_y - self.rect.centery
            distance_sq = dx*dx + dy*dy
            
            if self.is_alive:
                if 50 * 50 < distance_sq < 250*250:
                    self.chasing = True
                elif distance_sq > 400*400:
                    self.chasing = False
                
                if self.chasing and not self.attacking:
                    direction = pygame.Vector2(dx, dy)
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                    self.direction = direction
    
    def attack(self, player_world_x, player_world_y, player):
        if not self.is_buck or not self.aggressive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive and distance_sq < (70 * 70):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0
        
        if self.attacking:
            frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
            
            self.attack_timer -= 1
            
            if self.attack_timer == self.attack_duration // 2 and distance_sq < (70 * 70):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.attacking:
            super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)
            return
        
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)
        
        self.is_moving = self.direction.length_squared() > 0 and self.is_alive
        
        if self.is_moving or self.chasing == True or self.fleeing == True:
            self.hoof_timer -= dt
            if self.hoof_timer <= 0 and getattr(self, 'is_visible', True):
                sound_manager.play_sound(random.choice([f"hoofs{i}" for i in range(1, 7)]))
                self.hoof_timer = random.uniform(0.3, 0.7)
        else:
            self.hoof_timer = random.uniform(0.5, 1.0)
        
        if not self.is_alive:
            if self.last_direction == "right":
                self.image = pygame.transform.flip(self.dead_image_left, True, False)
            else:
                self.image = self.dead_image_left


class BlackBear(AggressiveMob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in black_bear_idle_images]
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in black_bear_walk_left_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in black_bear_attack_left_images]
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 80
        self.speed = 1
        self.full_health = 220 + (random.randint(7, 13) * self.level)
        self.health = self.full_health
        self.meat_resource = "Raw Bear Meat"
        self.special_drops = [{'item': 'Fur', 'chance': 0.6, 'min': 2, 'max': 4}]
        self.resource_amount = 8
        self.death_experience = 600  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1
        
        self.frame_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        
        self.attack_timer = 0
        self.attack_duration = 30
        self.attack_damage = 10
        
        self.aggressive = False
        self.enemy = False
    
    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 5, rect.y + 20, rect.width - 10, rect.height - 40)
    
    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 25
        bar_height = 4
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5
        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)
        
        if self.health < self.full_health * 0.5 and not self.aggressive:
            self.aggressive = True
            self.enemy = True
            self.fleeing = False
        
        if self.health < self.last_health:
            self.bar_timer = 5
            if not self.aggressive:
                self.fleeing = True
                self.flee_timer = 8
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        if not self.aggressive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive:
            if 50 * 50 < distance_sq < 250*250:
                self.chasing = True
            elif distance_sq > 400*400:
                self.chasing = False
            
            if self.chasing and not self.fleeing and not self.attacking:
                direction = pygame.Vector2(dx, dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                self.direction = direction
                self.speed = 3.0
            elif not self.attacking and not self.fleeing:
                self.speed = 1.0
    
    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        if self.aggressive:
            self.fleeing = False
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive:
            if self.fleeing and self.is_alive:
                if self.move_timer <= 0:
                    sleep_multiplier = 40 if player_sleeping else 1
                    decision_chance = min(0.02 * sleep_multiplier, 1.0)
                    if random.random() < decision_chance:
                        direction = pygame.Vector2(random.choice([(-1,0), (1,0), (0,-1), (0,1)]))
                    else:
                        direction = pygame.Vector2(-dx, -dy)
                        
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        
                    self.speed = 3.0
                    self.direction = direction
                    
                    self.move_timer = random.randint(30, 120)
                
                self.move_timer -= 1
                    
                if distance_sq > 400*400:
                    self.fleeing = False
                    self.speed = 1.0
                    
            if self.flee_timer > 0:
                self.flee_timer -= dt
            else:
                if distance_sq > 400*400:
                    self.fleeing = False
                    self.speed = 1.0
    
    def attack(self, player_world_x, player_world_y, player):
        if not self.aggressive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive and distance_sq < (70 * 70):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0
        
        if self.attacking:
            frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
            
            self.attack_timer -= 1
            
            if self.attack_timer == self.attack_duration // 2 and distance_sq < (70 * 70):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
            
            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.attacking:
            return
        
        if not self.is_alive:
            self.direction.xy = (0, 0)
            if self.last_direction == "right":
                self.image = pygame.transform.flip(black_bear_dead_image, True, False)
            else:
                self.image = black_bear_dead_image
            return
        
        if self.chasing and self.aggressive:
            if self.direction.length_squared() > 0:
                can_move_x, can_move_y = self.check_collision(self.direction, nearby_objects or [], nearby_mobs or [])
                
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                
                new_x = self.rect.x + movement.x if can_move_x else self.rect.x
                new_y = self.rect.y + movement.y if can_move_y else self.rect.y
                self.rect.topleft = (new_x, new_y)
                self.animate_walk()
            else:
                self.animate_stand()
        elif self.fleeing and not self.aggressive:
            if self.direction.length_squared() > 0:
                can_move_x, can_move_y = self.check_collision(self.direction, nearby_objects or [], nearby_mobs or [])
                
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                
                new_x = self.rect.x + movement.x if can_move_x else self.rect.x
                new_y = self.rect.y + movement.y if can_move_y else self.rect.y
                self.rect.topleft = (new_x, new_y)
                self.animate_walk()
            else:
                self.animate_stand()
        else:
            super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

class BrownBear(AggressiveMob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in brown_bear_idle_images]
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in brown_bear_walk_left_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in brown_bear_attack_left_images]
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 85
        self.speed = 1
        self.full_health = 300 + (random.randint(8, 20) * self.level)
        self.health = self.full_health
        self.meat_resource = "Raw Bear Meat"
        self.special_drops = [{'item': 'Fur', 'chance': 0.6, 'min': 2, 'max': 4}]
        self.resource_amount = 8
        
        self.frame_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        
        self.attack_timer = 0
        self.attack_duration = 30
        self.attack_damage = 15
        self.death_experience = 800 * (1 + (self.level * self.death_experience * .0001))
        self.level = 1
        
        self.aggressive = False
        self.enemy = False

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 5, rect.y + 30, rect.width - 10, rect.height - 50)
    
    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 25
        bar_height = 4
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5
        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)
        
        if self.health < self.last_health and not self.aggressive:
            self.aggressive = True
            self.enemy = True
        
        if self.health < self.last_health:
            self.bar_timer = 5
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        if not self.aggressive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive:
            if 50 * 50 < distance_sq < 250*250:
                self.chasing = True
            elif distance_sq > 400*400:
                self.chasing = False
            
            if self.chasing and not self.attacking:
                direction = pygame.Vector2(dx, dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                self.direction = direction
                self.speed = 3.5
            elif not self.attacking:
                self.speed = 1.0
    
    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        self.fleeing = False
    
    def attack(self, player_world_x, player_world_y, player):
        if not self.aggressive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive and distance_sq < (70 * 70):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0
        
        if self.attacking:
            frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
            
            self.attack_timer -= 1
            
            if self.attack_timer == self.attack_duration // 2 and distance_sq < (70 * 70):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
            
            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.attacking:
            return
        
        if not self.is_alive:
            self.direction.xy = (0, 0)
            if self.last_direction == "right":
                self.image = pygame.transform.flip(brown_bear_dead_image, True, False)
            else:
                self.image = brown_bear_dead_image
            return
        
        if self.chasing and self.aggressive:
            if self.direction.length_squared() > 0:
                can_move_x, can_move_y = self.check_collision(self.direction, nearby_objects or [], nearby_mobs or [])
                
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                
                new_x = self.rect.x + movement.x if can_move_x else self.rect.x
                new_y = self.rect.y + movement.y if can_move_y else self.rect.y
                self.rect.topleft = (new_x, new_y)
                self.animate_walk()
            else:
                self.animate_stand()
        else:
            super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

class Gila(AggressiveMob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in gila_idle_images]
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in gila_walk_left_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in gila_attack_left_images]
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 60
        self.speed = 1
        self.full_health = 60 + (random.randint(5, 10) * self.level)
        self.health = self.full_health
        self.resource = "Gila Meat"
        self.special_drops = [{'item': 'Venom Sac', 'chance': 0.1, 'min': 1, 'max': 2}]
        self.resource_amount = 2
        self.death_experience = 500  * (1 + (self.level * self.death_experience * .0001))
        self.level = 1
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        
        self.attack_timer = 0
        self.attack_duration = 25
        self.attack_damage = 6
        
        self.aggressive = False
        self.enemy = False
    

    def get_collision_rect(self, cam_x):
            rect = self.rect
            return pygame.Rect(rect.x - cam_x, rect.y + 30, rect.width, rect.height - 40)

    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 25
        bar_height = 4
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5
        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)
        
        if self.health < self.last_health and not self.aggressive:
            self.aggressive = True
            self.enemy = True
        
        if self.health < self.last_health:
            self.bar_timer = 5
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        self.fleeing = False
    
    def attack(self, player_world_x, player_world_y, player):
        if not self.aggressive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive and distance_sq < (50 * 50):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0
        
        if self.attacking:
            frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
            
            self.attack_timer -= 1
            
            if self.attack_timer == self.attack_duration // 2 and distance_sq < (50 * 50):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
            
            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.attacking:
            return
        
        if not self.is_alive:
            self.direction.xy = (0, 0)
            if self.last_direction == "right":
                self.image = pygame.transform.flip(gila_dead_image, True, False)
            else:
                self.image = gila_dead_image
            return
        
        if self.chasing and self.aggressive:
            if self.direction.length_squared() > 0:
                can_move_x, can_move_y = self.check_collision(self.direction, nearby_objects or [], nearby_mobs or [])
                
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                
                new_x = self.rect.x + movement.x if can_move_x else self.rect.x
                new_y = self.rect.y + movement.y if can_move_y else self.rect.y
                self.rect.topleft = (new_x, new_y)
                self.animate_walk()
            else:
                self.animate_stand()
        else:
            super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)


class Crow(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in crow_walk_left_images]
        self.fly_left_images = [pygame.image.load(img).convert_alpha() for img in crow_fly_left_images]
        self.start_fly_left_images = [pygame.image.load(img).convert_alpha() for img in crow_start_fly_left_images]
        self.landing_left_images = [pygame.image.load(img).convert_alpha() for img in crow_landing_left_images]
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.fly_right_images = [pygame.transform.flip(img, True, False) for img in self.fly_left_images]
        self.start_fly_right_images = [pygame.transform.flip(img, True, False) for img in self.start_fly_left_images]
        self.landing_right_images = [pygame.transform.flip(img, True, False) for img in self.landing_left_images]
        
        self.image = self.walk_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 140
        self.speed = 1
        self.full_health = 30 + (random.randint(5, 10) * self.level)
        self.health = self.full_health
        self.resource = "Feathers"
        self.special_drops = [{'item': 'Raw Small Meat', 'chance': 0.6, 'min': 2, 'max': 4}]
        self.resource_amount = 4
        self.death_experience = 400 * (1 + (self.level * self.death_experience * .0001))
        self.level = 1
        
        self.frame_index = 0
        self.animation_speed = 0.25
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        self.state = "walking"
        self.flying_timer = 0

    
    def get_collision_rect(self, cam_x):
            rect = self.rect
            return pygame.Rect(rect.x - cam_x + 25, rect.y + 30, rect.width - 43, rect.height - 47)
    
    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 25
        bar_height = 4
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5
        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)
        
        if self.health < self.last_health:
            self.bar_timer = 5
            if self.state != "flying":
                self.state = "flying"
                self.frame_index = 0
                self.flying_timer = random.randint(180, 300)
                self.direction = pygame.Vector2(random.choice([-1, 1]), random.uniform(-1.5, -0.5))
                if self.direction.length_squared() > 0:
                    self.direction = self.direction.normalize()
                self.speed = 1.5
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def check_collision(self, direction, nearby_objects, nearby_mobs):
        if self.state == "flying":
            return True, True 
        return super().check_collision(direction, nearby_objects, nearby_mobs)
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if not self.is_alive:
            self.direction.xy = (0, 0)
            self.state = "walking"
            if self.last_direction == "right":
                self.image = pygame.transform.flip(crow_dead_image, True, False)
            else:
                self.image = crow_dead_image
            return
        
        sleep_multiplier = 40 if player_sleeping else 1
        decision_chance = min(0.001 * sleep_multiplier, 1.0)
        if self.state == "walking" and random.random() < decision_chance:
            self.state = "flying"
            self.frame_index = 0
            self.flying_timer = random.randint(60, 180)
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.direction.length_squared() > 0:
                self.direction = self.direction.normalize()
        
        if self.state == "flying":
            self.flying_timer -= 1
            if self.flying_timer <= 0:
                self.state = "landing"
                self.frame_index = 0
                self.speed = 1.0
        
        if self.state == "landing" and self.frame_index >= len(self.landing_left_images) - 1:
            self.state = "walking"
            self.frame_index = 0
            self.direction = pygame.Vector2(0, 0)
        
        if self.state == "flying":
            if self.direction.length_squared() > 0:
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                self.rect.x += movement.x
                self.rect.y += movement.y
                if movement.x > 0:
                    self.last_direction = "right"
                elif movement.x < 0:
                    self.last_direction = "left"
            self.animate_stand()
        else:
            super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)
    
    def animate_stand(self, animation_speed_multiplier=1.0):
        if self.state == "walking":
            super().animate_stand(animation_speed_multiplier)
        elif self.state == "flying":
            if self.frame_index < len(self.start_fly_left_images):
                frames = self.start_fly_right_images if self.last_direction == "right" else self.start_fly_left_images
                effective_animation_speed = self.animation_speed * animation_speed_multiplier
                self.frame_index += effective_animation_speed
                if self.frame_index >= len(self.start_fly_left_images):
                    self.frame_index = 0
                self.image = frames[int(min(self.frame_index, len(frames) - 1))]
            else:
                frames = self.fly_right_images if self.last_direction == "right" else self.fly_left_images
                effective_animation_speed = self.animation_speed * animation_speed_multiplier
                self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
                self.image = frames[int(self.frame_index)]
        elif self.state == "landing":
            frames = self.landing_right_images if self.last_direction == "right" else self.landing_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = min(self.frame_index + effective_animation_speed, len(frames) - 1)
            self.image = frames[int(self.frame_index)]


class Dragon(Enemy):
    def __init__(self, x, y, name, dragon_type, level=1):
        super().__init__(x, y, name)
        self.dragon_type = dragon_type
        self.type_data = next((d for d in dragon_types if d["type"] == dragon_type), None)
        self.level = level
        
        images_dict = {
            "fire": fire_dragon_images,
            "ice": ice_dragon_images,
            "electric": electric_dragon_images,
            "poison": poison_dragon_images,
            "dusk": dusk_dragon_images
        }
        self.dragon_images = images_dict.get(dragon_type)
        
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["walk_left"]]
        self.idle_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["idle_left"]]
        self.start_fly_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["start_fly_left"]]
        self.fly_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["fly_left"]]
        self.end_fly_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["end_fly_left"]]
        self.bite_attack_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["bite_attack_left"]]
        self.breath_attack_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["breath_attack_left"]]
        self.breath_effect_left_images = [pygame.image.load(img).convert_alpha() for img in self.dragon_images["breath_effect_left"]]
        self.dead_image_left = pygame.image.load(self.dragon_images["dead_left"]).convert_alpha()
        
        scale = (1.0 + (level - 1) * 0.025) * 0.5
        self._scale_images(scale)
        self.size_scale = scale
        self.dead_image_left = pygame.transform.scale(self.dead_image_left, (int(self.dead_image_left.get_width() * scale), int(self.dead_image_left.get_height() * scale)))
        self.dead_image_right = pygame.transform.flip(self.dead_image_left, True, False)
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.idle_right_images = [pygame.transform.flip(img, True, False) for img in self.idle_left_images]
        self.start_fly_right_images = [pygame.transform.flip(img, True, False) for img in self.start_fly_left_images]
        self.fly_right_images = [pygame.transform.flip(img, True, False) for img in self.fly_left_images]
        self.end_fly_right_images = [pygame.transform.flip(img, True, False) for img in self.end_fly_left_images]
        self.bite_attack_right_images = [pygame.transform.flip(img, True, False) for img in self.bite_attack_left_images]
        self.breath_attack_right_images = [pygame.transform.flip(img, True, False) for img in self.breath_attack_left_images]
        self.breath_effect_right_images = [pygame.transform.flip(img, True, False) for img in self.breath_effect_left_images]
        
        self.image = self.idle_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.base_speed = 150
        self.speed = 1
        self.full_health = 500 + (random.randint(20, 40) * self.level)
        self.health = self.full_health
        self.resource = "Dragon Meat"
        self.meat_resource = "Dragon Meat"
        self.resource_amount = 5
        
        special_drops = [{'item': 'Dragon Scales', 'chance': 0.8, 'min': 2, 'max': 5}]
        if self.type_data:
            for gem_data in self.type_data["rare_gems"]:
                special_drops.append({'item': gem_data["gem"], 'chance': gem_data["chance"], 'min': 1, 'max': 2})
        self.special_drops = special_drops
        
        self.death_experience = 2000 * (1 + (self.level * self.death_experience * .0001))
        
        self.frame_index = 0
        self.animation_speed = 0.2
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        self.state = "walking"
        self.flying_timer = 0
        
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 40
        self.bite_damage = 1
        self.breath_damage = 2
        self.attack_cooldown = pygame.time.get_ticks()
        self.attack_delay = 2000
        
        self.breath_image = None
        self.breath_image_x = 0
        self.breath_image_y = 0
        
        self.immune_to_lava = (dragon_type == "fire")
    
    def _scale_images(self, scale):
        def scale_image_list(image_list):
            scaled = []
            for img in image_list:
                new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
                scaled.append(pygame.transform.scale(img, new_size))
            return scaled
        
        self.walk_left_images = scale_image_list(self.walk_left_images)
        self.idle_left_images = scale_image_list(self.idle_left_images)
        self.start_fly_left_images = scale_image_list(self.start_fly_left_images)
        self.fly_left_images = scale_image_list(self.fly_left_images)
        self.end_fly_left_images = scale_image_list(self.end_fly_left_images)
        self.bite_attack_left_images = scale_image_list(self.bite_attack_left_images)
        self.breath_attack_left_images = scale_image_list(self.breath_attack_left_images)
        self.breath_effect_left_images = scale_image_list(self.breath_effect_left_images)
    
    def get_collision_rect(self, cam_x):
        rect = self.rect
        
        x_offset = int(rect.width * 0.15)
        y_offset = int(rect.height * 0.45)
        width = int(rect.width * 0.70)
        height = int(rect.height * 0.45)
        
        base_rect = pygame.Rect(rect.x - cam_x + x_offset, rect.y + y_offset, width, height)
        return base_rect
    
    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        max_health = self.full_health
        health = self.health
        bar_width = 40
        bar_height = 5
        x = self.rect.centerx - bar_width / 2 - cam_x
        y = self.rect.top + 5
        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)
        
        if self.health < self.last_health:
            self.bar_timer = 5
            sleep_multiplier = 40 if player_sleeping else 1
            decision_chance = min(0.6 * sleep_multiplier, 1.0)
            if self.state != "flying" and random.random() < decision_chance:
                self.state = "flying"
                self.frame_index = 0
                self.flying_timer = random.randint(600, 1200)
                self.direction = pygame.Vector2(random.choice([-1, 1]), random.uniform(-1, -0.5))
                if self.direction.length_squared() > 0:
                    self.direction = self.direction.normalize()
                self.speed = 1.3
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt
        
        level_font = pygame.font.SysFont(None, 16)
        level_text = level_font.render(f"Lv{self.level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(int(self.rect.centerx - cam_x), int(y + 15)))
        draw_text_with_background(screen, level_text, level_rect.topleft[0], level_rect.topleft[1])
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def check_collision(self, direction, nearby_objects, nearby_mobs):
        if self.state == "flying":
            flying_mobs = [mob for mob in nearby_mobs if hasattr(mob, 'state') and mob.state == "flying"]
            if not flying_mobs:
                return True, True
            
            collision_rect = self.get_collision_rect(0)
            
            left_check = pygame.Rect(collision_rect.left - 1, collision_rect.top + 5, 1, collision_rect.height - 10)
            right_check = pygame.Rect(collision_rect.right, collision_rect.top + 5, 1, collision_rect.height - 10)
            top_check = pygame.Rect(collision_rect.left + 5, collision_rect.top - 1, collision_rect.width - 10, 1)
            bottom_check = pygame.Rect(collision_rect.left + 5, collision_rect.bottom, collision_rect.width - 10, 1)
            
            left_collision = any(left_check.colliderect(mob.get_collision_rect(0)) for mob in flying_mobs)
            right_collision = any(right_check.colliderect(mob.get_collision_rect(0)) for mob in flying_mobs)
            up_collision = any(top_check.colliderect(mob.get_collision_rect(0)) for mob in flying_mobs)
            down_collision = any(bottom_check.colliderect(mob.get_collision_rect(0)) for mob in flying_mobs)
            
            can_move_x = not ((direction.x > 0 and right_collision) or (direction.x < 0 and left_collision))
            can_move_y = not ((direction.y > 0 and down_collision) or (direction.y < 0 and up_collision))
            
            return can_move_x, can_move_y
        return super().check_collision(direction, nearby_objects, nearby_mobs)
    
    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.state == "flying":
            target_distance = 120
            if (target_distance * target_distance * 3) > distance_sq > (target_distance * target_distance):
                direction = pygame.Vector2(dx, dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                self.direction = direction
            else:
                self.direction = pygame.Vector2(0, 0)
        else:
            super().handle_player_proximity(dt, player_world_x, player_world_y, player, nearby_objects, nearby_mobs)
    
    def attack(self, player_world_x, player_world_y, player):
        if not self.is_alive:
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        breath_range = 150 * self.size_scale
        bite_range = 50 * self.size_scale
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_cooldown > self.attack_delay and distance_sq < (breath_range * breath_range):
            self.attack_cooldown = current_time
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.frame_index = 0.0
            self.attack_start_x = self.rect.x
        
        if self.attacking:
            if self.state == "flying":
                breath_attack_frames = self.breath_attack_right_images if self.last_direction == "right" else self.breath_attack_left_images
                breath_effect_frames = self.breath_effect_right_images if self.last_direction == "right" else self.breath_effect_left_images
                
                breath_frame_index = (self.frame_index + self.animation_speed * 0.8) % len(breath_attack_frames)
                self.frame_index = breath_frame_index
                
                self.image = breath_attack_frames[int(breath_frame_index)]
                self.breath_image = breath_effect_frames[int(breath_frame_index)]
                
                if self.last_direction == "left":
                    self.breath_image_x = self.rect.left - self.breath_image.get_width()
                else:
                    self.breath_image_x = self.rect.right
                self.breath_image_y = self.rect.centery - self.breath_image.get_height() // 2
                
                if self.attack_timer == self.attack_duration // 2 and distance_sq < (breath_range * breath_range):
                    if self.last_direction == "left":
                        player_in_breath = player_world_x < self.attack_start_x
                    else:
                        player_in_breath = player_world_x >= self.attack_start_x
                    
                    if player_in_breath:
                        player.health -= self.breath_damage
                        sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
            else:
                frames = self.bite_attack_right_images if self.last_direction == "right" else self.bite_attack_left_images
                self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
                self.image = frames[int(self.frame_index)]
                
                if self.attack_timer == self.attack_duration // 2 and distance_sq < (bite_range * bite_range):
                    player.health -= self.bite_damage
                    sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
            
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.breath_image = None
                if self.state == "flying":
                    self.frame_index = float(len(self.start_fly_left_images))
                else:
                    self.frame_index = 0.0
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.attacking:
            return
        
        sleep_multiplier = 40 if player_sleeping else 1
        decision_chance = min(0.001 * sleep_multiplier, 1.0)
        if self.state == "walking" and random.random() < decision_chance:
            self.state = "flying"
            self.frame_index = 0
            self.flying_timer = random.randint(600, 1200)
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.direction.length_squared() > 0:
                self.direction = self.direction.normalize()
            self.speed = 1.3
        
        if self.state == "flying":
            self.flying_timer -= 1
            if self.flying_timer <= 0:
                self.state = "landing"
                self.frame_index = 0
                self.speed = 1.0
        
        if self.state == "landing" and self.frame_index >= len(self.end_fly_left_images) - 1:
            self.state = "walking"
            self.frame_index = 0
            self.direction = pygame.Vector2(0, 0)
        
        if self.state == "flying":
            if self.direction.length_squared() > 0:
                actual_speed = self.get_speed() * dt
                movement = self.direction * actual_speed
                self.rect.x += movement.x
                self.rect.y += movement.y
                if movement.x > 0:
                    self.last_direction = "right"
                elif movement.x < 0:
                    self.last_direction = "left"
            self.animate_stand()
        else:
            super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)
        
        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_image_right
            else:
                self.image = self.dead_image_left
    
    def animate_stand(self, animation_speed_multiplier=1.0):
        if self.state == "walking":
            if self.last_direction == "right":
                frames = self.idle_right_images
            else:
                frames = self.idle_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
        elif self.state == "flying":
            total_start_frames = len(self.start_fly_left_images)
            if self.frame_index < total_start_frames:
                frames = self.start_fly_right_images if self.last_direction == "right" else self.start_fly_left_images
                effective_animation_speed = self.animation_speed * animation_speed_multiplier
                self.frame_index += effective_animation_speed
                self.image = frames[int(min(self.frame_index, total_start_frames - 1))]
            else:
                frames = self.fly_right_images if self.last_direction == "right" else self.fly_left_images
                fly_frame_index = (self.frame_index - total_start_frames) % len(frames)
                effective_animation_speed = self.animation_speed * animation_speed_multiplier
                self.frame_index += effective_animation_speed
                self.image = frames[int(fly_frame_index)]
        elif self.state == "landing":
            frames = self.end_fly_right_images if self.last_direction == "right" else self.end_fly_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = min(self.frame_index + effective_animation_speed, len(frames) - 1)
            self.image = frames[int(self.frame_index)]
    
    def animate_walk(self):
        if self.state == "walking":
            if self.direction.x > 0:
                self.last_direction = "right"
            elif self.direction.x < 0:
                self.last_direction = "left"
            
            frames = self.walk_right_images if self.last_direction == "right" else self.walk_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
        else:
            self.animate_stand()
