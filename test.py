from PIL import Image
import os

dir = "./split_training_images_50/train"

for ingredient in os.listdir(dir):
    ingredient_dir = os.path.join(dir, ingredient)
    print(os.listdir(ingredient_dir))