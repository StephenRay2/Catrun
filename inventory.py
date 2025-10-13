import pygame


player_stand_image = pygame.image.load("assets/sprites/player/CharacterCorynnFrontStanding.png")
player_stand_image = pygame.transform.scale(player_stand_image, (500, 500))

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
    
    {"item_name" : "Stone", "icon": "Stone.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Sticks", "icon": "Stick.png", "stack_size": 100, "weight": .1},

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
        self.inventory_image = pygame.transform.scale(pygame.image.load("assets/sprites/buttons/inventory_screen.png").convert_alpha(), (1100, 600))

    def draw_inventory(self, screen):
        
        x_pos = screen.get_width() / 2 - self.inventory_image.get_width() / 2
        y_pos = screen.get_height() / 2 - self.inventory_image.get_height() / 2
        inventory_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        pygame.draw.rect(inventory_surface, (0, 0, 0, 150), screen.get_rect())
        screen.blit(inventory_surface, (0, 0))
        screen.blit(self.inventory_image, (x_pos, y_pos - 20))
        screen.blit(player_stand_image, (700, 130))
        
    def draw_items(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 17
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
        used_slots = 0
        displayed_items = {}
        font = pygame.font.SysFont(None, 24)
        
        for i, item_name in enumerate(self.inventory_list):
            for item in items_list:
                if item["item_name"] == item_name:
                    total_count = self.inventory_list.count(item_name)
                    stacks_drawn = displayed_items.get(item_name, 0)
                    remaining = total_count - (stacks_drawn * item["stack_size"])
                    
                    if remaining > 0 and used_slots < self.capacity:
                        row = used_slots // self.columns
                        col = used_slots % self.columns
                        x = start_x + col * (self.slot_size + self.gap_size)
                        y = start_y + row * (self.slot_size + self.gap_size - 3)
                        
                        screen.blit(item["image"], (x, y))
                        
                        stack_num = min(remaining, item["stack_size"])
                        if stack_num > 1:
                            stack_text = font.render(str(stack_num), True, (255, 255, 255))
                            if stack_num == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif 99 > stack_num > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        
                        used_slots += 1
                        displayed_items[item_name] = stacks_drawn + 1
                        
                        if remaining > item["stack_size"]:
                            continue
                        else:
                            break
                    break


    def add(self, resource):
        self.inventory_list.extend(resource)
