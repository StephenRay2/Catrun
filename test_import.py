try:
    from structures import get_structure_class
    print("get_structure_class imported successfully")
    print(f"StoneFloor class: {get_structure_class('StoneFloor')}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
