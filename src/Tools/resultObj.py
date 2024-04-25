#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：F41095 
@File    ：resultObj.py
@Author  ：MoJeffrey
@Date    ：2024/4/25 17:15 
"""
import math


class resultObj:
    __id: int = None
    __coordinate: list = None
    __Name: str = None
    __Old = None

    def __init__(self, id, coordinate, Name):
        self.__id = int(id)
        self.__coordinate = coordinate
        self.__Name = Name

    def setOldResultObj(self, Old):
        self.__Old = Old

    def getId(self) -> int:
        return self.__id

    def getResult(self):
        return f"类别: {self.__Name}; 坐标： {self.__coordinate}; 距离: {self.calculate_distance()}; 斜率: {self.calculate_slope()}"

    def getCoordinate(self):
        return self.__coordinate

    @staticmethod
    def calculate_center(rect):
        # 计算矩形中心点坐标
        center_x = rect[0] + rect[2] / 2  # 左上角 x 坐标 + 宽度的一半
        center_y = rect[1] + rect[3] / 2  # 左上角 y 坐标 + 高度的一半
        return center_x, center_y

    def calculate_slope(self):
        if self.__Old is None:
            return 0

        rect1 = self.__coordinate
        rect2 = self.__Old.getCoordinate()

        # 计算两个矩形的中心点坐标
        center1 = resultObj.calculate_center(rect1)
        center2 = resultObj.calculate_center(rect2)

        # 计算斜率
        if center2[0] - center1[0] != 0:  # 避免除以零
            slope = (center2[1] - center1[1]) / (center2[0] - center1[0])
            return round(slope, 3)
        else:
            return 0

    def calculate_distance(self):
        if self.__Old is None:
            return 0

        rect1 = self.__coordinate
        rect2 = self.__Old.getCoordinate()

        # 计算两个矩形中心点的坐标
        x1 = rect1[0] + rect1[2] / 2  # rect1[0] 是左上角 x 坐标，rect1[2] 是宽度
        y1 = rect1[1] + rect1[3] / 2  # rect1[1] 是左上角 y 坐标，rect1[3] 是高度
        x2 = rect2[0] + rect2[2] / 2
        y2 = rect2[1] + rect2[3] / 2

        # 计算欧几里得距离
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return round(distance, 3)
