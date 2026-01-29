class SpatialHash:
    def __init__(self, cell_size: int):
        self.cell_size = cell_size
        self.cells = {}

    def clear(self) -> None:
        self.cells.clear()

    def _cell_range_for_rect(self, rect):
        min_x = int(rect.left // self.cell_size)
        max_x = int(rect.right // self.cell_size)
        min_y = int(rect.top // self.cell_size)
        max_y = int(rect.bottom // self.cell_size)
        return min_x, max_x, min_y, max_y

    def insert(self, obj, rect) -> None:
        min_x, max_x, min_y, max_y = self._cell_range_for_rect(rect)
        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                key = (cx, cy)
                bucket = self.cells.get(key)
                if bucket is None:
                    self.cells[key] = [obj]
                else:
                    bucket.append(obj)

    def query_rect(self, rect):
        min_x, max_x, min_y, max_y = self._cell_range_for_rect(rect)
        results = []
        seen_ids = set()
        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                bucket = self.cells.get((cx, cy))
                if not bucket:
                    continue
                for obj in bucket:
                    obj_id = id(obj)
                    if obj_id in seen_ids:
                        continue
                    seen_ids.add(obj_id)
                    results.append(obj)
        return results
