import pygame
from inventory import items_list, hotbar_image

class Smelter:
    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.active = False
        self.smelter_pos = None
        
        self.smelter_image = None
        self.smelter_lit_images = []
        try:
            for i in range(1, 6):
                img = pygame.image.load(f"assets/sprites/itemFrames/SmelterLit{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (400, 500))
                self.smelter_lit_images.append(img)
            if self.smelter_lit_images:
                self.smelter_image = self.smelter_lit_images[0]
        except Exception as e:
            print(f"Error loading smelter images: {e}")
            self.smelter_image = None
            self.smelter_lit_images = []
        
        self.input_slots = [None] * 6
        self.output_slots = [None] * 6
        self.fuel_slots = [None] * 4
        
        self.smelting_progress = [0.0] * 6
        self.smelting_times = [8.0] * 6
        self.is_smelting = [False] * 6
        
        self.fire_lit = False
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.5
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
        
        self.font_small = pygame.font.SysFont(None, 18)
        self.font_medium = pygame.font.SysFont(None, 22)
        
        self.slot_size = 48
        self.gap_size = 4
    
    def open(self, smelter_pos):
        self.active = True
        self.smelter_pos = smelter_pos
        self.fire_lit = False
        self.animation_frame = 0
        self.animation_timer = 0.0
    
    def close(self):
        self.active = False
        self.smelter_pos = None
        self.cancel_drag()
    
    def get_smelter_recipes(self):
        recipes = []
        seen = set()
        for item in items_list:
            if item.get("crafting_medium") == "smelter" and item.get("recipe"):
                item_name = item["item_name"]
                if item_name not in seen:
                    recipes.append(item)
                    seen.add(item_name)
        return recipes
    
    def can_smelt_item(self, item_name):
        for recipe in self.get_smelter_recipes():
            if recipe["item_name"] == item_name:
                return True
        return False
    
    def get_smelt_recipe(self, item_name):
        for recipe in self.get_smelter_recipes():
            if recipe["item_name"] == item_name:
                return recipe
        return None
    
    def light_fire(self):
        if not self._has_fuel():
            return False
        
        has_input = any(self.input_slots[i] is not None for i in range(6))
        if not has_input:
            return False
        
        self.fire_lit = True
        self.animation_frame = 0
        self.animation_timer = 0.0
        
        for i in range(6):
            if self.input_slots[i] is not None and not self.is_smelting[i]:
                self.is_smelting[i] = True
                self.smelting_progress[i] = 0.0
        
        return True
    
    def put_out_fire(self):
        self.fire_lit = False
        self.animation_frame = 0
        self.animation_timer = 0.0
    
    def _has_fuel(self):
        return any(self.fuel_slots[i] is not None for i in range(4))
    
    def _consume_fuel(self):
        if self.fuel_slots[0] is not None:
            self.fuel_slots[0]["quantity"] -= 1
            if self.fuel_slots[0]["quantity"] <= 0:
                self.fuel_slots[0] = None
                self._shift_fuel()
    
    def _shift_fuel(self):
        for i in range(3):
            self.fuel_slots[i] = self.fuel_slots[i + 1]
        self.fuel_slots[3] = None
    
    def update(self, dt):
        if not self.active:
            return
        
        if self.fire_lit:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_frame = (self.animation_frame + 1) % len(self.smelter_lit_images)
                self.animation_timer = 0.0
            
            fuel_consumption_rate = 1.0 / 60.0
            fuel_timer = getattr(self, 'fuel_timer', 0.0)
            fuel_timer += dt
            
            active_smelting = any(self.is_smelting[i] for i in range(6))
            if active_smelting:
                if fuel_timer >= fuel_consumption_rate:
                    self._consume_fuel()
                    fuel_timer = 0.0
                    if not self._has_fuel():
                        self.put_out_fire()
            
            self.fuel_timer = fuel_timer
            
            for i in range(6):
                if self.is_smelting[i] and self.input_slots[i] is not None:
                    self.smelting_progress[i] += dt
                    
                    if self.smelting_progress[i] >= self.smelting_times[i]:
                        self._complete_smelt(i)
                        self.smelting_progress[i] = 0.0
                        
                        if self.input_slots[i]["quantity"] > 0:
                            self.is_smelting[i] = True
                        else:
                            self.is_smelting[i] = False
                            self.input_slots[i] = None
    
    def _complete_smelt(self, slot_index):
        if self.input_slots[slot_index] is None:
            return
        
        input_item = self.input_slots[slot_index]
        recipe = self.get_smelt_recipe(input_item["item_name"])
        
        if recipe is None:
            return
        
        output_item_name = recipe["item_name"]
        output_amount = recipe.get("output_amount", 1)
        
        for item in items_list:
            if item["item_name"] == output_item_name:
                output_item = item
                break
        else:
            return
        
        if self.output_slots[slot_index] is None:
            new_output = output_item.copy()
            new_output["quantity"] = output_amount
            self.output_slots[slot_index] = new_output
        elif self.output_slots[slot_index]["item_name"] == output_item_name:
            max_stack = output_item.get("stack_size", 100)
            space_available = max_stack - self.output_slots[slot_index]["quantity"]
            amount_to_add = min(space_available, output_amount)
            self.output_slots[slot_index]["quantity"] += amount_to_add
        else:
            return
        
        self.input_slots[slot_index]["quantity"] -= 1
    
    def start_drag(self, slot_info):
        slot_index, slot_type = slot_info
        
        if slot_type == "inventory":
            slot = self.inventory.inventory_list[slot_index]
        elif slot_type == "hotbar":
            slot = self.inventory.hotbar_slots[slot_index]
        elif slot_type == "input":
            slot = self.input_slots[slot_index]
        elif slot_type == "output":
            slot = self.output_slots[slot_index]
        elif slot_type == "fuel":
            slot = self.fuel_slots[slot_index]
        else:
            slot = None
        
        if slot is not None:
            self.dragging = True
            self.dragged_item = slot.copy()
            self.dragged_from_slot = slot_index
            self.dragged_from_type = slot_type
            
            if slot_type == "inventory":
                self.inventory.inventory_list[slot_index] = None
            elif slot_type == "hotbar":
                self.inventory.hotbar_slots[slot_index] = None
            elif slot_type == "input":
                self.input_slots[slot_index] = None
            elif slot_type == "output":
                self.output_slots[slot_index] = None
            elif slot_type == "fuel":
                self.fuel_slots[slot_index] = None
    
    def end_drag(self, slot_info):
        if not self.dragging:
            return
        
        slot_index, slot_type = slot_info
        
        if slot_type == "inventory" or slot_type == "hotbar":
            is_hotbar = slot_type == "hotbar"
            if is_hotbar:
                target_slot = self.inventory.hotbar_slots[slot_index]
            else:
                target_slot = self.inventory.inventory_list[slot_index]
            
            if target_slot is None:
                if is_hotbar:
                    self.inventory.hotbar_slots[slot_index] = self.dragged_item
                else:
                    self.inventory.inventory_list[slot_index] = self.dragged_item
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
                    if is_hotbar:
                        self.inventory.hotbar_slots[slot_index] = self.dragged_item
                    else:
                        self.inventory.inventory_list[slot_index] = self.dragged_item
                else:
                    self.dragged_item = None
            else:
                if is_hotbar:
                    self.inventory.hotbar_slots[slot_index] = self.dragged_item
                else:
                    self.inventory.inventory_list[slot_index] = self.dragged_item
        
        elif slot_type in ["input", "output", "fuel"]:
            if slot_type == "input":
                target_slot = self.input_slots[slot_index]
            elif slot_type == "output":
                target_slot = self.output_slots[slot_index]
            else:
                target_slot = self.fuel_slots[slot_index]
            
            if target_slot is None:
                if slot_type == "input":
                    if self.can_smelt_item(self.dragged_item["item_name"]):
                        self.input_slots[slot_index] = self.dragged_item
                    else:
                        if self.dragged_from_type == "inventory":
                            self.inventory.inventory_list[self.dragged_from_slot] = self.dragged_item
                        elif self.dragged_from_type == "hotbar":
                            self.inventory.hotbar_slots[self.dragged_from_slot] = self.dragged_item
                        elif self.dragged_from_type in ["input", "output", "fuel"]:
                            if self.dragged_from_type == "input":
                                self.input_slots[self.dragged_from_slot] = self.dragged_item
                            elif self.dragged_from_type == "output":
                                self.output_slots[self.dragged_from_slot] = self.dragged_item
                            else:
                                self.fuel_slots[self.dragged_from_slot] = self.dragged_item
                elif slot_type == "output":
                    if self.dragged_from_type == "inventory":
                        self.inventory.inventory_list[self.dragged_from_slot] = self.dragged_item
                    elif self.dragged_from_type == "hotbar":
                        self.inventory.hotbar_slots[self.dragged_from_slot] = self.dragged_item
                    elif self.dragged_from_type in ["input", "output", "fuel"]:
                        if self.dragged_from_type == "input":
                            self.input_slots[self.dragged_from_slot] = self.dragged_item
                        elif self.dragged_from_type == "output":
                            self.output_slots[self.dragged_from_slot] = self.dragged_item
                        else:
                            self.fuel_slots[self.dragged_from_slot] = self.dragged_item
                else:
                    self.fuel_slots[slot_index] = self.dragged_item
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
                    if slot_type == "input":
                        self.input_slots[slot_index] = self.dragged_item
                    elif slot_type == "output":
                        self.output_slots[slot_index] = self.dragged_item
                    else:
                        self.fuel_slots[slot_index] = self.dragged_item
            else:
                if slot_type == "input":
                    self.input_slots[slot_index] = self.dragged_item
                elif slot_type == "output":
                    self.output_slots[slot_index] = self.dragged_item
                else:
                    self.fuel_slots[slot_index] = self.dragged_item
                
                if self.dragged_from_type == "input":
                    self.input_slots[self.dragged_from_slot] = target_slot
                elif self.dragged_from_type == "output":
                    self.output_slots[self.dragged_from_slot] = target_slot
                elif self.dragged_from_type == "fuel":
                    self.fuel_slots[self.dragged_from_slot] = target_slot
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
    
    def cancel_drag(self):
        if not self.dragging:
            return
        
        if self.dragged_from_type == "inventory":
            self.inventory.inventory_list[self.dragged_from_slot] = self.dragged_item
        elif self.dragged_from_type == "hotbar":
            self.inventory.hotbar_slots[self.dragged_from_slot] = self.dragged_item
        elif self.dragged_from_type == "input":
            self.input_slots[self.dragged_from_slot] = self.dragged_item
        elif self.dragged_from_type == "output":
            self.output_slots[self.dragged_from_slot] = self.dragged_item
        elif self.dragged_from_type == "fuel":
            self.fuel_slots[self.dragged_from_slot] = self.dragged_item
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
    
    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        inv_x = screen_width / 2 - 550
        inv_y = screen_height / 2 - 300
        
        inv_start_x = int(inv_x + 18)
        inv_start_y = int(inv_y + 44)
        
        smelter_x = int(inv_x + 600)
        smelter_y = int(inv_y)
        
        hotbar_x = screen_width // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen_height - 70
        slot_size = 48
        gap_size = 4
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        
        for i in range(self.inventory.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (i, "hotbar")
        
        columns = 5
        
        for slot_index in range(self.inventory.capacity):
            row = slot_index // columns
            col = slot_index % columns
            x = inv_start_x + col * (slot_size + gap_size)
            y = inv_start_y + row * (slot_size + gap_size - 3)
            
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, "inventory")
        
        input_start_x = smelter_x + 50
        input_start_y = smelter_y + 200
        
        for i in range(6):
            col = i % 3
            row = i // 3
            x = input_start_x + col * (slot_size + gap_size)
            y = input_start_y + row * (slot_size + gap_size)
            
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (i, "input")
        
        output_start_x = input_start_x + (3 * (slot_size + gap_size)) + 20
        
        for i in range(6):
            col = i % 3
            row = i // 3
            x = output_start_x + col * (slot_size + gap_size)
            y = input_start_y + row * (slot_size + gap_size)
            
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (i, "output")
        
        fuel_start_x = input_start_x
        fuel_start_y = input_start_y + (2 * (slot_size + gap_size)) + 60
        
        for i in range(4):
            col = i % 2
            row = i // 2
            x = fuel_start_x + col * (slot_size + gap_size)
            y = fuel_start_y + row * (slot_size + gap_size)
            
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (i, "fuel")
        
        return (None, None)
    
    def render(self, screen):
        if not self.active:
            return
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        inv_x = screen_width / 2 - 550
        inv_y = screen_height / 2 - 300
        
        inv_start_x = int(inv_x + 18)
        inv_start_y = int(inv_y + 44)
        
        self._render_inventory(screen, inv_start_x, inv_start_y)
        
        smelter_x = int(inv_x + 600)
        smelter_y = int(inv_y)
        
        if self.fire_lit and self.smelter_lit_images:
            screen.blit(self.smelter_lit_images[self.animation_frame], (smelter_x, smelter_y))
        elif self.smelter_image:
            screen.blit(self.smelter_image, (smelter_x, smelter_y))
        
        input_start_x = smelter_x + 50
        input_start_y = smelter_y + 200
        
        label_font = pygame.font.SysFont(None, 16)
        smelt_label = label_font.render("Smelt Input", True, (255, 200, 100))
        screen.blit(smelt_label, (input_start_x + 10, input_start_y - 35))
        
        for i in range(6):
            col = i % 3
            row = i // 3
            x = input_start_x + col * (self.slot_size + self.gap_size)
            y = input_start_y + row * (self.slot_size + self.gap_size)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, self.slot_size, self.slot_size), 1)
            
            if self.input_slots[i] is not None:
                item = self.input_slots[i]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        try:
                            icon = pygame.image.load(f"assets/sprites/items/{catalog_item['icon']}").convert_alpha()
                            icon = pygame.transform.scale(icon, (self.slot_size - 4, self.slot_size - 4))
                            screen.blit(icon, (x + 2, y + 2))
                        except:
                            pass
                        break
                
                if item["quantity"] > 1:
                    qty_text = self.font_small.render(str(item["quantity"]), True, (255, 255, 255))
                    screen.blit(qty_text, (x + self.slot_size - 20, y + self.slot_size - 18))
                
                if self.is_smelting[i]:
                    progress = self.smelting_progress[i] / self.smelting_times[i]
                    bar_height = int((self.slot_size - 4) * progress)
                    pygame.draw.rect(screen, (255, 100, 0), (x + 2, y + self.slot_size - 2 - bar_height, self.slot_size - 4, bar_height))
        
        output_start_x = input_start_x + (3 * (self.slot_size + self.gap_size)) + 20
        
        output_label = label_font.render("Output", True, (100, 200, 255))
        screen.blit(output_label, (output_start_x + 10, input_start_y - 35))
        
        for i in range(6):
            col = i % 3
            row = i // 3
            x = output_start_x + col * (self.slot_size + self.gap_size)
            y = input_start_y + row * (self.slot_size + self.gap_size)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, self.slot_size, self.slot_size), 1)
            
            if self.output_slots[i] is not None:
                item = self.output_slots[i]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        try:
                            icon = pygame.image.load(f"assets/sprites/items/{catalog_item['icon']}").convert_alpha()
                            icon = pygame.transform.scale(icon, (self.slot_size - 4, self.slot_size - 4))
                            screen.blit(icon, (x + 2, y + 2))
                        except:
                            pass
                        break
                
                if item["quantity"] > 1:
                    qty_text = self.font_small.render(str(item["quantity"]), True, (255, 255, 255))
                    screen.blit(qty_text, (x + self.slot_size - 20, y + self.slot_size - 18))
        
        button_y = input_start_y + (2 * (self.slot_size + self.gap_size)) + 30
        button_x = input_start_x + 80
        button_width = 100
        button_height = 40
        
        if self.fire_lit:
            button_color = (200, 100, 100)
            button_text = "Put Out Fire"
        else:
            button_color = (100, 200, 100)
            button_text = "Light Fire"
        
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y, button_width, button_height), 2)
        
        button_font = pygame.font.SysFont(None, 18)
        button_label = button_font.render(button_text, True, (255, 255, 255))
        text_rect = button_label.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_label, text_rect)
        
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        fuel_start_x = input_start_x
        fuel_start_y = button_y + 60
        
        fuel_label = label_font.render("Fuel", True, (255, 100, 100))
        screen.blit(fuel_label, (fuel_start_x + 10, fuel_start_y - 35))
        
        for i in range(4):
            col = i % 2
            row = i // 2
            x = fuel_start_x + col * (self.slot_size + self.gap_size)
            y = fuel_start_y + row * (self.slot_size + self.gap_size)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, self.slot_size, self.slot_size), 1)
            
            if self.fuel_slots[i] is not None:
                item = self.fuel_slots[i]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        try:
                            icon = pygame.image.load(f"assets/sprites/items/{catalog_item['icon']}").convert_alpha()
                            icon = pygame.transform.scale(icon, (self.slot_size - 4, self.slot_size - 4))
                            screen.blit(icon, (x + 2, y + 2))
                        except:
                            pass
                        break
                
                if item["quantity"] > 1:
                    qty_text = self.font_small.render(str(item["quantity"]), True, (255, 255, 255))
                    screen.blit(qty_text, (x + self.slot_size - 20, y + self.slot_size - 18))
        
        if self.dragging and self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            item = self.dragged_item
            for catalog_item in items_list:
                if catalog_item["item_name"] == item["item_name"]:
                    try:
                        icon = pygame.image.load(f"assets/sprites/items/{catalog_item['icon']}").convert_alpha()
                        icon = pygame.transform.scale(icon, (self.slot_size - 4, self.slot_size - 4))
                        screen.blit(icon, (mouse_pos[0] - self.slot_size // 2, mouse_pos[1] - self.slot_size // 2))
                    except:
                        pass
                    break
    
    def _render_inventory(self, screen, start_x, start_y):
        columns = 5
        slot_size = 48
        gap_size = 4
        
        for slot_index in range(self.inventory.capacity):
            row = slot_index // columns
            col = slot_index % columns
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * (slot_size + gap_size - 3)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, slot_size, slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, slot_size, slot_size), 1)
            
            if self.inventory.inventory_list[slot_index] is not None:
                item = self.inventory.inventory_list[slot_index]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        try:
                            icon = pygame.image.load(f"assets/sprites/items/{catalog_item['icon']}").convert_alpha()
                            icon = pygame.transform.scale(icon, (slot_size - 4, slot_size - 4))
                            screen.blit(icon, (x + 2, y + 2))
                        except:
                            pass
                        break
                
                if item["quantity"] > 1:
                    qty_text = self.font_small.render(str(item["quantity"]), True, (255, 255, 255))
                    screen.blit(qty_text, (x + slot_size - 20, y + slot_size - 18))
