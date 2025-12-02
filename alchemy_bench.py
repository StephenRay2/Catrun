import pygame

from inventory import items_list
from mortar_pestle import MortarPestle


class AlchemyBench(MortarPestle):
    def __init__(self, inventory_obj):
        super().__init__(inventory_obj)
        self.alchemy_bench_pos = None

        # Load alchemy UI background (reuse mortar layout for controls)
        self.alchemy_screen_image = None
        try:
            self.alchemy_screen_image = pygame.image.load(
                "assets/sprites/buttons/alchemy_screen.png"
            ).convert_alpha()
            self.alchemy_screen_image = pygame.transform.scale(self.alchemy_screen_image, (1100, 600))
        except Exception:
            self.alchemy_screen_image = None

        # Repoint the base class background to the alchemy artwork when available
        if self.alchemy_screen_image:
            self.mortar_pestle_screen_image = self.alchemy_screen_image

        # Swap in alchemy recipes
        self.recipes = self._load_alchemy_recipes()

    def _load_alchemy_recipes(self):
        recipes = []
        seen = set()
        for item in items_list:
            medium = item.get("crafting_medium")
            if medium == "alchemy_bench" and item.get("recipe"):
                item_name = item["item_name"]
                if item_name not in seen:
                    recipes.append(item)
                    seen.add(item_name)

            for alt in item.get("recipe_alternatives", []):
                alt_medium = alt.get("crafting_medium")
                if alt_medium == "alchemy_bench" and alt.get("recipe"):
                    recipe_obj = alt.copy()
                    recipe_obj["item_name"] = item["item_name"]
                    recipe_obj["icon"] = item.get("icon")
                    recipe_obj["image"] = item.get("image")
                    recipe_obj["image_hotbar"] = item.get("image_hotbar")
                    recipe_obj["stack_size"] = item.get("stack_size")
                    recipe_obj["weight"] = item.get("weight")
                    recipe_obj["type"] = item.get("type")
                    recipe_obj["description"] = item.get("description")
                    recipe_obj["use_effect"] = item.get("use_effect")
                    recipe_obj["placeable"] = item.get("placeable")
                    recipe_obj["consumable"] = item.get("consumable")
                    recipe_obj["durability"] = item.get("durability")
                    recipe_obj["tags"] = item.get("tags")
                    recipes.append(recipe_obj)
        return recipes

    def open(self, alchemy_bench_pos):
        self.alchemy_bench_pos = alchemy_bench_pos
        super().open(alchemy_bench_pos)

    def close(self):
        self.alchemy_bench_pos = None
        super().close()
