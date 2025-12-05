from structures import StoneFloor, StoneWall, StoneStairs

print("Testing structure creation...")

try:
    floor = StoneFloor(100, 100, 0)
    print(f"Floor created: sprite={floor.sprite}, size={floor.native_width}x{floor.native_height}")
except Exception as e:
    print(f"Floor error: {e}")
    import traceback
    traceback.print_exc()

try:
    wall = StoneWall(100, 100, 0)
    print(f"Wall created: sprite={wall.sprite}, size={wall.native_width}x{wall.native_height}")
except Exception as e:
    print(f"Wall error: {e}")
    import traceback
    traceback.print_exc()

try:
    stairs = StoneStairs(100, 100, 0)
    print(f"Stairs created: sprite={stairs.sprite}, size={stairs.native_width}x{stairs.native_height}")
except Exception as e:
    print(f"Stairs error: {e}")
    import traceback
    traceback.print_exc()
