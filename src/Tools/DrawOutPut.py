#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：F41096 
@File    ：DrawShow.py
@Author  ：MoJeffrey
@Date    ：2024/5/2 0:25 
"""
import cv2


class DrawOutPut:
    __font = cv2.FONT_HERSHEY_SIMPLEX
    __font_scale = 1
    __font_thickness = 2

    __image = None

    def __init__(self, text: str, image, position: str, background_color: tuple):
        text_size = cv2.getTextSize(text, self.__font, self.__font_scale, self.__font_thickness)[0]
        image_height, image_width = image.shape[:2]

        rect_width = text_size[0] + 2
        rect_height = text_size[1] + 10

        if position == 'upper_left':
            rect_x = 0
            rect_y = 0
        elif position == 'upper_right':
            rect_x = image_width - rect_width - 5
            rect_y = 0
        elif position == 'down_left':
            rect_x = 0
            rect_y = rect_height + 10
        else:
            rect_x = image_width - rect_width - 5
            rect_y = rect_height + 10

        rectangle_coordinate = (rect_x, rect_y)
        cv2.rectangle(image, rectangle_coordinate, (rect_x + rect_width, rect_y + rect_height), background_color, -1)

        text_coordinate = (rect_x + 5, rect_y + text_size[1] + 5)
        cv2.putText(image, text, text_coordinate, self.__font, self.__font_scale, (255, 255, 255), self.__font_thickness)

        self.__image = image

    def GetImage(self):
        return self.__image
