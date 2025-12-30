import random
import pygame

from buttons import inventory_tab
from debug import font_path
from inventory import items_list, hotbar_image
from ui_helpers import draw_close_button

_ITEM_LOOKUP = {item["item_name"]: item for item in items_list if "item_name" in item}

_EXCLUDED_ITEMS = {"Gold Coin"}
_EXCLUDED_TYPES = {"structure", "special"}
_EXCLUDED_TAGS = {"pet", "tamed_cat"}

_MERCHANT_KINDS = {
    1: "provisioner",
    2: "materials",
    3: "gear",
}

_RARITY_BY_NAME = {
    "Alchemy Bench": 65,
    "Amethyst": 85,
    "Apple": 3,
    "Apple Wood": 10,
    "Aquamarine": 80,
    "Arcane Crafter": 70,
    "Arrow": 6,
    "Ash Lotus": 50,
    "Baked Apple": 8,
    "Ball Of Twine": 6,
    "Bird Egg": 12,
    "Blood Berries": 2,
    "Bola": 18,
    "Bone": 25,
    "Bone Axe": 40,
    "Bone Hoe": 40,
    "Bone Mace": 42,
    "Bone Pickaxe": 42,
    "Bone Powder": 22,
    "Bone Shovel": 40,
    "Bone Spear": 48,
    "Bone Sword": 46,
    "Buck Antlers": 20,
    "Cage Key": 40,
    "Campfire": 10,
    "Ceramic Pot": 28,
    "Ceramic Shard": 10,
    "Chain Bola": 35,
    "Chest": 15,
    "Chest Key": 35,
    "Chitin": 18,
    "Clay": 7,
    "Coconut": 8,
    "Cooked Bear Meat": 9,
    "Cooked Beef": 7,
    "Cooked Bird Meat": 6,
    "Cooked Fish": 5,
    "Cooked Reptile Meat": 5,
    "Cooked Small Meat": 3,
    "Cooked Venison": 5,
    "Cooking Pot": 15,
    "Dawn Berries": 2,
    "Dawnshroom": 5,
    "Diamond": 85,
    "Dusk Berries": 3,
    "Dusk Dragon Scale": 50,
    "Dusk Dragon Scale Axe": 95,
    "Dusk Dragon Scale Hoe": 82,
    "Dusk Dragon Scale Mace": 90,
    "Dusk Dragon Scale Pickaxe": 95,
    "Dusk Dragon Scale Shovel": 84,
    "Dusk Dragon Scale Spear": 96,
    "Dusk Dragon Scale Sword": 97,
    "Dusk Egg": 36,
    "Dusk Wood": 4,
    "Duskacean Claw": 30,
    "Duskshroom": 5,
    "Duskwretch Claws": 35,
    "Electric Dragon Scale": 50,
    "Electric Dragon Scale Axe": 95,
    "Electric Dragon Scale Hoe": 82,
    "Electric Dragon Scale Mace": 90,
    "Electric Dragon Scale Pickaxe": 95,
    "Electric Dragon Scale Shovel": 84,
    "Electric Dragon Scale Spear": 96,
    "Electric Dragon Scale Sword": 97,
    "Emerald": 78,
    "Empty Cage": 19,
    "Empty Oil Lamp": 14,
    "Fangs": 18,
    "Feather": 3,
    "Fence": 8,
    "Fiber": 1,
    "Filled Waterskin": 10,
    "Fir Wood": 3,
    "Fire Bomb": 40,
    "Fire Dragon Egg": 25,
    "Fire Dragon Scale": 50,
    "Fire Dragon Scale Axe": 95,
    "Fire Dragon Scale Hoe": 82,
    "Fire Dragon Scale Mace": 90,
    "Fire Dragon Scale Pickaxe": 95,
    "Fire Dragon Scale Shovel": 84,
    "Fire Dragon Scale Spear": 96,
    "Fire Dragon Scale Sword": 97,
    "Fire Fern Leaf": 35,
    "Fish": 3,
    "Fishing Pole": 12,
    "Flint": 3,
    "Flint And Steel": 18,
    "Flute": 20,
    "Frost Fern Leaf": 35,
    "Fur": 10,
    "Garnet": 75,
    "Glass": 10,
    "Glass Bottle": 20,
    "Goat Horn": 20,
    "Gold Axe": 38,
    "Gold Chain": 15,
    "Gold Hoe": 35,
    "Gold Mace": 35,
    "Gold Pickaxe": 35,
    "Gold Ring": 35,
    "Gold Shovel": 35,
    "Gold Spear": 37,
    "Gold Sword": 40,
    "Hide": 8,
    "Ice Bomb": 40,
    "Ice Dragon Scale": 50,
    "Ice Dragon Scale Axe": 95,
    "Ice Dragon Scale Hoe": 92,
    "Ice Dragon Scale Mace": 90,
    "Ice Dragon Scale Pickaxe": 95,
    "Ice Dragon Scale Shovel": 84,
    "Ice Dragon Scale Spear": 96,
    "Ice Dragon Scale Sword": 97,
    "Inferno Horn": 47,
    "Lantern": 20,
    "Large Gold Amulet": 70,
    "Large Metal Amulet": 70,
    "Large Metal Bright Brew": 35,
    "Large Metal Canteen": 25,
    "Large Metal Chill Brew": 35,
    "Large Metal Health Brew": 35,
    "Large Metal Heat Brew": 35,
    "Large Metal Milk": 27,
    "Large Metal Olive Oil": 27,
    "Large Metal Orange Juice": 27,
    "Large Metal Stamina Brew": 35,
    "Large Metal Water": 26,
    "Lavabucket": 25,
    "Leather Boots": 20,
    "Leather Chestplate": 25,
    "Leather Gloves": 20,
    "Leather Helmet": 22,
    "Leather Leggings": 25,
    "Lizard Egg": 10,
    "Marsh Reed": 8,
    "Medium Glass Bright Brew": 25,
    "Medium Glass Chill Brew": 25,
    "Medium Glass Health Brew": 25,
    "Medium Glass Heat Brew": 25,
    "Medium Glass Milk": 22,
    "Medium Glass Olive Oil": 22,
    "Medium Glass Orange Juice": 22,
    "Medium Glass Stamina Brew": 25,
    "Medium Glass Water": 21,
    "Medium Gold Amulet": 50,
    "Medium Metal Amulet": 50,
    "Metal Axe": 34,
    "Metal Bucket": 20,
    "Metal Chain": 15,
    "Metal Fishing Pole": 25,
    "Metal Floor": 15,
    "Metal Hoe": 30,
    "Metal Ingot": 10,
    "Metal Ladder": 20,
    "Metal Mace": 30,
    "Metal Nail": 2,
    "Metal Pickaxe": 30,
    "Metal Ring": 35,
    "Metal Rod": 20,
    "Metal Shovel": 25,
    "Metal Spear": 32,
    "Metal Stairs": 15,
    "Metal Sword": 31,
    "Milk Bucket": 22,
    "Monster Meat": 10,
    "Mortar And Pestle": 13,
    "Mushroom": 4,
    "Mushroom Stew": 9,
    "Oak Wood": 3,
    "Oak Wood Stairs": 10,
    "Oak Wood Wall": 10,
    "Obsidian Axe": 60,
    "Obsidian Hoe": 50,
    "Obsidian Mace": 62,
    "Obsidian Pickaxe": 64,
    "Obsidian Shard": 20,
    "Obsidian Shovel": 54,
    "Obsidian Spear": 65,
    "Obsidian Sword": 66,
    "Oil Lamp": 16,
    "Olive Wood": 4,
    "Olives": 3,
    "Opal": 75,
    "Orange": 4,
    "Orange Wood": 4,
    "Palm Wood": 4,
    "Pearl": 77,
    "Phoenix Feather": 47,
    "Pineapple": 7,
    "Pock Eye": 32,
    "Poison Dragon Scale": 50,
    "Poison Dragon Scale Axe": 95,
    "Poison Dragon Scale Hoe": 92,
    "Poison Dragon Scale Mace": 90,
    "Poison Dragon Scale Pickaxe": 95,
    "Poison Dragon Scale Shovel": 84,
    "Poison Dragon Scale Spear": 96,
    "Poison Dragon Scale Sword": 97,
    "Poisonous Mushroom": 8,
    "Raw Bear Meat": 4,
    "Raw Beef": 4,
    "Raw Bird Meat": 3,
    "Raw Metal": 8,
    "Raw Reptile Meat": 3,
    "Raw Venison": 4,
    "Redrock Stone": 3,
    "Resurrection Coin": 120,
    "Rope": 10,
    "Rope Ladder": 20,
    "Ruby": 80,
    "Salt": 7,
    "Sand": 5,
    "Sapphire": 78,
    "Sea Meat": 5,
    "Sealing Paste": 10,
    "Small Bright Brew": 15,
    "Small Chill Brew": 15,
    "Small Gold Amulet": 30,
    "Small Gold Ring": 27,
    "Small Health Brew": 15,
    "Small Heat Brew": 15,
    "Small Meat": 2,
    "Small Metal Amulet": 30,
    "Small Metal Ring": 27,
    "Small Milk": 6,
    "Small Olive Oil": 8,
    "Small Orange Juice": 6,
    "Small Stamina Brew": 15,
    "Small Water": 6,
    "Smelter": 20,
    "Snowball": 1,
    "Spiked Wooden Club": 12,
    "Stick": 1,
    "Stone": 1,
    "Stone Axe": 15,
    "Stone Floor": 13,
    "Stone Hoe": 11,
    "Stone Mace": 13,
    "Stone Pickaxe": 15,
    "Stone Shovel": 11,
    "Stone Spear": 16,
    "Stone Stairs": 13,
    "Stone Sword": 14,
    "Stone Wall": 13,
    "Sun Berries": 2,
    "Teal Berries": 2,
    "Tent": 20,
    "Throwing Knife": 16,
    "Throwing Star": 16,
    "Topaz": 80,
    "Torch": 10,
    "Travelers Cloak": 35,
    "Tusk": 25,
    "Twilight Drupes": 2,
    "Twine": 3,
    "Venom Sac": 20,
    "Vio Berries": 2,
    "Water Well": 35,
    "Waterbucket": 21,
    "Watermelon": 8,
    "Waterskin": 10,
    "Willow Wood": 4,
    "Wood Boat": 30,
    "Wood Bow": 15,
    "Wood Floor": 8,
    "Wood Ladder": 8,
    "Wooden Axe": 8,
    "Wooden Bowl": 4,
    "Wooden Club": 4,
    "Wooden Crossbow": 19,
    "Wooden Cup": 2,
    "Wooden Hoe": 5,
    "Wooden Mace": 8,
    "Wooden Pickaxe": 8,
    "Wooden Shovel": 6,
    "Wooden Spear": 9,
    "Wooden Sword": 8,
    "Workbench": 25,
}


def _is_sellable(item_def):
    if not item_def or "item_name" not in item_def:
        return False
    if item_def.get("item_name") in _EXCLUDED_ITEMS:
        return False
    if item_def.get("structure_type"):
        return False
    if item_def.get("type") in _EXCLUDED_TYPES:
        return False
    tags = item_def.get("tags") or []
    if any(tag in _EXCLUDED_TAGS for tag in tags):
        return False
    return True


def _matches_kind(item_def, kind):
    item_type = item_def.get("type", "")
    tags = item_def.get("tags") or []

    if kind == "provisioner":
        return item_type in ("consumable", "potion") or "food" in tags
    if kind == "materials":
        return (
            item_type in ("raw_material", "crafted_material")
            or "material" in tags
            or "ore" in tags
        )
    if kind == "gear":
        return (
            item_type in ("weapon", "tool", "armor", "equipment", "clothing")
            or any(tag in tags for tag in ("weapon", "tool", "armor"))
        )
    return True


def _compute_price(item_def):
    rarity_value = _get_rarity(item_def)
    if rarity_value <= 20:
        multiplier = random.uniform(0, 4)
    elif rarity_value <= 40:
        multiplier = random.uniform(4, 10)
    elif rarity_value <= 60:
        multiplier = random.uniform(10, 20)
    elif rarity_value <= 80:
        multiplier = random.uniform(16, 30)
    else:
        multiplier = random.uniform(24, 40)

    return max(1, int(round(rarity_value * multiplier)))


def _get_rarity(item_def):
    if not item_def:
        return 1.0
    item_name = item_def.get("item_name")
    rarity = item_def.get("rarity")
    if rarity is None:
        rarity = _RARITY_BY_NAME.get(item_name)
    if rarity is None:
        rarity = 1
    return float(rarity)


def _compute_stock(item_def):
    rarity_value = _get_rarity(item_def)
    if rarity_value <= 20:
        return random.randint(8, 15)
    if rarity_value <= 40:
        return random.randint(6, 10)
    if rarity_value <= 60:
        return random.randint(4, 7)
    if rarity_value <= 80:
        return random.randint(2, 4)
    return random.randint(1, 2)


def generate_merchant_stock(variant):
    kind = _MERCHANT_KINDS.get(variant, "materials")
    candidates = [
        item_def["item_name"]
        for item_def in items_list
        if _is_sellable(item_def) and _matches_kind(item_def, kind)
    ]
    if not candidates:
        return []

    count = random.randint(10, 20)
    count = min(count, len(candidates))
    chosen = random.sample(candidates, count)
    return [
        {
            "item_name": name,
            "price": _compute_price(_ITEM_LOOKUP[name]),
            "stock": _compute_stock(_ITEM_LOOKUP[name]),
        }
        for name in chosen
        if name in _ITEM_LOOKUP
    ]


def refresh_merchant_stock(merchant, current_hour):
    if merchant is None:
        return False
    hour_value = int(current_hour) % 24
    last_hour = getattr(merchant, "last_refresh_hour", None)
    if (
        getattr(merchant, "shop_items", None) is None
        or last_hour is None
        or last_hour != hour_value
    ):
        merchant.shop_items = generate_merchant_stock(
            getattr(merchant, "merchant_variant", 1)
        )
        merchant.last_refresh_hour = hour_value
        return True
    return False


class MerchantUI:
    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.active = False
        self.merchant = None
        self.listings = []

        self.merchant_screen_image = None
        try:
            self.merchant_screen_image = pygame.image.load(
                "assets/sprites/buttons/merchant_screen.png"
            ).convert_alpha()
            self.merchant_screen_image = pygame.transform.scale(
                self.merchant_screen_image, (1100, 600)
            )
        except Exception:
            self.merchant_screen_image = None

        self.scroll_offset = 0
        self.listing_columns = 6
        self.listing_rows_visible = 4
        self.listing_slot_size = 64
        self.listing_gap = 4

        self.selected_listing = None
        self.double_click_listing = None
        self.double_click_timer = 0
        self.double_click_threshold = 0.3
        self.purchase_quantity = 1
        self.minus_button_rect = None
        self.plus_button_rect = None
        self.buy_button_rect = None

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False

        self.font_small = pygame.font.Font(font_path, 14)
        self.font_medium = pygame.font.Font(font_path, 18)
        self.font_large = pygame.font.Font(font_path, 22)
        self.close_rect = None
        self.last_item_click_time = 0
        self.last_item_click_slot = None
        self.last_item_click_type = None
        self.double_click_threshold_ms = 300

    def open(self, merchant, current_hour=None):
        self.active = True
        self.merchant = merchant
        self.scroll_offset = 0
        self.selected_listing = None
        self.double_click_listing = None
        self.purchase_quantity = 1
        self.minus_button_rect = None
        self.plus_button_rect = None
        self.buy_button_rect = None
        if merchant is not None:
            if getattr(merchant, "shop_items", None) is None:
                merchant.shop_items = generate_merchant_stock(
                    getattr(merchant, "merchant_variant", 1)
                )
            if current_hour is not None and getattr(merchant, "last_refresh_hour", None) is None:
                merchant.last_refresh_hour = int(current_hour) % 24
        self.listings = list(getattr(merchant, "shop_items", []) or [])
        for listing in self.listings:
            if "stock" not in listing:
                item_def = _ITEM_LOOKUP.get(listing.get("item_name"))
                listing["stock"] = _compute_stock(item_def)

    def close(self):
        self.active = False
        self.merchant = None
        self.selected_listing = None
        self.listings = []
        self.purchase_quantity = 1
        self.minus_button_rect = None
        self.plus_button_rect = None
        self.buy_button_rect = None
        self.inventory.close_drop_menu()
        self.cancel_drag()

    def _select_slot(self, slot_index, is_hotbar):
        if slot_index is None:
            return
        if is_hotbar:
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_hotbar_slot = slot_index
            self.inventory.selected_inventory_slot = None
        else:
            self.inventory.selection_mode = "inventory"
            self.inventory.selected_inventory_slot = slot_index

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
                    max_stack = item.get("stack_size", 100)
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
                if self.dragged_from_hotbar:
                    self.inventory.hotbar_slots[self.dragged_from_slot] = target_slot
                else:
                    self.inventory.inventory_list[self.dragged_from_slot] = target_slot
                new_selection_hotbar = slot_index
            else:
                self.inventory.inventory_list[slot_index] = self.dragged_item
                if self.dragged_from_hotbar:
                    self.inventory.hotbar_slots[self.dragged_from_slot] = target_slot
                else:
                    self.inventory.inventory_list[self.dragged_from_slot] = target_slot
                new_selection_inventory = slot_index

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
            self.inventory.selected_hotbar_slot = self.dragged_from_slot
            self.inventory.selection_mode = "hotbar"
            self.inventory.selected_inventory_slot = None
        else:
            self.inventory.inventory_list[self.dragged_from_slot] = self.dragged_item
            self.inventory.selected_inventory_slot = self.dragged_from_slot
            self.inventory.selection_mode = "inventory"

        self.dragging = False
        self.dragged_item = None
        self.dragged_from_slot = None
        self.dragged_from_hotbar = False
        self.inventory.recalc_weight()

    def get_slot_at_mouse(self, mouse_pos, screen):
        mouse_x, mouse_y = mouse_pos
        bg_x = screen.get_width() / 2 - self.merchant_screen_image.get_width() / 2
        bg_y = screen.get_height() / 2 - self.merchant_screen_image.get_height() / 2

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

    def open_drop_menu(self, slot_index, is_hotbar, mouse_pos):
        self._select_slot(slot_index, is_hotbar)
        return self.inventory.open_drop_menu(slot_index, is_hotbar, mouse_pos)

    def handle_mouse_click(self, mouse_pos, button, screen):
        if not self.active:
            return

        slot_index, is_hotbar = self.get_slot_at_mouse(mouse_pos, screen)
        if slot_index is not None and button == 1:
            return

        if button == 1 and self._handle_purchase_controls(mouse_pos):
            return

        listing_idx = self._get_listing_at_mouse(mouse_pos, screen)
        if listing_idx is not None:
            if button == 1:
                self.selected_listing = listing_idx
                self.purchase_quantity = 1

    def handle_mouse_scroll(self, direction):
        if not self.active:
            return

        columns = self.listing_columns
        total_rows = (len(self.listings) + columns - 1) // columns
        max_scroll = max(0, total_rows - self.listing_rows_visible)
        if direction > 0:
            self.scroll_offset = max(0, self.scroll_offset - 1)
        else:
            self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

    def check_item_double_click(self, slot_index, is_hotbar):
        now = pygame.time.get_ticks()
        slot_type = "hotbar" if is_hotbar else "inventory"
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

    def handle_item_double_click(self, slot_index, is_hotbar):
        return self.inventory.handle_item_double_click(slot_index, is_hotbar)

    def _get_listing_at_mouse(self, mouse_pos, screen):
        if not self.active:
            return None
        bg_x = screen.get_width() / 2 - self.merchant_screen_image.get_width() / 2
        bg_y = screen.get_height() / 2 - self.merchant_screen_image.get_height() / 2
        listing_start_x = bg_x + 18 + (8 * (64 + 4)) + 90
        listing_start_y = bg_y + 290

        rel_x = mouse_pos[0] - listing_start_x
        rel_y = mouse_pos[1] - listing_start_y
        if rel_x < 0 or rel_y < 0:
            return None

        col = int(rel_x // (self.listing_slot_size + self.listing_gap))
        row = int(rel_y // (self.listing_slot_size + self.listing_gap))
        if col >= self.listing_columns or row >= self.listing_rows_visible:
            return None

        listing_idx = (self.scroll_offset + row) * self.listing_columns + col
        if listing_idx < len(self.listings):
            return listing_idx
        return None

    def _get_selected_listing(self):
        if self.selected_listing is None:
            return None
        if self.selected_listing >= len(self.listings):
            return None
        return self.listings[self.selected_listing]

    def _get_max_purchase_quantity(self, listing):
        if not listing:
            return 0
        stock = max(0, int(listing.get("stock", 0)))
        price = int(listing.get("price", 0) or 0)
        if stock <= 0:
            return 0
        if price <= 0:
            return stock
        coins = self.inventory.get_item_count("Gold Coin")
        return min(stock, coins // price)

    def _can_afford(self, listing, quantity=1):
        if not listing:
            return False
        price = listing.get("price", 0)
        if price <= 0:
            return True
        return self.inventory.get_item_count("Gold Coin") >= price * max(1, quantity)

    def _handle_purchase_controls(self, mouse_pos):
        listing = self._get_selected_listing()
        if not listing:
            return False

        max_qty = self._get_max_purchase_quantity(listing)
        if self.minus_button_rect and self.minus_button_rect.collidepoint(mouse_pos):
            if max_qty > 0:
                self.purchase_quantity = max(1, self.purchase_quantity - 1)
            else:
                self.purchase_quantity = 0
            return True
        if self.plus_button_rect and self.plus_button_rect.collidepoint(mouse_pos):
            if max_qty > 0:
                self.purchase_quantity = min(max_qty, max(1, self.purchase_quantity + 1))
            else:
                self.purchase_quantity = 0
            return True
        if self.buy_button_rect and self.buy_button_rect.collidepoint(mouse_pos):
            quantity = max(0, self.purchase_quantity)
            if quantity > 0:
                self.purchase_listing(self.selected_listing, quantity)
            return True
        return False

    def purchase_listing(self, listing_idx, quantity=1):
        if listing_idx is None or listing_idx >= len(self.listings):
            return False
        listing = self.listings[listing_idx]
        item_name = listing.get("item_name")
        price = listing.get("price", 0)
        stock = int(listing.get("stock", 0) or 0)
        if not item_name or stock <= 0:
            return False
        if quantity <= 0:
            return False

        purchased = False
        for _ in range(quantity):
            if listing.get("stock", 0) <= 0:
                break
            if not self._can_afford(listing):
                break
            if not self.inventory.add([item_name]):
                break
            if price > 0:
                self.inventory.remove_item("Gold Coin", price)
            listing["stock"] = max(0, int(listing.get("stock", 0)) - 1)
            purchased = True

        self.purchase_quantity = min(
            max(1, self.purchase_quantity),
            self._get_max_purchase_quantity(listing),
        )
        return purchased

    def draw(self, screen):
        if not self.active:
            return

        width = screen.get_width()
        height = screen.get_height()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        x_pos = width / 2 - self.merchant_screen_image.get_width() / 2
        y_pos = height / 2 - self.merchant_screen_image.get_height() / 2

        if self.merchant_screen_image:
            screen.blit(self.merchant_screen_image, (x_pos, y_pos - 20))

        panel_rect = pygame.Rect(
            x_pos, y_pos - 20, self.merchant_screen_image.get_width(), self.merchant_screen_image.get_height()
        )
        self.close_rect = draw_close_button(screen, panel_rect)

        self._draw_inventory_items(screen, x_pos, y_pos)
        self._draw_listing_preview(screen, x_pos, y_pos)
        self._draw_listing_grid(screen, x_pos, y_pos)
        self._draw_listing_description(screen, x_pos, y_pos)

        self._draw_hotbar_background(screen)
        self._draw_hotbar_items(screen)
        self._draw_inventory_tab(screen)

        if self.dragging and self.dragged_item:
            self._draw_dragged_item(screen)

    def _draw_inventory_items(self, screen, bg_x, bg_y):
        start_x = bg_x + 18
        start_y = bg_y + 44
        slot_size = 64
        gap_size = 4
        columns = 8
        font = pygame.font.Font(font_path, 16)
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.capacity):
            slot = self.inventory.inventory_list[slot_index]
            row = slot_index // columns
            col = slot_index % columns
            x = start_x + col * (slot_size + gap_size)
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
                                ("merchant_inventory", slot_index),
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
        font = pygame.font.Font(font_path, 14)
        mouse_pos = pygame.mouse.get_pos()

        for slot_index in range(self.inventory.hotbar_size):
            slot = self.inventory.hotbar_slots[slot_index]
            x = first_slot_x + slot_index * slot_spacing
            y = slot_y

            is_selected = (
                self.inventory.selection_mode == "hotbar"
                and self.inventory.selected_hotbar_slot == slot_index
            )
            if is_selected:
                pygame.draw.rect(
                    screen, (255, 255, 120), (x - 2, y - 2, slot_size + 4, slot_size + 4), 2
                )

            if slot is not None:
                item_name = slot["item_name"]
                quantity = slot["quantity"]

                for item in items_list:
                    if item["item_name"] == item_name:
                        scaled_img = pygame.transform.scale(item["image"], (slot_size, slot_size))
                        screen.blit(scaled_img, (x, y))
                        if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                            self.inventory.register_hover_candidate(
                                ("merchant_hotbar", slot_index),
                                item_name,
                                (x, y, slot_size, slot_size),
                                slot_data=slot,
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

    def _draw_listing_preview(self, screen, bg_x, bg_y):
        if self.selected_listing is None or self.selected_listing >= len(self.listings):
            return
        listing = self.listings[self.selected_listing]
        item_def = _ITEM_LOOKUP.get(listing.get("item_name"))
        if not item_def:
            return

        preview_x = bg_x + 18 + (8 * (64 + 4)) + 100
        preview_y = bg_y + 34

        pygame.draw.rect(screen, (80, 80, 80), (preview_x, preview_y, 80, 80))
        pygame.draw.rect(screen, (150, 150, 150), (preview_x, preview_y, 80, 80), 2)

        if "image" in item_def:
            scaled_img = pygame.transform.scale(item_def["image"], (76, 76))
            screen.blit(scaled_img, (preview_x + 2, preview_y + 2))

    def _draw_listing_grid(self, screen, bg_x, bg_y):
        listing_start_x = bg_x + 18 + (8 * (64 + 4)) + 90
        listing_start_y = bg_y + 290
        slot_size = self.listing_slot_size
        gap_size = self.listing_gap
        columns = self.listing_columns
        mouse_pos = pygame.mouse.get_pos()

        for i, listing in enumerate(self.listings[self.scroll_offset * columns :]):
            if i >= self.listing_rows_visible * columns:
                break

            col = i % columns
            row = i // columns
            x = listing_start_x + col * (slot_size + gap_size)
            y = listing_start_y + row * (slot_size + gap_size - 3)

            listing_idx = self.scroll_offset * columns + i
            item_def = _ITEM_LOOKUP.get(listing.get("item_name"))
            if not item_def:
                continue

            stock = int(listing.get("stock", 0) or 0)
            can_buy = stock > 0 and self._can_afford(listing)

            if can_buy:
                pygame.draw.rect(screen, (100, 150, 100), (x, y, slot_size, slot_size))
            else:
                pygame.draw.rect(screen, (80, 80, 80), (x, y, slot_size, slot_size))

            pygame.draw.rect(screen, (150, 150, 150), (x, y, slot_size, slot_size), 2)
            if listing_idx == self.selected_listing:
                pygame.draw.rect(screen, (255, 255, 0), (x, y, slot_size, slot_size), 3)

            scaled_img = pygame.transform.scale(item_def["image"], (60, 60))
            screen.blit(scaled_img, (x + 2, y + 2))

            if stock > 0:
                stock_text = self.font_small.render(str(stock), True, (255, 255, 255))
                screen.blit(stock_text, (x + slot_size - stock_text.get_width() - 6, y + slot_size - stock_text.get_height() - 4))
            else:
                sold_text = self.font_small.render("Sold", True, (255, 120, 120))
                screen.blit(
                    sold_text,
                    (
                        x + (slot_size - sold_text.get_width()) // 2,
                        y + (slot_size - sold_text.get_height()) // 2,
                    ),
                )

            if pygame.Rect(x, y, slot_size, slot_size).collidepoint(mouse_pos):
                self.inventory.register_hover_candidate(
                    ("merchant_listing", listing_idx),
                    item_def.get("item_name", "Unknown"),
                    (x, y, slot_size, slot_size),
                )

        total_rows = (len(self.listings) + columns - 1) // columns
        max_scroll = max(0, total_rows - self.listing_rows_visible)
        if total_rows > self.listing_rows_visible:
            track_x = listing_start_x + columns * (slot_size + gap_size) + 10
            track_y = listing_start_y
            track_width = 10
            track_height = self.listing_rows_visible * (slot_size + gap_size - 3)

            pygame.draw.rect(
                screen,
                (50, 50, 70),
                (track_x, track_y, track_width, track_height),
                border_radius=3,
            )

            visible_ratio = self.listing_rows_visible / float(total_rows)
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

    def _wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test_line = word if current == "" else current + " " + word
            if font.size(test_line)[0] <= max_width:
                current = test_line
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if not lines:
            lines = [""]
        return lines

    def _draw_listing_description(self, screen, bg_x, bg_y):
        self.minus_button_rect = None
        self.plus_button_rect = None
        self.buy_button_rect = None

        if self.selected_listing is None or self.selected_listing >= len(self.listings):
            return
        listing = self.listings[self.selected_listing]
        item_def = _ITEM_LOOKUP.get(listing.get("item_name"))
        if not item_def:
            return

        desc_x = bg_x + 18 + (8 * (64 + 4)) + 200
        desc_y = bg_y + 44

        name_text = self.font_large.render(item_def["item_name"], True, (245, 240, 255))
        screen.blit(name_text, (desc_x, desc_y))

        desc_y += 40
        base_width = 200
        desired_width = int(base_width * 1.5)
        panel_right = bg_x + self.merchant_screen_image.get_width()
        available_width = max(0, panel_right - desc_x - 10)
        desc_width = min(desired_width, available_width)
        grid_top = bg_y + 290
        max_bottom = grid_top - 15
        small_line = self.font_small.get_linesize()
        line_step = small_line + 2
        reserved_height = (
            8
            + self.font_medium.get_linesize() + 4
            + small_line + 2
            + small_line + 2
            + small_line + 2
            + small_line + 8
            + 60
        )
        available_height = max_bottom - desc_y - reserved_height
        max_lines = int(available_height // line_step) if available_height > 0 else 0
        desc_start_y = desc_y
        desc_lines = []
        if max_lines > 0:
            desc_lines = self._wrap_text(
                item_def.get("description", ""),
                self.font_small,
                desc_width,
            )[:max_lines]
            for line_idx, line in enumerate(desc_lines):
                line_y = desc_start_y + (line_idx * line_step)
                if line_y + line_step > max_bottom:
                    break
                desc_text = self.font_small.render(line, True, (235, 235, 240))
                screen.blit(desc_text, (desc_x, line_y))

        if desc_lines:
            desc_y = desc_start_y + (len(desc_lines) * line_step)

        desc_y += 8
        if desc_y + self.font_medium.get_linesize() > max_bottom:
            return

        price = int(listing.get("price", 0) or 0)
        stock = int(listing.get("stock", 0) or 0)
        coins = self.inventory.get_item_count("Gold Coin")
        max_qty = self._get_max_purchase_quantity(listing)
        if max_qty > 0:
            self.purchase_quantity = max(1, min(self.purchase_quantity, max_qty))
        else:
            self.purchase_quantity = 0

        price_color = (120, 255, 120) if coins >= price else (255, 120, 120)
        price_text = self.font_medium.render(
            f"Price: {price} Gold Coins", True, price_color
        )
        screen.blit(price_text, (desc_x, desc_y))

        desc_y += self.font_medium.get_linesize() + 4
        stock_color = (235, 220, 180) if stock > 0 else (255, 120, 120)
        stock_text = self.font_small.render(f"Stock: {stock}", True, stock_color)
        screen.blit(stock_text, (desc_x, desc_y))

        desc_y += self.font_small.get_linesize() + 2
        coins_text = self.font_small.render(
            f"You have: {coins}", True, (220, 220, 220)
        )
        screen.blit(coins_text, (desc_x, desc_y))

        total_cost = price * max(0, self.purchase_quantity)
        desc_y += self.font_small.get_linesize() + 2
        total_color = (120, 255, 120) if coins >= total_cost else (255, 120, 120)
        total_text = self.font_small.render(
            f"Total: {total_cost} Gold Coins", True, total_color
        )
        screen.blit(total_text, (desc_x, desc_y))

        controls_y = desc_y + self.font_small.get_linesize() + 8
        if controls_y + 60 > max_bottom:
            return

        qty_label = self.font_small.render("Qty:", True, (220, 220, 220))
        screen.blit(qty_label, (desc_x, controls_y + 2))
        controls_x = desc_x + qty_label.get_width() + 8
        button_size = 22

        self.minus_button_rect = pygame.Rect(controls_x, controls_y, button_size, button_size)
        self.plus_button_rect = pygame.Rect(controls_x + button_size + 38, controls_y, button_size, button_size)
        qty_rect = pygame.Rect(controls_x + button_size + 6, controls_y - 2, 30, button_size + 4)

        button_color = (50, 50, 80)
        border_color = (190, 190, 200)
        pygame.draw.rect(screen, button_color, self.minus_button_rect, border_radius=4)
        pygame.draw.rect(screen, border_color, self.minus_button_rect, 1, border_radius=4)
        pygame.draw.rect(screen, button_color, self.plus_button_rect, border_radius=4)
        pygame.draw.rect(screen, border_color, self.plus_button_rect, 1, border_radius=4)
        pygame.draw.rect(screen, (30, 30, 45), qty_rect, border_radius=4)
        pygame.draw.rect(screen, border_color, qty_rect, 1, border_radius=4)

        minus_text = self.font_small.render("-", True, (235, 235, 235))
        plus_text = self.font_small.render("+", True, (235, 235, 235))
        screen.blit(
            minus_text,
            (
                self.minus_button_rect.centerx - minus_text.get_width() // 2,
                self.minus_button_rect.centery - minus_text.get_height() // 2,
            ),
        )
        screen.blit(
            plus_text,
            (
                self.plus_button_rect.centerx - plus_text.get_width() // 2,
                self.plus_button_rect.centery - plus_text.get_height() // 2,
            ),
        )

        qty_text = self.font_small.render(str(self.purchase_quantity), True, (235, 235, 235))
        screen.blit(
            qty_text,
            (
                qty_rect.centerx - qty_text.get_width() // 2,
                qty_rect.centery - qty_text.get_height() // 2,
            ),
        )

        buy_y = controls_y + button_size + 8
        self.buy_button_rect = pygame.Rect(desc_x, buy_y, 160, 30)
        can_buy = self.purchase_quantity > 0 and coins >= total_cost and stock > 0
        buy_color = (80, 130, 90) if can_buy else (60, 60, 70)
        buy_border = (200, 200, 200)
        pygame.draw.rect(screen, buy_color, self.buy_button_rect, border_radius=6)
        pygame.draw.rect(screen, buy_border, self.buy_button_rect, 1, border_radius=6)

        buy_label = "Buy"
        if self.purchase_quantity > 1:
            buy_label = f"Buy x{self.purchase_quantity}"
        buy_text = self.font_medium.render(buy_label, True, (240, 240, 240))
        screen.blit(
            buy_text,
            (
                self.buy_button_rect.centerx - buy_text.get_width() // 2,
                self.buy_button_rect.centery - buy_text.get_height() // 2,
            ),
        )

    def _draw_dragged_item(self, screen):
        if self.dragged_item is None:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for item in items_list:
            if item["item_name"] == self.dragged_item["item_name"]:
                screen.blit(item["image"], (mouse_x - 32, mouse_y - 32))

                if self.dragged_item["quantity"] > 1:
                    font = pygame.font.Font(font_path, 16)
                    qty_text = font.render(
                        str(self.dragged_item["quantity"]), True, (255, 255, 255)
                    )
                    screen.blit(qty_text, (mouse_x - 10, mouse_y - 5))
                break
