import cv2
from ultralytics import YOLO

# 加载YOLO模型
model = YOLO('yolov5s.pt')

# 打开视频文件
video_path = "./test.flv"
cap = cv2.VideoCapture(video_path)

# 循环遍历视频帧
while cap.isOpened():
    # 从视频读取一帧
    success, frame = cap.read()

    if success:
        # 在帧上运行YOLO追踪，持续追踪帧间的物体
        results = model.track(frame, persist=True)
        # 输出每次追踪推理结果的boxes。
        names = results[0].names
        cls = results[0].boxes.cls.tolist()
        resultObj = results[0].boxes.xywh.tolist()
        id = results[0].boxes.id.tolist()

        # # 在帧上展示结果
        annotated_frame = results[0].plot()
        #
        # for x in annotated_frame:
        #     for y in x:
        #         print(y)

        # # 展示带注释的帧
        cv2.imshow("YOLOv5 Tracking", annotated_frame)

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