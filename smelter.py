import pygame
from inventory import items_list, hotbar_image

class Smelter:
    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.active = False
        self.ui_open = False
        self.smelter_pos = None
        
        self.smelter_screen = None
        self.smelter_image = None
        self.smelter_lit_images = []
        self.light_fire_button = None
        self.put_out_fire_button = None
        
        try:
            self.smelter_screen = pygame.image.load("assets/sprites/buttons/smelter_screen.png").convert_alpha()
            self.smelter_screen = pygame.transform.scale(self.smelter_screen, (1100, 600))
        except Exception as e:
            print(f"Error loading smelter screen: {e}")
            self.smelter_screen = None
        
        try:
            self.light_fire_button = pygame.image.load("assets/sprites/buttons/LightFire.png").convert_alpha()
            self.put_out_fire_button = pygame.image.load("assets/sprites/buttons/PutOutFire.png").convert_alpha()
        except Exception as e:
            print(f"Error loading fire buttons: {e}")
            self.light_fire_button = None
            self.put_out_fire_button = None
        
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
        self.fuel_burn_duration = 0.0
        self.fuel_burn_remaining = 0.0
        self.current_fuel_name = None
        self.fuel_burn_times = {
            "Sticks": 10.0,
            "Fir Wood": 20.0,
            "Apple Wood": 20.0,
            "Dusk Wood": 20.0,
            "Oak Wood": 20.0,
            "Small Olive Oil": 15.0,
            "Medium Glass Olive Oil": 30.0,
            "Large Metal Olive Oil": 45.0
        }
        self.default_fuel_time = 12.0
        
        self.fire_lit = False
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.5
        self.last_fire_toggle = 0
        self.fire_toggle_cooldown = 200  # ms guard to prevent multi-click burn
        self.last_drag_time = 0
        self.drag_cooldown = 120  # debounce between drag starts (ms)
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
        
        self.font_small = pygame.font.SysFont(None, 20)
        self.font_medium = pygame.font.SysFont(None, 22)
        
        self.slot_size = 64
        self.gap_size = 4
    
    def open(self, smelter_pos):
        self.active = True
        self.ui_open = True
        self.smelter_pos = smelter_pos
    
    def close(self):
        self.ui_open = False
        self.active = self.fire_lit or any(self.is_smelting)
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
            if recipe.get("recipe"):
                for ingredient in recipe["recipe"]:
                    if ingredient.get("item") == item_name:
                        return True
        return False
    
    def has_fuel_tag(self, item_name):
        for item in items_list:
            if item["item_name"] == item_name:
                return "fuel" in item.get("tags", [])
        return False
    
    def get_smelt_recipe(self, item_name):
        for recipe in self.get_smelter_recipes():
            if recipe.get("recipe"):
                for ingredient in recipe["recipe"]:
                    if ingredient.get("item") == item_name:
                        return recipe
        return None
    
    def _has_output_space(self, output_item_name):
        max_stack = 100
        for item in items_list:
            if item["item_name"] == output_item_name:
                max_stack = item.get("stack_size", 100)
                break
        
        for slot in self.output_slots:
            if slot is None:
                return True
            if slot["item_name"] == output_item_name and slot.get("quantity", 0) < max_stack:
                return True
        return False
    
    def is_cooking(self):
        return self.fire_lit
    
    def get_world_sprite(self, target_size):
        if not self.is_cooking():
            return None
        source = None
        if self.smelter_lit_images:
            source = self.smelter_lit_images[self.animation_frame]
        elif self.smelter_image:
            source = self.smelter_image
        if source:
            return pygame.transform.scale(source, target_size)
        return None
    
    def light_fire(self):
        now = pygame.time.get_ticks()
        if now - self.last_fire_toggle < self.fire_toggle_cooldown:
            return False
        self.last_fire_toggle = now
        if not self._has_fuel():
            return False
        
        has_input = any(self.input_slots[i] is not None for i in range(6))
        if not has_input:
            return False
        
        self.fire_lit = True
        self.animation_frame = 0
        self.animation_timer = 0.0
        self._organize_fuel_slots()
        if self.fuel_slots[0] is None:
            self.fire_lit = False
            return False
        current_fuel_name = self.fuel_slots[0]["item_name"]
        self.current_fuel_name = current_fuel_name
        self._consume_fuel_unit()
        self.fuel_burn_duration = self.get_fuel_burn_time(current_fuel_name)
        self.fuel_burn_remaining = self.fuel_burn_duration
        
        for i in range(6):
            if self.input_slots[i] is not None and not self.is_smelting[i]:
                self.is_smelting[i] = True
                self.smelting_progress[i] = 0.0
        
        return True
    
    def put_out_fire(self):
        now = pygame.time.get_ticks()
        if now - self.last_fire_toggle < self.fire_toggle_cooldown:
            return
        self.last_fire_toggle = now
        self.fire_lit = False
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.fuel_burn_duration = 0.0
        self.fuel_burn_remaining = 0.0
    
    def _has_fuel(self):
        return any(slot is not None and slot.get("quantity", 0) > 0 for slot in self.fuel_slots)
    
    def _organize_fuel_slots(self):
        non_empty = [slot for slot in self.fuel_slots if slot is not None and slot.get("quantity", 0) > 0]
        for i in range(4):
            self.fuel_slots[i] = non_empty[i] if i < len(non_empty) else None
    
    def get_fuel_burn_time(self, item_name):
        return self.fuel_burn_times.get(item_name, self.default_fuel_time)
    
    def _consume_fuel_unit(self):
        self._organize_fuel_slots()
        if self.fuel_slots[0] is None:
            self.fuel_burn_duration = 0.0
            self.fuel_burn_remaining = 0.0
            return False
        
        self.fuel_slots[0]["quantity"] -= 1
        if self.fuel_slots[0]["quantity"] <= 0:
            self.fuel_slots[0] = None
            self._organize_fuel_slots()
        return True
    
    def update(self, dt):
        if not self.active:
            return
        
        if self.fire_lit:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_frame = (self.animation_frame + 1) % len(self.smelter_lit_images)
                self.animation_timer = 0.0
            
            if self.fuel_burn_remaining <= 0:
                self._organize_fuel_slots()
                if self.fuel_slots[0] is None:
                    self.put_out_fire()
                    return
                self.current_fuel_name = self.fuel_slots[0]["item_name"]
                self.fuel_burn_duration = self.get_fuel_burn_time(self.current_fuel_name)
                self.fuel_burn_remaining = self.fuel_burn_duration
            
            self.fuel_burn_remaining -= dt
            while self.fuel_burn_remaining <= 0 and self._has_fuel():
                overflow = -self.fuel_burn_remaining
                self._organize_fuel_slots()
                if self.fuel_slots[0] is None:
                    self.put_out_fire()
                    break
                next_fuel_name = self.fuel_slots[0]["item_name"]
                if not self._consume_fuel_unit():
                    break
                self.current_fuel_name = next_fuel_name
                self.fuel_burn_duration = self.get_fuel_burn_time(next_fuel_name)
                self.fuel_burn_remaining = self.fuel_burn_duration - overflow
            
            if self.fuel_burn_remaining <= 0 and not self._has_fuel():
                self.put_out_fire()
            
            for i in range(6):
                if self.is_smelting[i] and self.input_slots[i] is not None:
                    recipe = self.get_smelt_recipe(self.input_slots[i]["item_name"])
                    if recipe:
                        output_item_name = recipe["item_name"]
                        if not self._has_output_space(output_item_name):
                            self.smelting_progress[i] = 0.0
                            continue
                    self.smelting_progress[i] += dt
                    
                    if self.smelting_progress[i] >= self.smelting_times[i]:
                        self._complete_smelt(i)
                        self.smelting_progress[i] = 0.0
                        
                        if self.input_slots[i]["quantity"] > 0:
                            self.is_smelting[i] = True
                        else:
                            self.is_smelting[i] = False
                            self.input_slots[i] = None
        
        if not self.fire_lit and not any(self.is_smelting) and not self.ui_open:
            self.active = False
    
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
        # Find best output slot: first stack with space, otherwise first empty
        target_idx = None
        for i in range(6):
            slot = self.output_slots[i]
            if slot and slot["item_name"] == output_item_name:
                max_stack = output_item.get("stack_size", 100)
                if slot["quantity"] < max_stack:
                    target_idx = i
                    break
        if target_idx is None:
            for i in range(6):
                if self.output_slots[i] is None:
                    target_idx = i
                    break
        if target_idx is None:
            return
        
        if self.output_slots[target_idx] is None:
            new_output = output_item.copy()
            new_output["quantity"] = output_amount
            self.output_slots[target_idx] = new_output
        else:
            max_stack = output_item.get("stack_size", 100)
            space_available = max_stack - self.output_slots[target_idx]["quantity"]
            amount_to_add = min(space_available, output_amount)
            self.output_slots[target_idx]["quantity"] += amount_to_add
        
        self.input_slots[slot_index]["quantity"] -= 1
    
    def start_drag(self, slot_info):
        # Debounce to avoid accidental multi-pickups from rapid click events
        now = pygame.time.get_ticks()
        if self.dragging:
            return
        if now - self.last_drag_time < self.drag_cooldown:
            return
        self.last_drag_time = now
        slot_index, slot_type = slot_info
        
        source_container = None
        if slot_type == "inventory":
            source_container = self.inventory.inventory_list
        elif slot_type == "hotbar":
            source_container = self.inventory.hotbar_slots
        elif slot_type == "input":
            source_container = self.input_slots
        elif slot_type == "output":
            source_container = self.output_slots
        elif slot_type == "fuel":
            source_container = self.fuel_slots
        
        if source_container is None:
            return
        
        slot = source_container[slot_index]
        
        if slot is not None:
            self.dragging = True
            self.dragged_item = slot.copy()
            self.dragged_from_slot = slot_index
            self.dragged_from_type = slot_type
            self.dragged_source_container = source_container
            source_container[slot_index] = None
    
    def end_drag(self, slot_info):
        if not self.dragging:
            return
        
        slot_index, slot_type = slot_info
        
        source_container = getattr(self, "dragged_source_container", None)
        
        def restore_source(item):
            if source_container is not None:
                source_container[self.dragged_from_slot] = item
        
        def finish():
            self.dragging = False
            self.dragged_item = None
            self.dragged_from_slot = None
            self.dragged_from_type = None
            self.dragged_source_container = None
        
        def update_input_state(idx):
            if idx is None:
                return
            if idx < 0 or idx >= len(self.input_slots):
                return
            if self.input_slots[idx] is None:
                self.is_smelting[idx] = False
                self.smelting_progress[idx] = 0.0
            elif self.fire_lit:
                self.is_smelting[idx] = True
                self.smelting_progress[idx] = 0.0
        
        if slot_type in ["inventory", "hotbar"]:
            target_container = self.inventory.hotbar_slots if slot_type == "hotbar" else self.inventory.inventory_list
            target_slot = target_container[slot_index]
            
            if target_slot is None:
                target_container[slot_index] = self.dragged_item
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
                    restore_source(self.dragged_item)
            else:
                target_container[slot_index] = self.dragged_item
                restore_source(target_slot)
            
            finish()
            return
        
        elif slot_type in ["input", "output", "fuel"]:
            if slot_type == "input":
                target_container = self.input_slots
                can_place = self.can_smelt_item(self.dragged_item["item_name"])
            elif slot_type == "output":
                target_container = self.output_slots
                can_place = True
            else:
                target_container = self.fuel_slots
                can_place = self.has_fuel_tag(self.dragged_item["item_name"])
            
            target_slot = target_container[slot_index]
            
            if not can_place:
                restore_source(self.dragged_item)
                finish()
                return
            
            if target_slot is None:
                target_container[slot_index] = self.dragged_item
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
                    restore_source(self.dragged_item)
            else:
                target_container[slot_index] = self.dragged_item
                restore_source(target_slot)
            
            # Reset smelting state for affected input slots when fire is lit
            if target_container is self.input_slots:
                update_input_state(slot_index)
            if source_container is self.input_slots:
                update_input_state(self.dragged_from_slot)
            
            finish()
            return
        
        restore_source(self.dragged_item)
        finish()
        
    def cancel_drag(self):
        if not self.dragging:
            return
        source_container = getattr(self, "dragged_source_container", None)
        if source_container is not None:
            source_container[self.dragged_from_slot] = self.dragged_item
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
        self.dragged_source_container = None

    def toggle_fire(self):
        if self.fire_lit:
            self.put_out_fire()
        else:
            self.light_fire()
    
    def _get_layout(self, screen):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        panel_width = self.smelter_screen.get_width() if self.smelter_screen else 1100
        panel_height = self.smelter_screen.get_height() if self.smelter_screen else 600
        offset_y = 0
        
        panel_x = screen_width / 2 - panel_width / 2
        panel_y = screen_height / 2 - panel_height / 2
        
        smelter_x = int(panel_x + 650)  # shift smelter image right
        smelter_y = int(panel_y + offset_y)
        
        input_start_x = smelter_x + 50 - 3 - 50  # move input/output further left
        input_start_y = smelter_y + 150
        
        output_start_x = input_start_x + (3 * (self.slot_size + self.gap_size)) + 20
        # Center fuel between input and output columns
        fuel_width = 2 * self.slot_size + self.gap_size
        input_block_width = 3 * self.slot_size + 2 * self.gap_size
        output_block_width = input_block_width
        area_left = input_start_x
        area_right = output_start_x + output_block_width
        center_x = (area_left + area_right) / 2
        
        button_y = input_start_y + (2 * (self.slot_size + self.gap_size)) + 30
        button_width = self.light_fire_button.get_width() if self.light_fire_button else 100
        button_x = int(center_x - button_width / 2)
        
        fuel_start_x = int(center_x - fuel_width / 2)
        fuel_start_y = button_y + 60
        
        return {
            "panel_x": panel_x,
            "panel_y": panel_y,
            "panel_draw_y": panel_y - 20 + offset_y,
            "inv_start_x": int(panel_x + 18),
            "inv_start_y": int(panel_y + 44 + offset_y),
            "smelter_x": smelter_x,
            "smelter_y": smelter_y,
            "input_start_x": input_start_x,
            "input_start_y": input_start_y,
            "output_start_x": output_start_x,
            "button_x": button_x,
            "button_y": button_y,
            "fuel_start_x": fuel_start_x,
            "fuel_start_y": fuel_start_y
        }
    
    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        layout = self._get_layout(screen)
        hotbar_slot_size = self.slot_size * 0.75
        
        inv_start_x = layout["inv_start_x"]
        inv_start_y = layout["inv_start_y"]

        input_start_x = layout["input_start_x"]
        input_start_y = layout["input_start_y"]
        
        # Prioritize smelter slots so the overlapping inventory grid doesn't capture the hover
        for i in range(6):
            col = i % 3
            row = i // 3
            x = input_start_x + col * (self.slot_size + self.gap_size)
            y = input_start_y + row * (self.slot_size + self.gap_size)
            
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                return (i, "input")
        
        output_start_x = layout["output_start_x"]
        
        for i in range(6):
            col = i % 3
            row = i // 3
            x = output_start_x + col * (self.slot_size + self.gap_size)
            y = input_start_y + row * (self.slot_size + self.gap_size)
            
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                return (i, "output")
        
        fuel_start_x = layout["fuel_start_x"]
        fuel_start_y = layout["fuel_start_y"]
        
        for i in range(4):
            col = i % 2
            row = i // 2
            x = fuel_start_x + col * (self.slot_size + self.gap_size)
            y = fuel_start_y + row * (self.slot_size + self.gap_size)
            
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                return (i, "fuel")
        
        hotbar_x = screen_width // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen_height - 70
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        
        for i in range(self.inventory.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            if x <= mouse_x <= x + hotbar_slot_size and y <= mouse_y <= y + hotbar_slot_size:
                return (i, "hotbar")
        
        columns = self.inventory.columns
        
        for slot_index in range(self.inventory.capacity):
            row = slot_index // columns
            col = slot_index % columns
            x = inv_start_x + col * (self.slot_size + self.gap_size)
            y = inv_start_y + row * (self.slot_size + self.gap_size - 3)
            
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                return (slot_index, "inventory")
        
        return (None, None)
    
    def render(self, screen):
        if not self.active or not self.ui_open:
            return

        layout = self._get_layout(screen)
        mouse_pos = pygame.mouse.get_pos()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        smelter_screen_x = layout["panel_x"]
        smelter_screen_y = layout["panel_draw_y"]
        
        if self.smelter_screen:
            screen.blit(self.smelter_screen, (int(smelter_screen_x), int(smelter_screen_y)))
        
        inv_start_x = layout["inv_start_x"]
        inv_start_y = layout["inv_start_y"]
        
        self._render_inventory(screen, inv_start_x, inv_start_y)
        
        smelter_x = layout["smelter_x"]
        smelter_y = layout["smelter_y"]
        
        if self.fire_lit and self.smelter_lit_images:
            screen.blit(self.smelter_lit_images[self.animation_frame], (smelter_x, smelter_y))
        elif self.smelter_image:
            screen.blit(self.smelter_image, (smelter_x, smelter_y))
        
        input_start_x = layout["input_start_x"]
        input_start_y = layout["input_start_y"]
        
        label_font = pygame.font.SysFont(None, 16)
        smelt_label = label_font.render("Smelt Input", True, (255, 200, 100))
        screen.blit(smelt_label, (input_start_x + 10, input_start_y - 35))
        
        font = pygame.font.SysFont(None, 20)
        for i in range(6):
            col = i % 3
            row = i // 3
            x = input_start_x + col * (self.slot_size + self.gap_size)
            y = input_start_y + row * (self.slot_size + self.gap_size)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, self.slot_size, self.slot_size), 2)
            
            if self.is_smelting[i] and self.input_slots[i] is not None:
                progress = max(0.0, min(1.0, self.smelting_progress[i] / self.smelting_times[i]))
                bar_height = int((self.slot_size - 4) * progress)
                pygame.draw.rect(screen, (255, 100, 0), (x + 2, y + self.slot_size - 2 - bar_height, self.slot_size - 4, bar_height))
            
            if self.input_slots[i] is not None:
                item = self.input_slots[i]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        screen.blit(catalog_item["image"], (x, y))
                        break

                if item["quantity"] > 1:
                    qty_text = font.render(str(item["quantity"]), True, (255, 255, 255))
                    if item["quantity"] == 100:
                        screen.blit(qty_text, (x + 38, y + 44))
                    elif item["quantity"] > 9:
                        screen.blit(qty_text, (x + 42, y + 44))
                    else:
                        screen.blit(qty_text, (x + 47, y + 44))

                if pygame.Rect(x, y, self.slot_size, self.slot_size).collidepoint(mouse_pos):
                    self.inventory.register_hover_candidate(
                        ("smelter_input", i),
                        item["item_name"],
                        (x, y, self.slot_size, self.slot_size),
                        slot_data=item
                    )
        
        output_start_x = layout["output_start_x"]
        
        output_label = label_font.render("Output", True, (100, 200, 255))
        screen.blit(output_label, (output_start_x + 10, input_start_y - 35))
        
        for i in range(6):
            col = i % 3
            row = i // 3
            x = output_start_x + col * (self.slot_size + self.gap_size)
            y = input_start_y + row * (self.slot_size + self.gap_size)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, self.slot_size, self.slot_size), 2)
            
            if self.output_slots[i] is not None:
                item = self.output_slots[i]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        screen.blit(catalog_item["image"], (x, y))
                        break

                if item["quantity"] > 1:
                    qty_text = font.render(str(item["quantity"]), True, (255, 255, 255))
                    if item["quantity"] == 100:
                        screen.blit(qty_text, (x + 38, y + 44))
                    elif item["quantity"] > 9:
                        screen.blit(qty_text, (x + 42, y + 44))
                    else:
                        screen.blit(qty_text, (x + 47, y + 44))

                if pygame.Rect(x, y, self.slot_size, self.slot_size).collidepoint(mouse_pos):
                    self.inventory.register_hover_candidate(
                        ("smelter_output", i),
                        item["item_name"],
                        (x, y, self.slot_size, self.slot_size),
                        slot_data=item
                    )
        
        button_y = layout["button_y"]
        button_x = layout["button_x"]
        
        if self.fire_lit:
            if self.put_out_fire_button:
                screen.blit(self.put_out_fire_button, (button_x, button_y))
                self.button_rect = self.put_out_fire_button.get_rect(topleft=(button_x, button_y))
            else:
                self.button_rect = pygame.Rect(button_x, button_y, 100, 40)
        else:
            if self.light_fire_button:
                screen.blit(self.light_fire_button, (button_x, button_y))
                self.button_rect = self.light_fire_button.get_rect(topleft=(button_x, button_y))
            else:
                self.button_rect = pygame.Rect(button_x, button_y, 100, 40)
        
        fuel_start_x = layout["fuel_start_x"]
        fuel_start_y = layout["fuel_start_y"]
        
        fuel_label = label_font.render("Fuel", True, (255, 100, 100))
        screen.blit(fuel_label, (fuel_start_x + 10, fuel_start_y - 35))
        
        for i in range(4):
            col = i % 2
            row = i // 2
            x = fuel_start_x + col * (self.slot_size + self.gap_size)
            y = fuel_start_y + row * (self.slot_size + self.gap_size)
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (150, 150, 150), (x, y, self.slot_size, self.slot_size), 2)
            
            fuel_ratio = None
            display_item = self.fuel_slots[i]
            if display_item is None and i == 0 and self.fire_lit and self.current_fuel_name:
                display_item = {"item_name": self.current_fuel_name, "quantity": 1}
            
            if i == 0 and self.fire_lit and self.fuel_burn_duration > 0:
                fuel_ratio = max(0.0, min(1.0, self.fuel_burn_remaining / self.fuel_burn_duration))
            if fuel_ratio is not None:
                bar_height = int((self.slot_size - 4) * fuel_ratio)
                pygame.draw.rect(screen, (50, 200, 50), (x + 2, y + self.slot_size - 2 - bar_height, self.slot_size - 4, bar_height))
            
            if display_item is not None:
                for catalog_item in items_list:
                    if catalog_item["item_name"] == display_item["item_name"]:
                        screen.blit(catalog_item["image"], (x, y))
                        break

                if display_item.get("quantity", 1) > 1:
                    qty_text = font.render(str(display_item["quantity"]), True, (255, 255, 255))
                    if display_item["quantity"] == 100:
                        screen.blit(qty_text, (x + 38, y + 44))
                    elif display_item["quantity"] > 9:
                        screen.blit(qty_text, (x + 42, y + 44))
                    else:
                        screen.blit(qty_text, (x + 47, y + 44))

                if pygame.Rect(x, y, self.slot_size, self.slot_size).collidepoint(mouse_pos):
                    self.inventory.register_hover_candidate(
                        ("smelter_fuel", i),
                        display_item["item_name"],
                        (x, y, self.slot_size, self.slot_size),
                        slot_data=display_item
                    )
        
        if self.dragging and self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            item = self.dragged_item
            for catalog_item in items_list:
                if catalog_item["item_name"] == item["item_name"]:
                    image_to_draw = catalog_item.get("image_hotbar") if self.dragged_from_type == "hotbar" and catalog_item.get("image_hotbar") else catalog_item["image"]
                    screen.blit(image_to_draw, (mouse_pos[0] - image_to_draw.get_width() // 2, mouse_pos[1] - image_to_draw.get_height() // 2))
                    break
    
    def _render_inventory(self, screen, start_x, start_y):
        columns = self.inventory.columns
        font = pygame.font.SysFont(None, 20)
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.capacity):
            row = slot_index // columns
            col = slot_index % columns
            x = start_x + col * (self.slot_size + self.gap_size)
            y = start_y + row * (self.slot_size + self.gap_size - 3)

            if self.inventory.inventory_list[slot_index] is not None:
                item = self.inventory.inventory_list[slot_index]
                for catalog_item in items_list:
                    if catalog_item["item_name"] == item["item_name"]:
                        screen.blit(catalog_item["image"], (x, y))

                        quantity = item["quantity"]
                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        if pygame.Rect(x, y, self.slot_size, self.slot_size).collidepoint(mouse_pos):
                            self.inventory.register_hover_candidate(
                                ("smelter_inventory", slot_index),
                                item["item_name"],
                                (x, y, self.slot_size, self.slot_size),
                                slot_data=item
                            )
                        break
