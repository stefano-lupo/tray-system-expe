import numpy as np
import timeit
from keras import models
from keras.layers import Conv2D, Dense, Flatten

from core.config import IMAGE_SEGMENT_SIZE_PX, NUM_CLASSES, SMALL_MODEL, RES_NET_MODEL, CUSTOM_MODEL, FINAL_MODEL

class Network:

    def __init__(self, network="custom"):

        model_file = RES_NET_MODEL if network == "resnet" else FINAL_MODEL

        # Apparently this fixes the weird bug
        self.model = models.load_model(model_file)
        self.model._make_predict_function()

    def predict(self, img: np.ndarray):
        start = timeit.default_timer()
        vals = self.model.predict(img)
        stop = timeit.default_timer()
        # print("Took %s seconds for forward pass" % str(stop - start))
        # print(vals)
        return vals
