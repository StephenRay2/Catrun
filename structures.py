import pygame
import math
from typing import Dict, List, Tuple, Optional


class Structure(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, z: int, structure_type: str, direction: int = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.structure_type = structure_type
        self.direction = direction
        self.destroyed = False
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.native_width = 64
        self.native_height = 64
        self.sprite = None  # Backwards compat; use visible_sprite for rendering
        self.base_sprite = None
        self.visible_sprite = None
        self.item_frame = 0
        self.hidden_pixel_rows = []
        self.current_snap_point_index = 0
        self.all_snap_points = []
        self.hidden_top_rows = 0
        self.hidden_bottom_rows = 0
        self.hide_top = False
        self.hide_bottom = False
        self.current_transparency = 0.0
        self.draw_offset_y = 0

    def get_collision_rect(self, cam_x: float = 0) -> pygame.Rect:
        """Return a rect in the requested coordinate space. cam_x defaults to world space."""
        return pygame.Rect(self.x - cam_x, self.y, self.native_width, self.native_height)

    def _rect_overlap_height(self, rect_a: pygame.Rect, rect_b: pygame.Rect) -> float:
        return max(0, min(rect_a.bottom, rect_b.bottom) - max(rect_a.top, rect_b.top))

    def _rect_overlap_width(self, rect_a: pygame.Rect, rect_b: pygame.Rect) -> float:
        return max(0, min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left))

    def _apply_hidden_rows(self):
        """Regenerate the visible sprite when edge rows are hidden."""
        if self.base_sprite is None:
            self.visible_sprite = None
            self.sprite = None
            return

        width = self.base_sprite.get_width()
        height = self.base_sprite.get_height()
        src_rect = pygame.Rect(0, 0, width, height)
        dest_y = 0

        if self.hide_top and self.hidden_top_rows > 0:
            src_rect.y += self.hidden_top_rows
            src_rect.height -= self.hidden_top_rows
            dest_y = self.hidden_top_rows

        if self.hide_bottom and self.hidden_bottom_rows > 0:
            src_rect.height -= self.hidden_bottom_rows

        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.base_sprite, (0, dest_y), src_rect)
        self.visible_sprite = sprite
        self.sprite = sprite  # maintain legacy attribute
        self._apply_alpha()

    def _apply_alpha(self):
        if self.visible_sprite is None:
            return
        alpha_value = int(255 * (1 - max(0.0, min(1.0, self.current_transparency))))
        self.visible_sprite.set_alpha(alpha_value)

    def set_transparency(self, transparency: float):
        """Apply transparency where 0 = opaque and 1 = fully transparent."""
        self.current_transparency = max(0.0, min(1.0, transparency))
        if self.visible_sprite is None and self.base_sprite is not None:
            self._apply_hidden_rows()
        self._apply_alpha()

    def get_neighbors(self, all_structures: List['Structure']) -> Dict[str, Optional['Structure']]:
        neighbors = {
            "left": None,
            "right": None,
            "above": None,
            "below": None,
            "top_left": None,
            "top_right": None,
            "bottom_left": None,
            "bottom_right": None,
            "above_z": None
        }

        self_rect = pygame.Rect(self.x, self.y, self.native_width, self.native_height)
        tolerance = 6

        for struct in all_structures:
            if struct is self:
                continue

            struct_rect = pygame.Rect(struct.x, struct.y, struct.native_width, struct.native_height)

            if struct.z == self.z:
                vertical_overlap = self._rect_overlap_height(self_rect, struct_rect)
                horizontal_overlap = self._rect_overlap_width(self_rect, struct_rect)

                if vertical_overlap >= self.native_height * 0.25:
                    if abs(struct_rect.left - self_rect.right) <= tolerance:
                        neighbors["right"] = struct
                    elif abs(self_rect.left - struct_rect.right) <= tolerance:
                        neighbors["left"] = struct

                if horizontal_overlap >= self.native_width * 0.25:
                    if abs(struct_rect.top - self_rect.bottom) <= tolerance:
                        neighbors["below"] = struct
                    elif abs(self_rect.top - struct_rect.bottom) <= tolerance:
                        neighbors["above"] = struct

            elif struct.z == self.z + 1:
                if self._rect_overlap_height(self_rect, struct_rect) > 0 and self._rect_overlap_width(self_rect, struct_rect) > 0:
                    neighbors["above_z"] = struct

        return neighbors
    
    def update_item_frame(self, all_structures: List['Structure']):
        # Overridden by subclasses that need neighbor-aware visuals
        self.hide_top = False
        self.hide_bottom = False
        self._apply_hidden_rows()
    
    def update_visibility(self, player_z: int, player_rect: Optional[pygame.Rect] = None):
        # Default: fully visible unless overridden in subclass
        self.set_transparency(0.0)
    
    def draw(self, screen: pygame.Surface, cam_x: float, cam_y: float = 0):
        if self.visible_sprite is None and self.base_sprite is not None:
            self._apply_hidden_rows()
        sprite_to_draw = self.visible_sprite or self.base_sprite
        if sprite_to_draw and not self.destroyed:
            screen.blit(sprite_to_draw, (self.x - cam_x, self.y + self.draw_offset_y - cam_y))
    
    def rotate(self):
        self.direction = (self.direction + 1) % 4
        self._update_sprite()
        self._apply_hidden_rows()
    
    def cycle_snap_point(self):
        if self.all_snap_points:
            self.current_snap_point_index = (self.current_snap_point_index + 1) % len(self.all_snap_points)
    
    def get_current_snap_point(self) -> Tuple[float, float]:
        if self.all_snap_points:
            return self.all_snap_points[self.current_snap_point_index]
        return (self.x, self.y)
    
    def get_snap_points(self) -> List[Tuple[float, float]]:
        if self.all_snap_points:
            return self.all_snap_points
        w, h = self.native_width, self.native_height
        return [
            (self.x, self.y),  # current anchor
            (self.x + w, self.y),  # right
            (self.x - w, self.y),  # left
            (self.x, self.y + h),  # below
            (self.x, self.y - h),  # above
        ]
    
    def _update_sprite(self):
        pass


class StoneFloor(Structure):
    def __init__(self, x: float, y: float, z: int, direction: int = 0):
        super().__init__(x, y, z, "Stone Floor", direction)
        self.hidden_bottom_rows = 3
        try:
            self.base_sprite = pygame.image.load("assets/sprites/itemFrames/StoneFloorBottom.png").convert_alpha()
            self.native_width = self.base_sprite.get_width()
            self.native_height = self.base_sprite.get_height()
        except Exception as e:
            print(f"[WARN] Failed to load StoneFloor sprite: {e}")
            self.base_sprite = None
            self.native_width = 64
            self.native_height = 64
        self.all_snap_points = []
        self._apply_hidden_rows()
    
    def can_support_structure_above(self) -> bool:
        return True

    def update_item_frame(self, all_structures: List['Structure']):
        self.hide_bottom = False
        self.draw_offset_y = 0
        my_rect = pygame.Rect(self.x, self.y, self.native_width, self.native_height)
        tolerance = 6

        for struct in all_structures:
            if struct is self or struct.z != self.z:
                continue
            other_rect = pygame.Rect(struct.x, struct.y, struct.native_width, struct.native_height)
            horizontal_overlap = self._rect_overlap_width(my_rect, other_rect)
            if horizontal_overlap < self.native_width * 0.25:
                continue
            if abs(other_rect.top - my_rect.bottom) <= tolerance:
                self.hide_bottom = True
                self.draw_offset_y = 3
                break

        self._apply_hidden_rows()


class StoneWall(Structure):
    sprite_files = {
        0: "assets/sprites/itemFrames/StoneWallDown.png",
        1: "assets/sprites/itemFrames/StoneWallRight.png",
        2: "assets/sprites/itemFrames/StoneWallUp.png",
        3: "assets/sprites/itemFrames/StoneWallRight.png",
    }
    flip_horizontally = {
        0: False,
        1: False,
        2: False,
        3: True,
    }
    variant_sets = {
        "down": {
            "solo": "assets/sprites/itemFrames/StoneWallDownCenterSingle.png",
            "left": "assets/sprites/itemFrames/StoneWallDownCenterLeft.png",
            "right": "assets/sprites/itemFrames/StoneWallDownCenterRight.png",
            "both": "assets/sprites/itemFrames/StoneWallDownCenter.png",
        },
        "up": {
            "solo": "assets/sprites/itemFrames/StoneWallUpCenterSingle.png",
            "left": "assets/sprites/itemFrames/StoneWallUpCenterLeft.png",
            "right": "assets/sprites/itemFrames/StoneWallUpCenterRight.png",
            "both": "assets/sprites/itemFrames/StoneWallUpCenter.png",
        },
    }
    
    def __init__(self, x: float, y: float, z: int, direction: int = 0):
        super().__init__(x, y, z, "Stone Wall", direction)
        self.hidden_top_rows = 3
        self.direction = direction
        self.current_variant_key = "solo"
        self.collision_height = 12  # Only bottom band collides so player can walk behind
        self._update_sprite()
        if self.base_sprite:
            self.native_width = self.base_sprite.get_width()
            self.native_height = self.base_sprite.get_height()
        else:
            self.native_width = 64
            self.native_height = 64
        self.all_snap_points = []
        self._apply_hidden_rows()

    def get_collision_rect(self, cam_x: float = 0) -> pygame.Rect:
        height = min(self.collision_height, self.native_height)
        return pygame.Rect(self.x - cam_x, self.y + self.native_height - height, self.native_width, height)
    
    def _load_sprite(self, sprite_file: Optional[str], flip: bool = False):
        if not sprite_file:
            return
        try:
            sprite = pygame.image.load(sprite_file).convert_alpha()
            if flip:
                sprite = pygame.transform.flip(sprite, True, False)
            self.base_sprite = sprite
            self.sprite = sprite
            self.native_width = sprite.get_width()
            self.native_height = sprite.get_height()
            self._apply_hidden_rows()
        except Exception as exc:
            print(f"[WARN] Failed to load wall sprite {sprite_file}: {exc}")
    
    def _select_variant(self, has_left: bool, has_right: bool) -> Tuple[Optional[str], bool]:
        dir_mod = self.direction % 4
        flip = self.flip_horizontally.get(dir_mod, False)

        # Horizontal walls keep their dedicated sprites; don't swap to vertical variants
        if dir_mod in (1, 3):
            return self.sprite_files.get(dir_mod), flip

        orientation = "up" if dir_mod == 2 else "down"
        variant_key = "both" if has_left and has_right else "left" if has_left else "right" if has_right else "solo"
        file_map = self.variant_sets.get(orientation, {})
        sprite_file = file_map.get(variant_key) or self.sprite_files.get(dir_mod)
        return sprite_file, flip
    
    def _update_sprite(self):
        sprite_file = self.sprite_files.get(self.direction % 4)
        flip = self.flip_horizontally.get(self.direction % 4, False)
        self._load_sprite(sprite_file, flip)
    
    def update_item_frame(self, all_structures: List['Structure']):
        neighbors = self.get_neighbors(all_structures)
        self.hide_top = False
        has_left = isinstance(neighbors.get("left"), StoneWall)
        has_right = isinstance(neighbors.get("right"), StoneWall)
        top_cover = False

        above_neighbor = neighbors.get("above")
        above_z_neighbor = neighbors.get("above_z")
        if isinstance(above_neighbor, (StoneWall, StoneFloor)):
            top_cover = True
        if isinstance(above_z_neighbor, (StoneWall, StoneFloor)):
            top_cover = True

        self.hide_top = top_cover
        self.item_frame = int(has_left) | (int(has_right) << 1)

        sprite_file, flip = self._select_variant(has_left, has_right)
        self._load_sprite(sprite_file, flip)

    def update_visibility(self, player_z: int, player_rect: Optional[pygame.Rect] = None):
        # Fade only when player overlaps on same z
        if self.z > player_z:
            self.set_transparency(0.99)
        elif self.z == player_z and player_rect and self.get_collision_rect().colliderect(player_rect):
            self.set_transparency(0.6)
        else:
            self.set_transparency(0.0)


class StoneStairs(Structure):
    sprite_files = {
        0: "assets/sprites/itemFrames/StoneStairsRight.png",
        1: "assets/sprites/itemFrames/StoneStairsUp.png",
        2: "assets/sprites/itemFrames/StoneStairsRight.png",
        3: "assets/sprites/itemFrames/StoneStairsDown.png",
    }
    flip_horizontally = {
        0: False,
        1: False,
        2: True,
        3: False,
    }
    stair_profiles = {
        0: {
            "lower_point": (8, 70),
            "upper_point": (120, 12),
            # Shifted left so collision mask doesn't block; upper moved to stair end
            "lower_entry": pygame.Rect(-12, 36, 30, 44),
            "upper_entry": pygame.Rect(92, -22, 30, 44),
            "slow": 1.0,
        },
        1: {
            "lower_point": (32, 56),
            "upper_point": (32, 8),
            "lower_entry": pygame.Rect(0, 32, 64, 42),
            "upper_entry": pygame.Rect(0, -12, 64, 42),
            "slow": 1.0,
        },
        2: {
            "lower_point": (120, 70),
            "upper_point": (8, 12),
            # Mirror of direction 0 adjustments
            "lower_entry": pygame.Rect(110, 36, 30, 44),
            "upper_entry": pygame.Rect(-22, -22, 30, 44),
            "slow": 1.0,
        },
        3: {
            # Opposite orientation of "up": climb while moving downward
            "lower_point": (32, 8),
            "upper_point": (32, 56),
            "lower_entry": pygame.Rect(0, -12, 64, 42),
            "upper_entry": pygame.Rect(0, 32, 64, 42),
            "slow": 0.85,
        },
    }

    def __init__(self, x: float, y: float, z: int, direction: int = 0):
        super().__init__(x, y, z, "Stone Stairs", direction)
        self.direction = direction
        self.descending = False
        self.climb_speed_multiplier = 1.0
        self.path_lower: Tuple[float, float] = (x, y)
        self.path_upper: Tuple[float, float] = (x, y)
        self.lower_entry_rect = pygame.Rect(x, y, 16, 16)
        self.upper_entry_rect = pygame.Rect(x, y, 16, 16)
        self.mask_offset_y = 0
        self.mask = None
        self.mask_bbox = pygame.Rect(0, 0, 0, 0)
        self._update_sprite()
        if self.base_sprite:
            self.native_width = self.base_sprite.get_width()
            self.native_height = self.base_sprite.get_height()
        else:
            self.native_width = 64
            self.native_height = 64
        self._refresh_mask()
        self._configure_geometry()
        self._apply_hidden_rows()

    def _update_sprite(self):
        sprite_file = self.sprite_files.get(self.direction % 4)
        flip = self.flip_horizontally.get(self.direction % 4, False)
        if sprite_file:
            try:
                sprite = pygame.image.load(sprite_file).convert_alpha()
                if flip:
                    sprite = pygame.transform.flip(sprite, True, False)
                self.base_sprite = sprite
                self.sprite = sprite
                self.native_width = sprite.get_width()
                self.native_height = sprite.get_height()
            except Exception as exc:
                print(f"[WARN] Failed to load StoneStairs sprite: {exc}")

    def _refresh_mask(self):
        if self.base_sprite:
            try:
                self.mask = pygame.mask.from_surface(self.base_sprite)
                bbox = None
                if hasattr(self.mask, "get_bounding_rect"):
                    try:
                        bbox = self.mask.get_bounding_rect()
                    except Exception:
                        bbox = None
                if bbox is None and hasattr(self.mask, "get_bounding_rects"):
                    rects = self.mask.get_bounding_rects()
                    if rects:
                        bbox = rects[0]
                if bbox is None:
                    outline = self.mask.outline()
                    if outline:
                        xs = [p[0] for p in outline]
                        ys = [p[1] for p in outline]
                        min_x, max_x = min(xs), max(xs)
                        min_y, max_y = min(ys), max(ys)
                        bbox = pygame.Rect(min_x, min_y, max(0, max_x - min_x + 1), max(0, max_y - min_y + 1))
                self.mask_bbox = bbox if bbox else pygame.Rect(0, 0, self.native_width, self.native_height)
            except Exception as exc:
                print(f"[WARN] Failed to build mask for StoneStairs: {exc}")
                self.mask = None
                self.mask_bbox = pygame.Rect(0, 0, self.native_width, self.native_height)
        else:
            self.mask = None
            self.mask_bbox = pygame.Rect(0, 0, self.native_width, self.native_height)

    def get_collision_rect(self, cam_x: float = 0) -> pygame.Rect:
        bbox = self.mask_bbox if self.mask_bbox and self.mask_bbox.width > 0 else pygame.Rect(0, 0, self.native_width, self.native_height)
        return pygame.Rect(self.x + bbox.x - cam_x, self.y + self.mask_offset_y + bbox.y, bbox.width, bbox.height)

    def get_mask_data(self) -> Optional[Tuple[pygame.Mask, Tuple[float, float]]]:
        """Return mask and world offset for mask-based checks."""
        if self.mask:
            return self.mask, (self.x, self.y + self.mask_offset_y)
        print("[DEBUG] StoneStairs missing mask; falling back to rect")
        return None

    def _configure_geometry(self):
        profile = self.stair_profiles.get(self.direction % 4, self.stair_profiles[0])
        lp = profile["lower_point"]
        up = profile["upper_point"]
        self.path_lower = (self.x + lp[0], self.y + self.mask_offset_y + lp[1])
        self.path_upper = (self.x + up[0], self.y + self.mask_offset_y + up[1])
        # Extend path slightly so the player reaches the sprite end cleanly
        vec = pygame.Vector2(self.path_upper) - pygame.Vector2(self.path_lower)
        if vec.length_squared() > 0:
            direction_vec = vec.normalize()
            self.path_lower = tuple((pygame.Vector2(self.path_lower) - direction_vec * 12))
            self.path_upper = tuple((pygame.Vector2(self.path_upper) + direction_vec * 32))
        # Align entry rectangles based on stair direction
        if self.mask_bbox:
            left_edge = self.x + self.mask_bbox.x
            right_edge = self.x + self.mask_bbox.x + self.mask_bbox.width
            top_edge = self.y + self.mask_bbox.y
            bottom_edge = self.y + self.mask_bbox.y + self.mask_bbox.height
        else:
            left_edge = self.x
            right_edge = self.x + self.native_width
            top_edge = self.y
            bottom_edge = self.y + self.native_height
        
        direction = self.direction % 4
        if direction in (1, 3):
            # Vertical stairs: entry at top and bottom
            entry_w, entry_h = self.native_width, 3
            self.lower_entry_rect = pygame.Rect(
                left_edge,
                bottom_edge,
                entry_w,
                entry_h,
            )
            self.upper_entry_rect = pygame.Rect(
                left_edge,
                top_edge - entry_h,
                entry_w,
                entry_h,
            )
            # Path endpoints stay at center x, but move beyond top/bottom edges
            half_player_height = 32
            center_x = (left_edge + right_edge) / 2
            self.path_lower = (center_x, bottom_edge + half_player_height)
            self.path_upper = (center_x, top_edge - half_player_height)
        else:
            # Horizontal stairs: entry at left and right
            entry_w, entry_h = 3, 56
            self.lower_entry_rect = pygame.Rect(
                left_edge - entry_w,
                self.path_lower[1] - entry_h / 2,
                entry_w,
                entry_h,
            )
            self.upper_entry_rect = pygame.Rect(
                right_edge,
                self.path_upper[1] - entry_h / 2,
                entry_w,
                entry_h,
            )
            # Move actual path start/end half a player width beyond the mask
            half_player_width = 32
            self.path_lower = (left_edge - half_player_width, self.path_lower[1])
            self.path_upper = (right_edge + half_player_width, self.path_upper[1])
        self.climb_speed_multiplier = profile.get("slow", 1.0)

        self.all_snap_points = []
        if self.mask:
            outline = self.mask.outline()
            if outline:
                step = max(1, len(outline) // 24)  # sample outline to limit snap list
                for idx in range(0, len(outline), step):
                    px, py = outline[idx]
                    self.all_snap_points.append((self.x + px, self.y + self.mask_offset_y + py))
        if not self.all_snap_points:
            # Fallback: mask bounding box anchors if outline missing
            bbox = self.mask_bbox if self.mask_bbox and self.mask_bbox.width > 0 else pygame.Rect(0, 0, self.native_width, self.native_height)
            x0 = self.x + bbox.x
            y0 = self.y + self.mask_offset_y + bbox.y
            x1 = x0 + bbox.width
            y1 = y0 + bbox.height
            mx = (x0 + x1) / 2
            my = (y0 + y1) / 2
            self.all_snap_points = [
                (x0, y0), (x1, y0), (x0, y1), (x1, y1),
                (mx, y0), (mx, y1), (x0, my), (x1, my),
            ]
        else:
            # Ensure bottom-left of the opaque mask is always a snap anchor
            bbox = self.mask_bbox if self.mask_bbox and self.mask_bbox.width > 0 else pygame.Rect(0, 0, self.native_width, self.native_height)
            bottom_left = (self.x + bbox.x, self.y + bbox.y + bbox.height)
            self.all_snap_points.append(bottom_left)

    def toggle_descending(self):
        """Toggle between ascending (z to z+1) and descending (z to z-1) mode."""
        self.descending = not self.descending

    def rotate(self):
        self.direction = (self.direction + 1) % 4
        self._update_sprite()
        self._refresh_mask()
        self._configure_geometry()
        self._apply_hidden_rows()

    def draw(self, screen: pygame.Surface, cam_x: float, cam_y: float = 0):
        super().draw(screen, cam_x, cam_y)
        # Debug markers for path endpoints: taller bars to visualize snap path
        try:
            lower = self.path_lower
            upper = self.path_upper
            # Use entry rectangles for both markers so they match size/position
            lower_rect_screen = pygame.Rect(self.lower_entry_rect.x - cam_x, self.lower_entry_rect.y - cam_y, self.lower_entry_rect.width, self.lower_entry_rect.height)
            upper_rect_screen = pygame.Rect(self.upper_entry_rect.x - cam_x, self.upper_entry_rect.y - cam_y, self.upper_entry_rect.width, self.upper_entry_rect.height)

            pygame.draw.rect(screen, (0, 255, 0), lower_rect_screen, 0)  # filled green
            pygame.draw.rect(screen, (0, 0, 255), lower_rect_screen, 2)   # blue outline

            pygame.draw.rect(screen, (255, 0, 0), upper_rect_screen, 0)   # filled red
            pygame.draw.rect(screen, (255, 165, 0), upper_rect_screen, 2) # orange outline
            # Mask overlay to visualize actual collision footprint
            if self.mask:
                mask_surf = self.mask.to_surface(setcolor=(0, 255, 255, 80), unsetcolor=(0, 0, 0, 0))
                mask_surf.set_alpha(120)
                screen.blit(mask_surf, (self.x - cam_x, self.y + self.mask_offset_y - cam_y))
                # Bounding box outline
                if self.mask_bbox:
                    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(self.x - cam_x + self.mask_bbox.x, self.y + self.mask_offset_y - cam_y + self.mask_bbox.y, self.mask_bbox.width, self.mask_bbox.height), 1)
        except Exception:
            pass

    def get_path_points(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return self.path_lower, self.path_upper

    def get_entry_rects(self) -> Tuple[pygame.Rect, pygame.Rect]:
        return self.lower_entry_rect, self.upper_entry_rect

    def project_progress(self, point: Tuple[float, float]) -> float:
        start = pygame.Vector2(self.path_lower)
        end = pygame.Vector2(self.path_upper)
        path_vec = end - start
        if path_vec.length_squared() == 0:
            return 0.0
        t = (pygame.Vector2(point) - start).dot(path_vec) / path_vec.length_squared()
        return max(0.0, min(1.0, t))

    def movement_matches_path(self, move_vec: pygame.Vector2, from_lower: bool) -> bool:
        if move_vec.length_squared() == 0:
            return False
        path_vec = pygame.Vector2(self.path_upper) - pygame.Vector2(self.path_lower)
        if path_vec.length_squared() == 0:
            return False
        desired = path_vec.normalize()
        if not from_lower:
            desired = -desired
        move_dir = move_vec.normalize()
        # Require at least some agreement with the stair direction
        return move_dir.dot(desired) > 0.35


class StructureManager:
    def __init__(self):
        self.structures: List[Structure] = []
        self.structures_by_z: Dict[int, List[Structure]] = {}
        self.placement_preview: Optional[Structure] = None
        self.snap_enabled = True
        
    def add_structure(self, structure: Structure):
        self.structures.append(structure)
        if structure.z not in self.structures_by_z:
            self.structures_by_z[structure.z] = []
        self.structures_by_z[structure.z].append(structure)
        self.update_all_connections()
        
    def remove_structure(self, structure: Structure):
        if structure in self.structures:
            self.structures.remove(structure)
        if structure.z in self.structures_by_z:
            if structure in self.structures_by_z[structure.z]:
                self.structures_by_z[structure.z].remove(structure)
        self.check_z_level_integrity()
        self.update_all_connections()
        
    def get_structures_at_z(self, z: int) -> List[Structure]:
        return self.structures_by_z.get(z, [])
    
    def find_snap_points(self, player_z: int, origin: Optional[Tuple[float, float]] = None, nearby_range: float = 200) -> List[Tuple[float, float, int]]:
        snap_points = []
        current_z_structures = self.get_structures_at_z(player_z)
        z_above_structures = self.get_structures_at_z(player_z + 1)
        z_below_structures = self.get_structures_at_z(player_z - 1) if player_z > 0 else []
        all_nearby = current_z_structures + z_above_structures + z_below_structures
        
        for struct in all_nearby:
            if getattr(struct, "destroyed", False):
                continue
            for point in struct.get_snap_points():
                px, py = point[0], point[1]
                if origin:
                    dist = math.hypot(px - origin[0], py - origin[1])
                    if dist > nearby_range:
                        continue
                # For stairs, add top-level snap first so it wins ties when distances are equal
                if isinstance(struct, StoneStairs):
                    snap_points.append((px, py, struct.z + 1))
                snap_points.append((px, py, struct.z))
                
        return snap_points
    
    def get_preview_position(self, mouse_pos: Tuple[float, float], player_z: int, shift_held: bool, snap_index: int = 0, snap_radius: float = 120) -> Optional[Tuple[float, float]]:
        if shift_held or not self.snap_enabled:
            return mouse_pos[0], mouse_pos[1], player_z
        
        snap_points = self.find_snap_points(player_z, origin=mouse_pos, nearby_range=snap_radius)
        if not snap_points:
            return mouse_pos[0], mouse_pos[1], player_z

        snap_points.sort(key=lambda pt: (math.hypot(mouse_pos[0] - pt[0], mouse_pos[1] - pt[1]), -pt[2]))
        snap_index = snap_index % len(snap_points)
        chosen = snap_points[snap_index]
        return (chosen[0], chosen[1], chosen[2] if len(chosen) > 2 else player_z)
    
    def check_z_level_integrity(self):
        z_levels_to_remove = []
        
        for z, structures in self.structures_by_z.items():
            if z == 0:
                continue
                
            has_support = False
            z_below_structures = self.get_structures_at_z(z - 1)
            
            for struct in structures:
                if getattr(struct, "destroyed", False):
                    continue
                for support_struct in z_below_structures:
                    if getattr(support_struct, "destroyed", False):
                        continue
                    # Allow any structure to serve as support (floors always support; other solids count too)
                    if isinstance(support_struct, StoneFloor) or self._structures_overlap(struct, support_struct):
                        has_support = True
                        break
                if has_support:
                    break
                    
            if not has_support:
                z_levels_to_remove.append(z)
        
        for z in z_levels_to_remove:
            structures_copy = self.structures_by_z[z].copy()
            for struct in structures_copy:
                self.remove_structure(struct)
        if z_levels_to_remove:
            for z in z_levels_to_remove:
                if z in self.structures_by_z:
                    del self.structures_by_z[z]
            self.update_all_connections()
    
    def _structures_overlap(self, struct1: Structure, struct2: Structure) -> bool:
        rect1 = pygame.Rect(struct1.x, struct1.y, struct1.native_width, struct1.native_height)
        rect2 = pygame.Rect(struct2.x, struct2.y, struct2.native_width, struct2.native_height)
        return rect1.colliderect(rect2)
    
    def update_all_connections(self):
        for struct in self.structures:
            if getattr(struct, "destroyed", False):
                continue
            struct.update_item_frame(self.structures)
    
    def update_visibility(self, player_z: int, player_rect: Optional[pygame.Rect] = None):
        for struct in self.structures:
            if getattr(struct, "destroyed", False):
                continue
            struct.update_visibility(player_z, player_rect)
    
    def draw_all(self, screen: pygame.Surface, cam_x: float, player_z: int, player_rect: Optional[pygame.Rect] = None, filter_fn=None):
        self.update_visibility(player_z, player_rect)
        
        for z in sorted(self.structures_by_z.keys()):
            for struct in self.structures_by_z[z]:
                if filter_fn and not filter_fn(struct):
                    continue
                struct.draw(screen, cam_x)
    
    def get_falling_target_z(self, player_pos: Tuple[float, float], current_z: int) -> Optional[int]:
        for z in range(current_z - 1, -1, -1):
            structures = self.get_structures_at_z(z)
            for struct in structures:
                if getattr(struct, "destroyed", False):
                    continue
                if isinstance(struct, (StoneFloor, StoneStairs)):
                    if hasattr(struct, "get_mask_data"):
                        data = struct.get_mask_data()
                        if data:
                            mask, origin = data
                            px = int(player_pos[0] - origin[0])
                            py = int(player_pos[1] - origin[1])
                            if 0 <= px < mask.get_size()[0] and 0 <= py < mask.get_size()[1]:
                                if mask.get_at((px, py)):
                                    return z
                    struct_rect = pygame.Rect(struct.x, struct.y, struct.native_width, struct.native_height)
                    if struct_rect.collidepoint(player_pos):
                        return z
        return None
    
    def calculate_fall_damage(self, z_from: int, z_to: int) -> int:
        if z_from <= 0:
            return 0
        return 10 + (15 * (z_from - 1))


def get_structure_class(structure_type):
    if structure_type == "StoneFloor":
        return StoneFloor
    elif structure_type == "StoneWall":
        return StoneWall
    elif structure_type == "StoneStairs":
        return StoneStairs
    return None
