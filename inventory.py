import pygame
from mob_placement import player
from buttons import inventory_tab, crafting_tab, level_up_tab, cats_tab, inventory_tab_unused, crafting_tab_unused, level_up_tab_unused, cats_tab_unused



player_inventory_image = pygame.image.load("assets/sprites/player/CharacterCorynnFrontStanding.png")
player_inventory_image = pygame.transform.scale(player_inventory_image, (500, 500))

image_path = "assets/sprites/items"

items_list = [
    {"item_name" : "Apples", "icon": "Apple.png", "stack_size": 100, "weight": .5},

    {"item_name" : "Apple Wood", "icon": "AppleWood.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Dusk Wood", "icon": "DuskWood.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Fir Wood", "icon": "FirWood.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Oak Wood", "icon": "OakWood.png", "stack_size": 100, "weight": 1},

    {"item_name" : "Blood Berries", "icon": "BloodBerries.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Dawn Berries", "icon": "DawnBerries.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Dusk Berries", "icon": "DuskBerries.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Sun Berries", "icon": "SunBerries.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Teal Berries", "icon": "TealBerries.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Twilight Drupes", "icon": "TwilightDrupes.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Vio Berries", "icon": "VioBerries.png", "stack_size": 100, "weight": .05},
    
    {"item_name" : "Stone", "icon": "Stone.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Sticks", "icon": "Stick.png", "stack_size": 100, "weight": .2},
    {"item_name" : "Poisonous Mushrooms", "icon": "PoisonousMushroom.png", "stack_size": 100, "weight": .1},
    {"item_name" : "Fiber", "icon": "Fiber.png", "stack_size": 100, "weight": .05},
    {"item_name" : "Hide", "icon": "Hide.png", "stack_size": 100, "weight": .3},


    {"item_name" : "Fence", "icon": "Fence.png", "stack_size": 100, "weight": 6},
    {"item_name" : "Empty Cage", "icon": "EmptyCage.png", "stack_size": 1, "weight": 8},
]

for item in items_list:
    item["image"] = pygame.transform.scale(
        pygame.image.load(f"{image_path}/{item['icon']}").convert_alpha(),
        (60, 60)
    )


class Inventory():
    def __init__(self, capacity):
        self.capacity = capacity
        self.inventory_list = []
        self.slot_size = 64
        self.rows = 8
        self.columns = 8
        self.gap_size = 4
        self.padding_size = 5
        self.total_inventory_weight = 0
        self.state = "inventory"
        self.inventory_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/inventory_screen.png").convert_alpha(), (1100, 600))
        self.crafting_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/crafting_screen.png").convert_alpha(), (1100, 600))
        self.level_up_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/level_up_screen.png").convert_alpha(), (1100, 600))
        self.cat_screen_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/cats_screen.png").convert_alpha(), (1100, 600))

    def draw_inventory(self, screen):
        
        width = screen.get_width()
        height = screen.get_height()
        x_pos = screen.get_width() / 2 - self.inventory_image.get_width() / 2
        y_pos = screen.get_height() / 2 - self.inventory_image.get_height() / 2
        if self.state == "inventory":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.inventory_image, (x_pos, y_pos - 20))
            screen.blit(player_inventory_image, (700, 130))

            screen.blit(inventory_tab, (width // 2 - 533, height // 2 - 303))
            crafting_tab_unused.draw(screen)
            level_up_tab_unused.draw(screen)
            cats_tab_unused.draw(screen)

        elif self.state == "crafting":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.crafting_image, (x_pos, y_pos - 20))

            inventory_tab_unused.draw(screen)
            screen.blit(crafting_tab, (width // 2 - 397, height // 2 - 303))
            level_up_tab_unused.draw(screen)
            cats_tab_unused.draw(screen)
    
        elif self.state == "level_up":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.level_up_image, (x_pos, y_pos - 20))
            screen.blit(player_inventory_image, (700, 130))

            inventory_tab_unused.draw(screen)
            crafting_tab_unused.draw(screen)
            screen.blit(level_up_tab, (width // 2 - 261, height // 2 - 303))
            cats_tab_unused.draw(screen)

        elif self.state == "cats":
            inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
            screen.blit(inventory_surface, (0, 0))
            screen.blit(self.cat_screen_image, (x_pos, y_pos - 20))

            inventory_tab_unused.draw(screen)
            crafting_tab_unused.draw(screen)
            level_up_tab_unused.draw(screen)
            screen.blit(cats_tab, (width // 2 - 125, height // 2 - 303))
        
    def draw_items(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 17
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
        used_slots = 0
        displayed_items = {}
        font = pygame.font.SysFont(None, 20)
        
        self.total_inventory_weight = 0
        
        unique_items = []
        seen = set()
        for item_name in self.inventory_list:
            if item_name not in seen:
                unique_items.append(item_name)
                seen.add(item_name)
        
        for item_name in unique_items:
            for item in items_list:
                if item["item_name"] == item_name:
                    total_count = self.inventory_list.count(item_name)
                    total_item_weight = round(total_count * item["weight"], 1)
                    
                    self.total_inventory_weight += total_item_weight
                    
                    stacks_drawn = 0
                    remaining = total_count
                    
                    while remaining > 0 and used_slots < self.capacity:
                        row = used_slots // self.columns
                        col = used_slots % self.columns
                        x = start_x + col * (self.slot_size + self.gap_size)
                        y = start_y + row * (self.slot_size + self.gap_size - 3)
                        
                        screen.blit(item["image"], (x, y))
                        
                        stack_num = min(remaining, item["stack_size"])
                        weight_text = font.render(str(total_item_weight), True, (200, 200, 50))
                        screen.blit(weight_text, (x + 38, y + 4))
                        if stack_num > 1:
                            stack_text = font.render(str(stack_num), True, (255, 255, 255))
                            if stack_num == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif 99 > stack_num > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        
                        used_slots += 1
                        stacks_drawn += 1
                        remaining -= item["stack_size"]
                    
                    break
        
        player.weight = self.total_inventory_weight
        weight_text = font.render("Weight: ", True, (200, 200, 50))
        weight_num_text = font.render(str(f"{round(self.total_inventory_weight, 1)} / {player.max_weight}"), True, (200, 200, 50))
        total_weight_pos_x = screen.get_width()/2
        screen.blit(weight_text, (total_weight_pos_x + 20, 110))
        screen.blit(weight_num_text, (total_weight_pos_x + 20, 125))


    def add(self, resource):
        self.inventory_list.extend(resource)

inventory = Inventory(64)