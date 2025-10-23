import pygame
import random
from world import *
from sounds import *
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 40)
xl_font = pygame.font.Font(None, 100)
size = 64

############ PLAYER IMAGES #################

player_stand_image = pygame.image.load("assets/sprites/player/CharacterCorynnFrontStanding.png")
player_stand_image_back = pygame.image.load("assets/sprites/player/CharacterCorynnBackStanding.png")
player_stand_left = pygame.image.load("assets/sprites/player/CharacterCorynnLeftStanding.png")
player_stand_right = pygame.image.load("assets/sprites/player/CharacterCorynnRightStanding.png")
player_walk_down_images = [pygame.image.load("assets/sprites/player/CorynnWalkDown1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDown2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDown3.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDown4.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDown5.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDown6.png").convert_alpha()]
player_walk_up_images = [pygame.image.load("assets/sprites/player/CorynnWalkUp1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUp2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUp3.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUp4.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUp5.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUp6.png").convert_alpha()]
player_walk_left_images = [pygame.image.load("assets/sprites/player/CorynnWalkLeft1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeft2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeft3.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeft4.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeft5.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeft6.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeft7.png").convert_alpha()]
player_stand_attack_down_images = [pygame.image.load("assets/sprites/player/CorynnFrontStandAttack1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnFrontStandAttack2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnFrontStandAttack3.png").convert_alpha()]
player_stand_attack_up_images = [pygame.image.load("assets/sprites/player/CorynnBackStandAttack1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnBackStandAttack2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnBackStandAttack3.png").convert_alpha()]
player_stand_attack_left_images = [pygame.image.load("assets/sprites/player/CorynnLeftStandAttack1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnLeftStandAttack2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnLeftStandAttack3.png").convert_alpha()]
player_walk_down_attack_images = [pygame.image.load("assets/sprites/player/CorynnWalkDownAttack1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDownAttack2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDownAttack3.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDownAttack4.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDownAttack5.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkDownAttack6.png").convert_alpha()]
player_walk_up_attack_images = [pygame.image.load("assets/sprites/player/CorynnWalkUpAttack1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUpAttack2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUpAttack3.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUpAttack4.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUpAttack5.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkUpAttack6.png").convert_alpha()]
player_walk_left_attack_images = [pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack1.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack2.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack3.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack4.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack5.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack6.png").convert_alpha(), pygame.image.load("assets/sprites/player/CorynnWalkLeftAttack7.png").convert_alpha()] 

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
        self.max_health = 100 * self.health_leveler
        self.health = 100
        self.stamina_leveler = 1
        self.max_stamina = 100 * self.stamina_leveler
        self.stamina = 100
        self.hunger_leveler = 1
        self.max_hunger = 100 * self.hunger_leveler
        self.hunger = 100
        self.full_timer = 60
        self.water_leveler = 1
        self.max_water = 100 * self.water_leveler
        self.water = 100
        self.water_full_timer = 60
        self.warmth_leveler = 1
        self.max_warmth = 100
        self.warmth = 100
        self.weight = 0
        self.max_weight = 100
        self.damage = 5
        self.attack = 1
        self.base_speed = 275
        self.speed = 1
        self.defense = 1
        self.level = 1
        self.experience = 0
        self.exp_total = 0
        self.next_level_exp = 100
        self.level_up_timer = 0
        self.stamina_timer = 0
        self.stamina_message_timer = 0

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


    def attacking(self, nearby_mobs, player_world_x, player_world_y):
        if pygame.mouse.get_pressed()[0] and not self.exhausted:
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
                        mob.health -= self.damage * self.attack
                        if mob.health < old_health:
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
                                sound_manager.play_sound(random.choice([f"cow_moo1", "cow_moo2"]))



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

    def get_speed(self):
        return self.base_speed * self.speed

    def regain_health(self, dt):
        if 1 <= self.health <= self.max_health:
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
                    self.hunger -= dt / 40

    def regain_stamina(self, dt, screen):
        if self.stamina_timer > 0:
            self.stamina_timer -= dt
            return
        
        if self.stamina < self.max_stamina:
            if self.water == self.max_water:
                self.stamina += dt * 16
            elif self.water > self.max_water * 0.7:
                self.stamina += dt * 10
            elif self.water > self.max_water * 0.4:
                self.stamina += dt * 6
            elif self.water > self.max_water * 0.1:
                self.stamina += dt * 2
            else:
                self.stamina -= dt / 12
                self.health -= dt / 12

        if self.water == 100:
            self.water_full_timer -= dt
            if self.water_full_timer <= 0:
                self.water -= dt / 100
        elif self.water > 0:
            self.water -= dt / 60

        if self.stamina > 10 and self.speed < 1:
            self.speed = 1


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
            self.speed = .3
            self.exhausted = True
        elif self.stamina <= 10: 
            self.speed = .4
            self.exhausted = False
        elif self.stamina <= 20: 
            self.speed = .6
            self.exhausted = False
        else:
            self.speed = 1
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
            

    def lose_water(self, dt):
        if self.water > 0:
            if self.water == 100:
                self.water_full_timer -= dt
                if self.water_full_timer <= 0:
                    self.water -= dt/100
            else:
                self.water -= dt / 100
                self.water_full_timer = 60

    def level_up(self, screen):
            self.level += 1
            self.exp_total += self.next_level_exp
            if self.level <= 10:
                self.next_level_exp = int(100 + (self.exp_total * 0.3))
            elif self.level <= 30:
                self.next_level_exp = int(200 + (self.exp_total * 0.122))
            elif self.level <= 50:
                self.next_level_exp = int(500 + (self.exp_total * 0.045))
            elif self.level <= 70:
                self.next_level_exp = int(1000 + (self.exp_total * 0.01))
            elif self.level <= 100:
                self.next_level_exp = int(1500 + (self.exp_total * 0.007))
            self.level_up_timer = 10
            sound_manager.play_sound("level_up")

    def show_level_up_message(self, screen):
        level_up_text = large_font.render(
            f"You leveled up to level {self.level}! Upgrade stats in inventory!",
            True, (20, 255, 20)
        )
        screen.blit(level_up_text, (
            screen.get_width() // 2 - level_up_text.get_width() // 2,
            20
        ))

    def take_damage(self, damage):
        self.health -= damage
        sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1,5)]))

    def feed_cat(self, cat):
        pass

    def health_bar(self, screen):
        max_health = self.max_health
        health = self.health
        bar_width = self.max_health * 2
        bar_height = 18
        x = 43
        y = 64

        health_ratio = health / max_health
        health_width = int(bar_width * health_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if health_ratio > .4:
            pygame.draw.rect(screen, (200, 40, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (255, 80, 60), pygame.Rect(x, y, health_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        health_text = f"{int(health)} / {max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))

    def stamina_bar(self, screen):
        max_stamina = self.max_stamina
        stamina = self.stamina
        bar_width = max_stamina * 2
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
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))


    def hunger_bar(self, screen):
        max_hunger = self.max_hunger
        hunger = self.hunger
        bar_width = max_hunger * 2
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
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))

    def water_bar(self, screen):
        max_water = self.max_water
        water = self.water
        bar_width = self.max_water * 2
        bar_height = 18
        x = 43
        y = 118

        water_ratio = water / max_water
        water_width = int(bar_width * water_ratio)

        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height), border_radius=5)
        if water_ratio > .4:
            pygame.draw.rect(screen, (0, 40, 255), pygame.Rect(x, y, water_width, bar_height), border_radius=5)
        else:
            pygame.draw.rect(screen, (100, 100, 255), pygame.Rect(x, y, water_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=2, border_radius=5)

        water_text = f"{int(water)} / {max_water}"
        text_surface = font.render(water_text, True, (255, 255, 255))
        text_x = x + (bar_width / 2) - (text_surface.get_width() / 2)
        text_y = y + (bar_height / 2) - (text_surface.get_height() / 2)
        
        screen.blit(text_surface, (text_x, text_y))

    def exp_bar(self, screen):
        next_level_exp = self.next_level_exp
        experience = self.experience
        bar_width = 800
        bar_height = 5
        x = screen.get_width()//2 - 400
        y = screen.get_height() - 105

        experience_ratio = experience / next_level_exp
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


    def keep_in_screen(self, screen_height):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x, rect.y, rect.width, rect.height)

    def check_collision(self, direction, nearby_objects, nearby_mobs):
        all_nearby = nearby_objects + nearby_mobs

        collision_rect = self.get_collision_rect(0)
        
        left_check = pygame.Rect(collision_rect.left - 1, collision_rect.top + 5, 1, collision_rect.height - 10)
        right_check = pygame.Rect(collision_rect.right, collision_rect.top + 5, 1, collision_rect.height - 10)
        top_check = pygame.Rect(collision_rect.left + 5, collision_rect.top - 1, collision_rect.width - 10, 1)
        bottom_check = pygame.Rect(collision_rect.left + 5, collision_rect.bottom, collision_rect.width - 10, 1)

        left_collision = any(left_check.colliderect(obj.get_collision_rect(0)) for obj in all_nearby)
        right_collision = any(right_check.colliderect(obj.get_collision_rect(0)) for obj in all_nearby)
        up_collision = any(top_check.colliderect(obj.get_collision_rect(0)) for obj in all_nearby)
        down_collision = any(bottom_check.colliderect(obj.get_collision_rect(0)) for obj in all_nearby)

        can_move_x = not ((direction.x > 0 and right_collision) or (direction.x < 0 and left_collision))
        can_move_y = not ((direction.y > 0 and down_collision) or (direction.y < 0 and up_collision))

        return can_move_x, can_move_y

    def get_speed(self):
        return self.base_speed * self.speed

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if not hasattr(self, "cow") and self.move_timer <= 0 and self.is_alive and not self.fleeing:
            if random.random() < 0.02:
                self.direction.xy = random.choice([(-1,0), (1,0), (0,-1), (0,1), (0,0), (0,0), (0,0)])
                self.move_timer = random.randint(30, 120)
            else:
                self.direction.xy = (0, 0)
        else:
            self.move_timer -= 1

        if hasattr(self, "cow") and self.move_timer <= 0 and self.is_alive and not self.fleeing:
            if random.random() < 0.02:
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

            self.animate_walk()
        else:
            self.animate_stand()

        if not self.is_alive:
            self.direction.xy = (0, 0)

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
        self.frame_index = (self.frame_index + self.animation_speed) % len(self.walk_right_images)
        frames = self.walk_right_images if direction == "right" else self.walk_left_images
        self.image = frames[int(self.frame_index)]

    def animate_stand(self):
        if self.last_direction == "right":
            stand_attr = getattr(self, "stand_right_image", None) or getattr(self, "stand_right_images", None)
        else:
            stand_attr = getattr(self, "stand_left_image", None) or getattr(self, "stand_left_images", None)

        if stand_attr is None:
            return

        if isinstance(stand_attr, pygame.Surface):
            self.image = stand_attr
        elif isinstance(stand_attr, (list, tuple)):
            self.frame_index = (self.frame_index + self.animation_speed) % len(stand_attr)
            self.image = stand_attr[int(self.frame_index)]

    def handle_health(self, screen, cam_x, dt):
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
            self.is_alive = False

    def harvest(self, player=None):
        if not self.destroyed and not self.is_alive:
            resource_collected = min(self.resource_amount, (1 * player.attack))
            self.resource_amount -= resource_collected
            
            if self.resource_amount <= 0:
                self.destroyed = True
            player.experience += harvest_experience * resource_collected
            player.exp_total += harvest_experience * resource_collected
            return [self.resource] * resource_collected
        return []
    
    def flee(self, player_world_x, player_world_y, dt):
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
                    if random.random() < 0.02:
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

        self.tame_max = 100
        self.tame = 0
        self.tamed = False

        self.full_health = 100
        self.health = 100
        self.max_hunger = 100
        self.hunger = 100
        self.base_speed = 160
        self.speed = 1

        self.dead_cat_right_image = pygame.image.load(self.cat_type["dead_image"]).convert_alpha()
        self.dead_cat_left_image = pygame.transform.flip(self.dead_cat_right_image, True, False)

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_cat_right_image
            else:
                self.image = self.dead_cat_left_image

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))


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
        self.full_health = 50
        self.health = 50

        self.frame_index = 0
        self.animation_speed = 0.3
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right" 
        self.dead_squirrel_right_image = pygame.transform.scale(pygame.image.load(squirrel_dead_image).convert_alpha(), (48, 48))
        self.dead_squirrel_left_image = pygame.transform.flip(self.dead_squirrel_right_image, True, False)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

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

        self.full_health = 150
        self.health = 150
        self.base_speed = 70
        self.speed = 1
        self.resource = "Raw Beef"
        self.resource_amount = 5
        self.cow = "moo"

        self.dead_cow_right_image = pygame.transform.scale(pygame.image.load(self.cow_type["dead_image"]).convert_alpha(), (size, size))
        self.dead_cow_left_image = pygame.transform.flip(self.dead_cow_right_image, True, False)

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_cow_right_image
            else:
                self.image = self.dead_cow_left_image

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))


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
        self.resource = "Chicken"
        self.resource_amount = 2
        self.full_health = 70
        self.health = 70

        self.frame_index = 0
        self.animation_speed = 0.3
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right"
        self.dead_chicken_right_image = pygame.transform.scale(pygame.image.load(chicken_dead_image).convert_alpha(), (40, 40))
        self.dead_chicken_left_image = pygame.transform.flip(self.dead_chicken_right_image, True, False)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

        if not self.is_alive:
            if self.last_direction == "right":
                self.image = self.dead_chicken_right_image
            else:
                self.image = self.dead_chicken_left_image


class Enemy(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.chasing = False
        self.enemy = True
        self.attacking = False

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

    def flee(self, player_world_x, player_world_y, dt):
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

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.is_alive:
            if getattr(self, "attacking", False):
                return
            if not self.chasing:
                if self.move_timer <= 0:
                    if random.random() < 0.02:
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

                self.animate_walk()
            else:
                self.animate_stand()

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
        self.health = 100
        self.resource = "Hide"
        self.resource_amount = random.randint(4, 9)

    

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

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

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

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

        self.last_direction = "right" 
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 20

        self.attack_damage = 4
        self.base_speed = 150
        self.speed = 1
        self.full_health = 150
        self.health = 150
        self.resource = "Hide"
        self.resource_amount = random.randint(4, 9)

        self.state = "idle"
        self.was_moving = False
        self.is_moving = False
        self.transition_done = False

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 10, rect.y + 50, rect.width - 20, rect.height - 70)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

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

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

        if self.attacking:
            return

        self.is_moving = self.direction.length_squared() > 0 and self.is_alive

        if self.is_moving and not self.was_moving:
            if self.chasing:
                self.state = "chase"
                sound_manager.play_sound(random.choice(["duskwretch_roar1", "duskwretch_roar2"]))
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

        self.animate_state(dt)
        self.was_moving = self.is_moving

        if not self.is_alive:
            if self.last_direction == "left":
                self.image = duskwretch_dead_image_left
            else:
                self.image = duskwretch_dead_image_right

    def animate_state(self, dt):
        if self.state == "attacking":
            return
            
        elif self.state == "start_walk":
            self.animation_speed = .1
            frames = self.start_walk_right_images if self.last_direction == "right" else self.start_walk_left_images
            self.frame_index += self.animation_speed
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
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

        elif self.state == "chase":
            self.animation_speed = .13
            frames = self.chase_right_images if self.last_direction == "right" else self.chase_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

        elif self.state == "end_walk":
            frames = self.end_walk_right_images if self.last_direction == "right" else self.end_walk_left_images
            self.frame_index += self.animation_speed
            if self.frame_index >= len(frames):
                self.state = "idle"
                self.frame_index = 0
            else:
                self.image = frames[int(self.frame_index)]

        elif self.state == "idle":
            frames = self.stand_right_images if self.last_direction == "right" else self.stand_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

    def flee(self, player_world_x, player_world_y, dt):
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

    def flee(self, player_world_x, player_world_y, dt):
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
                    if random.random() < 0.02:
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

    def handle_health(self, screen, cam_x, dt):
        super().handle_health(screen, cam_x, dt)
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
        self.health = 80
        self.resource = "Hide"
        self.resource_amount = random.randint(2, 5)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

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

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        super().update(dt, player, nearby_objects, nearby_mobs)

        if not self.is_alive:
            pass


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
        self.full_health = 60
        self.health = 60
        self.resource = "Venison"
        self.resource_amount = 4
        self.frame_index = 0
        self.animation_speed = 0.2
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        self.hoof_timer = 0
        self.is_moving = False

        if self.is_buck:
            self.aggressive = False
            self.enemy = False
        else:
            self.aggressive = False
            self.enemy = False

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        was_moving = self.direction.length_squared() > 0
        
        super().update(dt, player, nearby_objects, nearby_mobs)
        
        self.is_moving = self.direction.length_squared() > 0 and self.is_alive
        
        if self.is_moving:
            self.hoof_timer -= dt
            if self.hoof_timer <= 0:
                sound_manager.play_sound(random.choice([f"hoofs{i}" for i in range(1,7)]))
                self.hoof_timer = random.uniform(0.3, 0.7)

    def get_collision_rect(self, cam_x):
            rect = self.rect
            return pygame.Rect(rect.x - cam_x + 15, rect.y + 50, rect.width - 30, rect.height - 55)

    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def handle_health(self, screen, cam_x, dt):
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
    
    def flee(self, player_world_x, player_world_y, dt):
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
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.attacking:
            return
        
        super().update(dt, player, nearby_objects, nearby_mobs)
        
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
        self.full_health = 220
        self.health = 220
        self.resource = "Bear Hide"
        self.resource_amount = 8
        
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
    
    def handle_health(self, screen, cam_x, dt):
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
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
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
    
    def flee(self, player_world_x, player_world_y, dt):
        if self.aggressive:
            self.fleeing = False
            return
        
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive:
            if self.fleeing and self.is_alive:
                if self.move_timer <= 0:
                    if random.random() < 0.02:
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
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.attacking:
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
            super().update(dt, player, nearby_objects, nearby_mobs)
        
        if not self.is_alive:
            if self.last_direction == "right":
                self.image = pygame.transform.flip(black_bear_dead_image, True, False)
            else:
                self.image = black_bear_dead_image

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
        self.full_health = 300
        self.health = 300
        self.resource = "Bear Hide"
        self.resource_amount = 8
        
        self.frame_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        
        self.attack_timer = 0
        self.attack_duration = 30
        self.attack_damage = 15
        
        self.aggressive = False
        self.enemy = False

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 5, rect.y + 30, rect.width - 10, rect.height - 50)
    
    def handle_health(self, screen, cam_x, dt):
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
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
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
    
    def flee(self, player_world_x, player_world_y, dt):
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
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.attacking:
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
            super().update(dt, player, nearby_objects, nearby_mobs)
        
        if not self.is_alive:
            if self.last_direction == "right":
                self.image = pygame.transform.flip(brown_bear_dead_image, True, False)
            else:
                self.image = brown_bear_dead_image

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
        self.full_health = 40
        self.health = 40
        self.resource = "Gila Meat"
        self.resource_amount = 2
        
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

    def handle_health(self, screen, cam_x, dt):
        """Override to become aggressive immediately when attacked"""
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
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def flee(self, player_world_x, player_world_y, dt):
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
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.attacking:
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
            super().update(dt, player, nearby_objects, nearby_mobs)
        
        if not self.is_alive:
            if self.last_direction == "right":
                self.image = pygame.transform.flip(gila_dead_image, True, False)
            else:
                self.image = gila_dead_image


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
        self.full_health = 30
        self.health = 30
        self.resource = "Feathers"
        self.resource_amount = 1
        
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
    
    def draw(self, screen, cam_x):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))
    
    def handle_health(self, screen, cam_x, dt):
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
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None):
        if self.state == "walking" and random.random() < 0.001:
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
            super().update(dt, player, nearby_objects, nearby_mobs)
        
        if not self.is_alive:
            if self.last_direction == "right":
                self.image = pygame.transform.flip(crow_dead_image, True, False)
            else:
                self.image = crow_dead_image
    
    def animate_stand(self):
        if self.state == "walking":
            super().animate_stand()
        elif self.state == "flying":
            if self.frame_index < len(self.start_fly_left_images):
                frames = self.start_fly_right_images if self.last_direction == "right" else self.start_fly_left_images
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.start_fly_left_images):
                    self.frame_index = 0  # Reset for main flying loop
                self.image = frames[int(min(self.frame_index, len(frames) - 1))]
            else:
                frames = self.fly_right_images if self.last_direction == "right" else self.fly_left_images
                self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
                self.image = frames[int(self.frame_index)]
        elif self.state == "landing":
            frames = self.landing_right_images if self.last_direction == "right" else self.landing_left_images
            self.frame_index = min(self.frame_index + self.animation_speed, len(frames) - 1)
            self.image = frames[int(self.frame_index)]