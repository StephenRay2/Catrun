import pygame
import random
import math
import os
from world import *
from sounds import *
from debug import font_path, font
from player import Player, TempPlayerCollision
hud_font = pygame.font.Font(font_path, 14)
font = pygame.font.Font(font_path, 18)
large_font = pygame.font.Font(font_path, 28)
xl_font = pygame.font.Font(font_path, 72)
size = 64

def draw_text_with_background(screen, text_surface, x, y, padding=4):
    """Draw text with a semi-transparent black background box."""
    bg_rect = text_surface.get_rect(topleft=(x, y)).inflate(padding * 2, padding)
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 150))
    screen.blit(bg_surface, bg_rect.topleft)
    screen.blit(text_surface, (x, y))


def draw_mob_name_and_level(mob, screen, cam_x, y_offset=-14):
    """Draw mob's name and level label above its head, if available."""
    try:
        level_value = getattr(mob, "level", None)
        if level_value is None:
            return
        
        display_name = getattr(mob, "cat_name", None)
        if not display_name:
            display_name = getattr(mob, "name", None)
        
        if not display_name:
            return
        
        name_font = pygame.font.Font(font_path, 12)
        label = f"{display_name} Lv{int(level_value)}"
        name_text = name_font.render(label, True, (255, 255, 255))
        text_x = int(mob.rect.centerx - cam_x - name_text.get_width() / 2)
        text_y = int(mob.rect.top + y_offset)
        draw_text_with_background(screen, name_text, text_x, text_y)
    except Exception:
        # Never let name drawing break gameplay.
        pass


def apply_wild_mob_level_scaling(mob):
    """
    Apply level-based stat scaling for wild mobs.
    Similar to tamed cats gaining one stat point per level, but:
      - Points are auto-spent into random stats for wild mobs.
      - Each upgrade is 90% of the tamed cat upgrade amounts.
    This should be called once after the mob's level has been set.
    """
    # Do not touch player-controlled characters or already-tamed cats.
    if mob.__class__.__name__ == "Player":
        return
    # Cat is defined later in this module; once imported, we can safely
    # use isinstance checks at runtime.
    try:
        from mobs import Cat  # type: ignore
        if isinstance(mob, Cat) and getattr(mob, "tamed", False):
            return
    except Exception:
        # If Cat isn't available for any reason, fall through and treat
        # this as a generic wild mob.
        pass

    level = int(getattr(mob, "level", 1) or 1)
    extra_levels = max(0, level - 1)
    if extra_levels <= 0:
        return

    # Determine which stats this mob actually has.
    possible_stats = []
    if any(hasattr(mob, attr) for attr in ("full_health", "max_health", "health")):
        possible_stats.append("health")
    # Only treat attack as upgradable if there's a numeric field, not just
    # an attack() method.
    has_numeric_attack = hasattr(mob, "attack_damage") or (
        hasattr(mob, "attack") and not callable(getattr(mob, "attack"))
    )
    if has_numeric_attack:
        possible_stats.append("attack")
    if hasattr(mob, "defense"):
        possible_stats.append("defense")

    if not possible_stats:
        return

    # 90% of cat's per-point increases.
    HEALTH_INC = 10 * 0.9   # cat: +10 max health
    ATTACK_INC = 2 * 0.9    # cat: +2 attack
    DEFENSE_INC = 2 * 0.9   # cat: +2 defense

    for _ in range(extra_levels):
        stat = random.choice(possible_stats)
        if stat == "health":
            inc = HEALTH_INC
            if hasattr(mob, "max_health"):
                mob.max_health = getattr(mob, "max_health", getattr(mob, "full_health", getattr(mob, "health", 0))) + inc
                mob.health = min(mob.health + inc, mob.max_health)
            elif hasattr(mob, "full_health"):
                mob.full_health += inc
                mob.health = min(mob.health + inc, mob.full_health)
            elif hasattr(mob, "health"):
                mob.health += inc
        elif stat == "attack":
            inc = ATTACK_INC
            if hasattr(mob, "attack_damage"):
                mob.attack_damage = getattr(mob, "attack_damage", 0) + inc
            elif hasattr(mob, "attack") and not callable(getattr(mob, "attack")):
                mob.attack = getattr(mob, "attack", 0) + inc
        elif stat == "defense" and hasattr(mob, "defense"):
            inc = DEFENSE_INC
            mob.defense = getattr(mob, "defense", 0) + inc

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

pock_rock_projectiles = []
try:
    pock_stone_sprite = pygame.transform.scale(
        pygame.image.load("assets/sprites/items/Stone.png").convert_alpha(), (32, 32)
    )
except Exception:
    pock_stone_sprite = None

redmite_idle_left_images = [pygame.image.load(f"assets/sprites/mobs/RedmiteLeftIdle{i}.png").convert_alpha() for i in range(1, 4)]
redmite_walk_left_images = [pygame.image.load(f"assets/sprites/mobs/RedmiteLeftWalk{i}.png").convert_alpha() for i in range(1, 4)]
redmite_latch_left_images = [pygame.image.load(f"assets/sprites/mobs/RedmiteLeftLatch{i}.png").convert_alpha() for i in range(1, 4)]
redmite_latched_left_image = pygame.image.load("assets/sprites/mobs/RedmiteLeftLatched.png").convert_alpha()
redmite_latched_up_image = pygame.image.load("assets/sprites/mobs/RedmiteUpLatched.png").convert_alpha()


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

polar_bear_idle_images = ["assets/sprites/mobs/PolarBearIdle1.png", "assets/sprites/mobs/PolarBearIdle2.png", "assets/sprites/mobs/PolarBearIdle3.png", "assets/sprites/mobs/PolarBearIdle4.png"]
polar_bear_attack_left_images = ["assets/sprites/mobs/PolarBearAttack1.png", "assets/sprites/mobs/PolarBearAttack2.png", "assets/sprites/mobs/PolarBearAttack3.png"]
polar_bear_walk_left_images = ["assets/sprites/mobs/PolarBearWalkLeft1.png", "assets/sprites/mobs/PolarBearWalkLeft2.png", "assets/sprites/mobs/PolarBearWalkLeft3.png", "assets/sprites/mobs/PolarBearWalkLeft4.png", "assets/sprites/mobs/PolarBearWalkLeft5.png", "assets/sprites/mobs/PolarBearWalkLeft6.png"]
polar_bear_dead_image = pygame.image.load("assets/sprites/mobs/PolarBearDead.png").convert_alpha()

panda_idle_images = ["assets/sprites/mobs/PandaBearIdle1.png", "assets/sprites/mobs/PandaBearIdle2.png", "assets/sprites/mobs/PandaBearIdle3.png", "assets/sprites/mobs/PandaBearIdle4.png"]
panda_walk_left_images = ["assets/sprites/mobs/PandaBearWalkLeft1.png", "assets/sprites/mobs/PandaBearWalkLeft2.png", "assets/sprites/mobs/PandaBearWalkLeft3.png", "assets/sprites/mobs/PandaBearWalkLeft4.png", "assets/sprites/mobs/PandaBearWalkLeft5.png", "assets/sprites/mobs/PandaBearWalkLeft6.png"]
panda_dead_image = pygame.image.load("assets/sprites/mobs/PandaBearDead.png").convert_alpha()

gila_idle_images = ["assets/sprites/mobs/GilaIdle1.png", "assets/sprites/mobs/GilaIdle2.png"]
gila_walk_left_images = ["assets/sprites/mobs/GilaWalkLeft1.png", "assets/sprites/mobs/GilaWalkLeft2.png", "assets/sprites/mobs/GilaWalkLeft3.png"]
gila_attack_left_images = ["assets/sprites/mobs/GilaAttackLeft1.png", "assets/sprites/mobs/GilaAttackLeft2.png", "assets/sprites/mobs/GilaAttackLeft3.png"]
gila_dead_image = pygame.image.load("assets/sprites/mobs/GilaDead.png").convert_alpha()
salamander_idle_images = ["assets/sprites/mobs/SalamanderIdle1.png", "assets/sprites/mobs/SalamanderIdle2.png"]
salamander_walk_left_images = ["assets/sprites/mobs/SalamanderWalkLeft1.png", "assets/sprites/mobs/SalamanderWalkLeft2.png", "assets/sprites/mobs/SalamanderWalkLeft3.png"]
salamander_attack_left_images = ["assets/sprites/mobs/SalamanderAttackLeft1.png", "assets/sprites/mobs/SalamanderAttackLeft2.png", "assets/sprites/mobs/SalamanderAttackLeft3.png"]
salamander_dead_image = pygame.image.load("assets/sprites/mobs/SalamanderDead.png").convert_alpha()

crow_walk_left_images = ["assets/sprites/mobs/CrowWalkLeft1.png", "assets/sprites/mobs/CrowWalkLeft2.png", "assets/sprites/mobs/CrowWalkLeft3.png", "assets/sprites/mobs/CrowWalkLeft4.png", "assets/sprites/mobs/CrowWalkLeft5.png"]
crow_fly_left_images = ["assets/sprites/mobs/CrowFlyLeft1.png", "assets/sprites/mobs/CrowFlyLeft2.png", "assets/sprites/mobs/CrowFlyLeft3.png", "assets/sprites/mobs/CrowFlyLeft4.png"]
crow_start_fly_left_images = ["assets/sprites/mobs/CrowStartFlyLeft1.png", "assets/sprites/mobs/CrowStartFlyLeft2.png", "assets/sprites/mobs/CrowStartFlyLeft3.png", "assets/sprites/mobs/CrowStartFlyLeft4.png", "assets/sprites/mobs/CrowStartFlyLeft5.png", "assets/sprites/mobs/CrowStartFlyLeft6.png"]
crow_landing_left_images = ["assets/sprites/mobs/CrowLandingLeft1.png", "assets/sprites/mobs/CrowLandingLeft2.png", "assets/sprites/mobs/CrowLandingLeft3.png", "assets/sprites/mobs/CrowLandingLeft4.png", "assets/sprites/mobs/CrowLandingLeft5.png", "assets/sprites/mobs/CrowLandingLeft6.png", "assets/sprites/mobs/CrowLandingLeft7.png", "assets/sprites/mobs/CrowLandingLeft8.png"]
crow_dead_image = pygame.image.load("assets/sprites/mobs/CrowDead.png").convert_alpha()

ashhound_idle_left_images = ["assets/sprites/mobs/AshhoundLeftIdle1.png", "assets/sprites/mobs/AshhoundLeftIdle2.png", "assets/sprites/mobs/AshhoundLeftIdle3.png"]
ashhound_move_left_images = ["assets/sprites/mobs/AshhoundLeftMove1.png", "assets/sprites/mobs/AshhoundLeftMove2.png", "assets/sprites/mobs/AshhoundLeftMove3.png", "assets/sprites/mobs/AshhoundLeftMove4.png"]
ashhound_attack_left_images = ["assets/sprites/mobs/AshhoundLeftAttack1.png", "assets/sprites/mobs/AshhoundLeftAttack2.png", "assets/sprites/mobs/AshhoundLeftAttack3.png"]
ashhound_move_attack_left_images = ["assets/sprites/mobs/AshhoundLeftMoveAttack1.png", "assets/sprites/mobs/AshhoundLeftMoveAttack2.png", "assets/sprites/mobs/AshhoundLeftMoveAttack3.png", "assets/sprites/mobs/AshhoundLeftMoveAttack4.png"]
ashhound_dead_image_left = pygame.image.load("assets/sprites/mobs/AshhoundLeftDead.png").convert_alpha()
ashhound_dead_image_right = pygame.transform.flip(ashhound_dead_image_left, True, False)

# Wastedog variants (left-facing source frames only; we flip to get right-facing)
wastedog_variant_prefixes = {
    "black": "BlackWastedogLeft",
    "red": "RedWastedogLeft",
    "yellow": "YellowWastedogLeft",
}

def _build_wastedog_variant(prefix):
    def paths(kind, count):
        return [f"assets/sprites/mobs/{prefix}{kind}{i}.png" for i in range(1, count + 1)]
    return {
        "idle": paths("Idle", 3),
        "move": paths("Move", 4),
        "move_attack": paths("MoveAttack", 4),
        "attack": paths("Attack", 3),
    }

wastedog_variant_frames = {k: _build_wastedog_variant(v) for k, v in wastedog_variant_prefixes.items()}

wolf_idle_left_images = [f"assets/sprites/mobs/WolfLeftIdle{i}.png" for i in range(1, 4)]
wolf_walk_left_images = [f"assets/sprites/mobs/WolfLeftWalk{i}.png" for i in range(1, 5)]
wolf_run_left_images = [f"assets/sprites/mobs/WolfLeftRun{i}.png" for i in range(1, 5)]
wolf_run_attack_left_images = [f"assets/sprites/mobs/WolfLeftRunAttack{i}.png" for i in range(1, 5)]
wolf_attack_left_images = [f"assets/sprites/mobs/WolfLeftAttack{i}.png" for i in range(1, 4)]
wolf_dead_left_image = "assets/sprites/mobs/WolfLeftDead.png"

glowbird_walk_left_images = ["assets/sprites/mobs/GlowbirdWalkLeft1.png", "assets/sprites/mobs/GlowbirdWalkLeft2.png", "assets/sprites/mobs/GlowbirdWalkLeft3.png", "assets/sprites/mobs/GlowbirdWalkLeft4.png", "assets/sprites/mobs/GlowbirdWalkLeft5.png"]
glowbird_fly_left_images = ["assets/sprites/mobs/GlowbirdFlyLeft1.png", "assets/sprites/mobs/GlowbirdFlyLeft2.png", "assets/sprites/mobs/GlowbirdFlyLeft3.png", "assets/sprites/mobs/GlowbirdFlyLeft4.png"]
glowbird_start_fly_left_images = ["assets/sprites/mobs/GlowbirdStartFlyLeft1.png", "assets/sprites/mobs/GlowbirdStartFlyLeft2.png", "assets/sprites/mobs/GlowbirdStartFlyLeft3.png", "assets/sprites/mobs/GlowbirdStartFlyLeft4.png", "assets/sprites/mobs/GlowbirdStartFlyLeft5.png", "assets/sprites/mobs/GlowbirdStartFlyLeft6.png"]
glowbird_landing_left_images = ["assets/sprites/mobs/GlowbirdLandingLeft1.png", "assets/sprites/mobs/GlowbirdLandingLeft2.png", "assets/sprites/mobs/GlowbirdLandingLeft3.png", "assets/sprites/mobs/GlowbirdLandingLeft4.png", "assets/sprites/mobs/GlowbirdLandingLeft5.png", "assets/sprites/mobs/GlowbirdLandingLeft6.png", "assets/sprites/mobs/GlowbirdLandingLeft7.png", "assets/sprites/mobs/GlowbirdLandingLeft8.png"]
glowbird_dead_image = pygame.image.load("assets/sprites/mobs/GlowbirdDead.png").convert_alpha()

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


class Mob(pygame.sprite.Sprite):
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
        # Spawn protection: remember the starting location to avoid instant spawn kills.
        self.spawn_protection_center = pygame.Vector2(x, y)
        self.spawn_protection_radius = 900
        self.spawn_protection_radius_sq = self.spawn_protection_radius * self.spawn_protection_radius

        self.exhausted = False
        self.dead = False
        self.score = 0
        self.last_direction = "down"
        self.attack_cooldown = pygame.time.get_ticks()
        self.attack_delay = 300
        self.mob_noise_delay = 3
        self.redmite_slots = [None, None, None, None]
        
        self.swimming = False
        self.in_lava = False
        self.swim_stamina_drain = 0.3
        self.lava_damage_rate = 40  # damage per second in lava
        self.lava_damage_timer = 0
        self.current_liquid = None
        self.ground_slow_factor = 1.0

    def is_in_spawn_protection(self):
        return False

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
                # Track which mob the player is actively hitting this swing
                self.attacking_target = None

                for mob in nearby_mobs:
                    # Prevent friendly fire on tamed cats
                    if isinstance(mob, Cat) and getattr(mob, "tamed", False):
                        continue

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
                        # Do not damage latched redmites with player attacks; cats handle them.
                        RedmiteCls = globals().get("Redmite")
                        if RedmiteCls and isinstance(mob, RedmiteCls) and getattr(mob, "latched_to_player", False):
                            continue
                        # Remember this as the current attack target so pets can assist
                        self.attacking_target = mob
                        old_health = mob.health
                        # Flat damage plus strength upgrades
                        mob.health -= self.attack
                        if hasattr(mob, "register_attack"):
                            mob.register_attack(self)
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
        score_text = hud_font.render(f"Score: {self.determine_score(dungeon_depth)}", True, (255, 255, 255))
        x = screen.get_width() - score_text.get_width() - 20
        y = 30
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
        lvl = self.level
        self.level += 1
        self.exp_total += self.next_level_exp
        if self.level > 0:
            self.next_level_exp += (self.next_level_exp * self.req_multiplier)
            if lvl <= 10:
                self.req_multiplier -= 0.034
            elif lvl <= 20:
                self.req_multiplier -= 0.012
            elif lvl <= 30:
                self.req_multiplier -= 0.0005
            elif lvl <= 40:
                self.req_multiplier -= 0.0004
            elif lvl <= 50:
                self.req_multiplier -= 0.00019
            elif lvl <= 60:
                self.req_multiplier -= 0.00009
            elif lvl <= 70:
                self.req_multiplier -= 0.00008
            elif lvl <= 80:
                self.req_multiplier -= 0.00007
            elif lvl < 100:
                self.req_multiplier -= 0.00003
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
        speed = speed * weight_multiplier
        # Banks (e.g., snowbanks) slightly slow the player while walking on them.
        speed *= getattr(self, "ground_slow_factor", 1.0)
        return speed

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
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(health_text, True, (255, 255, 255))
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
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(stamina_text, True, (255, 255, 255))
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
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(hunger_text, True, (255, 255, 255))
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
        small_font = pygame.font.Font(font_path, 11)
        text_surface = small_font.render(thirst_text, True, (255, 255, 255))
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
        self.attackers = set()
        self.last_attacker = None
        self.ground_slow_factor = 1.0
        
        self.swimming = False
        self.in_lava = False
        self.lava_damage_rate = 50
        self.lava_damage_timer = 0
        self.immune_to_lava = False
        self.current_liquid = None
        self.snowball_slow_stacks = 0
        self.snowball_slow_timer = 0.0


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

    def register_attack(self, attacker):
        """Track eligible attackers for XP sharing, retaliation, and remember the last hitter."""
        if attacker is None:
            return
        is_player = attacker.__class__.__name__ == "Player"
        is_tamed_cat = attacker.__class__.__name__ == "Cat" and getattr(attacker, "tamed", False)
        is_enemy_mob = getattr(attacker, "enemy", False) or isinstance(attacker, (Wolf, Wastedog))
        
        if is_tamed_cat and (not getattr(attacker, "is_alive", True) or getattr(attacker, "destroyed", False)):
            return
        if is_enemy_mob and (not getattr(attacker, "is_alive", True) or getattr(attacker, "destroyed", False)):
            return
        if not (is_player or is_tamed_cat or is_enemy_mob):
            return
        
        self.attackers.add(attacker)
        self.last_attacker = attacker
        
        if is_enemy_mob and not isinstance(self, (Wolf, Wastedog)):
            self.chasing = True
            self.aggro_timer = getattr(self, "aggro_timeout", 6.0)

    def give_experience(self, player):
        if self.health >= 1 or self.death_experience <= 0:
            return

        def is_valid_attacker(attacker):
            if attacker is None:
                return False
            if attacker is player:
                return True
            if attacker.__class__.__name__ == "Cat" and getattr(attacker, "tamed", False):
                return getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False)
            return False

        def award(attacker, amount):
            if amount <= 0 or attacker is None:
                return
            if attacker is player:
                player.experience += amount
                player.exp_total += amount
            elif getattr(attacker, "tamed", False) and hasattr(attacker, "gain_experience"):
                attacker.gain_experience(amount)

        eligible_attackers = [att for att in self.attackers if is_valid_attacker(att)]
        if not eligible_attackers:
            self.death_experience = 0
            return

        primary_attacker = self.last_attacker if is_valid_attacker(self.last_attacker) else None
        if primary_attacker is None and eligible_attackers:
            primary_attacker = eligible_attackers[-1]

        exp_gain = self.death_experience
        bonus_gain = exp_gain * 0.2

        award(primary_attacker, exp_gain)
        for attacker in eligible_attackers:
            if attacker is not primary_attacker:
                award(attacker, bonus_gain)

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
        # Treat banks (e.g., snowbanks) as non-solid so entities can walk
        # through them, but still allow them to affect movement speed.
        try:
            from world import Bank
        except Exception:
            Bank = None

        solid_objects = []
        for obj in nearby_objects:
            if hasattr(obj, 'liquid_type'):
                continue
            if Bank is not None and isinstance(obj, Bank):
                continue
            solid_objects.append(obj)
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

        # Clamp movement to global world boundaries (prevents slipping past cliffs).
        try:
            import world as world_data
            min_x = getattr(world_data, "spawn_min_x", None)
            max_x = getattr(world_data, "spawn_max_x", None)
            if min_x is not None and direction.x < 0 and collision_rect.left <= min_x:
                can_move_x = False
            if max_x is not None and direction.x > 0 and collision_rect.right >= max_x:
                can_move_x = False
        except Exception:
            pass

        return can_move_x, can_move_y

    def get_speed(self):
        speed = self.base_speed * self.speed
        if self.swimming:
            speed *= 0.5
        if getattr(self, "snowball_slow_stacks", 0) > 0:
            slow_mult = max(0.2, 1 - 0.12 * self.snowball_slow_stacks)
            speed *= slow_mult
        # Banks (snowbanks, etc.) apply a mild ground slow.
        speed *= getattr(self, "ground_slow_factor", 1.0)
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

        # Default ground-slow each frame; terrain like banks can override it.
        self.ground_slow_factor = 1.0

        if self.snowball_slow_timer > 0:
            self.snowball_slow_timer = max(0.0, self.snowball_slow_timer - dt)
            if self.snowball_slow_timer == 0:
                self.snowball_slow_stacks = 0
        
        sleep_multiplier = 40 if player_sleeping else 1
        animation_speed_multiplier = sleep_multiplier  # Use same multiplier for animations

        # Allow subclasses (like Cat) to take full control over movement
        # decisions by setting disable_autonomous_movement = True.
        if not getattr(self, "disable_autonomous_movement", False):
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
            # Banks (e.g., snowbanks) slightly slow walking speed when
            # standing on them, but no longer block movement.
            if nearby_objects:
                try:
                    from world import Bank
                except Exception:
                    Bank = None
                if Bank is not None:
                    collision_rect = self.get_collision_rect(0)
                    for obj in nearby_objects:
                        if isinstance(obj, Bank):
                            obj_rect = obj.get_collision_rect(0) if hasattr(obj, "get_collision_rect") else obj.rect
                            if collision_rect.colliderect(obj_rect):
                                self.ground_slow_factor = 0.75
                                break

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

        health_ratio = health / max_health if max_health > 0 else 0
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

        # Draw name + level above this mob, unless it's a special case
        # like a latched redmite that is handled elsewhere.
        if not getattr(self, "latched_to_player", False):
            # Cats render their own name/level when named; avoid duplicate labels.
            has_custom_cat_label = (self.__class__.__name__ == "Cat" and getattr(self, "cat_name", None))
            if not has_custom_cat_label:
                draw_mob_name_and_level(self, screen, cam_x)

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
                gain = harvest_experience * len(resources)
                player.experience += gain
                player.exp_total += gain

                # Tamed cats get 10% of any EXP the player gains
                # from harvesting (similar to mob death EXP sharing).
                try:
                    from mob_placement import cats as world_cats
                    share = max(0, gain * 0.1)
                    if share > 0:
                        for cat in world_cats:
                            if getattr(cat, "tamed", False):
                                cat.gain_experience(share)
                except Exception:
                    pass
            
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

from cats import Cat, cat_types, CAT_ATTACK_IMAGE_PATHS

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
        self.death_experience = int(75 * (1 + (self.level  * .001)))
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
        self.death_experience = int(100  * (1 + (self.level * .001)))
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
        self.death_experience = int(70  * (1 + (self.level * .001)))
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
        self.death_experience = int(500  * (1 + (self.level * .0001)))
        self.level = 1
        self.aggro_timer = 0.0
        self.aggro_timeout = 6.0

    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        if self.is_alive:
            target_dx = dx
            target_dy = dy
            
            if 50 * 50 < distance_sq < 140 * 140:
                self.chasing = True
                self.aggro_timer = self.aggro_timeout
            elif distance_sq > 260 * 260:
                self.chasing = False
                self.aggro_timer = 0.0

            if self.chasing and getattr(self, "attackers", set()):
                for attacker in list(self.attackers):
                    if getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False):
                        adx = attacker.rect.centerx - self.rect.centerx
                        ady = attacker.rect.centery - self.rect.centery
                        adist_sq = adx * adx + ady * ady
                        if adist_sq < distance_sq:
                            target_dx = adx
                            target_dy = ady
                            break

            if self.chasing and self.aggro_timer > 0:
                self.aggro_timer -= dt
                if self.aggro_timer <= 0:
                    self.chasing = False
                    self.aggro_timer = 0.0

            if self.chasing and not self.fleeing:
                direction = pygame.Vector2(target_dx, target_dy)
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                self.direction = direction 

    def _target_is_moving(self, target):
        if target is None:
            return False
        direction = getattr(target, "direction", None)
        if direction is None:
            return False
        try:
            return direction.length_squared() > 0
        except Exception:
            return False

    def _target_moving_away(self, target_x, target_y, target):
        if target is None:
            return False
        direction = getattr(target, "direction", None)
        if direction is None or direction.length_squared() == 0:
            return False
        to_target = pygame.Vector2(target_x - self.rect.centerx, target_y - self.rect.centery)
        if to_target.length_squared() == 0:
            return False
        try:
            target_dir = direction.normalize()
        except Exception:
            return False
        to_target_norm = to_target.normalize()
        return target_dir.dot(to_target_norm) > 0.4
    
    def get_attackers_in_range(self, attack_range_sq=3600):
        """Return list of attackers within range for AOE attacks."""
        in_range = []
        for attacker in getattr(self, "attackers", set()):
            if not getattr(attacker, "is_alive", True) or getattr(attacker, "destroyed", False):
                continue
            dx = attacker.rect.centerx - self.rect.centerx
            dy = attacker.rect.centery - self.rect.centery
            dist_sq = dx * dx + dy * dy
            if dist_sq < attack_range_sq:
                in_range.append(attacker)
        return in_range

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
            
            if not self.chasing and getattr(self, "attackers", set()):
                for attacker in list(self.attackers):
                    if getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False):
                        dx = attacker.rect.centerx - self.rect.centerx
                        dy = attacker.rect.centery - self.rect.centery
                        dist_sq = dx * dx + dy * dy
                        if dist_sq < (200 * 200):
                            self.chasing = True
                            self.aggro_timer = getattr(self, "aggro_timeout", 6.0)
                            break
            
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
        self.death_experience = int(500  * (1 + (self.level * 0.05)))
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
                if player and hasattr(player, "health"):
                    player.health -= self.attack_damage
                    sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
                
                attackers_in_range = self.get_attackers_in_range(2500)
                for attacker in attackers_in_range:
                    if hasattr(attacker, "health"):
                        attacker.health = max(0, attacker.health - self.attack_damage)
                        if hasattr(attacker, "register_attack"):
                            attacker.register_attack(self)

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


class Ashhound(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.name = name
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in ashhound_move_left_images]
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in ashhound_idle_left_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in ashhound_attack_left_images]
        self.move_attack_left_images = [pygame.image.load(img).convert_alpha() for img in ashhound_move_attack_left_images]

        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        self.move_attack_right_images = [pygame.transform.flip(img, True, False) for img in self.move_attack_left_images]

        self.image = self.stand_right_images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.14
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right"
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 54
        self.attack_animation_speed = 0.018

        self.attack_damage = 6
        self.base_speed = 170
        self.speed = 1
        self.full_health = 220 + (random.randint(10, 16) * self.level)
        self.health = self.full_health
        self.resource = "Monster Meat"
        self.resource_amount = random.randint(3, 6)
        self.death_experience = int(700 * (1 + (self.level * 0.04)))
        self.level = 1
        self.immune_to_lava = True

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 8, rect.y + 32, rect.width - 16, rect.height - 40)

    def attack(self, player_world_x, player_world_y, player):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx * dx + dy * dy
        if self.chasing:
            self.speed = 2.2
        else:
            self.speed = 1

        if self.is_alive and (self.health / self.full_health) < 0.15:
            if not self.fleeing:
                self.fleeing = True
                self.flee_timer = 8
            self.attacking = False
            return

        if self.fleeing:
            self.attacking = False
            return

        if self.is_alive and distance_sq < (60 * 60):
            if isinstance(player, Player) and hasattr(player, "is_in_spawn_protection") and player.is_in_spawn_protection():
                self.attacking = False
                return
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0

        if self.attacking:
            target_moving = self._target_is_moving(player)
            target_moving_away = self._target_moving_away(player_world_x, player_world_y, player)
            if target_moving_away or (self.chasing and self.direction.length_squared() > 0):
                frames = self.move_attack_right_images if self.last_direction == "right" else self.move_attack_left_images
            elif not target_moving:
                frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            else:
                if self.direction.length_squared() > 0:
                    frames = self.move_attack_right_images if self.last_direction == "right" else self.move_attack_left_images
                else:
                    frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

            self.attack_timer -= 1

            if self.attack_timer == self.attack_duration // 2 and distance_sq < (60 * 60):
                player.health -= self.attack_damage
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])

    def animate_walk(self, animation_speed_multiplier=1.0):
        if self.direction.x > 0:
            self.last_direction = "right"
        elif self.direction.x < 0:
            self.last_direction = "left"
        if getattr(self, "chasing", False):
            frames = self.move_attack_right_images if self.last_direction == "right" else self.move_attack_left_images
        else:
            frames = self.walk_right_images if self.last_direction == "right" else self.walk_left_images
        effective_animation_speed = self.animation_speed * animation_speed_multiplier
        self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
        self.image = frames[int(self.frame_index)]

    def animate_stand(self, animation_speed_multiplier=1.0):
        frames = self.stand_right_images if self.last_direction == "right" else self.stand_left_images
        effective_animation_speed = self.animation_speed * animation_speed_multiplier * 0.5
        self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
        self.image = frames[int(self.frame_index)]

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

        if not self.is_alive:
            self.direction.xy = (0, 0)
            self.image = ashhound_dead_image_right if self.last_direction == "right" else ashhound_dead_image_left




class Wolf(Enemy):
    pack_targets = {}
    pack_alphas = {}

    def __init__(self, x, y, name, pack_id=None):
        super().__init__(x, y, name)
        self.name = name
        self.walk_left_images = [pygame.image.load(p).convert_alpha() for p in wolf_walk_left_images]
        self.run_left_images = [pygame.image.load(p).convert_alpha() for p in wolf_run_left_images]
        self.attack_left_images = [pygame.image.load(p).convert_alpha() for p in wolf_attack_left_images]
        self.run_attack_left_images = [pygame.image.load(p).convert_alpha() for p in wolf_run_attack_left_images]
        self.stand_left_images = [pygame.image.load(p).convert_alpha() for p in wolf_idle_left_images]
        self.dead_image_left = pygame.image.load(wolf_dead_left_image).convert_alpha()

        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.run_right_images = [pygame.transform.flip(img, True, False) for img in self.run_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        self.run_attack_right_images = [pygame.transform.flip(img, True, False) for img in self.run_attack_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.dead_image_right = pygame.transform.flip(self.dead_image_left, True, False)

        self.image = self.stand_right_images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.last_direction = "right"
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 22

        self.attack_damage = 4
        self.base_speed = 150
        self.speed = 1
        self.full_health = 180 + (random.randint(8, 14) * self.level)
        self.health = self.full_health
        self.resource = "Raw Small Meat"
        self.resource_amount = random.randint(2, 4)
        self.death_experience = int(600 * (1 + (self.level * 0.04)))
        self.level = 1
        self.pack_id = pack_id if pack_id is not None else random.randint(1, 10_000_000)
        self.is_alpha = False
        self.prey_target = None
        self.attack_animation_speed = 0.018
        self.attack_duration = 54
        self.eat_heal_fraction = 0.25  # heal 25% of max health per full carcass
        self.eat_progress = 0.0        # time spent eating current carcass
        self.eat_time_required = 1.5   # seconds required to fully consume a carcass
        
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.follow_offset = (random.randint(-40, 40), random.randint(-40, 40))
        self.decision_timer = random.uniform(0.5, 1.5)
        self.pack_state = "idle"
        self.pack_chase_timeout = 0.0

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 6, rect.y + 30, rect.width - 12, rect.height - 36)
    
    def get_pack_collision_rect(self, cam_x):
        """Return a small collision box for pack-to-pack interactions (15w x 5h)."""
        rect = self.rect
        center_x = rect.centerx - cam_x
        center_y = rect.centery
        return pygame.Rect(center_x - 7, center_y - 2, 15, 5)

    def check_collision(self, direction, nearby_objects, nearby_mobs):
        """Override to use smaller collision box for pack members."""
        try:
            from world import Bank
        except Exception:
            Bank = None

        solid_objects = []
        for obj in nearby_objects:
            if hasattr(obj, 'liquid_type'):
                continue
            if Bank is not None and isinstance(obj, Bank):
                continue
            solid_objects.append(obj)
        
        packmates = [m for m in nearby_mobs if isinstance(m, Wolf) and m.pack_id == self.pack_id and m is not self]
        other_mobs = [m for m in nearby_mobs if m not in packmates]
        all_nearby = solid_objects + other_mobs

        def get_obj_collision_rect(obj):
            if hasattr(obj, 'get_collision_rect'):
                return obj.get_collision_rect(0)
            elif isinstance(obj, dict) and 'rect' in obj:
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

        pack_collision_rect = self.get_pack_collision_rect(0)
        pack_left_check = pygame.Rect(pack_collision_rect.left - 1, pack_collision_rect.top, 1, pack_collision_rect.height)
        pack_right_check = pygame.Rect(pack_collision_rect.right, pack_collision_rect.top, 1, pack_collision_rect.height)
        pack_top_check = pygame.Rect(pack_collision_rect.left, pack_collision_rect.top - 1, pack_collision_rect.width, 1)
        pack_bottom_check = pygame.Rect(pack_collision_rect.left, pack_collision_rect.bottom, pack_collision_rect.width, 1)

        def get_packmate_collision_rect(packmate):
            return packmate.get_pack_collision_rect(0)

        pack_left_collision = any(pack_left_check.colliderect(get_packmate_collision_rect(pm)) for pm in packmates)
        pack_right_collision = any(pack_right_check.colliderect(get_packmate_collision_rect(pm)) for pm in packmates)
        pack_up_collision = any(pack_top_check.colliderect(get_packmate_collision_rect(pm)) for pm in packmates)
        pack_down_collision = any(pack_bottom_check.colliderect(get_packmate_collision_rect(pm)) for pm in packmates)

        left_collision = left_collision or pack_left_collision
        right_collision = right_collision or pack_right_collision
        up_collision = up_collision or pack_up_collision
        down_collision = down_collision or pack_down_collision

        can_move_x = not ((direction.x > 0 and right_collision) or (direction.x < 0 and left_collision))
        can_move_y = not ((direction.y > 0 and down_collision) or (direction.y < 0 and up_collision))

        # Clamp to world bounds so wolves respect cliff edges too.
        try:
            import world as world_data
            min_x = getattr(world_data, "spawn_min_x", None)
            max_x = getattr(world_data, "spawn_max_x", None)
            if min_x is not None and direction.x < 0 and collision_rect.left <= min_x:
                can_move_x = False
            if max_x is not None and direction.x > 0 and collision_rect.right >= max_x:
                can_move_x = False
        except Exception:
            pass

        return can_move_x, can_move_y
    
    def _valid_target(self, target):
        if target is None:
            return False
        if getattr(target, "destroyed", False):
            return False
        if hasattr(target, "is_alive") and not getattr(target, "is_alive", True):
            return False
        return True

    def _is_enemy(self, obj):
        return getattr(obj, "enemy", False)

    def _can_eat(self, obj):
        """Return True if this object is a valid carcass the wolf can eat."""
        if obj is None:
            return False
        if getattr(obj, "destroyed", False):
            return False
        # Only eat dead mobs that provide meat.
        if not hasattr(obj, "is_alive") or getattr(obj, "is_alive", True):
            return False
        if not hasattr(obj, "meat_resource"):
            return False
        return True

    def _eat_carcass(self, corpse):
        """Consume a dead animal to heal and remove the carcass."""
        if not self._can_eat(corpse):
            return
        # Heal the wolf by a fraction of its max health.
        heal_amount = max(10, int(self.full_health * self.eat_heal_fraction))
        self.health = min(self.full_health, self.health + heal_amount)
        # Remove the corpse from the world so it can't be harvested anymore.
        corpse.destroyed = True
        # Stop chasing/attacking once we've eaten.
        self.chasing = False
        self.attacking = False
        self.direction.xy = (0, 0)
    
    def _apply_light_separation(self, packmates):
        """Apply gentle separation to prevent overlap within the pack."""
        separation_radius = 25
        for other in packmates:
            dx = self.rect.centerx - other.rect.centerx
            dy = self.rect.centery - other.rect.centery
            dist = math.hypot(dx, dy)
            
            if dist < separation_radius and dist > 0:
                self.vel_x += (dx / dist) * 0.05
                self.vel_y += (dy / dist) * 0.05
    
    def _update_smooth_velocity(self, desired_dx, desired_dy, smoothing=0.8):
        """Smoothly blend velocity toward desired direction."""
        length = math.hypot(desired_dx, desired_dy)
        if length > 0:
            desired_dx /= length
            desired_dy /= length
        
        self.vel_x = self.vel_x * smoothing + desired_dx * (1.0 - smoothing)
        self.vel_y = self.vel_y * smoothing + desired_dy * (1.0 - smoothing)

    def _choose_target(self, player_world_x, player_world_y, player, nearby_mobs):
        # Wolves prefer nearby non-enemy mobs; fall back to player.
        candidates = []
        for mob in nearby_mobs or []:
            if mob is self or isinstance(mob, Wolf):
                continue
            if getattr(mob, "destroyed", False):
                continue
            if self._is_enemy(mob):
                continue
            dx = mob.rect.centerx - self.rect.centerx
            dy = mob.rect.centery - self.rect.centery
            dist_sq = dx * dx + dy * dy
            candidates.append((mob.rect.centerx, mob.rect.centery, mob, dist_sq))

        if candidates:
            target = min(candidates, key=lambda c: c[3])
            return target[0], target[1], target[2]

        # Default to player
        return player_world_x, player_world_y, player

    def _attack_volume_scale(self, listener_pos):
        """Scale attack sound based on how far the listener (player) is; keep a stronger floor for audibility."""
        if not listener_pos:
            return 1.0
        listener_x, listener_y = listener_pos
        dist = math.hypot(listener_x - self.rect.centerx, listener_y - self.rect.centery)
        falloff_start = 120
        falloff_end = 700
        if dist <= falloff_start:
            return 1.0
        attenuation = 1.0 - (dist - falloff_start) / max(1.0, (falloff_end - falloff_start))
        return max(0.6, min(1.0, attenuation))

    def attack(self, target_x, target_y, target, listener_pos=None):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance_sq = dx * dx + dy * dy
        if self.chasing:
            self.speed = 1.9
        else:
            self.speed = 1

        if self.is_alive and (self.health / self.full_health) < 0.15:
            if not self.fleeing:
                self.fleeing = True
                self.flee_timer = 8
            self.attacking = False
            return

        if self.fleeing:
            self.attacking = False
            return

        if self.is_alive and distance_sq < (60 * 60):
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0

        if self.attacking:
            target_moving = self._target_is_moving(target)
            target_moving_away = self._target_moving_away(target_x, target_y, target)
            if target_moving_away:
                frames = self.run_attack_right_images if self.last_direction == "right" else self.run_attack_left_images
            elif not target_moving:
                frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            else:
                if self.chasing or self.direction.length_squared() > 0:
                    frames = self.run_attack_right_images if self.last_direction == "right" else self.run_attack_left_images
                else:
                    frames = self.attack_right_images if self.last_direction == "right" else self.attack_left_images
            attack_anim_speed = self.attack_animation_speed
            self.frame_index = (self.frame_index + attack_anim_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

            self.attack_timer -= 1

            if self.attack_timer == self.attack_duration // 2 and distance_sq < (60 * 60):
                if hasattr(target, "health"):
                    if isinstance(target, Player) and hasattr(target, "is_in_spawn_protection") and target.is_in_spawn_protection():
                        pass  # Don't damage the player inside the spawn protection bubble.
                    else:
                        target.health = max(0, target.health - self.attack_damage)
                        if hasattr(target, "register_attack"):
                            target.register_attack(self)
                # Make sure player hit audio stays audible; use distance falloff otherwise.
                volume_scale = 1.0 if listener_pos else self._attack_volume_scale(listener_pos)
                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]), volume_scale=volume_scale)
                
                attackers_in_range = self.get_attackers_in_range(3600)
                for attacker in attackers_in_range:
                    if hasattr(attacker, "health"):
                        attacker.health = max(0, attacker.health - self.attack_damage)
                        if hasattr(attacker, "register_attack"):
                            attacker.register_attack(self)

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])

    def animate_walk(self, animation_speed_multiplier=1.0):
        if self.direction.x > 0:
            self.last_direction = "right"
        elif self.direction.x < 0:
            self.last_direction = "left"
        frames = self.run_right_images if getattr(self, "chasing", False) else self.walk_right_images
        frames = frames if self.last_direction == "right" else (self.run_left_images if getattr(self, "chasing", False) else self.walk_left_images)
        effective_animation_speed = self.animation_speed * animation_speed_multiplier
        self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
        self.image = frames[int(self.frame_index)]

    def animate_stand(self, animation_speed_multiplier=1.0):
        frames = self.stand_right_images if self.last_direction == "right" else self.stand_left_images
        effective_animation_speed = self.animation_speed * animation_speed_multiplier * 0.5
        self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
        self.image = frames[int(self.frame_index)]

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        # Handle player proximity with normal Enemy aggro logic (50-140px range, 6-second timeout)
        player_world_x = getattr(player, "world_x", player.rect.centerx if player else self.rect.centerx)
        player_world_y = getattr(player, "world_y", player.rect.centery if player else self.rect.centery)
        if player:
            self.handle_player_proximity(dt, player_world_x, player_world_y, player, nearby_objects, nearby_mobs)

        # Pack-wide state management: if ANY wolf detects danger, activate pack chase
        self.pack_chase_timeout -= dt
        if getattr(self, "chasing", False) and self.pack_chase_timeout < 2.0:
            Wolf.pack_targets[self.pack_id] = getattr(self, "prey_target", player)
            self.pack_state = "chase"
            self.pack_chase_timeout = 6.0

        # Acquire or share pack target (only for non-player targets)
        current_pack_target = Wolf.pack_targets.get(self.pack_id)
        if not self._valid_target(current_pack_target) or isinstance(current_pack_target, Player):
            Wolf.pack_targets.pop(self.pack_id, None)
            current_pack_target = None
            self.pack_state = "idle"

        packmates = [m for m in (nearby_mobs or []) if isinstance(m, Wolf) and m.pack_id == self.pack_id and m is not self]

        # Ensure there is a designated alpha for this pack.
        alpha = Wolf.pack_alphas.get(self.pack_id)
        if not alpha or getattr(alpha, "destroyed", False) or not getattr(alpha, "is_alive", True):
            candidates = [w for w in packmates + [self] if not getattr(w, "destroyed", False) and getattr(w, "is_alive", True)]
            if candidates:
                alpha = min(candidates, key=lambda w: id(w))
                Wolf.pack_alphas[self.pack_id] = alpha
            else:
                alpha = None
                Wolf.pack_alphas.pop(self.pack_id, None)
        self.is_alpha = (alpha is self)

        if current_pack_target and self._valid_target(current_pack_target):
            target_obj = current_pack_target
            target_x = getattr(target_obj, "world_x", target_obj.rect.centerx)
            target_y = getattr(target_obj, "world_y", target_obj.rect.centery)
        else:
            target_x, target_y, target_obj = self._choose_target(
                player_world_x,
                player_world_y,
                player,
                nearby_mobs,
            )
            if self._valid_target(target_obj) and not isinstance(target_obj, Player):
                Wolf.pack_targets[self.pack_id] = target_obj

        # Cohesion: stay near pack center
        coh_vector = pygame.Vector2(0, 0)
        cohesion_weight = 0.0
        if packmates:
            center_x = sum(m.rect.centerx for m in packmates + [self]) / (len(packmates) + 1)
            center_y = sum(m.rect.centery for m in packmates + [self]) / (len(packmates) + 1)
            offset_to_center = pygame.Vector2(center_x - self.rect.centerx, center_y - self.rect.centery)
            if offset_to_center.length_squared() > 0:
                coh_vector = offset_to_center.normalize()
                distance_to_center = offset_to_center.length()
                desired_pack_radius = 140
                spread_threshold = 220
                if distance_to_center > spread_threshold:
                    cohesion_weight = 0.65
                elif distance_to_center > desired_pack_radius:
                    cohesion_weight = 0.5
                else:
                    cohesion_weight = 0.35

        # Set chasing based on target distance and current aggro state
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance_sq = dx * dx + dy * dy
        base_chasing = getattr(self, "chasing", False)
        if isinstance(target_obj, Player):
            # Player chasing is controlled by handle_player_proximity (range + timeout)
            pass
        else:
            # For non-player targets, activate chasing if in range
            self.chasing = base_chasing or distance_sq < (260 * 260)

        alpha = Wolf.pack_alphas.get(self.pack_id)
        
        if not self.is_alpha and alpha and alpha is not self and getattr(alpha, "is_alive", True) and not getattr(alpha, "destroyed", False):
            alpha_dx = alpha.rect.centerx - self.rect.centerx
            alpha_dy = alpha.rect.centery - self.rect.centery
            dist_alpha_sq = alpha_dx * alpha_dx + alpha_dy * alpha_dy
            
            if dist_alpha_sq > (400 * 400):
                target_x = alpha.rect.centerx + self.follow_offset[0]
                target_y = alpha.rect.centery + self.follow_offset[1]
            else:
                target_x = alpha.rect.centerx + self.follow_offset[0]
                target_y = alpha.rect.centery + self.follow_offset[1]
                self.chasing = getattr(alpha, "chasing", False) or self.pack_state == "chase"

        desired_dx = target_x - self.rect.centerx
        desired_dy = target_y - self.rect.centery
        
        if self.chasing and not self.fleeing:
            self._update_smooth_velocity(desired_dx, desired_dy, smoothing=0.8)
            self.speed = 1.9
        elif self.pack_state == "chase":
            self._update_smooth_velocity(desired_dx, desired_dy, smoothing=0.85)
            self.speed = 1.5
        else:
            self._update_smooth_velocity(desired_dx, desired_dy, smoothing=0.9)
            self.speed = 1.0

        self._apply_light_separation(packmates)

        if abs(self.vel_x) > 0.01 or abs(self.vel_y) > 0.01:
            can_move_x, can_move_y = self.check_collision(
                pygame.Vector2(self.vel_x, self.vel_y),
                nearby_objects or [],
                nearby_mobs or []
            )
            actual_speed = self.get_speed() * dt
            movement_x = self.vel_x * actual_speed if can_move_x else 0
            movement_y = self.vel_y * actual_speed if can_move_y else 0
            
            self.rect.x += movement_x
            self.rect.y += movement_y
            
            if self.vel_x > 0.1:
                self.last_direction = "right"
            elif self.vel_x < -0.1:
                self.last_direction = "left"
            
            if self.chasing or self.pack_state == "chase":
                self.animate_walk(animation_speed_multiplier=1.0)
            else:
                self.animate_walk()
        else:
            self.animate_stand()
        
        if self.attacking:
            direction = pygame.Vector2(desired_dx, desired_dy)
            if direction.length_squared() > 0:
                direction = direction.normalize()
                if abs(direction.x) >= abs(direction.y):
                    self.last_direction = "right" if direction.x >= 0 else "left"
                else:
                    self.last_direction = "down" if direction.y >= 0 else "up"

        # If we've reached any nearby carcass, eat it instead of attacking.
        eat_radius = 40
        try:
            wolf_rect = self.get_collision_rect(0)
        except Exception:
            wolf_rect = self.rect

        eat_candidates = []
        # Prefer a specific target if it's a carcass, but also allow other nearby carcasses.
        if self._can_eat(target_obj):
            eat_candidates.append(target_obj)
        for mob in nearby_mobs or []:
            if mob is target_obj:
                continue
            if self._can_eat(mob):
                eat_candidates.append(mob)

        eating_now = False
        for corpse in eat_candidates:
            try:
                if hasattr(corpse, "get_collision_rect"):
                    corpse_rect = corpse.get_collision_rect(0)
                else:
                    corpse_rect = corpse.rect
                expanded_corpse = corpse_rect.inflate(eat_radius * 2, eat_radius * 2)
                intersects = wolf_rect.colliderect(expanded_corpse)
            except Exception:
                dx_eat = corpse.rect.centerx - self.rect.centerx
                dy_eat = corpse.rect.centery - self.rect.centery
                intersects = (dx_eat * dx_eat + dy_eat * dy_eat) <= (eat_radius * eat_radius)

            if intersects:
                eating_now = True
                self.eat_progress += dt
                # Pause movement/attacks while eating
                self.direction.xy = (0, 0)
                if self.eat_progress >= self.eat_time_required:
                    self._eat_carcass(corpse)
                    self.eat_progress = 0.0
                    if not self.is_alive:
                        self.direction.xy = (0, 0)
                    return
                # Only work on one carcass at a time
                break

        if not eating_now:
            # Reset progress if we moved away from all carcasses
            self.eat_progress = 0.0

        # Attack if close - use actual target position, not formation position
        listener_pos = (player_world_x, player_world_y) if player else None
        actual_target_x = getattr(target_obj, "world_x", target_obj.rect.centerx) if target_obj else target_x
        actual_target_y = getattr(target_obj, "world_y", target_obj.rect.centery) if target_obj else target_y
        self.attack(actual_target_x, actual_target_y, target_obj, listener_pos=listener_pos)

        # Update decision timer for idle formation changes
        if not self.chasing and self.pack_state != "chase":
            self.decision_timer -= dt
            if self.decision_timer <= 0:
                self.follow_offset = (random.randint(-40, 40), random.randint(-40, 40))
                self.decision_timer = random.uniform(0.5, 1.5)

        if not self.is_alive:
            self.vel_x = 0
            self.vel_y = 0
            self.image = self.dead_image_right if self.last_direction == "right" else self.dead_image_left


class Wastedog(Wolf):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.name = name
        variant_key, variant_frames = random.choice(list(wastedog_variant_frames.items()))
        self.walk_left_images = [pygame.image.load(p).convert_alpha() for p in variant_frames["move"]]
        self.run_left_images = self.walk_left_images
        self.stand_left_images = [pygame.image.load(p).convert_alpha() for p in variant_frames["idle"]]
        attack_source = variant_frames.get("attack") or variant_frames["move_attack"]
        self.attack_left_images = [pygame.image.load(p).convert_alpha() for p in attack_source]
        self.move_attack_left_images = [pygame.image.load(p).convert_alpha() for p in variant_frames["move_attack"]]

        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.run_right_images = [pygame.transform.flip(img, True, False) for img in self.run_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        self.run_attack_left_images = self.move_attack_left_images
        self.run_attack_right_images = [pygame.transform.flip(img, True, False) for img in self.run_attack_left_images]

        self.dead_image_left = self.stand_left_images[0]
        self.dead_image_right = self.stand_right_images[0]

        self.image = self.stand_right_images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_index = 0
        self.animation_speed = 0.2
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0

        self.attack_timer = 0
        self.attack_duration = 54

        self.attack_damage = 6
        self.base_speed = 210
        self.speed = 1
        self.full_health = 220 + (random.randint(10, 16) * self.level)
        self.health = self.full_health
        self.resource = "Monster Meat"
        self.resource_amount = random.randint(3, 6)
        self.death_experience = int(700 * (1 + (self.level * 0.04)))
        self.level = 1
        self.immune_to_lava = True

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 8, rect.y + 32, rect.width - 16, rect.height - 40)

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
        self.death_experience = int(1000  * (1 + (self.level * 0.05)))
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

class PockRock:
    """Simple projectile for pock throws; mirrors player stones."""
    def __init__(self, x, y, target_x, target_y, damage):
        self.pos = pygame.Vector2(x, y)
        direction = pygame.Vector2(target_x - x, target_y - y)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        distance = direction.length()
        direction = direction.normalize()
        # Keep speed similar to player throws; clamp for short/long throws.
        self.speed = max(6.0, min(10.0, distance / 30.0))
        self.vel = direction
        self.max_distance = 500
        self.damage = damage
        self.distance_traveled = 0.0
        self.sprite = pock_stone_sprite
        self.sprite_size = self.sprite.get_width() if self.sprite else 16
        self.rect = pygame.Rect(
            x - self.sprite_size // 2, y - self.sprite_size // 2, self.sprite_size, self.sprite_size
        )
        self.destroyed = False

    def update_rect(self):
        self.rect.topleft = (self.pos.x - self.sprite_size // 2, self.pos.y - self.sprite_size // 2)

    def update(self, dt):
        if self.destroyed:
            return
        step = self.speed * max(1.0, dt * 60.0)
        move = self.vel * step
        self.distance_traveled += move.length()
        if self.distance_traveled >= self.max_distance:
            self.destroyed = True
            return
        self.pos += move
        self.update_rect()

    def draw(self, screen, cam_x):
        if self.destroyed:
            return
        if self.sprite:
            screen.blit(self.sprite, (int(self.pos.x - cam_x - self.sprite_size // 2), int(self.pos.y - self.sprite_size // 2)))
        else:
            pygame.draw.circle(screen, (150, 140, 130), (int(self.pos.x - cam_x), int(self.pos.y)), max(2, self.sprite_size // 2))


def spawn_pock_rock(x, y, target_x, target_y, damage):
    pock_rock_projectiles.append(PockRock(x, y, target_x, target_y, damage))


def update_pock_rocks(dt, player_world_x, player_world_y, player, mobs):
    player_rect = pygame.Rect(player_world_x - player.rect.width // 2,
                              player_world_y - player.rect.height // 2,
                              player.rect.width,
                              player.rect.height)
    small_targets = [m for m in mobs if isinstance(m, (Cat, Squirrel, Chicken, Crow, Glowbird))]

    for rock in list(pock_rock_projectiles):
        rock.update(dt)
        if rock.destroyed:
            pock_rock_projectiles.remove(rock)
            continue

        # Hit player
        if rock.rect.colliderect(player_rect):
            player.health -= rock.damage
            rock.destroyed = True
            sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
            pock_rock_projectiles.remove(rock)
            continue

        # Hit small critters
        hit_any = False
        for mob in small_targets:
            if mob.rect.colliderect(rock.rect):
                if hasattr(mob, "health"):
                    mob.health = max(0, mob.health - rock.damage)
                if hasattr(mob, "register_attack"):
                    mob.register_attack(None)
                hit_any = True
                break
        if hit_any:
            rock.destroyed = True
            pock_rock_projectiles.remove(rock)

class Redmite(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.stand_left_images = [pygame.transform.scale(img, (24, 24)) for img in redmite_idle_left_images]
        self.walk_left_images = [pygame.transform.scale(img, (24, 24)) for img in redmite_walk_left_images]
        self.latch_left_images = [pygame.transform.scale(img, (24, 24)) for img in redmite_latch_left_images]
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.latch_right_images = [pygame.transform.flip(img, True, False) for img in self.latch_left_images]

        self.latched_left_image = pygame.transform.scale(redmite_latched_left_image, (24, 24))
        self.latched_right_image = pygame.transform.flip(self.latched_left_image, True, False)
        self.latched_up_image = pygame.transform.scale(redmite_latched_up_image, (24, 24))

        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_index = 0
        self.animation_speed = 0.18
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"

        self.attacking = False
        self.throwing = False
        self.throw_timer = 0
        self.latching = False
        self.latched_to_player = False
        self.latched_slot = None
        self.damage_timer = 0
        self.damage_interval = 1.0
        self.latched_offset = (0, 0)

        self.attack_damage = 2
        self.base_speed = 200
        self.speed = 1
        self.full_health = 20 + random.randint(0, 10)
        self.health = self.full_health
        self.resource = "Chitin"
        self.special_drops = []
        self.resource_amount = 1
        self.death_experience = int(120 * (1 + (self.level * 0.02)))
        self.level = 1
        self.enemy = True
        self.aggressive = True

    def latch_to_player(self, player):
        if getattr(player, "redmite_slots", None) is None:
            player.redmite_slots = [None, None, None, None]
        for idx, slot in enumerate(player.redmite_slots):
            if slot is None:
                player.redmite_slots[idx] = self
                self.latched_slot = idx
                self.latched_to_player = True
                self.latching = False
                self.direction.xy = (0, 0)
                return True
        return False

    def detach(self, player=None):
        if player and getattr(player, "redmite_slots", None):
            if self.latched_slot is not None and 0 <= self.latched_slot < len(player.redmite_slots):
                if player.redmite_slots[self.latched_slot] is self:
                    player.redmite_slots[self.latched_slot] = None
        self.latched_slot = None
        self.latched_to_player = False
        self.latching = False

    def get_collision_rect(self, cam_x):
        rect = self.rect
        return pygame.Rect(rect.x - cam_x + 4, rect.y + 6, rect.width - 8, rect.height - 12)

    def attack(self, target_world_x, target_world_y, target_entity):
        if not isinstance(target_entity, Player):
            return
        if self.latched_to_player:
            return
        dx = target_world_x - self.rect.centerx
        dy = target_world_y - self.rect.centery
        distance_sq = dx * dx + dy * dy
        if self.is_alive and distance_sq < (28 * 28):
            if self.latch_to_player(target_entity):
                self.frame_index = 0.0
                self.latching = True

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if not self.is_alive:
            self.direction.xy = (0, 0)
            return

        if self.latched_to_player:
            if player is not None and not getattr(player, "is_alive", True):
                self.detach(player)
                return
            self.direction.xy = (0, 0)
            self.damage_timer += dt
            if self.damage_timer >= self.damage_interval and player:
                player.health -= 1
                self.damage_timer = 0
            if player:
                self.rect.center = (
                    getattr(player, "world_x", player.rect.centerx),
                    getattr(player, "world_y", player.rect.centery),
                )
            return

        super().update(dt, player, nearby_objects, nearby_mobs, player_sleeping)

    def animate_stand(self, animation_speed_multiplier=1.0):
        if self.latched_to_player:
            return
        super().animate_stand(animation_speed_multiplier)

    def animate_walk(self, animation_speed_multiplier=1.0):
        if self.latched_to_player:
            return
        super().animate_walk(animation_speed_multiplier)

    def draw(self, screen, cam_x):
        if self.latched_to_player:
            # Latched mites are drawn with the player overlay.
            return
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y))

    def handle_health(self, screen, cam_x, dt, player_sleeping=False):
        super().handle_health(screen, cam_x, dt, player_sleeping)
        if self.health <= 0 and self.latched_to_player:
            self.detach()
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
        self.rock_spawned = False
        self.throw_min_range_sq = 40 * 40
        self.throw_max_range_sq = 500 * 500
        self.throw_cooldown = 0
        self.throw_cooldown_duration = 90

        # Melee attack (used when the target is very close)
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 20
        # Use a slightly larger melee radius than the minimum throw range
        # so that when the player is "too close to throw", the Pock swaps
        # to a regular melee instead of trying to walk in place.
        self.melee_range_sq = 45 * 45

        self.attack_damage = 5
        self.base_speed = 120
        self.speed = 1
        self.full_health = 100 + (random.randint(12, 20) * self.level)
        self.health = self.full_health
        self.resource = "Hide"
        self.resource_amount = random.randint(2, 5)
        self.death_experience = int(500  * (1 + (self.level * 0.05)))
        self.level = 1

    def attack(self, target_world_x, target_world_y, target_entity):
        if target_entity is None or getattr(target_entity, "destroyed", False) or not getattr(target_entity, "is_alive", True):
            return

        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

        dx = target_world_x - self.rect.centerx
        dy = target_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy

        # Always face the target while engaged.
        self.last_direction = "right" if dx >= 0 else "left"

        # === Melee attack when very close ===
        if distance_sq <= self.melee_range_sq:
            # Stop trying to walk into the target when already in melee.
            self.direction.xy = (0, 0)
            # Cancel any ongoing throw so we fully commit to melee.
            self.throwing = False
            self.rock_spawned = False

            if not self.attacking and self.is_alive:
                self.attacking = True
                self.attack_timer = self.attack_duration
                self.frame_index = 0.0

            if self.attacking:
                # Reuse idle frames as a simple melee animation.
                frames = self.stand_right_images if self.last_direction == "right" else self.stand_left_images
                if frames:
                    self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
                    self.image = frames[int(self.frame_index)]

                self.attack_timer -= 1

                # Apply damage halfway through the swing if still in range.
                if self.attack_timer == self.attack_duration // 2 and distance_sq <= self.melee_range_sq:
                    if hasattr(target_entity, "health"):
                        target_entity.health = max(0, target_entity.health - self.attack_damage)
                        # Play the regular player hit sound when hitting the player.
                        try:
                            if isinstance(target_entity, Player):
                                sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
                        except NameError:
                            # Fallback if Player is not in scope for any reason.
                            pass

                if self.attack_timer <= 0:
                    self.attacking = False
                    self.frame_index = 0.0
                    self.image = (self.stand_right_images[0] if self.last_direction == "right"
                                  else self.stand_left_images[0])

            # While in melee mode we skip ranged throwing logic.
            return

        if self.is_alive and self.throw_min_range_sq < distance_sq < self.throw_max_range_sq and self.throw_cooldown <= 0:
            if not self.throwing:
                self.throwing = True
                self.throw_timer = self.throw_duration
                self.frame_index = 0.0
                self.rock_spawned = False
                self.direction.xy = (0, 0)
        elif not self.throwing and distance_sq >= self.throw_min_range_sq:
            # Walk toward the target between throws to close the gap.
            direction = pygame.Vector2(dx, dy)
            if direction.length_squared() > 0:
                self.direction = direction.normalize()

        if self.throwing:
            frames = self.throw_right_images if self.last_direction == "right" else self.throw_left_images
            self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]

            self.throw_timer -= 1

            if not self.rock_spawned and self.throw_timer <= self.throw_duration // 2:
                spawn_pock_rock(self.rect.centerx, self.rect.centery - 8, target_world_x, target_world_y, self.attack_damage)
                self.rock_spawned = True

            if self.throw_timer <= 0:
                self.throwing = False
                self.frame_index = 0.0
                self.image = (self.stand_right_images[0] if self.last_direction == "right"
                            else self.stand_left_images[0])
                self.throw_cooldown = self.throw_cooldown_duration

    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if self.throwing:
            # Lock movement/AI while throwing to keep animation visible.
            if not self.is_alive:
                self.image = pock_dead_image_right if self.last_direction == "right" else pock_dead_image_left
            return

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

            self.death_experience = int(300  * (1 + (self.level * 0.04)))
            self.aggressive = False
            self.enemy = False
        else:

            self.death_experience = int(150  * (1 + (self.level * 0.001)))
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

        draw_mob_name_and_level(self, screen, cam_x)
        
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
        self.death_experience = int(600  * (1 + (self.level * 0.05)))
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

        draw_mob_name_and_level(self, screen, cam_x)
        
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
        self.death_experience = int(800 * (1 + (self.level * 0.05)))
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

        draw_mob_name_and_level(self, screen, cam_x)
        
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
            target_dx = dx
            target_dy = dy
            
            if 50 * 50 < distance_sq < 250*250:
                self.chasing = True
            elif distance_sq > 400*400:
                self.chasing = False
            
            if self.chasing and getattr(self, "attackers", set()):
                for attacker in list(self.attackers):
                    if getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False):
                        adx = attacker.rect.centerx - self.rect.centerx
                        ady = attacker.rect.centery - self.rect.centery
                        adist_sq = adx * adx + ady * ady
                        if adist_sq < distance_sq:
                            target_dx = adx
                            target_dy = ady
                            break
            
            if self.chasing and not self.attacking:
                direction = pygame.Vector2(target_dx, target_dy)
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
        
        target_x = player_world_x
        target_y = player_world_y
        
        if getattr(self, "attackers", set()):
            for attacker in list(self.attackers):
                if getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False):
                    adx = attacker.rect.centerx - self.rect.centerx
                    ady = attacker.rect.centery - self.rect.centery
                    adist_sq = adx * adx + ady * ady
                    if adist_sq < distance_sq:
                        target_x = attacker.rect.centerx
                        target_y = attacker.rect.centery
                        distance_sq = adist_sq
                        break
        
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
                if player is not None and int(target_x) == int(player_world_x) and int(target_y) == int(player_world_y):
                    player.health -= self.attack_damage
                    sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
                else:
                    for attacker in list(getattr(self, "attackers", set())):
                        if attacker.rect.centerx == int(target_x) and attacker.rect.centery == int(target_y):
                            attacker.health -= self.attack_damage
                            break
            
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

class PolarBear(AggressiveMob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in polar_bear_idle_images]
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in polar_bear_walk_left_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in polar_bear_attack_left_images]
        
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
        self.death_experience = int(800 * (1 + (self.level * 0.05)))
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

        draw_mob_name_and_level(self, screen, cam_x)
        
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
            target_dx = dx
            target_dy = dy
            
            if 50 * 50 < distance_sq < 250*250:
                self.chasing = True
            elif distance_sq > 400*400:
                self.chasing = False
            
            if self.chasing and getattr(self, "attackers", set()):
                for attacker in list(self.attackers):
                    if getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False):
                        adx = attacker.rect.centerx - self.rect.centerx
                        ady = attacker.rect.centery - self.rect.centery
                        adist_sq = adx * adx + ady * ady
                        if adist_sq < distance_sq:
                            target_dx = adx
                            target_dy = ady
                            break
            
            if self.chasing and not self.attacking:
                direction = pygame.Vector2(target_dx, target_dy)
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
        
        target_x = player_world_x
        target_y = player_world_y
        
        if getattr(self, "attackers", set()):
            for attacker in list(self.attackers):
                if getattr(attacker, "is_alive", True) and not getattr(attacker, "destroyed", False):
                    adx = attacker.rect.centerx - self.rect.centerx
                    ady = attacker.rect.centery - self.rect.centery
                    adist_sq = adx * adx + ady * ady
                    if adist_sq < distance_sq:
                        target_x = attacker.rect.centerx
                        target_y = attacker.rect.centery
                        distance_sq = adist_sq
                        break
        
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
                if player is not None and int(target_x) == int(player_world_x) and int(target_y) == int(player_world_y):
                    player.health -= self.attack_damage
                    sound_manager.play_sound(random.choice([f"player_get_hit{i}" for i in range(1, 5)]))
                else:
                    for attacker in list(getattr(self, "attackers", set())):
                        if attacker.rect.centerx == int(target_x) and attacker.rect.centery == int(target_y):
                            attacker.health -= self.attack_damage
                            break
            
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
                self.image = pygame.transform.flip(polar_bear_dead_image, True, False)
            else:
                self.image = polar_bear_dead_image
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

class PandaBear(AggressiveMob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in panda_idle_images]
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in panda_walk_left_images]
        
        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 120
        self.speed = 1
        self.full_health = 150 + (random.randint(5, 10) * self.level)
        self.health = self.full_health
        self.meat_resource = "Raw Bear Meat"
        self.special_drops = [{'item': 'Fur', 'chance': 0.5, 'min': 1, 'max': 2}]
        self.resource_amount = 12
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        
        self.death_experience = int(400 * (1 + (self.level * 0.03)))
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
        
        if self.health < self.last_health:
            self.bar_timer = 5
            self.fleeing = True
        
        if self.bar_timer > 0:
            pygame.draw.rect(screen, (255, 20, 20), pygame.Rect(x, y, bar_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (40, 250, 40), pygame.Rect(x, y, health_width, bar_height), border_radius=2)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, bar_width, bar_height), width=1, border_radius=2)
            self.bar_timer -= dt

        draw_mob_name_and_level(self, screen, cam_x)
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def handle_player_proximity(self, dt, player_world_x, player_world_y, player=None, nearby_objects=None, nearby_mobs=None):
        return
    
    def flee(self, player_world_x, player_world_y, dt, player_sleeping=False):
        dx = player_world_x - self.rect.centerx
        dy = player_world_y - self.rect.centery
        distance_sq = dx*dx + dy*dy
        
        if self.is_alive and distance_sq < 300*300:
            if self.fleeing:
                if self.move_timer <= 0:
                    direction = pygame.Vector2(-dx, -dy)
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                    
                    self.speed = 1.8
                    self.direction = direction
                    self.move_timer = random.randint(30, 120)
                
                self.move_timer -= 1
                
                if distance_sq > 500*500:
                    self.fleeing = False
                    self.speed = 1.0
                    self.direction = pygame.Vector2(0, 0)
    
    def attack(self, player_world_x, player_world_y, player):
        pass
    
    def update(self, dt, player=None, nearby_objects=None, nearby_mobs=None, player_sleeping=False):
        if not self.is_alive:
            self.direction.xy = (0, 0)
            if self.last_direction == "right":
                self.image = pygame.transform.flip(panda_dead_image, True, False)
            else:
                self.image = panda_dead_image
            return
        
        if self.fleeing:
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
        self.dead_left_image = gila_dead_image
        self.dead_right_image = pygame.transform.flip(self.dead_left_image, True, False)
        
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 60
        self.speed = 1
        self.full_health = 60 + (random.randint(5, 10) * self.level)
        self.health = self.full_health
        self.resource = "Gila Meat"
        self.special_drops = [{'item': 'Venom Sac', 'chance': 0.1, 'min': 1, 'max': 2}]
        self.resource_amount = 2
        self.death_experience = int(200  * (1 + (self.level * 0.03)))
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

        draw_mob_name_and_level(self, screen, cam_x)
        
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
            self.image = self.dead_right_image if self.last_direction == "right" else self.dead_left_image
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


class Salamander(Gila):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.stand_left_images = [pygame.image.load(img).convert_alpha() for img in salamander_idle_images]
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in salamander_walk_left_images]
        self.attack_left_images = [pygame.image.load(img).convert_alpha() for img in salamander_attack_left_images]

        self.walk_right_images = [pygame.transform.flip(img, True, False) for img in self.walk_left_images]
        self.stand_right_images = [pygame.transform.flip(img, True, False) for img in self.stand_left_images]
        self.attack_right_images = [pygame.transform.flip(img, True, False) for img in self.attack_left_images]
        self.dead_left_image = salamander_dead_image
        self.dead_right_image = pygame.transform.flip(self.dead_left_image, True, False)

        # Reset the base image and rect to use the salamander sprites.
        self.image = self.stand_left_images[0]
        self.rect = self.image.get_rect(center=(x, y))


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
        # Crows have a small amount of meat that predators can eat.
        self.meat_resource = "Raw Small Meat"
        self.special_drops = [{'item': 'Raw Small Meat', 'chance': 0.6, 'min': 2, 'max': 4}]
        self.resource_amount = 4
        self.death_experience = int(100 * (1 + (self.level * 0.01)))
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

        draw_mob_name_and_level(self, screen, cam_x)
        
        self.last_health = self.health
        if self.health <= 0:
            self.is_alive = False
    
    def check_collision(self, direction, nearby_objects, nearby_mobs):
        if self.state == "flying":
            try:
                from world import CliffSide
                cliffs = [obj for obj in nearby_objects if isinstance(obj, CliffSide)]
            except Exception:
                cliffs = []
            if not cliffs:
                return True, True
            return super().check_collision(direction, cliffs, [])
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


class Glowbird(Mob):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        
        self.walk_left_images = [pygame.image.load(img).convert_alpha() for img in glowbird_walk_left_images]
        self.fly_left_images = [pygame.image.load(img).convert_alpha() for img in glowbird_fly_left_images]
        self.start_fly_left_images = [pygame.image.load(img).convert_alpha() for img in glowbird_start_fly_left_images]
        self.landing_left_images = [pygame.image.load(img).convert_alpha() for img in glowbird_landing_left_images]
        
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
        self.death_experience = int(100 * (1 + (self.level * 0.01)))
        self.level = 1
        
        self.frame_index = 0
        self.animation_speed = 0.25
        self.direction = pygame.Vector2(0, 0)
        self.move_timer = 0
        self.last_direction = "left"
        self.state = "walking"
        self.flying_timer = 0
        # Emits a smaller, cool-colored light compared to torches
        self.light_radius = 110
        self.light_tint = (10, 40, 120)

    
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

        draw_mob_name_and_level(self, screen, cam_x)
        
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
                self.image = pygame.transform.flip(glowbird_dead_image, True, False)
            else:
                self.image = glowbird_dead_image
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
        self.resource = "Monster Meat"
        self.meat_resource = "Monster Meat"
        self.resource_amount = 5
        
        special_drops = [{'item': 'Dragon Scales', 'chance': 0.8, 'min': 2, 'max': 5}]
        if self.type_data:
            for gem_data in self.type_data["rare_gems"]:
                special_drops.append({'item': gem_data["gem"], 'chance': gem_data["chance"], 'min': 1, 'max': 2})
        self.special_drops = special_drops
        
        self.death_experience = int(2000 * (1 + (self.level * 0.07)))
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

        # Dragons also get the unified name+level label.
        draw_mob_name_and_level(self, screen, cam_x)
        
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
    
    def animate_walk(self, animation_speed_multiplier=1.0):
        if self.state == "walking":
            if self.direction.x > 0:
                self.last_direction = "right"
            elif self.direction.x < 0:
                self.last_direction = "left"

            frames = self.walk_right_images if self.last_direction == "right" else self.walk_left_images
            effective_animation_speed = self.animation_speed * animation_speed_multiplier
            self.frame_index = (self.frame_index + effective_animation_speed) % len(frames)
            self.image = frames[int(self.frame_index)]
        else:
            self.animate_stand(animation_speed_multiplier)
