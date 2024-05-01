#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：F41095 
@File    ：resultObj.py
@Author  ：MoJeffrey
@Date    ：2024/4/25 17:15 
"""
import copy
import logging
import math


class resultObj:
    __id: int = None
    __coordinate: list = None
    __center_line = None
    __Name: str = None
    __Old = None
    __firstObj = None
    __inFirst = None
    __outFirst = None
    __IsInOrOut = None
    __IsError = False
    __slope = 0
    __distance = 0

    def __init__(self, id, coordinate, Name):
        self.__id = int(id)
        self.__coordinate = coordinate
        self.__Name = Name

    def IsInOrOut(self, in_line: tuple, out_line: tuple):
        """
        传出 None 则还未判断结果
        传出 True 先in
        传出 False 先out
        :return:
        """
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        def intersect(A, B):
            return ccw(A[0], B[0], B[1]) != ccw(A[1], B[0], B[1]) and ccw(A[0], A[1], B[0]) != ccw(A[0], A[1], B[1])

        if self.__IsError:
            return None

        if self.__Name != 'person':
            return None

        if self.__Old is None:
            return None

        if self.__IsInOrOut is not None:
            return None

        line = self.getStartToNowLine()

        if intersect(in_line, line) and self.__inFirst is None:
            self.__inFirst = True if self.__outFirst is None else False

        if intersect(out_line, line) and self.__outFirst is None:
            self.__outFirst = True if self.__inFirst is None else False

        if self.__inFirst == True and self.__outFirst == False:
            self.__IsInOrOut = True
        elif self.__inFirst == False and self.__outFirst == True:
            self.__IsInOrOut = False

        return self.__IsInOrOut

    def getStartToNowLine(self):
        return (resultObj.calculate_center(self.__coordinate), resultObj.calculate_center(self.__firstObj.getCoordinate()))
    def setFirstObj(self):
        self.__firstObj = copy.deepcopy(self)

    def setOldResultObj(self, Old):
        self.__Old = Old
        self.__IsError = self.__Old.getError()
        self.__firstObj = self.__Old.getFirstObj()
        self.__outFirst = self.__Old.getOutFirst()
        self.__inFirst = self.__Old.getInFirst()
        self.__IsInOrOut = self.__Old.getIsInOrOut()
        self.calculate_slope()
        self.calculate_distance()

    def IsError(self, slope_upper_limit: float, slope_down_limit, average_distance: float, distance_scope: float, id: int = None):
        if (slope_upper_limit < self.__slope or slope_down_limit > self.__slope) and self.__slope != 0:
            self.__IsError = True

            if id is not None and self.__id == id:
                logging.info(f"id: {self.__id} 追踪记录: 斜率异常; 当前斜率: {self.__slope}")

        down_distance = average_distance - distance_scope
        up_distance = average_distance + distance_scope

        if (up_distance < self.__distance or down_distance > self.__distance) and self.__distance != 0:
            self.__IsError = True
            if id is not None and self.__id == id:
                logging.info(f"id: {self.__id} 追踪记录: 距离异常; 距离斜率: {self.__distance}")

        return self.__IsError

    def getError(self):
        return self.__IsError

    def getOld(self):
        return self.__Old

    def getFirstObj(self):
        return self.__firstObj

    def getCenterLine(self):
        return self.__center_line

    def getIsInOrOut(self):
        return self.__IsInOrOut

    def getOutFirst(self):
        return self.__outFirst

    def getInFirst(self):
        return self.__inFirst

    def getId(self) -> int:
        return self.__id

    def getResult(self):
        return f"类别: {self.__Name}; 坐标： {self.__coordinate}; 距离: {self.getDistance()}; 斜率: {self.getSlope()}"

    def getCoordinate(self):
        return self.__coordinate

    def getDistance(self):
        return self.__distance

    def getSlope(self):
        return self.__slope

    @staticmethod
    def calculate_center(rect):
        # 计算矩形中心点坐标
        center_x = rect[0] + rect[2] / 2  # 左上角 x 坐标 + 宽度的一半
        center_y = rect[1] + rect[3] / 2  # 左上角 y 坐标 + 高度的一半
        return center_x, center_y

    def calculate_slope(self):
        if self.__Old is None:
            return

        rect1 = self.__coordinate
        rect2 = self.__Old.getCoordinate()

        # 计算两个矩形的中心点坐标
        center1 = resultObj.calculate_center(rect1)
        center2 = resultObj.calculate_center(rect2)

        self.__center_line = (center1, center2)
        # 计算斜率
        if center2[0] - center1[0] != 0:  # 避免除以零
            slope = (center2[1] - center1[1]) / (center2[0] - center1[0])
            self.__slope = round(slope, 3)

    def calculate_distance(self):
        if self.__Old is None:
            return

        rect1 = self.__coordinate
        rect2 = self.__Old.getCoordinate()

        # 计算两个矩形中心点的坐标
        x1 = rect1[0] + rect1[2] / 2  # rect1[0] 是左上角 x 坐标，rect1[2] 是宽度
        y1 = rect1[1] + rect1[3] / 2  # rect1[1] 是左上角 y 坐标，rect1[3] 是高度
        x2 = rect2[0] + rect2[2] / 2
        y2 = rect2[1] + rect2[3] / 2

        # 计算欧几里得距离
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.__distance = round(distance, 3)
