import logging
import os
import time

import cv2

from Tools.config import config

os.environ['YOLO_VERBOSE'] = str(False)
from ultralytics import YOLO

from Tools.ColorEnum import Color
from Tools.DrawLine import DrawLine
from Tools.DrawOutPut import DrawOutPut
from Tools.ExcelWrite import ExcelWrite
from Tools.resultObj import resultObj

# 加载YOLO模型
model = YOLO('yolov5s.pt')
config.Init_Logging()

# 打开视频文件
video_path = "./test.flv"
cap = cv2.VideoCapture(video_path)

data_list = {}


class Record:
    id = 11

    # 入场线
    in_num = 0
    in_list = []
    in_start_point = (600, 130)
    in_end_point = (1920, 190)
    in_line = (in_start_point, in_end_point)
    in_color = Color.PURPLE.value

    # 出场线
    out_num = 0
    out_list = []
    out_start_point = (170, 220)
    out_end_point = (1920, 700)
    out_line = (out_start_point, out_end_point)
    out_color = Color.BLUE.value

    # 异常
    error_num = 0
    error_list = []
    error_color = Color.GREEN.value
    error_slope_upper_limit = 3.2
    error_slope_down_limit = -3.2
    error_average_distance = 100
    error_distance_scope = 100


def getData(results, EW: ExcelWrite, second: int):
    names = results[0].names
    cls_list = results[0].boxes.cls.tolist()
    coordinate_list = results[0].boxes.xywh.tolist()
    id_list: list = results[0].boxes.id.tolist()

    for index in range(len(id_list)):
        id = id_list[index]
        obj = resultObj(id, coordinate_list[index], names[cls_list[index]])

        if id in data_list:
            obj.setOldResultObj(data_list[id])
        else:
            EW.writeFId(obj.getId())
            obj.setFirstObj()

        Result = obj.getResult()
        EW.write(second, obj.getId(), Result)
        data_list[id] = obj

        IsInOrOut = obj.IsInOrOut(Record.in_line, Record.out_line)

        if IsInOrOut is None:
            continue

        if obj.IsError(Record.error_slope_upper_limit, Record.error_slope_down_limit, Record.error_average_distance, Record.error_distance_scope, Record.id):
            Record.error_num += 1
            Record.error_list.append(id)
            continue

        if IsInOrOut:
            Record.in_num += 1
            Record.in_list.append(id)
        else:
            Record.out_num += 1
            Record.out_list.append(id)

    logging.info(f'入场人员: {Record.in_list}')
    logging.info(f'出场人员: {Record.out_list}')
    logging.info(f'异常人员: {Record.error_list}')

if __name__ == '__main__':
    EW = ExcelWrite()
    prev_process_time = time.time()
    second = 1

    # 循环遍历视频帧
    while cap.isOpened():
        # 从视频读取一帧
        success, frame = cap.read()

        if success:
            # 在帧上运行YOLO追踪，持续追踪帧间的物体
            results = model.track(frame, persist=True)
            # 输出每次追踪推理结果的boxes。

            # # 在帧上展示结果
            annotated_frame = results[0].plot()

            if time.time() - prev_process_time >= 1.0:
                EW.writeFRow(second)
                getData(results, EW, second)
                second += 1
                EW.save()
                prev_process_time = time.time()

            # 入场绘图
            in_DS = DrawOutPut('IN:' + str(Record.in_num), annotated_frame, 'upper_left', Record.in_color)
            in_DL = DrawLine(Record.in_start_point, Record.in_end_point, Record.in_color, in_DS.GetImage())

            # 出场绘图
            out_DS = DrawOutPut('OUT:' + str(Record.out_num), in_DL.GetImage(), 'upper_right', Record.out_color)
            out_DL = DrawLine(Record.out_start_point, Record.out_end_point, Record.out_color, out_DS.GetImage())

            # 异常人员
            out_DS = DrawOutPut('ERROR:' + str(Record.error_num), out_DL.GetImage(), 'down_left', Record.error_color)

            if Record.id in data_list:
                d = data_list[Record.id]
                if d.getOld() is not None:
                    line = d.getStartToNowLine()
                    new = []
                    for a in line:
                        for x in a:
                            new.append(int(x))
                    out_DS = DrawLine((new[0], new[1]), (new[2], new[3]), Record.error_color, out_DS.GetImage())
                    logging.info(f'id: {Record.id} 追踪记录; inFirst: {d.getInFirst()}; OutFirst: {d.getOutFirst()}; Error: {d.getError()}')

            # # 展示带注释的帧
            cv2.imshow("YOLOv5 Tracking", out_DS.GetImage())

            # exit()
            # 如果按下'q'则退出循环
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # 如果视频结束则退出循环
            break

    # 释放视频捕获对象并关闭显示窗口
    cap.release()
    cv2.destroyAllWindows()