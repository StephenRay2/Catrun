import pygame

from crafting_bench import CraftingBench
from inventory import hotbar_image, items_list
from buttons import Button
from world import width, height


class ArcaneCrafter(CraftingBench):
    def __init__(self, inventory_obj):
        super().__init__(inventory_obj)

        # Use arcane crafting background for the crafting screen
        self.workbench_screen_image = None
        try:
            self.workbench_screen_image = pygame.image.load(
                "assets/sprites/buttons/arcane_crafting_screen.png"
            ).convert_alpha()
            self.workbench_screen_image = pygame.transform.scale(
                self.workbench_screen_image, (1100, 600)
            )
        except Exception:
            self.workbench_screen_image = None

        # Enchanting screen background
        self.enchanting_screen_image = None
        try:
            self.enchanting_screen_image = pygame.image.load(
                "assets/sprites/buttons/enchanting_screen.png"
            ).convert_alpha()
            # Slightly wider and a bit taller than the crafting screen
            self.enchanting_screen_image = pygame.transform.scale(
                self.enchanting_screen_image, (1119, 600)
            )
        except Exception:
            self.enchanting_screen_image = None

        # Tabs for crafting / enchanting
        tab_size = (134, 44)
        self.arcane_crafting_tab_image = None
        self.arcane_crafting_tab_unused_image = None
        self.arcane_enchanting_tab_image = None
        self.arcane_enchanting_tab_unused_image = None

        try:
            img = pygame.image.load(
                "assets/sprites/buttons/arcane_crafting_tab.png"
            ).convert_alpha()
            self.arcane_crafting_tab_image = pygame.transform.scale(img, tab_size)
        except Exception:
            self.arcane_crafting_tab_image = None

        try:
            img = pygame.image.load(
                "assets/sprites/buttons/arcane_crafting_tab_unused.png"
            ).convert_alpha()
            self.arcane_crafting_tab_unused_image = pygame.transform.scale(img, tab_size)
        except Exception:
            self.arcane_crafting_tab_unused_image = None

        enchanting_paths = [
            "assets/sprites/buttons/arcane_enchanting_tab.png",
        ]
        self.arcane_enchanting_tab_image = None
        for path in enchanting_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
                self.arcane_enchanting_tab_image = pygame.transform.scale(img, tab_size)
                break
            except Exception:
                continue

        try:
            img = pygame.image.load(
                "assets/sprites/buttons/arcane_enchanting_tab_unused.png"
            ).convert_alpha()
            self.arcane_enchanting_tab_unused_image = pygame.transform.scale(img, tab_size)
        except Exception:
            self.arcane_enchanting_tab_unused_image = None

        # Enchant button
        self.enchant_button_image = None
        try:
            img = pygame.image.load(
                "assets/sprites/buttons/enchant_button.png"
            ).convert_alpha()
            self.enchant_button_image = img
        except Exception:
            self.enchant_button_image = None

        # Tab buttons (positions mirror the inventory/crafting tabs)
        crafting_tab_x = width // 2 - 533
        crafting_tab_y = height // 2 - 303
        enchanting_tab_x = crafting_tab_x + tab_size[0]

        self.crafting_tab_active_button = (
            Button(crafting_tab_x, crafting_tab_y, self.arcane_crafting_tab_image)
            if self.arcane_crafting_tab_image
            else None
        )
        self.crafting_tab_inactive_button = (
            Button(crafting_tab_x, crafting_tab_y, self.arcane_crafting_tab_unused_image)
            if self.arcane_crafting_tab_unused_image
            else None
        )
        self.enchanting_tab_active_button = (
            Button(enchanting_tab_x, crafting_tab_y, self.arcane_enchanting_tab_image)
            if self.arcane_enchanting_tab_image
            else None
        )
        self.enchanting_tab_inactive_button = (
            Button(
                enchanting_tab_x,
                crafting_tab_y,
                self.arcane_enchanting_tab_unused_image,
            )
            if self.arcane_enchanting_tab_unused_image
            else None
        )

        # Current screen mode: "crafting" (like workbench) or "enchanting"
        self.mode = "crafting"

        # Simple placeholders for enchanting slots (no logic yet)
        self.enchant_input_rect = None
        self.enchant_catalyst_rect = None
        self.enchant_output_rect = None
        self.enchant_button_rect = None

        # Enchanting slot data
        self.enchant_input_slot = None
        self.enchant_catalyst_slot = None
        self.enchant_output_slot = None

        # Arcane crafter recipes only
        self.recipes = self._load_arcane_recipes()

    def _load_arcane_recipes(self):
        recipes = []
        seen = set()
        for item in items_list:
            medium = item.get("crafting_medium")
            if medium == "arcane_crafter" and item.get("recipe"):
                item_name = item["item_name"]
                if item_name not in seen:
                    recipes.append(item)
                    seen.add(item_name)
        return recipes

    def handle_mouse_click(self, mouse_pos, button, screen):
        if not self.active:
            return

        # Tab switching first
        if button == 1:
            if self.mode == "crafting":
                if (
                    self.enchanting_tab_inactive_button
                    and self.enchanting_tab_inactive_button.rect.collidepoint(mouse_pos)
                ):
                    self.mode = "enchanting"
                    return
            else:
                if (
                    self.crafting_tab_inactive_button
                    and self.crafting_tab_inactive_button.rect.collidepoint(mouse_pos)
                ):
                    self.mode = "crafting"
                    return

        # Crafting screen behaves like the workbench
        if self.mode == "crafting":
            super().handle_mouse_click(mouse_pos, button, screen)
            return

        # Enchanting screen: for now, just UI, no special behavior
        return

    def draw(self, screen):
        if not self.active:
            return

        width_local = screen.get_width()
        height_local = screen.get_height()

        overlay = pygame.Surface((width_local, height_local), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        if self.mode == "crafting":
            self._draw_crafting_screen(screen)
        else:
            self._draw_enchanting_screen(screen)

    def _draw_crafting_screen(self, screen):
        width_local = screen.get_width()
        height_local = screen.get_height()

        x_pos = width_local / 2 - self.workbench_screen_image.get_width() / 2
        y_pos = height_local / 2 - self.workbench_screen_image.get_height() / 2

        if self.workbench_screen_image:
            screen.blit(self.workbench_screen_image, (x_pos, y_pos - 20))

        # Reuse workbench rendering for inventory/recipes/hotbar
        self._draw_inventory_items(screen, x_pos, y_pos)
        self._draw_recipe_preview(screen, x_pos, y_pos)
        self._draw_recipe_grid(screen, x_pos, y_pos)
        self._draw_recipe_description(screen, x_pos, y_pos)

        self._draw_hotbar_background(screen)
        self._draw_hotbar_items(screen)
        self._draw_arcane_tabs(screen)

        if self.dragging and self.dragged_item:
            self._draw_dragged_item(screen)

    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos

        # Crafting mode: mirror workbench behavior (inventory/hotbar)
        if self.mode == "crafting":
            slot_index, is_hotbar = super().get_slot_at_mouse(mouse_pos, screen)
            if slot_index is None:
                return (None, None)
            return (slot_index, "hotbar" if is_hotbar else "inventory")

        # Enchanting mode
        width_local = screen.get_width()
        height_local = screen.get_height()

        # Inventory grid (4x16) – must match _draw_enchanting_inventory
        columns = 16
        rows = 4
        slot_size = 64
        gap_size = 4

        total_width = columns * slot_size + (columns - 1) * gap_size
        layout_center_y = height_local / 2
        layout_rect = pygame.Rect(
            width_local // 2 - 558, int(layout_center_y - 302), 1116, 605
        )

        start_x = layout_rect.centerx - total_width // 2
        start_y = layout_rect.bottom - (rows * slot_size + (rows - 1) * gap_size) - 30

        for slot_index in range(self.inventory.capacity):
            row = slot_index // columns
            col = slot_index % columns
            if row >= rows:
                break
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * (slot_size + gap_size - 3)
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, "inventory")

        # Hotbar region – mirror _draw_hotbar_background/_draw_hotbar_items
        hotbar_x = width_local // 2 - hotbar_image.get_width() // 2
        hotbar_y = height_local - 70
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

        # Enchanting slots
        slot_mapping = [
            ("input", self.enchant_input_rect),
            ("catalyst", self.enchant_catalyst_rect),
            ("output", self.enchant_output_rect),
        ]
        for slot_type, rect in slot_mapping:
            if rect is not None and rect.collidepoint(mouse_pos):
                return (0, slot_type)

        return (None, None)

    def start_drag(self, slot_info):
        if self.mode == "crafting":
            slot_index, slot_type = slot_info
            is_hotbar = slot_type == "hotbar"
            super().start_drag(slot_index, is_hotbar)
            return

        # Enchanting mode – similar to smelter/campfire
        now = pygame.time.get_ticks()
        if self.dragging:
            return
        if now - getattr(self, "last_drag_time", 0) < getattr(self, "drag_cooldown", 120):
            return
        self.last_drag_time = now

        slot_index, slot_type = slot_info

        # Keep selection state in sync for inventory / hotbar so outlines render.
        if slot_type == "inventory":
            self._select_slot(slot_index, is_hotbar=False)
            source_container = self.inventory.inventory_list
        elif slot_type == "hotbar":
            self._select_slot(slot_index, is_hotbar=True)
            source_container = self.inventory.hotbar_slots
        elif slot_type == "input":
            source_container = [self.enchant_input_slot]
        elif slot_type == "catalyst":
            source_container = [self.enchant_catalyst_slot]
        elif slot_type == "output":
            source_container = [self.enchant_output_slot]
        else:
            return

        slot = source_container[0] if slot_type in ["input", "catalyst", "output"] else source_container[slot_index]

        if slot is None:
            return

        self.dragging = True
        self.dragged_item = slot.copy()
        self.dragged_from_slot = slot_index
        self.dragged_from_type = slot_type
        self.dragged_source_container = source_container

        if slot_type in ["input", "catalyst", "output"]:
            if slot_type == "input":
                self.enchant_input_slot = None
            elif slot_type == "catalyst":
                self.enchant_catalyst_slot = None
            else:
                self.enchant_output_slot = None
        else:
            source_container[slot_index] = None

    def end_drag(self, slot_info):
        if self.mode == "crafting":
            slot_index, slot_type = slot_info
            is_hotbar = slot_type == "hotbar"
            super().end_drag(slot_index, is_hotbar)
            return

        if not self.dragging:
            return

        slot_index, slot_type = slot_info
        source_container = getattr(self, "dragged_source_container", None)

        def restore_source(item):
            if source_container is None:
                return
            if self.dragged_from_type in ["input", "catalyst", "output"]:
                if self.dragged_from_type == "input":
                    self.enchant_input_slot = item
                elif self.dragged_from_type == "catalyst":
                    self.enchant_catalyst_slot = item
                else:
                    self.enchant_output_slot = item
            elif self.dragged_from_type in ["inventory", "hotbar"]:
                source_container[self.dragged_from_slot] = item

        def finish():
            self.dragging = False
            self.dragged_item = None
            self.dragged_from_slot = None
            self.dragged_from_type = None
            self.dragged_source_container = None

        # Inventory / hotbar targets
        if slot_type in ["inventory", "hotbar"]:
            target_container = self.inventory.hotbar_slots if slot_type == "hotbar" else self.inventory.inventory_list
            target_slot = target_container[slot_index]

            if target_slot is None:
                target_container[slot_index] = self.dragged_item
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
                    restore_source(self.dragged_item)
            else:
                target_container[slot_index] = self.dragged_item
                restore_source(target_slot)

            finish()
            return

        # Enchanting slots targets
        if slot_type in ["input", "catalyst", "output"]:
            if slot_type == "input":
                target_slot = self.enchant_input_slot
            elif slot_type == "catalyst":
                target_slot = self.enchant_catalyst_slot
            else:
                target_slot = self.enchant_output_slot

            if target_slot is None:
                new_slot = self.dragged_item
                if slot_type == "input":
                    self.enchant_input_slot = new_slot
                elif slot_type == "catalyst":
                    self.enchant_catalyst_slot = new_slot
                else:
                    self.enchant_output_slot = new_slot
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
                    restore_source(self.dragged_item)
            else:
                old_target = target_slot
                if slot_type == "input":
                    self.enchant_input_slot = self.dragged_item
                elif slot_type == "catalyst":
                    self.enchant_catalyst_slot = self.dragged_item
                else:
                    self.enchant_output_slot = self.dragged_item
                restore_source(old_target)

            finish()
            return

        # Fallback – restore to source
        restore_source(self.dragged_item)
        finish()

    def cancel_drag(self):
        if self.mode == "crafting":
            super().cancel_drag()
            return

        if not self.dragging:
            return
        source_container = getattr(self, "dragged_source_container", None)
        if source_container is not None:
            if self.dragged_from_type == "input":
                self.enchant_input_slot = self.dragged_item
            elif self.dragged_from_type == "catalyst":
                self.enchant_catalyst_slot = self.dragged_item
            elif self.dragged_from_type == "output":
                self.enchant_output_slot = self.dragged_item
            elif self.dragged_from_type in ["inventory", "hotbar"]:
                source_container[self.dragged_from_slot] = self.dragged_item

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
        self.dragged_source_container = None

    def open_drop_menu(self, slot_index, slot_type, mouse_pos):
        # Crafting mode uses workbench inventory/hotbar drop menu
        if self.mode == "crafting":
            is_hotbar = slot_type == "hotbar"
            return super().open_drop_menu(slot_index, is_hotbar, mouse_pos)

        # Enchanting mode: only special menu for enchant slots
        if slot_type == "input":
            slot = self.enchant_input_slot
        elif slot_type == "catalyst":
            slot = self.enchant_catalyst_slot
        elif slot_type == "output":
            slot = self.enchant_output_slot
        else:
            return False

        if slot is None or slot.get("quantity", 0) <= 0:
            return False

        self.inventory.open_special_menu_drop(slot, "arcane_crafter", mouse_pos)
        return True

        if self.crafting_amount_menu is not None:
            self._draw_craft_menu(screen)

    def _draw_enchanting_screen(self, screen):
        width_local = screen.get_width()
        height_local = screen.get_height()

        bg_x = width_local / 2 - 4
        # Layout rect stays centered; draw rect is shifted up so only the image moves.
        layout_center_y = height_local / 2
        # Move about 5 pixels higher than before
        draw_center_y = layout_center_y - 20

        if self.enchanting_screen_image:
            layout_rect = self.enchanting_screen_image.get_rect(
                center=(bg_x, layout_center_y)
            )
            draw_rect = self.enchanting_screen_image.get_rect(
                center=(bg_x, draw_center_y)
            )
            screen.blit(self.enchanting_screen_image, draw_rect.topleft)
        else:
            layout_rect = pygame.Rect(
                width_local // 2 - 550, height_local // 2 - 300, 1100, 605
            )
            draw_rect = layout_rect.move(0, -30)
            pygame.draw.rect(screen, (30, 30, 60), draw_rect)

        # Inventory at the bottom: 4 rows of 16 (based on layout_rect, so it stays put)
        self._draw_enchanting_inventory(screen, layout_rect)

        # Enchanting slots and button in the upper half of the screen (based on layout_rect)
        self._draw_enchanting_slots_and_button(screen, layout_rect)

        # Hotbar overlay at the bottom like other UIs
        self._draw_hotbar_background(screen)
        self._draw_hotbar_items(screen)
        self._draw_arcane_tabs(screen)

        if self.dragging and self.dragged_item:
            self._draw_dragged_item(screen)

    def _draw_arcane_tabs(self, screen):
        if self.mode == "crafting":
            if self.crafting_tab_active_button:
                self.crafting_tab_active_button.draw(screen)
            if self.enchanting_tab_inactive_button:
                self.enchanting_tab_inactive_button.draw(screen)
        else:
            if self.crafting_tab_inactive_button:
                self.crafting_tab_inactive_button.draw(screen)
            if self.enchanting_tab_active_button:
                self.enchanting_tab_active_button.draw(screen)

    def _draw_enchanting_inventory(self, screen, bg_rect):
        # Inventory at bottom, 4 rows x 16 columns
        columns = 16
        rows = 4
        slot_size = 64
        gap_size = 4

        total_width = columns * slot_size + (columns - 1) * gap_size
        start_x = bg_rect.centerx - total_width // 2
        # Move grid down by 7px
        start_y = bg_rect.bottom - (rows * slot_size + (rows - 1) * gap_size) - 30

        font = pygame.font.SysFont(None, 20)
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.capacity):
            slot = self.inventory.inventory_list[slot_index]

            row = slot_index // columns
            col = slot_index % columns
            if row >= rows:
                break

            x = start_x + col * (slot_size + gap_size)
            # Match vertical spacing used in the crafting screen inventory
            y = start_y + row * (slot_size + gap_size - 3)

            pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            is_selected = (
                self.inventory.selection_mode == "inventory"
                and self.inventory.selected_inventory_slot == slot_index
            )
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
                                ("arcane_enchant_inventory", slot_index),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot,
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

    def _draw_enchanting_slots_and_button(self, screen, bg_rect):
        # Layout: input slot on the left upper half, catalyst underneath, output on the right
        slot_size = 72
        # Make vertical gap between input and catalyst much smaller
        gap_y = 6

        center_y = bg_rect.top + bg_rect.height // 3

        # Shift left group (input/catalyst) 150px to the right
        input_x = bg_rect.left + 380
        input_y = center_y - slot_size - 5

        catalyst_x = input_x
        catalyst_y = input_y + slot_size + gap_y

        # Move output slot 150px to the left
        output_x = bg_rect.right - slot_size - 390
        output_y = center_y - slot_size + 30

        self.enchant_input_rect = pygame.Rect(input_x, input_y, slot_size, slot_size)
        self.enchant_catalyst_rect = pygame.Rect(
            catalyst_x, catalyst_y, slot_size, slot_size
        )
        self.enchant_output_rect = pygame.Rect(output_x, output_y, slot_size, slot_size)

        for rect in [
            self.enchant_input_rect,
            self.enchant_catalyst_rect,
            self.enchant_output_rect,
        ]:
            pygame.draw.rect(screen, (80, 80, 80), rect)
            pygame.draw.rect(screen, (200, 200, 220), rect, 3)

        # Draw items in enchant slots (no mechanics yet)
        font = pygame.font.SysFont(None, 20)
        mouse_pos = pygame.mouse.get_pos()

        slot_mapping = [
            ("input", self.enchant_input_slot, self.enchant_input_rect),
            ("catalyst", self.enchant_catalyst_slot, self.enchant_catalyst_rect),
            ("output", self.enchant_output_slot, self.enchant_output_rect),
        ]

        for slot_type, slot_data, rect in slot_mapping:
            if slot_data is None:
                continue
            item_name = slot_data["item_name"]
            quantity = slot_data.get("quantity", 1)

            for item in items_list:
                if item["item_name"] == item_name:
                    screen.blit(item["image"], (rect.x, rect.y))
                    if rect.collidepoint(mouse_pos):
                        self.inventory.register_hover_candidate(
                            (f"arcane_{slot_type}_slot", 0),
                            item_name,
                            (rect.x, rect.y, rect.width, rect.height),
                            slot_data=slot_data,
                        )
                    if quantity > 1:
                        stack_text = font.render(str(quantity), True, (255, 255, 255))
                        screen.blit(stack_text, (rect.x + rect.width - 22, rect.y + rect.height - 20))
                    break

        # Enchant button between catalyst and output
        if self.enchant_button_image:
            button_rect = self.enchant_button_image.get_rect()
            button_rect.centerx = (self.enchant_catalyst_rect.right + self.enchant_output_rect.left) // 2
            button_rect.centery = self.enchant_catalyst_rect.centery
            screen.blit(self.enchant_button_image, button_rect.topleft)
            self.enchant_button_rect = button_rect
        else:
            button_width = 160
            button_height = 50
            x = (self.enchant_catalyst_rect.right + self.enchant_output_rect.left) // 2 - button_width // 2
            y = self.enchant_catalyst_rect.centery - button_height // 2
            self.enchant_button_rect = pygame.Rect(x, y, button_width, button_height)
            pygame.draw.rect(screen, (60, 120, 200), self.enchant_button_rect)
            pygame.draw.rect(screen, (220, 240, 255), self.enchant_button_rect, 2)
