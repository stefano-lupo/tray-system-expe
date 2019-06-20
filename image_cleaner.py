###############################################
# Some images got corrupted so this script can 
# detect corrupt ones and deletes them
# There should be 0 bad images if you run this 
# script for the second time on the same data
###############################################

from PIL import Image
import os

base_dir = "./dataset_split_50/"    # Path to split directory
test_or_train = "train"             # Run once for training set and once for test set
dir = os.path.join(base_dir, test_or_train)

total = 0
for ingredient in os.listdir(dir):
    ingredient_dir = os.path.join(dir, ingredient)
    good_images = 0
    bad_images = 0
    for img in os.listdir(ingredient_dir):
        full_path = os.path.join(ingredient_dir, img)
        total = total + 1
        try:
            im = Image.open(full_path)
            good_images = good_images + 1
        except:
            print("Corrupt: %s" % full_path)
            bad_images = bad_images + 1
            # os.remove(full_path)          # Comment this for dry run
            continue
    print("Had %d good images in %s" % (good_images, ingredient))
    print("Had %d bad images in %s" % (bad_images, ingredient))
