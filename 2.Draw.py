import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import numpy as np
from skimage import transform
from tensorflow.python.ops.gen_math_ops import imag_eager_fallback
from classifier import digitClassifier as dc


class drawingCanvas():
    def __init__(self):
        self.penrange = np.load('penrange.npy')
        self.cap = cv2.VideoCapture(0)
        self.canvas = None
        # initial position on pen
        self.x1, self.y1 = 0, 0
        # used to toggle between pen and eraser mode
        self.val = 1
        self.draw()

    def draw(self):
        while True:
            k = cv2.waitKey(1) & 0xFF
            _, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)

            if self.canvas is None:
                self.canvas = np.zeros_like(self.frame)

            mask = self.CreateMask()
            contours = self.ContourDetect(mask)
            self.display()
            if k == ord('d'):
                self.drawLine(contours)
                #self.display()
            #k = cv2.waitKey(1) & 0xFF
            if k == ord('o'):
                print("Key press is detected!")
                image = self.canvas
                fileName = "stream.jpg"
                cv2.imwrite(fileName, image)
                #self.digit_predict(image)
                imageLabel = dc.driver(dc, fileName)
                print(imageLabel)

            self.takeAction(k)

            # if esc key is pressed exit
            if k == 27:
                break

    def CreateMask(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        lower_range = self.penrange[0]
        upper_range = self.penrange[1]
        mask = cv2.inRange(hsv, lower_range, upper_range)
        return mask

    def ContourDetect(self, mask):
        # Find Contours
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def drawLine(self, contours):
        # if contour area is not none and is greater than 100 draw the line
        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 100:
            c = max(contours, key=cv2.contourArea)
            x2, y2, w, h = cv2.boundingRect(c)

            if self.x1 == 0 and self.y1 == 0:
                self.x1, self.y1 = x2, y2
            else:
                # Draw the line on the canvas
                self.canvas = cv2.line(self.canvas, (self.x1, self.y1), (x2, y2), [
                                       255*self.val, 0, 0], 10)
            # New point becomes the previous point
            self.x1, self.y1 = x2, y2
        else:
            # If there were no contours detected then make x1,y1 = 0 (reset)
            self.x1, self.y1 = 0, 0

    def display(self):
        # Merge the canvas and the frame.
        self.frame = cv2.add(self.frame, self.canvas)
        cv2.imshow('frame', self.frame)
        cv2.imshow('canvas', self.canvas)

    def takeAction(self, k):
        # When c is pressed clear the entire canvas
        if k == ord('c'):
            self.canvas = None
        # press e to change between eraser mode and writing mode
        if k == ord('e'):
            self.val = int(not self.val)
    
    def digit_predict(self, frame):

        imageLabel = dc.driver(dc, frame)
        print(imageLabel)  





if __name__ == '__main__':
    drawingCanvas()

cv2.destroyAllWindows()