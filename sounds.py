import pygame
import random
import time
import threading
from world import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.sounds = {}
        self.songs = []
        self.ambient_sounds = []
        self.playing_randomly = False
        self.ambient_running = False

    def add_song(self, path):
        self.songs.append(path)


    def add_sound(self, name, path, volume=.15):
        self.sounds[name] = pygame.mixer.Sound(path)
        self.sounds[name].set_volume(volume)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, path, loop=True, volume=0.4, fade_in=0):
        if path != self.current_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_in)
            self.current_music = path

    def stop_music(self, fade_out=0):
        if fade_out > 0:
            pygame.mixer.music.fadeout(fade_out)
            time.sleep(fade_out / 1000)
        else:
            pygame.mixer.music.stop()
        self.current_music = None
        self.playing_randomly = False
        self.ambient_running = False

    def _random_music_loop(self, min_delay=5, max_delay=20, volume=0.6, start_delay=100, fade_in=0):
        if start_delay > 0:
            time.sleep(start_delay)
        while self.playing_randomly:
            song = random.choice(self.songs)
            pygame.mixer.music.load(song)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(fade_ms=fade_in)
            while pygame.mixer.music.get_busy() and self.playing_randomly:
                time.sleep(1)
            if not self.playing_randomly:
                break
            delay = random.uniform(min_delay, max_delay)
            time.sleep(delay)

    def play_random_ambient_music(self, min_delay=5, max_delay=20, volume=0.4, start_delay=100, fade_in=1000):
        if not self.songs or self.playing_randomly:
            return
        self.playing_randomly = True
        threading.Thread(
            target=self._random_music_loop,
            args=(min_delay, max_delay, volume, start_delay, fade_in),
            daemon=True
        ).start()

    def _ambient_loop(self, min_delay=3, max_delay=15):
        while self.ambient_running:
            if self.ambient_sounds:
                sound = random.choice(self.ambient_sounds)
                sound.play()
            delay = random.uniform(min_delay, max_delay)
            time.sleep(delay)

    def play_random_ambient_sounds(self, min_delay=3, max_delay=15):
        if self.ambient_running:
            return
        self.ambient_running = True
        threading.Thread(target=self._ambient_loop, args=(min_delay, max_delay), daemon=True).start()

    def play_random_event_sound(self, name, chance=0.5):
        if name in self.sounds and random.random() < chance:
            self.sounds[name].play()


sound_manager = SoundManager()

sound_manager.add_song("assets/music/In The Night.mp3")
sound_manager.add_song("assets/music/Explorer.wav")
sound_manager.add_song("assets/music/IntoTheDarkness.wav")
sound_manager.add_song("assets/music/One More Step.wav")
sound_manager.add_song("assets/music/Mushrooms.wav")

sound_manager.add_sound("animal_breath", "assets/sounds/animal_breath.wav")
sound_manager.add_sound("bear_get_hit", "assets/sounds/bear_get_hit.wav")
sound_manager.add_sound("break_bush1", "assets/sounds/break_bush1.wav")
sound_manager.add_sound("break_bush2", "assets/sounds/break_bush2.wav")
sound_manager.add_sound("break_item", "assets/sounds/break_item.wav")
sound_manager.add_sound("buck_get_hit", "assets/sounds/buck_get_hit.wav")
sound_manager.add_sound("cat_attack1", "assets/sounds/cat_attack1.wav")
sound_manager.add_sound("cat_attack2", "assets/sounds/cat_attack2.wav")
sound_manager.add_sound("cat_attack3", "assets/sounds/cat_attack3.wav")
sound_manager.add_sound("cat_attack4", "assets/sounds/cat_attack4.wav")
sound_manager.add_sound("cat_attack5", "assets/sounds/cat_attack5.wav")
sound_manager.add_sound("cat_attack6", "assets/sounds/cat_attack6.wav")
sound_manager.add_sound("cat_get_hit1", "assets/sounds/cat_get_hit1.wav")
sound_manager.add_sound("cat_meow1", "assets/sounds/cat_meow1.wav", volume = .1)
sound_manager.add_sound("cat_meow2", "assets/sounds/cat_meow2.wav", volume = .1)
sound_manager.add_sound("cat_meow3", "assets/sounds/cat_meow3.wav", volume = .1)
sound_manager.add_sound("cat_meow4", "assets/sounds/cat_meow4.wav", volume = .1)
sound_manager.add_sound("cat_meow5", "assets/sounds/cat_meow5.wav", volume = .1)
sound_manager.add_sound("cat_meow6", "assets/sounds/cat_meow6.wav", volume = .1)
sound_manager.add_sound("cat_purr1", "assets/sounds/cat_purr1.wav")
sound_manager.add_sound("cat_purr2", "assets/sounds/cat_purr2.wav")
sound_manager.add_sound("cat_thrown1", "assets/sounds/cat_thrown1.wav")
sound_manager.add_sound("chicken_cluck1", "assets/sounds/chicken_cluck1.wav", volume = .1)
sound_manager.add_sound("chicken_cluck2", "assets/sounds/chicken_cluck2.wav", volume = .1)
sound_manager.add_sound("chicken_cluck3", "assets/sounds/chicken_cluck3.wav", volume = .1)
sound_manager.add_sound("chicken_cluck4", "assets/sounds/chicken_cluck4.wav", volume = .1)
sound_manager.add_sound("chicken_cluck5", "assets/sounds/chicken_cluck5.wav", volume = .1)
sound_manager.add_sound("chicken_cluck6", "assets/sounds/chicken_cluck6.wav", volume = .1)
sound_manager.add_sound("chicken_get_hit1", "assets/sounds/chicken_get_hit1.wav")
sound_manager.add_sound("chicken_get_hit2", "assets/sounds/chicken_get_hit2.wav")
sound_manager.add_sound("chicken_get_hit3", "assets/sounds/chicken_get_hit3.wav")
sound_manager.add_sound("collect_stone1", "assets/sounds/collect_stone1.wav")
sound_manager.add_sound("collect_stone2", "assets/sounds/collect_stone2.wav")
sound_manager.add_sound("cow_moo1", "assets/sounds/cow_moo1.wav", volume = .1)
sound_manager.add_sound("cow_moo2", "assets/sounds/cow_moo2.wav", volume = .1)
sound_manager.add_sound("crow_caw1", "assets/sounds/crow_caw1.wav")
sound_manager.add_sound("crow_caw2", "assets/sounds/crow_caw2.wav")
sound_manager.add_sound("crow_caw3", "assets/sounds/crow_caw3.wav")
sound_manager.add_sound("deer_get_hit", "assets/sounds/deer_get_hit.wav")
sound_manager.add_sound("drop_item", "assets/sounds/drop_item.wav")
sound_manager.add_sound("duskwretch_growl", "assets/sounds/duskwretch_growl.wav", volume = .05)
sound_manager.add_sound("duskwretch_roar1", "assets/sounds/duskwretch_roar1.wav")
sound_manager.add_sound("duskwretch_roar2", "assets/sounds/duskwretch_roar2.wav")
sound_manager.add_sound("duskwretch_chase_steps1", "assets/sounds/duskwretch_chase_steps1.wav")
sound_manager.add_sound("duskwretch_chase_steps2", "assets/sounds/duskwretch_chase_steps2.wav")
sound_manager.add_sound("duskwretch_chase_steps3", "assets/sounds/duskwretch_chase_steps3.wav")
sound_manager.add_sound("duskwretch_chase_steps4", "assets/sounds/duskwretch_chase_steps4.wav")
sound_manager.add_sound("duskwretch_chase_steps5", "assets/sounds/duskwretch_chase_steps5.wav")
sound_manager.add_sound("fire", "assets/sounds/fire.wav")
sound_manager.add_sound("fire_breath", "assets/sounds/fire_breath.wav")
sound_manager.add_sound("footstep_dirt1", "assets/sounds/footstep_dirt1.wav")
sound_manager.add_sound("footstep_dirt2", "assets/sounds/footstep_dirt2.wav")
sound_manager.add_sound("footstep_dirt3", "assets/sounds/footstep_dirt3.wav")
sound_manager.add_sound("footstep_dirt4", "assets/sounds/footstep_dirt4.wav")
sound_manager.add_sound("footstep_dirt5", "assets/sounds/footstep_dirt5.wav")
sound_manager.add_sound("footstep_dirt6", "assets/sounds/footstep_dirt6.wav")
sound_manager.add_sound("footstep_grass1", "assets/sounds/footstep_grass1.wav")
sound_manager.add_sound("footstep_grass2", "assets/sounds/footstep_grass2.wav")
sound_manager.add_sound("footstep_grass3", "assets/sounds/footstep_grass3.wav")
sound_manager.add_sound("footstep_grass4", "assets/sounds/footstep_grass4.wav")
sound_manager.add_sound("footstep_grass5", "assets/sounds/footstep_grass5.wav")
sound_manager.add_sound("footstep_grass6", "assets/sounds/footstep_grass6.wav")
sound_manager.add_sound("footstep_sand1", "assets/sounds/footstep_sand1.wav")
sound_manager.add_sound("footstep_sand2", "assets/sounds/footstep_sand2.wav")
sound_manager.add_sound("footstep_sand3", "assets/sounds/footstep_sand3.wav")
sound_manager.add_sound("footstep_sand4", "assets/sounds/footstep_sand4.wav")
sound_manager.add_sound("footstep_sand5", "assets/sounds/footstep_sand5.wav")
sound_manager.add_sound("footstep_sand6", "assets/sounds/footstep_sand6.wav")
sound_manager.add_sound("gather_wood1", "assets/sounds/gather_wood1.wav")
sound_manager.add_sound("gather_wood2", "assets/sounds/gather_wood2.wav")
sound_manager.add_sound("gather_wood3", "assets/sounds/gather_wood3.wav")
sound_manager.add_sound("harvest_stone1", "assets/sounds/harvest_stone1.wav")
sound_manager.add_sound("harvest_stone2", "assets/sounds/harvest_stone2.wav")
sound_manager.add_sound("harvest_stone3", "assets/sounds/harvest_stone3.wav")
sound_manager.add_sound("harvest_stone4", "assets/sounds/harvest_stone4.wav")
sound_manager.add_sound("harvest_stone5", "assets/sounds/harvest_stone5.wav")
sound_manager.add_sound("harvest_stone6", "assets/sounds/harvest_stone6.wav")
sound_manager.add_sound("hoofs1", "assets/sounds/hoofs1.wav")
sound_manager.add_sound("hoofs2", "assets/sounds/hoofs2.wav")
sound_manager.add_sound("hoofs3", "assets/sounds/hoofs3.wav")
sound_manager.add_sound("hoofs4", "assets/sounds/hoofs4.wav")
sound_manager.add_sound("hoofs5", "assets/sounds/hoofs5.wav")
sound_manager.add_sound("hoofs6", "assets/sounds/hoofs6.wav")
sound_manager.add_sound("item_equip", "assets/sounds/item_equip.wav")
sound_manager.add_sound("pickup_stick", "assets/sounds/pickup_stick.wav")
sound_manager.add_sound("place_item", "assets/sounds/place_item.wav")
sound_manager.add_sound("player_get_hit1", "assets/sounds/player_get_hit1.wav")
sound_manager.add_sound("player_get_hit2", "assets/sounds/player_get_hit2.wav")
sound_manager.add_sound("player_get_hit3", "assets/sounds/player_get_hit3.wav")
sound_manager.add_sound("player_get_hit4", "assets/sounds/player_get_hit4.wav")
sound_manager.add_sound("rain", "assets/sounds/rain.wav")
sound_manager.add_sound("pick_berry1", "assets/sounds/pick_berry1.wav")
sound_manager.add_sound("pick_berry2", "assets/sounds/pick_berry2.wav")
sound_manager.add_sound("pick_berry3", "assets/sounds/pick_berry3.wav")
sound_manager.add_sound("pick_berry4", "assets/sounds/pick_berry4.wav")
sound_manager.add_sound("level_up", "assets/sounds/level_up_sound.wav")
sound_manager.add_sound("chop_wood1", "assets/sounds/chop_wood1.wav")
sound_manager.add_sound("chop_wood2", "assets/sounds/chop_wood2.wav")
sound_manager.add_sound("chop_wood3", "assets/sounds/chop_wood3.wav")
sound_manager.add_sound("hammer_wood1", "assets/sounds/hammer_wood1.wav")
sound_manager.add_sound("hammer_wood2", "assets/sounds/hammer_wood2.wav")
sound_manager.add_sound("hammer_wood3", "assets/sounds/hammer_wood3.wav")
sound_manager.add_sound("pickup_grass1", "assets/sounds/pickup_grass1.wav")
sound_manager.add_sound("pickup_grass2", "assets/sounds/pickup_grass2.wav")
sound_manager.add_sound("pickup_grass3", "assets/sounds/pickup_grass3.wav")
sound_manager.add_sound("squirrel_chirp1", "assets/sounds/squirrel_chirp1.wav")
sound_manager.add_sound("squirrel_chirp2", "assets/sounds/squirrel_chirp2.wav")
sound_manager.add_sound("squirrel_chirp3", "assets/sounds/squirrel_chirp3.wav")
sound_manager.add_sound("squirrel_get_hit", "assets/sounds/squirrel_get_hit.wav")
sound_manager.add_sound("consume_item1", "assets/sounds/consume_item1.wav")
sound_manager.add_sound("consume_item2", "assets/sounds/consume_item2.wav")
sound_manager.add_sound("consume_item3", "assets/sounds/consume_item3.wav")
sound_manager.add_sound("consume_item4", "assets/sounds/consume_item4.wav")
sound_manager.add_sound("consume_item5", "assets/sounds/consume_item5.wav")
sound_manager.add_sound("consume_item6", "assets/sounds/consume_item6.wav")
sound_manager.add_sound("consume_water1", "assets/sounds/consume_water1.wav")
sound_manager.add_sound("consume_water2", "assets/sounds/consume_water2.wav")
sound_manager.add_sound("consume_water3", "assets/sounds/consume_water3.wav")
sound_manager.add_sound("consume_water4", "assets/sounds/consume_water4.wav")

grass_steps = [f"footstep_grass{i}" for i in range(1, 7)]