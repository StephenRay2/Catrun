import os

folder_path = "assets/sprites/items"
i = 0
for picture in os.listdir(folder_path):
    i += 1
    if picture.endswith((".png", ".jpg", ".jpeg")):
        print(f"{i}. {picture}")

