import numpy as np

from keras import models
from keras.layers import Conv2D, Dense, Flatten

from core.config import IMAGE_SEGMENT_SIZE_PX, NUM_CLASSES, WEIGHTS_FILE

class Network:

    def __init__(self, num_classes=NUM_CLASSES, weights_file=WEIGHTS_FILE):
        model = models.Sequential()

        model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(IMAGE_SEGMENT_SIZE_PX, IMAGE_SEGMENT_SIZE_PX, 3)))
        model.add(Conv2D(32, kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(NUM_CLASSES, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.summary()
        model.load_weights(WEIGHTS_FILE)
        self.model = model

    def predict(self, img: np.ndarray):
        vals = self.model.predict(img)
        print(vals)

