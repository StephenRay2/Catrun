import pygame

from inventory import items_list, hotbar_image
from buttons import inventory_tab
from debug import font_path


class ChestUI:
    """Simple storage UI for chests; mirrors workbench drag/drop behavior."""

    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.active = False
        self.chest_slots = [None] * 36
        self.chest_structure = None

        self.chest_screen_image = None
        try:
            self.chest_screen_image = pygame.image.load(
                "assets/sprites/buttons/chest_inventory_screen.png"
            ).convert_alpha()
            self.chest_screen_image = pygame.transform.scale(self.chest_screen_image, (1100, 600))
        except Exception:
            self.chest_screen_image = None

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None

        self.font_small = pygame.font.Font(font_path, 14)
        self.font_medium = pygame.font.Font(font_path, 18)

        self.slot_size = 64
        self.gap_size = 4
        self.player_columns = 8
        self.chest_columns = 6
        self.row_step = self.slot_size + self.gap_size - 3

    def open(self, chest_structure):
        self.active = True
        self.chest_structure = chest_structure
        # Ensure this chest has a storage payload
        if chest_structure.get("storage") is None:
            chest_structure["storage"] = [None] * 36
        elif len(chest_structure["storage"]) != 36:
            # Preserve existing contents as much as possible, clamp to new size
            trimmed = chest_structure["storage"][:36]
            while len(trimmed) < 36:
                trimmed.append(None)
            chest_structure["storage"] = trimmed
        # Keep a direct reference so we mutate in-place
        self.chest_slots = chest_structure["storage"]
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None

    def close(self):
        self.active = False
        self.cancel_drag()
        self.chest_structure = None
        self.inventory.close_drop_menu()

    def _slot_list_for_type(self, slot_type):
        if slot_type == "inventory":
            return self.inventory.inventory_list
        if slot_type == "hotbar":
            return self.inventory.hotbar_slots
        if slot_type == "chest":
            return self.chest_slots
        return None

    def start_drag(self, slot_index, slot_type):
        if slot_index is None or slot_type is None:
            return
        self.inventory.close_drop_menu()

        source_list = self._slot_list_for_type(slot_type)
        if source_list is None:
            return
        slot = source_list[slot_index]
        if slot is None:
            return

        self.dragging = True
        self.dragged_item = slot.copy()
        self.dragged_from_slot = slot_index
        self.dragged_from_type = slot_type
        source_list[slot_index] = None

        # Keep inventory selection in sync for player slots
        if slot_type == "hotbar":
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_hotbar_slot = slot_index
            self.inventory.selected_inventory_slot = None
        elif slot_type == "inventory":
            self.inventory.selection_mode = "inventory"
            self.inventory.selected_inventory_slot = slot_index

        self.inventory.recalc_weight()

    def end_drag(self, slot_index, slot_type):
        if not self.dragging or slot_index is None or slot_type is None:
            return

        target_list = self._slot_list_for_type(slot_type)
        if target_list is None:
            return

        target_slot = target_list[slot_index]
        new_selection_hotbar = None
        new_selection_inventory = None

        if target_slot is None:
            target_list[slot_index] = self.dragged_item
            if slot_type == "hotbar":
                new_selection_hotbar = slot_index
            elif slot_type == "inventory":
                new_selection_inventory = slot_index

        elif target_slot["item_name"] == self.dragged_item["item_name"]:
            max_stack = 100
            for item in items_list:
                if item["item_name"] == self.dragged_item["item_name"]:
                    max_stack = item.get("stack_size", 100)
                    break

            space_available = max_stack - target_slot["quantity"]
            amount_to_add = min(space_available, self.dragged_item["quantity"])

            target_slot["quantity"] += amount_to_add
            self.dragged_item["quantity"] -= amount_to_add

            if self.dragged_item["quantity"] > 0:
                source_list = self._slot_list_for_type(self.dragged_from_type)
                if source_list is not None and self.dragged_from_slot is not None:
                    source_list[self.dragged_from_slot] = self.dragged_item
            if slot_type == "hotbar":
                new_selection_hotbar = slot_index
            elif slot_type == "inventory":
                new_selection_inventory = slot_index

        else:
            target_list[slot_index] = self.dragged_item
            source_list = self._slot_list_for_type(self.dragged_from_type)
            if source_list is not None and self.dragged_from_slot is not None:
                source_list[self.dragged_from_slot] = target_slot
            if slot_type == "hotbar":
                new_selection_hotbar = slot_index
            elif slot_type == "inventory":
                new_selection_inventory = slot_index

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None

        if new_selection_hotbar is not None:
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_hotbar_slot = new_selection_hotbar
            self.inventory.selected_inventory_slot = None
        elif new_selection_inventory is not None:
            self.inventory.selection_mode = "inventory"
            self.inventory.selected_inventory_slot = new_selection_inventory

        self.inventory.recalc_weight()

    def cancel_drag(self):
        if not self.dragging:
            return

        source_list = self._slot_list_for_type(self.dragged_from_type)
        if source_list is not None and self.dragged_from_slot is not None:
            source_list[self.dragged_from_slot] = self.dragged_item

        if self.dragged_from_type == "hotbar":
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_hotbar_slot = self.dragged_from_slot
            self.inventory.selected_inventory_slot = None
        elif self.dragged_from_type == "inventory":
            self.inventory.selection_mode = "inventory"
            self.inventory.selected_inventory_slot = self.dragged_from_slot

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
        self.inventory.recalc_weight()

    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        if self.chest_screen_image:
            bg_x = screen.get_width() / 2 - self.chest_screen_image.get_width() / 2
            bg_y = screen.get_height() / 2 - self.chest_screen_image.get_height() / 2
        else:
            bg_x = screen.get_width() / 2 - 550
            bg_y = screen.get_height() / 2 - 300

        # Hotbar
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
                return (i, "hotbar")

        # Player inventory
        start_x = bg_x + 18
        start_y = bg_y + 44
        slot_size = self.slot_size
        gap_size = self.gap_size

        for slot_index in range(self.inventory.capacity):
            row = slot_index // self.player_columns
            col = slot_index % self.player_columns
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * self.row_step
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, "inventory")

        # Chest slots (offset down/right)
        chest_start_x = start_x + self.player_columns * (slot_size + gap_size) + 2 * (slot_size + gap_size) - 40
        chest_start_y = start_y + 2 * self.row_step - 7
        for slot_index in range(len(self.chest_slots)):
            row = slot_index // self.chest_columns
            col = slot_index % self.chest_columns
            x = chest_start_x + col * (slot_size + gap_size)
            y = chest_start_y + row * self.row_step
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, "chest")

        return (None, None)

    def open_drop_menu(self, slot_index, slot_type, mouse_pos):
        if slot_type not in ("hotbar", "inventory"):
            return False
        if slot_index is None:
            return False
        if slot_type == "hotbar":
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_hotbar_slot = slot_index
            self.inventory.selected_inventory_slot = None
        else:
            self.inventory.selection_mode = "inventory"
            self.inventory.selected_inventory_slot = slot_index
        return self.inventory.open_drop_menu(slot_index, slot_type == "hotbar", mouse_pos)

    def draw(self, screen):
        if not self.active:
            return

        width = screen.get_width()
        height = screen.get_height()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        if self.chest_screen_image:
            x_pos = width / 2 - self.chest_screen_image.get_width() / 2
            y_pos = height / 2 - self.chest_screen_image.get_height() / 2
            screen.blit(self.chest_screen_image, (x_pos, y_pos - 20))
        else:
            x_pos = width / 2 - 550
            y_pos = height / 2 - 300

        self._draw_inventory_items(screen, x_pos, y_pos)
        self._draw_chest_items(screen, x_pos, y_pos)
        self._draw_hotbar(screen)
        self._draw_inventory_tab(screen)

        if self.dragging and self.dragged_item:
            self._draw_dragged_item(screen)

    def _draw_inventory_items(self, screen, bg_x, bg_y):
        start_x = bg_x + 18
        start_y = bg_y + 44
        slot_size = self.slot_size
        gap_size = self.gap_size
        columns = self.player_columns
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.capacity):
            slot = self.inventory.inventory_list[slot_index]
            row = slot_index // columns
            col = slot_index % columns
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * self.row_step

            pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            is_selected = (
                self.inventory.selection_mode == "inventory"
                and self.inventory.selected_inventory_slot == slot_index
            )
            border_color = (255, 255, 120) if is_selected else (200, 200, 200)
            if self.dragging and slot_index == self.dragged_from_slot and self.dragged_from_type == "inventory":
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
                                ("chest_inventory", slot_index),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot,
                            )
                        if quantity > 1:
                            stack_text = self.font_medium.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        break

    def _draw_chest_items(self, screen, bg_x, bg_y):
        start_x = bg_x + 18
        start_y = bg_y + 44
        slot_size = self.slot_size
        gap_size = self.gap_size

        chest_start_x = start_x + self.player_columns * (slot_size + gap_size) + 2 * (slot_size + gap_size) - 40
        chest_start_y = start_y + 2 * self.row_step - 7
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(len(self.chest_slots)):
            slot = self.chest_slots[slot_index]
            row = slot_index // self.chest_columns
            col = slot_index % self.chest_columns
            x = chest_start_x + col * (slot_size + gap_size)
            y = chest_start_y + row * self.row_step

            pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            border_color = (200, 200, 200)
            if self.dragging and slot_index == self.dragged_from_slot and self.dragged_from_type == "chest":
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
                                ("chest_slot", slot_index),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot,
                            )
                        if quantity > 1:
                            stack_text = self.font_medium.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 38, y + 44))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 42, y + 44))
                            else:
                                screen.blit(stack_text, (x + 47, y + 44))
                        break

    def _draw_hotbar(self, screen):
        font = self.font_medium
        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        slot_size = 48
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(hotbar_image, (hotbar_x, hotbar_y))

        for i, slot in enumerate(self.inventory.hotbar_slots):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            is_selected = (
                self.inventory.selection_mode == "hotbar"
                and self.inventory.selected_hotbar_slot == i
            )
            border_color = (255, 255, 120) if is_selected else (200, 200, 200)
            if self.dragging and self.dragged_from_type == "hotbar" and self.dragged_from_slot == i:
                border_color = (150, 150, 150)
            pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            pygame.draw.rect(screen, border_color, (x, y, slot_size, slot_size), 2)

            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]
                for item in items_list:
                    if item["item_name"] == item_name:
                        screen.blit(item["image_hotbar"], (x + 7, y + 6))
                        if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                            self.inventory.register_hover_candidate(
                                ("chest_hotbar", i),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot,
                            )
                        if quantity > 1:
                            stack_text = font.render(str(quantity), True, (255, 255, 255))
                            if quantity == 100:
                                screen.blit(stack_text, (x + 25, y + 26))
                            elif quantity > 9:
                                screen.blit(stack_text, (x + 30, y + 26))
                            else:
                                screen.blit(stack_text, (x + 36, y + 26))
                        break

    def _draw_inventory_tab(self, screen):
        tab_x = screen.get_width() // 2 - 533
        tab_y = screen.get_height() // 2 - 303
        screen.blit(inventory_tab, (tab_x, tab_y))

    def _draw_dragged_item(self, screen):
        if not self.dragging or not self.dragged_item:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        item_image = None
        for item in items_list:
            if item["item_name"] == self.dragged_item["item_name"]:
                item_image = item["image"]
                break
        if item_image:
            screen.blit(item_image, (mouse_x - 32, mouse_y - 32))
