from PIL import Image
import os

base_dir = "./split_training_images_cleaned_50/"
test_or_train = "test"
dir = os.path.join(base_dir, test_or_train)

total = 0
for ingredient in os.listdir(dir):
    ingredient_dir = os.path.join(dir, ingredient)
    # print(os.listdir(ingredient_dir))
    good = 0
    bad = 0
    for img in os.listdir(ingredient_dir):
        full_path = os.path.join(ingredient_dir, img)
        total = total + 1
        try:
            im = Image.open(full_path)
            good = good + 1
        except:
            # print("problem with: %s" % full_path)/
            bad = bad + 1
            os.remove(full_path)
            continue
    print("Good was %d " % good)
    print("Bad was %d " % bad)
print("Total %d " % total)