import logging
import os
import threading
import time

from Tools.ExcelWrite import ExcelWrite
from Tools.resultObj import resultObj

os.environ['YOLO_VERBOSE'] = str(False)

from Tools.config import config
from ultralytics import YOLO
from pathlib import Path
from Tools.ImgData import ImgData
import cv2
FILE = Path(__file__).resolve()

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
        logging.info(Result)
        data_list[id] = obj

def main():
    config().Init()
    model = YOLO(f'{config.Sys_WEIGHTS_PATH}')

    ImgList = ImgData()
    EW = ExcelWrite()
    prev_process_time = time.time()
    second = 1

    for ret, frame in ImgList:
        if not ret:
            break

        results = model.track(frame, persist=True)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv5", annotated_frame)

        if time.time() - prev_process_time >= 1.0:
            logging.info('=================================================================')
            EW.writeFRow(second)
            getData(results, EW, second)
            second += 1
            EW.save()
            logging.info('=================================================================')
            prev_process_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == '__main__':
    main()
