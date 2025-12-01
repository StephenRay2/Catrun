import pygame
from inventory import items_list, hotbar_image
from buttons import inventory_tab

class MortarPestle:
    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.active = False
        self.mortar_pestle_pos = None
        
        self.mortar_pestle_screen_image = None
        try:
            self.mortar_pestle_screen_image = pygame.image.load("assets/sprites/buttons/mortar_and_pestle_screen.png").convert_alpha()
            self.mortar_pestle_screen_image = pygame.transform.scale(self.mortar_pestle_screen_image, (1100, 600))
        except:
            self.mortar_pestle_screen_image = None
        
        self.recipes = self._load_mortar_pestle_recipes()
        
        self.scroll_offset = 0
        self.recipe_columns = 6
        self.recipe_slot_size = 64
        self.recipe_gap = 4
        self.recipe_rows_visible = 4
        
        self.selected_recipe = None
        self.double_click_recipe = None
        self.double_click_timer = 0
        self.double_click_threshold = 0.3
        
        self.crafting_amount_menu = None
        self.crafting_amount_menu_x = 0
        self.crafting_amount_menu_y = 0
        self.custom_craft_input = ""
        self.custom_craft_active = False
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        
        self.font_small = pygame.font.SysFont(None, 18)
        self.font_medium = pygame.font.SysFont(None, 22)
        self.font_large = pygame.font.SysFont(None, 28)
    
    def _load_mortar_pestle_recipes(self):
        recipes = []
        seen = set()
        for item in items_list:
            medium = item.get("crafting_medium")
            if medium == "mortar_and_pestle" and item.get("recipe"):
                item_name = item["item_name"]
                if item_name not in seen:
                    recipes.append(item)
                    seen.add(item_name)
        return recipes

    def _select_slot(self, slot_index, is_hotbar):
        """Keep inventory selection in sync while using the mortar pestle UI."""
        if slot_index is None:
            return
        if is_hotbar:
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_hotbar_slot = slot_index
            self.inventory.selected_inventory_slot = None
        else:
            self.inventory.selection_mode = "inventory"
            self.inventory.selected_inventory_slot = slot_index
    
    def _can_craft(self, recipe):
        required = recipe.get("recipe", [])
        for req in required:
            item_name = req.get("item")
            item_tag = req.get("item_tag")
            amount_needed = req.get("amount", 1)
            
            if item_name:
                total_amount = self.inventory.get_item_count(item_name)
            elif item_tag:
                total_amount = self.inventory.get_items_by_tag_count(item_tag)
            else:
                total_amount = 0
            
            if total_amount < amount_needed:
                return False
        return True
    
    def _subtract_ingredients(self, recipe):
        required = recipe.get("recipe", [])
        for req in required:
            item_name = req.get("item")
            item_tag = req.get("item_tag")
            amount_needed = req.get("amount", 1)
            
            if item_name:
                self.inventory.remove_item(item_name, amount_needed)
            elif item_tag:
                self.inventory.remove_items_by_tag(item_tag, amount_needed)
    
    def craft_item(self, recipe, amount=1):
        for _ in range(amount):
            if not self._can_craft(recipe):
                return False
            
            self._subtract_ingredients(recipe)
            
            output_item = next(item for item in items_list if item["item_name"] == recipe["item_name"])
            output_copy = output_item.copy()
            output_copy["quantity"] = recipe.get("output_amount", 1)
            
            if not self.inventory.add([output_item["item_name"] for _ in range(recipe.get("output_amount", 1))]):
                return False
        
        return True
    
    def start_drag(self, slot_index, is_hotbar):
        if slot_index is None:
            return
        self.inventory.close_drop_menu()
        self._select_slot(slot_index, is_hotbar)
        if is_hotbar:
            slot = self.inventory.hotbar_slots[slot_index]
        else:
            slot = self.inventory.inventory_list[slot_index]
        
        if slot is not None:
            self.dragging = True
            self.dragged_item = slot.copy()
            self.dragged_from_slot = slot_index
            self.dragged_from_hotbar = is_hotbar
            
            if is_hotbar:
                self.inventory.hotbar_slots[slot_index] = None
            else:
                self.inventory.inventory_list[slot_index] = None
            self.inventory.recalc_weight()
    
    def end_drag(self, slot_index, is_hotbar):
        if not self.dragging:
            return
        
        if is_hotbar:
            target_slot = self.inventory.hotbar_slots[slot_index]
        else:
            target_slot = self.inventory.inventory_list[slot_index]
        
        new_selection_hotbar = None
        new_selection_inventory = None

        if target_slot is None:
            if is_hotbar:
                self.inventory.hotbar_slots[slot_index] = self.dragged_item
                new_selection_hotbar = slot_index
            else:
                self.inventory.inventory_list[slot_index] = self.dragged_item
                new_selection_inventory = slot_index
        
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
                    self.inventory.hotbar_slots[self.dragged_from_slot] = self.dragged_item
                else:
                    self.inventory.inventory_list[self.dragged_from_slot] = self.dragged_item
            if is_hotbar:
                new_selection_hotbar = slot_index
            else:
                new_selection_inventory = slot_index
        
        else:
            if is_hotbar:
                self.inventory.hotbar_slots[slot_index] = self.dragged_item
                new_selection_hotbar = slot_index
            else:
                self.inventory.inventory_list[slot_index] = self.dragged_item
                new_selection_inventory = slot_index
            
            if self.dragged_from_hotbar:
                self.inventory.hotbar_slots[self.dragged_from_slot] = target_slot
            else:
                self.inventory.inventory_list[self.dragged_from_slot] = target_slot
        
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        if new_selection_hotbar is not None:
            self.inventory.selected_hotbar_slot = new_selection_hotbar
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_inventory_slot = None
        elif new_selection_inventory is not None:
            self.inventory.selected_inventory_slot = new_selection_inventory
            self.inventory.selection_mode = "inventory"
        self.inventory.recalc_weight()
    
    def cancel_drag(self):
        if not self.dragging:
            return
        
        if self.dragged_from_hotbar:
            self.inventory.hotbar_slots[self.dragged_from_slot] = self.dragged_item
        else:
            self.inventory.inventory_list[self.dragged_from_slot] = self.dragged_item
        
        if self.dragged_from_hotbar:
            self.inventory.selected_hotbar_slot = self.dragged_from_slot
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_inventory_slot = None
        else:
            self.inventory.selected_inventory_slot = self.dragged_from_slot
            self.inventory.selection_mode = "inventory"

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        self.inventory.recalc_weight()
    
    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        if self.mortar_pestle_screen_image:
            bg_x = screen.get_width() / 2 - self.mortar_pestle_screen_image.get_width() / 2
            bg_y = screen.get_height() / 2 - self.mortar_pestle_screen_image.get_height() / 2
        else:
            bg_x = screen.get_width() / 2 - 550
            bg_y = screen.get_height() / 2 - 300
        
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        slot_size = 48
        gap_size = 4
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        
        for i in range(self.inventory.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (i, True)
        
        start_x = bg_x + 18
        start_y = bg_y + 44
        columns = 8
        slot_size = 64
        gap_size = 4
        
        for slot_index in range(self.inventory.capacity):
            row = slot_index // columns
            col = slot_index % columns
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * (slot_size + gap_size - 3)
            
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, False)
        
        return (None, None)
    
    def open(self, mortar_pestle_pos):
        self.active = True
        self.mortar_pestle_pos = mortar_pestle_pos
        self.scroll_offset = 0
        self.selected_recipe = None
        self.double_click_recipe = None
    
    def close(self):
        self.active = False
        self.mortar_pestle_pos = None
        self.selected_recipe = None
        self.crafting_amount_menu = None
        self.inventory.close_drop_menu()
        self.cancel_drag()
    
    def open_drop_menu(self, slot_index, is_hotbar, mouse_pos):
        self._select_slot(slot_index, is_hotbar)
        return self.inventory.open_drop_menu(slot_index, is_hotbar, mouse_pos)
    
    def handle_mouse_click(self, mouse_pos, button, screen):
        if not self.active:
            return
        
        if self.custom_craft_active:
            if self.crafting_amount_menu is not None:
                if not self._is_in_craft_menu(mouse_pos):
                    self.custom_craft_active = False
                    self.custom_craft_input = ""
                    self.crafting_amount_menu = None
            return
        
        if self.crafting_amount_menu is not None:
            if self._is_in_craft_menu(mouse_pos):
                menu_option = self._get_craft_menu_option(mouse_pos)
                if menu_option == 1:
                    self.craft_item(self.recipes[self.crafting_amount_menu])
                    self.crafting_amount_menu = None
                elif menu_option == 2:
                    max_craftable = self._get_max_craftable(self.recipes[self.crafting_amount_menu])
                    self.craft_item(self.recipes[self.crafting_amount_menu], max_craftable)
                    self.crafting_amount_menu = None
                elif menu_option == 3:
                    self.custom_craft_active = True
                    self.custom_craft_input = ""
            else:
                self.crafting_amount_menu = None
            return
        
        slot_index, is_hotbar = self.get_slot_at_mouse(mouse_pos, screen)
        if slot_index is not None and button == 1:
            return
        
        recipe_idx = self._get_recipe_at_mouse(mouse_pos, screen)
        if recipe_idx is not None:
            if button == 1:
                current_time = pygame.time.get_ticks() / 1000.0
                
                if self.double_click_recipe == recipe_idx and current_time - self.double_click_timer < self.double_click_threshold:
                    self.craft_item(self.recipes[recipe_idx])
                    self.double_click_recipe = None
                else:
                    self.selected_recipe = recipe_idx
                    self.double_click_recipe = recipe_idx
                    self.double_click_timer = current_time
            elif button == 3:
                self.show_craft_menu(mouse_pos, recipe_idx)
    
    def handle_mouse_scroll(self, direction):
        if not self.active:
            return
        
        if self.custom_craft_active:
            return
        
        columns = 6
        total_rows = (len(self.recipes) + columns - 1) // columns
        max_scroll = max(0, total_rows - self.recipe_rows_visible)
        if direction > 0:
            self.scroll_offset = max(0, self.scroll_offset - 1)
        else:
            self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
    
    def handle_key_event(self, event):
        if not self.custom_craft_active or self.crafting_amount_menu is None:
            return
        
        if event.key == pygame.K_RETURN:
            if self.custom_craft_input:
                try:
                    amount = int(self.custom_craft_input)
                    max_craftable = self._get_max_craftable(self.recipes[self.crafting_amount_menu])
                    amount = min(amount, max_craftable)
                    amount = max(1, amount)
                    self.craft_item(self.recipes[self.crafting_amount_menu], amount)
                except ValueError:
                    pass
            self.custom_craft_active = False
            self.custom_craft_input = ""
            self.crafting_amount_menu = None
        elif event.key == pygame.K_BACKSPACE:
            self.custom_craft_input = self.custom_craft_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            self.custom_craft_active = False
            self.custom_craft_input = ""
            self.crafting_amount_menu = None
        elif event.unicode.isdigit():
            if len(self.custom_craft_input) < 5:
                self.custom_craft_input += event.unicode
    
    def show_craft_menu(self, mouse_pos, recipe_idx):
        self.crafting_amount_menu = recipe_idx
        self.crafting_amount_menu_x = mouse_pos[0]
        self.crafting_amount_menu_y = mouse_pos[1]
    
    def _get_recipe_at_mouse(self, mouse_pos, screen):
        if not self.active:
            return None
        
        if self.mortar_pestle_screen_image:
            bg_x = screen.get_width() / 2 - self.mortar_pestle_screen_image.get_width() / 2
            bg_y = screen.get_height() / 2 - self.mortar_pestle_screen_image.get_height() / 2
        else:
            bg_x = screen.get_width() / 2 - 550
            bg_y = screen.get_height() / 2 - 300
        recipe_start_x = bg_x + 18 + (8 * (64 + 4)) + 90
        recipe_start_y = bg_y + 290
        columns = 6
        
        rel_x = mouse_pos[0] - recipe_start_x
        rel_y = mouse_pos[1] - recipe_start_y
        
        if rel_x < 0 or rel_y < 0:
            return None
        
        col = int(rel_x // (self.recipe_slot_size + self.recipe_gap))
        row = int(rel_y // (self.recipe_slot_size + self.recipe_gap))
        
        if col >= columns or row >= self.recipe_rows_visible:
            return None
        
        recipe_idx = (self.scroll_offset + row) * columns + col
        
        if recipe_idx < len(self.recipes):
            return recipe_idx
        return None
    
    def _is_in_craft_menu(self, mouse_pos):
        if self.crafting_amount_menu is None:
            return False
        menu_x, menu_y = self._get_craft_menu_position()
        menu_width = 180
        menu_height = 110
        
        if menu_x <= mouse_pos[0] <= menu_x + menu_width and menu_y <= mouse_pos[1] <= menu_y + menu_height:
            return True
        
        if self.custom_craft_active:
            input_bg_y = menu_y - 35
            if menu_x <= mouse_pos[0] <= menu_x + menu_width and input_bg_y <= mouse_pos[1] <= input_bg_y + 30:
                return True
        
        return False
    
    def _get_craft_menu_position(self):
        menu_x = self.crafting_amount_menu_x + 45
        menu_y = self.crafting_amount_menu_y
        return (int(menu_x), int(menu_y))
    
    def _get_craft_menu_option(self, mouse_pos):
        menu_x, menu_y = self._get_craft_menu_position()
        relative_y = mouse_pos[1] - menu_y
        option_height = 30
        
        if relative_y < option_height:
            return 1
        elif relative_y < option_height * 2:
            return 2
        elif relative_y < option_height * 3:
            return 3
        return None
    
    def _get_max_craftable(self, recipe):
        max_amount = float('inf')
        required = recipe.get("recipe", [])
        
        for req in required:
            item_name = req.get("item")
            item_tag = req.get("item_tag")
            amount_needed = req.get("amount", 1)
            
            if item_name:
                total_amount = self.inventory.get_item_count(item_name)
            elif item_tag:
                total_amount = self.inventory.get_items_by_tag_count(item_tag)
            else:
                total_amount = 0
            
            if amount_needed > 0:
                max_amount = min(max_amount, total_amount // amount_needed)
        
        return max(1, int(max_amount)) if max_amount != float('inf') else 1
    
    def draw(self, screen):
        if not self.active:
            return
        
        width = screen.get_width()
        height = screen.get_height()
        
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        if self.mortar_pestle_screen_image:
            x_pos = width / 2 - self.mortar_pestle_screen_image.get_width() / 2
            y_pos = height / 2 - self.mortar_pestle_screen_image.get_height() / 2
            screen.blit(self.mortar_pestle_screen_image, (x_pos, y_pos - 20))
        else:
            x_pos = width / 2 - 550
            y_pos = height / 2 - 300
        
        self._draw_inventory_items(screen, x_pos, y_pos)
        self._draw_recipe_preview(screen, x_pos, y_pos)
        self._draw_recipe_grid(screen, x_pos, y_pos)
        self._draw_recipe_description(screen, x_pos, y_pos)
        
        self._draw_hotbar_background(screen)
        self._draw_hotbar_items(screen)
        self._draw_inventory_tab(screen)
        
        if self.dragging and self.dragged_item:
            self._draw_dragged_item(screen)
        
        if self.crafting_amount_menu is not None:
            self._draw_craft_menu(screen)
    
    def _draw_inventory_items(self, screen, bg_x, bg_y):
        start_x = bg_x + 18
        start_y = bg_y + 44
        slot_size = 64
        gap_size = 4
        columns = 8
        font = pygame.font.SysFont(None, 20)
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.capacity):
            slot = self.inventory.inventory_list[slot_index]

            row = slot_index // columns
            col = slot_index % columns
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * (slot_size + gap_size - 3)
            
            pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            is_selected = (self.inventory.selection_mode == "inventory" and self.inventory.selected_inventory_slot == slot_index)
            border_color = (255, 255, 120) if is_selected else (200, 200, 200)
            if self.dragging and slot_index == self.dragged_from_slot and not self.dragged_from_hotbar:
                border_color = (150, 150, 150)
            pygame.draw.rect(screen, border_color, (x, y, slot_size, slot_size), 2)
            
            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]

                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image"], (x, y))
                        if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                            self.inventory.register_hover_candidate(
                                ("mortar_pestle_inventory", slot_index),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot
                            )

                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        break
    
    def _draw_hotbar_background(self, screen):
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        screen.blit(hotbar_image, (hotbar_x, hotbar_y))
    
    def _draw_hotbar_items(self, screen):
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        slot_size = 48
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        font = pygame.font.SysFont(None, 18)
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.hotbar_size):
            slot = self.inventory.hotbar_slots[slot_index]

            x = first_slot_x + slot_index * slot_spacing
            y = slot_y

            is_selected = (self.inventory.selection_mode == "hotbar" and self.inventory.selected_hotbar_slot == slot_index)
            if is_selected:
                pygame.draw.rect(screen, (255, 255, 120), (x - 2, y - 2, slot_size + 4, slot_size + 4), 2)
            
            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]

                for item in items_list:
                    if item["item_name"] == item_name:
                        scaled_img = pygame.transform.scale(item["image"], (slot_size, slot_size))
                        screen.blit(scaled_img, (x, y))
                        if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                            self.inventory.register_hover_candidate(
                                ("mortar_pestle_hotbar", slot_index),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot
                            )

                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 28, y + 32))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 32, y + 32))
                            else:
                                screen.blit(stack_text, (x + 35, y + 32))
                        break
    
    def _draw_inventory_tab(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        screen.blit(inventory_tab, (width // 2 - 533, height // 2 - 303))
    
    def _draw_recipe_preview(self, screen, bg_x, bg_y):
        if self.selected_recipe is None or self.selected_recipe >= len(self.recipes):
            return
        
        recipe = self.recipes[self.selected_recipe]
        preview_x = bg_x + 18 + (8 * (64 + 4)) + 100
        preview_y = bg_y + 34
        
        pygame.draw.rect(screen, (80, 80, 80), (preview_x, preview_y, 80, 80))
        pygame.draw.rect(screen, (150, 150, 150), (preview_x, preview_y, 80, 80), 2)
        
        if "image" in recipe:
            scaled_img = pygame.transform.scale(recipe["image"], (76, 76))
            screen.blit(scaled_img, (preview_x + 2, preview_y + 2))
    
    def _draw_recipe_grid(self, screen, bg_x, bg_y):
        recipe_start_x = bg_x + 18 + (8 * (64 + 4)) + 90
        recipe_start_y = bg_y + 290
        slot_size = 64
        gap_size = 4
        columns = self.recipe_columns
        mouse_pos = pygame.mouse.get_pos()

        for i, recipe in enumerate(self.recipes[self.scroll_offset * columns:]):
            if i >= self.recipe_rows_visible * columns:
                break

            col = i % columns
            row = i // columns
            
            x = recipe_start_x + col * (slot_size + gap_size)
            y = recipe_start_y + row * (slot_size + gap_size - 3)
            
            recipe_idx = self.scroll_offset * columns + i
            
            if self._can_craft(recipe):
                pygame.draw.rect(screen, (100, 150, 100), (x, y, slot_size, slot_size))
            else:
                pygame.draw.rect(screen, (80, 80, 80), (x, y, slot_size, slot_size))
            
            pygame.draw.rect(screen, (150, 150, 150), (x, y, slot_size, slot_size), 2)
            
            if recipe_idx == self.selected_recipe:
                pygame.draw.rect(screen, (255, 255, 0), (x, y, slot_size, slot_size), 3)

            if "image" in recipe:
                scaled_img = pygame.transform.scale(recipe["image"], (60, 60))
                screen.blit(scaled_img, (x + 2, y + 2))

            if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                self.inventory.register_hover_candidate(
                    ("mortar_pestle_recipe", recipe_idx),
                    recipe.get("item_name", "Unknown"),
                    (x, y, slot_size, slot_size),
                    recipe=recipe.get("recipe")
                )

        total_rows = (len(self.recipes) + columns - 1) // columns
        max_scroll = max(0, total_rows - self.recipe_rows_visible)
        if total_rows > self.recipe_rows_visible:
            track_x = recipe_start_x + columns * (slot_size + gap_size) + 10
            track_y = recipe_start_y
            track_width = 10
            track_height = self.recipe_rows_visible * (slot_size + gap_size - 3)

            pygame.draw.rect(
                screen,
                (50, 50, 70),
                (track_x, track_y, track_width, track_height),
                border_radius=3,
            )

            visible_ratio = self.recipe_rows_visible / float(total_rows)
            thumb_height = max(20, int(track_height * visible_ratio))

            if max_scroll > 0:
                scroll_ratio = self.scroll_offset / float(max_scroll)
            else:
                scroll_ratio = 0.0

            thumb_y = track_y + int((track_height - thumb_height) * scroll_ratio)

            pygame.draw.rect(
                screen,
                (180, 180, 210),
                (track_x + 1, thumb_y, track_width - 2, thumb_height),
                border_radius=3,
            )
    
    def _draw_recipe_description(self, screen, bg_x, bg_y):
        if self.selected_recipe is None or self.selected_recipe >= len(self.recipes):
            return
        
        recipe = self.recipes[self.selected_recipe]
        desc_x = bg_x + 18 + (8 * (64 + 4)) + 200
        desc_y = bg_y + 44
        
        name_text = self.font_large.render(recipe["item_name"], True, (20, 20, 50))
        screen.blit(name_text, (desc_x, desc_y))
        
        desc_y += 40
        max_width = 200
        words = recipe.get("description", "").split()
        line = ""
        for word in words:
            test_line = line + word + " "
            test_width = self.font_small.size(test_line)[0]
            if test_width > max_width:
                if line:
                    desc_text = self.font_small.render(line, True, (0, 0, 0))
                    screen.blit(desc_text, (desc_x, desc_y))
                    desc_y += 18
                line = word + " "
            else:
                line = test_line
        if line:
            desc_text = self.font_small.render(line, True, (0, 0, 0))
            screen.blit(desc_text, (desc_x, desc_y))
            desc_y += 18
        
        desc_y += 15
        recipe_label = self.font_medium.render("Recipe:", True, (20, 20, 50))
        screen.blit(recipe_label, (desc_x, desc_y))
        
        desc_y += 30
        if recipe.get("recipe"):
            for requirement in recipe["recipe"]:
                if "item" in requirement:
                    item_name = requirement["item"]
                    amount = requirement["amount"]
                    have = self.inventory.get_item_count(item_name)
                elif "item_tag" in requirement:
                    item_name = requirement["item_tag"].replace("_", " ").title()
                    amount = requirement["amount"]
                    have = self.inventory.get_items_by_tag_count(requirement["item_tag"])
                else:
                    continue
                
                color = (50, 255, 50) if have >= amount else (255, 50, 50)
                req_text = self.font_small.render(f"{item_name}: {have}/{amount}", True, color)
                screen.blit(req_text, (desc_x, desc_y))
                desc_y += 22
    
    def _draw_dragged_item(self, screen):
        if self.dragged_item is None:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for item in items_list:
            if item["item_name"] == self.dragged_item["item_name"]:
                screen.blit(item["image"], (mouse_x - 32, mouse_y - 32))
                
                if self.dragged_item["quantity"] > 1:
                    font = pygame.font.SysFont(None, 20)
                    qty_text = font.render(str(self.dragged_item["quantity"]), True, (255, 255, 255))
                    screen.blit(qty_text, (mouse_x - 10, mouse_y - 5))
                break
    
    def _draw_craft_menu(self, screen):
        if self.crafting_amount_menu is None or self.crafting_amount_menu >= len(self.recipes):
            return
        
        recipe = self.recipes[self.crafting_amount_menu]
        menu_x, menu_y = self._get_craft_menu_position()
        menu_width = 180
        menu_height = 110
        option_height = 30
        
        pygame.draw.rect(screen, (40, 40, 60), (menu_x, menu_y, menu_width, menu_height), border_radius=5)
        pygame.draw.rect(screen, (200, 150, 100), (menu_x, menu_y, menu_width, menu_height), width=2, border_radius=5)
        
        max_craftable = self._get_max_craftable(recipe)
        option1_text = self.font_small.render("Craft 1", True, (255, 255, 200))
        option2_text = self.font_small.render(f"Craft All ({max_craftable})", True, (255, 255, 200))
        option3_text = self.font_small.render("Custom Amount", True, (255, 255, 200))
        
        pygame.draw.rect(screen, (50, 50, 80), (menu_x, menu_y, menu_width, option_height))
        pygame.draw.rect(screen, (80, 80, 120), (menu_x, menu_y + option_height, menu_width, option_height))
        pygame.draw.rect(screen, (60, 60, 100), (menu_x, menu_y + option_height * 2, menu_width, option_height))
        
        screen.blit(option1_text, (menu_x + 10, menu_y + 7))
        screen.blit(option2_text, (menu_x + 10, menu_y + option_height + 5))
        screen.blit(option3_text, (menu_x + 10, menu_y + option_height * 2 + 7))
        
        if self.custom_craft_active:
            input_bg_x = menu_x
            input_bg_y = menu_y - 35
            pygame.draw.rect(screen, (40, 40, 60), (input_bg_x, input_bg_y, menu_width, 30), border_radius=5)
            pygame.draw.rect(screen, (200, 150, 100), (input_bg_x, input_bg_y, menu_width, 30), width=2, border_radius=5)
            
            input_text = self.font_small.render(f"Amount: {self.custom_craft_input}_", True, (255, 255, 200))
            screen.blit(input_text, (input_bg_x + 10, input_bg_y + 7))
