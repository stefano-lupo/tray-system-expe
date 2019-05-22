import numpy as np

from keras import models
from keras.layers import Conv2D, Dense, Flatten

from core.config import IMAGE_SEGMENT_SIZE_PX, NUM_CLASSES, SMALL_MODEL, RES_NET_MODEL

class Network:

    def __init__(self, network="resnet"):

        model_file = RES_NET_MODEL if network == "resnet" else SMALL_MODEL
        self.model = models.load_model(model_file)


        # model = models.Sequential()
        # model.add(
        #     Conv2D(64, kernel_size=3, activation='relu', input_shape=(IMAGE_SEGMENT_SIZE_PX, IMAGE_SEGMENT_SIZE_PX, 3)))
        # model.add(Conv2D(32, kernel_size=3, activation='relu'))
        # model.add(Flatten())
        # model.add(Dense(NUM_CLASSES, activation='softmax'))
        #
        # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        # model.summary()
        # model.load_weights(SMALL_MODEL)
        # self.model = model

    def predict(self, img: np.ndarray):
        vals = self.model.predict(img)
        # print(vals)
        return vals
