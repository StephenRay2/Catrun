import pygame
from mob_placement import player
from buttons import inventory_tab, crafting_tab, level_up_tab, cats_tab, inventory_tab_unused, crafting_tab_unused, level_up_tab_unused, cats_tab_unused


hotbar_image = pygame.image.load("assets/sprites/buttons/hotbar.png").convert_alpha()
hotbar_image = pygame.transform.scale(hotbar_image, (686, 74))
player_inventory_image = pygame.image.load("assets/sprites/player/CharacterCorynnFrontStanding.png")
player_inventory_image = pygame.transform.scale(player_inventory_image, (500, 500))

image_path = "assets/sprites/items"

items_list = [
    {"item_name" : "Apples", "icon": "Apple.png", "stack_size": 100, "weight": .25},

    {"item_name" : "Apple Wood", "icon": "AppleWood.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Dusk Wood", "icon": "DuskWood.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Fir Wood", "icon": "FirWood.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Oak Wood", "icon": "OakWood.png", "stack_size": 100, "weight": .5},

    {"item_name" : "Blood Berries", "icon": "BloodBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Dawn Berries", "icon": "DawnBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Dusk Berries", "icon": "DuskBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Sun Berries", "icon": "SunBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Teal Berries", "icon": "TealBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Twilight Drupes", "icon": "TwilightDrupes.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Vio Berries", "icon": "VioBerries.png", "stack_size": 100, "weight": .01},
    {"item_name" : "Raw Beef", "icon": "RawBeef.png", "stack_size": 100, "weight": .25},
    
    {"item_name" : "Stone", "icon": "Stone.png", "stack_size": 100, "weight": .5},
    {"item_name" : "Raw Metal", "icon": "RawMetal.png", "stack_size": 100, "weight": 1},
    {"item_name" : "Sticks", "icon": "Stick.png", "stack_size": 100, "weight": .2},
    {"item_name" : "Poisonous Mushrooms", "icon": "PoisonousMushroom.png", "stack_size": 100, "weight": .05},
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
        self.inventory_list = [None] * capacity
        self.slot_size = 64
        self.rows = 8
        self.columns = 8
        self.gap_size = 4
        self.padding_size = 5
        self.total_inventory_weight = 0
        self.state = "inventory"
        self.hotbar_size = 10
        self.hotbar_slots = [None] * self.hotbar_size
        self.selected_hotbar_slot = 0
        self.inventory_full_message_timer = 0
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
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

    def draw_hotbar(self, screen):
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 100
        screen.blit(hotbar_image, (hotbar_x, hotbar_y))
        
        font = pygame.font.SysFont(None, 20)
        first_slot_x = hotbar_x + 6
        slot_y = hotbar_y + 6
        slot_spacing = 68
        
        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            
            if i == self.selected_hotbar_slot:
                highlight_surface = pygame.Surface((self.slot_size + 8, self.slot_size + 8), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (255, 255, 255, 150), (0, 0, self.slot_size + 8, self.slot_size + 8), 3)
                screen.blit(highlight_surface, (x - 6, y - 6))
            
            slot = self.hotbar_slots[i]
            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))
                        
                        stack_weight = round(quantity * item["weight"], 1)
                        weight_text = font.render(str(stack_weight), True, (200, 200, 50))
                        screen.blit(weight_text, (x + 38, y + 4))
                        
                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity >= 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        
                        break
        
    def draw_items(self, screen):
        start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 17
        start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
        font = pygame.font.SysFont(None, 20)
        self.total_inventory_weight = 0

        for hotbar_slot in self.hotbar_slots:
            if hotbar_slot is not None:
                item_name = hotbar_slot["item_name"]
                quantity = hotbar_slot["quantity"]
                
                for item in items_list:
                    if item["item_name"] == item_name:
                        stack_weight = round(quantity * item["weight"], 1)
                        self.total_inventory_weight += stack_weight
                        break

        for slot_index in range(self.capacity):
            slot = self.inventory_list[slot_index]

            row = slot_index // self.columns
            col = slot_index % self.columns
            x = start_x + col * (self.slot_size + self.gap_size)
            y = start_y + row * (self.slot_size + self.gap_size - 3)

            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]

                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))
                        
                        stack_weight = round(quantity * item["weight"], 1)
                        self.total_inventory_weight += stack_weight
                        
                        weight_text = font.render(str(stack_weight), True, (200, 200, 50))
                        screen.blit(weight_text, (x + 38, y + 4))
                        
                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        
                        break
        
        player.weight = self.total_inventory_weight
        weight_text = font.render("Weight: ", True, (200, 200, 50))
        weight_num_text = font.render(str(f"{round(self.total_inventory_weight, 1)} / {player.max_weight}"), True, (200, 200, 50))
        total_weight_pos_x = screen.get_width()/2
        screen.blit(weight_text, (total_weight_pos_x + 20, 110))
        screen.blit(weight_num_text, (total_weight_pos_x + 20, 125))


    def add(self, resource):
        all_added = True
        
        for item_name in resource:
            stacked = False
            
            for item_data in items_list:
                if item_data["item_name"] == item_name:
                    max_stack = item_data["stack_size"]
                    
                    for i in range(self.hotbar_size):
                        slot = self.hotbar_slots[i]
                        if slot and slot["item_name"] == item_name:
                            if slot["quantity"] < max_stack:
                                slot["quantity"] += 1
                                stacked = True
                                break
                    
                    if not stacked:
                        for i in range(self.capacity):
                            slot = self.inventory_list[i]
                            if slot and slot["item_name"] == item_name:
                                if slot["quantity"] < max_stack:
                                    slot["quantity"] += 1
                                    stacked = True
                                    break
                    
                    if not stacked:
                        for i in range(self.hotbar_size):
                            if self.hotbar_slots[i] is None:
                                self.hotbar_slots[i] = {
                                    "item_name": item_name,
                                    "quantity": 1
                                }
                                stacked = True
                                break
                    
                    if not stacked:
                        for i in range(self.capacity):
                            if self.inventory_list[i] is None:
                                self.inventory_list[i] = {
                                    "item_name": item_name,
                                    "quantity": 1
                                }
                                stacked = True
                                break
                    
                    break
            
            if not stacked:
                all_added = False
                if self.inventory_full_message_timer <= 0:
                    self.inventory_full_message_timer = 2.0
        
        return all_added
    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 100
        first_slot_x = hotbar_x + 6
        slot_y = hotbar_y + 6
        slot_spacing = 68
        
        for i in range(self.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                return (i, True)
        
        if self.state == "inventory":
            start_x = (screen.get_width() / 2 - self.inventory_image.get_width() / 2) + 17
            start_y = (screen.get_height() / 2 - self.inventory_image.get_height() / 2) + 44
            
            for slot_index in range(self.capacity):
                row = slot_index // self.columns
                col = slot_index % self.columns
                x = start_x + col * (self.slot_size + self.gap_size)
                y = start_y + row * (self.slot_size + self.gap_size - 3)
                
                if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                    return (slot_index, False)
        
        return (None, None) 
    
    def start_drag(self, slot_index, is_hotbar):
        if is_hotbar:
            slot = self.hotbar_slots[slot_index]
        else:
            slot = self.inventory_list[slot_index]
        
        if slot is not None:
            self.dragging = True
            self.dragged_item = slot.copy()
            self.dragged_from_slot = slot_index
            self.dragged_from_hotbar = is_hotbar
            
            if is_hotbar:
                self.hotbar_slots[slot_index] = None
            else:
                self.inventory_list[slot_index] = None

    def update_drag(self, mouse_pos):
        pass

    def end_drag(self, slot_index, is_hotbar, screen):
        if not self.dragging:
            return
        
        if is_hotbar:
            target_slot = self.hotbar_slots[slot_index]
        else:
            target_slot = self.inventory_list[slot_index]
        
        if target_slot is None:
            if is_hotbar:
                self.hotbar_slots[slot_index] = self.dragged_item
            else:
                self.inventory_list[slot_index] = self.dragged_item
        
        elif target_slot["item_name"] == self.dragged_item["item_name"]:
            max_stack = 100
            for item in items_list:
                if item["item_name"] == self.dragged_item["item_name"]:
                    max_stack = item["stack_size"]
                    break

            space_available = max_stack - target_slot["quantity"]
            amount_to_add = min(space_available, self.dragged_item["quantity"])
            
            target_slot["quantity"] += amount_to_add
            self.dragged_item["quantity"] -= amount_to_add
            
            if self.dragged_item["quantity"] > 0:
                if self.dragged_from_hotbar:
                    self.hotbar_slots[self.dragged_from_slot] = self.dragged_item
                else:
                    self.inventory_list[self.dragged_from_slot] = self.dragged_item
        
        else:
            if is_hotbar:
                self.hotbar_slots[slot_index] = self.dragged_item
            else:
                self.inventory_list[slot_index] = self.dragged_item
            
            if self.dragged_from_hotbar:
                self.hotbar_slots[self.dragged_from_slot] = target_slot
            else:
                self.inventory_list[self.dragged_from_slot] = target_slot
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False

    def cancel_drag(self):
        if not self.dragging:
            return
        
        if self.dragged_from_hotbar:
            self.hotbar_slots[self.dragged_from_slot] = self.dragged_item
        else:
            self.inventory_list[self.dragged_from_slot] = self.dragged_item
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False

    def draw_dragged_item(self, screen):
        if not self.dragging or self.dragged_item is None:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for item in items_list:
            if item["item_name"] == self.dragged_item["item_name"]:
                temp_surface = item["image"].copy()
                temp_surface.set_alpha(180)
                screen.blit(temp_surface, (mouse_x - self.slot_size // 2, mouse_y - self.slot_size // 2))
                
                if self.dragged_item["quantity"] > 1:
                    font = pygame.font.SysFont(None, 20)
                    quantity = self.dragged_item["quantity"]
                    stack_text = font.render(str(quantity), True, (255, 255, 255))
                    
                    x = mouse_x - self.slot_size // 2
                    y = mouse_y - self.slot_size // 2
                    
                    if quantity >= 100:
                        screen.blit(stack_text, (x + 38, y + 44))
                    elif quantity > 9:
                        screen.blit(stack_text, (x + 42, y + 44))
                    else:
                        screen.blit(stack_text, (x + 47, y + 44))
                
                break

inventory = Inventory(64)