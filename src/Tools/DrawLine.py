#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：F41096 
@File    ：DrawShow.py
@Author  ：MoJeffrey
@Date    ：2024/5/2 0:25 
"""
import cv2


class DrawLine:
    __font = cv2.FONT_HERSHEY_SIMPLEX
    __font_scale = 1
    __thickness = 5

    __image = None

    def __init__(self, start_point: tuple, end_point: tuple, color: tuple, image):
        cv2.line(image, start_point, end_point, color, self.__thickness)

        self.__image = image

    def GetImage(self):
        return self.__image
