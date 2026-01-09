import pygame
import random

from inventory import items_list, hotbar_image
from buttons import inventory_tab
from debug import font_path
from ui_helpers import draw_close_button

_WEAPON_KEYWORDS = (
    "axe",
    "sword",
    "spear",
    "mace",
    "pickaxe",
    "shovel",
    "hoe",
    "club",
    "bow",
    "crossbow",
)

_EXCLUDE_LOOT_NAMES = {"Gold Coin", "Resurrection Coin"}


class EnemyInventoryUI:
    """Loot UI for dead enemy mobs."""

    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.active = False
        self.enemy_slots = []
        self.enemy = None

        self.enemy_screen_image = None
        try:
            self.enemy_screen_image = pygame.image.load(
                "assets/sprites/buttons/enemy_inventory.png"
            ).convert_alpha()
            self.enemy_screen_image = pygame.transform.scale(
                self.enemy_screen_image, (1100, 600)
            )
        except Exception:
            self.enemy_screen_image = None

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None

        self.font_small = pygame.font.Font(font_path, 14)
        self.font_medium = pygame.font.Font(font_path, 18)
        self.close_rect = None
        self.last_item_click_time = 0
        self.last_item_click_slot = None
        self.last_item_click_type = None
        self.double_click_threshold_ms = 300

        self.slot_size = 64
        self.gap_size = 4
        self.player_columns = self.inventory.columns
        self.enemy_columns = 6
        self.enemy_rows = self.inventory.rows
        self.row_step = self.slot_size + self.gap_size - 3
        self.panel_padding = 18

        self._loot_pools = None
        self.transfer_all_rect = None

    def open(self, enemy):
        if enemy is None:
            return False
        if not getattr(enemy, "is_humanoid", False):
            return False

        slots = getattr(enemy, "loot_inventory", None)
        if slots is None:
            slots = self._generate_loot(enemy)
            enemy.loot_inventory = slots

        slots = self._normalize_loot_slots(slots)
        enemy.loot_inventory = slots
        self.enemy_slots = slots
        self.enemy = enemy

        if not any(slot is not None for slot in self.enemy_slots):
            return False

        self.active = True
        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_type = None
        self.transfer_all_rect = None
        return True

    def close(self):
        self.active = False
        self.cancel_drag()
        self.enemy = None
        self.enemy_slots = []
        self.transfer_all_rect = None
        self.inventory.close_drop_menu()

    def _normalize_loot_slots(self, slots):
        slot_count = self.enemy_columns * self.enemy_rows
        if not isinstance(slots, list):
            slots = []
        slots = list(slots)
        if len(slots) < slot_count:
            slots.extend([None] * (slot_count - len(slots)))
        elif len(slots) > slot_count:
            slots = slots[:slot_count]
        return slots

    def _slot_list_for_type(self, slot_type):
        if slot_type == "inventory":
            return self.inventory.inventory_list
        if slot_type == "hotbar":
            return self.inventory.hotbar_slots
        if slot_type == "enemy":
            return self.enemy_slots
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

    def _get_layout(self, screen):
        if self.enemy_screen_image:
            bg_x = screen.get_width() / 2 - self.enemy_screen_image.get_width() / 2
            bg_y = screen.get_height() / 2 - self.enemy_screen_image.get_height() / 2
            panel_width = self.enemy_screen_image.get_width()
            panel_height = self.enemy_screen_image.get_height()
        else:
            bg_x = screen.get_width() / 2 - 550
            bg_y = screen.get_height() / 2 - 300
            panel_width = 1100
            panel_height = 600

        start_x = bg_x + self.panel_padding
        start_y = bg_y + 44
        enemy_grid_width = (
            self.enemy_columns * self.slot_size
            + (self.enemy_columns - 1) * self.gap_size
        )
        enemy_start_x = bg_x + panel_width - self.panel_padding - enemy_grid_width - 20
        enemy_start_y = start_y
        return (
            bg_x,
            bg_y,
            panel_width,
            panel_height,
            start_x,
            start_y,
            enemy_start_x,
            enemy_start_y,
        )

    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        (
            bg_x,
            bg_y,
            panel_width,
            panel_height,
            start_x,
            start_y,
            enemy_start_x,
            enemy_start_y,
        ) = self._get_layout(screen)

        hotbar_x = screen.get_width() // 2 - hotbar_image.get_width() // 2
        hotbar_y = screen.get_height() - 70
        slot_size = 48
        first_slot_x = hotbar_x + 4.5
        slot_y = hotbar_y + 4.5
        slot_spacing = 51

        for i in range(self.inventory.hotbar_size):
            x = first_slot_x + i * slot_spacing
            y = slot_y
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (i, "hotbar")

        slot_size = self.slot_size
        gap_size = self.gap_size

        for slot_index in range(self.inventory.capacity):
            row = slot_index // self.player_columns
            col = slot_index % self.player_columns
            x = start_x + col * (slot_size + gap_size)
            y = start_y + row * self.row_step
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, "inventory")

        for slot_index in range(len(self.enemy_slots)):
            row = slot_index // self.enemy_columns
            col = slot_index % self.enemy_columns
            if row >= self.enemy_rows:
                break
            x = enemy_start_x + col * (slot_size + gap_size)
            y = enemy_start_y + row * self.row_step
            if x <= mouse_x <= x + slot_size and y <= mouse_y <= y + slot_size:
                return (slot_index, "enemy")

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

    def handle_mouse_click(self, mouse_pos, button):
        if not self.active:
            return False
        if button == 1 and self.transfer_all_rect and self.transfer_all_rect.collidepoint(mouse_pos):
            self.inventory.close_drop_menu()
            self.transfer_all()
            return True
        return False

    def transfer_all(self):
        if self.dragging:
            self.cancel_drag()
        for idx in range(len(self.enemy_slots)):
            slot = self.enemy_slots[idx]
            if slot is None:
                continue
            self.inventory._move_stack_to_lists(
                self.enemy_slots,
                idx,
                [self.inventory.inventory_list, self.inventory.hotbar_slots],
            )

    def check_item_double_click(self, slot_index, slot_type):
        now = pygame.time.get_ticks()
        if (
            self.last_item_click_slot == slot_index
            and self.last_item_click_type == slot_type
            and (now - self.last_item_click_time) < self.double_click_threshold_ms
        ):
            self.last_item_click_slot = None
            self.last_item_click_type = None
            self.last_item_click_time = 0
            return True
        self.last_item_click_slot = slot_index
        self.last_item_click_type = slot_type
        self.last_item_click_time = now
        return False

    def handle_item_double_click(self, slot_index, slot_type):
        if slot_type == "enemy":
            return self.inventory._move_stack_to_lists(
                self.enemy_slots,
                slot_index,
                [self.inventory.inventory_list, self.inventory.hotbar_slots],
            )
        if slot_type == "inventory":
            return self.inventory._move_stack_to_lists(
                self.inventory.inventory_list,
                slot_index,
                [self.enemy_slots],
            )
        if slot_type == "hotbar":
            return self.inventory._move_stack_to_lists(
                self.inventory.hotbar_slots,
                slot_index,
                [self.enemy_slots],
            )
        return False

    def draw(self, screen):
        if not self.active:
            return

        width = screen.get_width()
        height = screen.get_height()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        (
            bg_x,
            bg_y,
            panel_width,
            panel_height,
            start_x,
            start_y,
            enemy_start_x,
            enemy_start_y,
        ) = self._get_layout(screen)

        if self.enemy_screen_image:
            screen.blit(self.enemy_screen_image, (bg_x, bg_y - 20))

        panel_rect = pygame.Rect(bg_x, bg_y - 20, panel_width, panel_height)
        self.close_rect = draw_close_button(screen, panel_rect)

        self._draw_inventory_items(screen, start_x, start_y)
        self._draw_enemy_items(screen, enemy_start_x, enemy_start_y)
        self._draw_transfer_all_button(screen, enemy_start_x, enemy_start_y)
        self._draw_hotbar(screen)
        self._draw_inventory_tab(screen)

        if self.dragging and self.dragged_item:
            self._draw_dragged_item(screen)

    def _draw_inventory_items(self, screen, start_x, start_y):
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
                                ("enemy_inventory_player", slot_index),
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

    def _draw_enemy_items(self, screen, enemy_start_x, enemy_start_y):
        slot_size = self.slot_size
        gap_size = self.gap_size
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(len(self.enemy_slots)):
            slot = self.enemy_slots[slot_index]
            row = slot_index // self.enemy_columns
            col = slot_index % self.enemy_columns
            if row >= self.enemy_rows:
                break
            x = enemy_start_x + col * (slot_size + gap_size)
            y = enemy_start_y + row * self.row_step

            pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            border_color = (200, 200, 200)
            if self.dragging and slot_index == self.dragged_from_slot and self.dragged_from_type == "enemy":
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
                                ("enemy_inventory_slot", slot_index),
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

    def _draw_transfer_all_button(self, screen, enemy_start_x, enemy_start_y):
        button_width = 140
        button_height = 26
        x = enemy_start_x
        y = enemy_start_y - button_height - 6
        if y < 10:
            y = 10
        self.transfer_all_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(screen, (70, 90, 120), self.transfer_all_rect, border_radius=6)
        pygame.draw.rect(screen, (200, 200, 220), self.transfer_all_rect, 1, border_radius=6)
        label = self.font_small.render("Transfer All", True, (235, 235, 235))
        screen.blit(
            label,
            (
                self.transfer_all_rect.centerx - label.get_width() // 2,
                self.transfer_all_rect.centery - label.get_height() // 2,
            ),
        )

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
                                ("enemy_inventory_hotbar", i),
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

    def _get_item_def(self, item_name):
        for item in items_list:
            if item["item_name"] == item_name:
                return item
        return None

    def _extract_equipped_items(self, enemy):
        def normalize(value):
            if value is None:
                return []
            if isinstance(value, str):
                return [value]
            if isinstance(value, dict):
                name = value.get("item_name")
                return [name] if name else []
            if isinstance(value, (list, tuple)):
                items = []
                for entry in value:
                    items.extend(normalize(entry))
                return items
            return []

        equipped = []
        for attr in ("weapon_name", "weapon", "weapon_item"):
            equipped.extend(normalize(getattr(enemy, attr, None)))
        for attr in ("armor_name", "armor", "armor_item", "armor_items", "equipped_armor"):
            equipped.extend(normalize(getattr(enemy, attr, None)))

        deduped = []
        seen = set()
        for name in equipped:
            if not name or name in seen:
                continue
            seen.add(name)
            deduped.append(name)
        return deduped

    def _build_loot_pools(self):
        pools = {
            "food": [],
            "material": [],
            "weapon": [],
            "armor": [],
            "key": [],
            "pet": [],
        }
        for item in items_list:
            name = item.get("item_name")
            if not name or name in _EXCLUDE_LOOT_NAMES:
                continue
            if item.get("placeable"):
                continue
            item_type = item.get("type", "")
            tags = [tag.lower() for tag in (item.get("tags") or [])]
            name_lower = name.lower()

            if item_type == "armor":
                pools["armor"].append(item)
            if (
                item_type in ("weapon", "tool")
                or "weapon" in tags
                or "tool" in tags
                or any(keyword in name_lower for keyword in _WEAPON_KEYWORDS)
            ):
                pools["weapon"].append(item)
            if "food" in tags:
                pools["food"].append(item)
            if item_type == "key" or "key" in tags:
                pools["key"].append(item)
            if "tamed_cat" in tags or item_type == "pet":
                pools["pet"].append(item)
            if (
                item_type in ("raw_material", "material", "gem")
                or "material" in tags
                or "gemstone" in tags
                or "arcane material" in tags
            ):
                pools["material"].append(item)

        return pools

    def _get_loot_pools(self):
        if self._loot_pools is None:
            self._loot_pools = self._build_loot_pools()
        return self._loot_pools

    def _generate_loot(self, enemy):
        slots = [None] * (self.enemy_columns * self.enemy_rows)

        def add_item(item_name, quantity=1):
            item_def = self._get_item_def(item_name)
            if not item_def:
                return False
            max_stack = item_def.get("stack_size", 100)
            remaining = int(quantity)
            if remaining <= 0:
                return False

            while remaining > 0:
                stacked = False
                for slot in slots:
                    if slot and slot.get("item_name") == item_name and slot.get("quantity", 0) < max_stack:
                        space = max_stack - slot.get("quantity", 0)
                        add_amount = min(space, remaining)
                        slot["quantity"] += add_amount
                        remaining -= add_amount
                        stacked = True
                        if remaining <= 0:
                            return True
                if stacked and remaining <= 0:
                    return True
                try:
                    empty_index = slots.index(None)
                except ValueError:
                    return False
                add_amount = min(max_stack, remaining)
                slots[empty_index] = self.inventory.create_item_instance(item_def, add_amount)
                remaining -= add_amount
            return True

        if getattr(enemy, "is_merchant", False):
            for listing in getattr(enemy, "shop_items", []) or []:
                item_name = listing.get("item_name")
                stock = int(listing.get("stock", 0) or 0)
                if item_name and stock > 0:
                    add_item(item_name, stock)
            gold_amount = int(getattr(enemy, "gold_coins", 0) or 0)
            if gold_amount > 0:
                add_item("Gold Coin", gold_amount)
            enemy.shop_items = []
            enemy.gold_coins = 0
            return slots

        for name in self._extract_equipped_items(enemy):
            add_item(name, 1)

        level = int(getattr(enemy, "level", 1) or 1)
        gold_amount = None
        for attr in ("gold_coins", "gold", "gold_amount", "coins"):
            value = getattr(enemy, attr, None)
            if isinstance(value, (int, float)) and value > 0:
                gold_amount = int(value)
                break
        if gold_amount is None:
            gold_amount = max(1, random.randint(1, 3) + level // 3)
        add_item("Gold Coin", gold_amount)

        extra_count = random.randint(1, 3)
        if level >= 20:
            extra_count += 1
        if level >= 40:
            extra_count += 1

        pools = self._get_loot_pools()
        categories = ["material", "food", "weapon", "armor", "key", "pet"]
        weights = [4, 3, 2, 1, 1, 0.2]
        qty_ranges = {
            "material": (2, 6),
            "food": (1, 3),
            "weapon": (1, 1),
            "armor": (1, 1),
            "key": (1, 1),
            "pet": (1, 1),
        }

        added = 0
        attempts = 0
        max_attempts = max(8, extra_count * 3)
        while added < extra_count and attempts < max_attempts:
            attempts += 1
            category = random.choices(categories, weights=weights, k=1)[0]
            pool = pools.get(category) or []
            if not pool:
                continue
            item_def = random.choice(pool)
            qty_min, qty_max = qty_ranges.get(category, (1, 1))
            qty = random.randint(qty_min, qty_max)
            if add_item(item_def["item_name"], qty):
                added += 1

        return slots
