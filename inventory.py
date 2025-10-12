import pygame


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
        self.gap_size = 5
        self.padding_size = 5
        self.inventory_width = ((self.slot_size * self.columns) + (self.gap_size * (self.columns - 1)) + (self.padding_size * 2))
        self.inventory_height = ((self.slot_size * self.rows) + (self.gap_size * (self.rows - 1)) + (self.padding_size * 2))

    def draw_inventory(self, screen):
        inventory_surface = pygame.Surface((self.inventory_width, self.inventory_height), pygame.SRCALPHA)
        pygame.draw.rect(inventory_surface, (0, 0, 0, 100), inventory_surface.get_rect())
        screen.blit(inventory_surface, ((screen.get_width()/2 - self.inventory_width/2), (screen.get_height()/2 - self.inventory_height/2)))

    def draw_items(self, screen):
        start_x = screen.get_width() / 2 - self.inventory_width / 2 + self.padding_size
        start_y = screen.get_height() / 2 - self.inventory_height / 2 + self.padding_size
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
                        y = start_y + row * (self.slot_size + self.gap_size)
                        
                        screen.blit(item["image"], (x, y))
                        
                        stack_num = min(remaining, item["stack_size"])
                        if stack_num > 1:
                            stack_text = font.render(str(stack_num), True, (255, 255, 255))
                            screen.blit(stack_text, (x + 45, y + 45))
                        
                        used_slots += 1
                        displayed_items[item_name] = stacks_drawn + 1
                        
                        if remaining > item["stack_size"]:
                            continue
                        else:
                            break
                    break


    def add(self, resource):
        self.inventory_list.extend(resource)
