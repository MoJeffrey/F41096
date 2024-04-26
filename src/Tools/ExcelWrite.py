#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：F41095 
@File    ：ExcelWrite.py
@Author  ：MoJeffrey
@Date    ：2024/4/25 22:03 
"""
import logging
import os
import time
from typing import List

import xlwt
from datetime import datetime

from Tools.resultObj import resultObj


class ExcelWrite:

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('结果', cell_overwrite_ok=True)
    __fileName: str = None

    def __init__(self):

        if not os.path.exists('./output'):
            os.makedirs('./output')

        dt = datetime.fromtimestamp(time.time())
        self.__fileName = dt.strftime('%Y-%m-%d %H:%M:%S:%f')
        self.__fileName = str(time.time())
        self.style = xlwt.XFStyle()
        self.style.alignment.wrap = 1

    def writeFId(self, Id):
        self.sheet.write(0, Id, Id, style=self.style)

    def writeFRow(self, second):
        self.sheet.write(second, 0, second, style=self.style)

    def write(self, row: int, col: int, data: str):
        newData = data.replace('; ', ';\n')
        lenStr = newData.split(';\n')[1]
        self.sheet.write(row, col, newData, style=self.style)
        self.sheet.col(col).width = 256 * (len(lenStr) + 4)

    def save(self):
        self.workbook.save(f'./output/[{self.__fileName}]output.xls')