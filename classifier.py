import tensorflow as tf
from PIL import Image
import numpy as np
from skimage import transform


class digitClassifier():

    model = tf.keras.models.load_model(
        'D:/Projects/Python/VirtualPen_OpenCV/Model', compile=False, options=False)
    class_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def loadImage(self, filename):
        
        np_image = Image.open(filename)
        np_image = np.array(np_image).astype('float32')/255
        np_image = transform.resize(np_image, (28, 28, 1))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image

    def driver(self, imageName):
       
        image = self.loadImage(self, imageName)
        result = self.model.predict(image)
        num = int(result.argmax(axis=-1))
        label = self.class_names[num]
        return label
