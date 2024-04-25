import cv2
import numpy as np
from PIL import ImageGrab

from Tools.config import config


class ImgData:
    __FPS: int = None

    def __init__(self):
        self.count = 0
        if config.Sys_CAMERA == 0:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(config.Sys_VIDEO_PATH)

        self.__FPS = int(self.cap.get(5))

    def release(self):
        self.cap.release()

    def getFPS(self):
        return self.__FPS

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        return ret, frame
