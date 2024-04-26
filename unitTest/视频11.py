import time

import cv2
from ultralytics import YOLO

from Tools.ExcelWrite import ExcelWrite
from Tools.resultObj import resultObj

# 加载YOLO模型
model = YOLO('yolov5s.pt')

# 打开视频文件
video_path = "./test.flv"
cap = cv2.VideoCapture(video_path)


data_list = {}


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

        Result = obj.getResult()
        EW.write(second, obj.getId(), Result)
        data_list[id] = obj

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

        # # 展示带注释的帧
        cv2.imshow("YOLOv5 Tracking", annotated_frame)

        if time.time() - prev_process_time >= 1.0:
            EW.writeFRow(second)
            getData(results, EW, second)
            second += 1
            EW.save()
            prev_process_time = time.time()

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