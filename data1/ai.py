
import numpy as np
import pyrealsense2 as rs
import time
import cv2
import math
net = cv2.dnn.readNet("C:/Users/ludiw/PycharmProjects/pythonProject21/yolo-obj.cfg",
                      "C:/Users/ludiw/PycharmProjects/pythonProject21/yolo-obj.weights")

# 使用CUDA加速
#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
finallcoord =[]
# 加载物体类别的名称
classes = []
with open("C:/Users/ludiw/PycharmProjects/pythonProject21/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

print("加载完毕")
##################################

def calculate_angles(X, Y, Z):
    # 初始化参数
    a1, a2, a3, a4 = 12, 12, 12, 12  # a1为底部圆台高度，剩下三个为三个机械臂长度
    P = 14  # 底部圆盘半径

    # 计算j1的值
    if X == 0:
        j1 = 90
    else:
        j1 = math.atan((Y + P) / X) * (180 / math.pi)

    n, m = 0, 0

    # 第一个循环
    for i in range(181):
        j_all = math.pi * i / 180
        len_ = math.sqrt((Y + P) ** 2 + X ** 2)
        high = Z

        L = len_ - a4 * math.sin(j_all)
        H = high - a4 * math.cos(j_all) - a1

        Cosj3 = ((L * L) + (H * H) - (a2 ** 2) - (a3 ** 2)) / (2 * a2 * a3)
        # Ensure Cosj3 is within [-1, 1]
        Cosj3 = min(max(Cosj3, -1), 1)
        Sinj3 = math.sqrt(1 - Cosj3 ** 2)

        j3 = math.atan2(Sinj3, Cosj3) * (180 / math.pi)

        K2 = a3 * math.sin(j3 / (180 / math.pi))
        K1 = a2 + a3 * math.cos(j3 / (180 / math.pi))

        Cosj2 = (K2 * L + K1 * H) / (K1 ** 2 + K2 ** 2)
        Sinj2 = math.sqrt(1 - Cosj2 ** 2)

        j2 = math.atan2(Sinj2, Cosj2) * (180 / math.pi)
        j4 = j_all * (180 / math.pi) - j2 - j3

        if 0 <= j2 <= 180 and 0 <= j3 <= 180 and -90 <= j4 <= 90:
            n += 1

    # 第二个循环
    for i in range(181):
        j_all = math.pi * i / 180
        len_ = math.sqrt((Y + P) ** 2 + X ** 2)
        high = Z

        L = len_ - a4 * math.sin(j_all)
        H = high - a4 * math.cos(j_all) - a1

        Cosj3 = ((L * L) + (H * H) - (a2 ** 2) - (a3 ** 2)) / (2 * a2 * a3)
        # Ensure Cosj3 is within [-1, 1]
        Cosj3 = min(max(Cosj3, -1), 1)
        Sinj3 = math.sqrt(1 - Cosj3 ** 2)

        j3 = math.atan2(Sinj3, Cosj3) * (180 / math.pi)

        K2 = a3 * math.sin(j3 / (180 / math.pi))
        K1 = a2 + a3 * math.cos(j3 / (180 / math.pi))

        Cosj2 = (K2 * L + K1 * H) / (K1 ** 2 + K2 ** 2)
        Sinj2 = math.sqrt(1 - Cosj2 ** 2)

        j2 = math.atan2(Sinj2, Cosj2) * (180 / math.pi)
        j4 = j_all * (180 / math.pi) - j2 - j3

        if 0 <= j2 <= 180 and 0 <= j3 <= 180 and -90 <= j4 <= 90:
            m += 1
            if m == n // 2 or m == (n + 1) // 2:
                break

    return j1, j2, j3, j4





########################################
# 初始化深度摄像头
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# 创建对齐对象
align_to_color = rs.align(rs.stream.color)

print("初始化完毕")

# 初始化FPS计算
prev_time = time.time()

try:
    while True:
        frames = pipeline.wait_for_frames()

        # 对齐深度帧到彩色帧
        aligned_frames = align_to_color.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        image = np.asanyarray(color_frame.get_data())
        height, width, _ = image.shape

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(net.getUnconnectedOutLayersNames())
        detection_results = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # 获取中心点的深度值
                    center_depth = aligned_depth_frame.get_distance(center_x, center_y)
                    center_depth2 = aligned_depth_frame.get_distance(320, 240)
                    #print(center_depth2)
                    # 计算中心坐标
                    center_x_coord = int(center_x)
                    center_y_coord = int(center_y)

                    detection_results.append({
                        "class_id": class_id,
                        "class_name": classes[class_id],
                        "confidence": float(confidence),
                        "bbox": [x, y, w, h],
                        "center_depth": center_depth,
                        "center_depth2":center_depth2,
                        "center_x_coord": center_x_coord,
                        "center_y_coord": center_y_coord
                    })

        for result in detection_results:
            #global finallcoord
            x, y, w, h = result["bbox"]
            class_name = result["class_name"]
            confidence = result["confidence"]
            center_depth = result["center_depth"]
            center_depth2= result["center_depth2"]
            center_x_coord = result["center_x_coord"]
            center_y_coord = result["center_y_coord"]

            color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = f"{class_name} ({confidence:.2f}) - Distance: {center_depth:.2f} meters"
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # 输出中心坐标

            delta_x = center_x_coord - 320
            delta_y = center_y_coord - 240
            angle_rad = math.atan2(delta_y, -delta_x)
            # 将弧度转换为角度
            angle_deg = math.degrees(angle_rad)
            length= center_depth2 ** 2 - center_depth ** 2
            delta_x_new = length * math.cos(angle_rad)
            delta_y_new = length * math.sin(angle_rad)
            Z=center_depth2
            center_text = f"Center Coord: ({center_x_coord}, {center_y_coord})"
            cv2.putText(image, center_text, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            finallcoord = (delta_x_new, delta_y_new, Z)
            j1, j2, j3, j4 = calculate_angles(*finallcoord)
            print("+---------------------------------------------------------------------------------------+")
            print("| Object Detection Results                                                             |")
            print("|---------------------------------------------------------------------------------------|")
            print(f"| Detected Object: {text:67} |")
            print("|---------------------------------------------------------------------------------------|")
            print(f"|{finallcoord}")
            print("|---------------------------------------------------------------------------------------|")
            print(f"| Center Text: {center_text:66} |")
            print("|---------------------------------------------------------------------------------------|")
            print("| Calculated Angles:                                                                    |")
            print(f"|   j1: {j1:.2f}°|")
            print(f"|   j2: {j2:.2f}° |")
            print(f"|   j3: {j3:.2f}°|")
            print(f"|   j4: {j4:.2f}° |")
            print("+---------------------------------------------------------------------------------------+")

            # 计算并显示FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(image, f"FPS: {fps:.2f}", (width-120, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Object Detection", image)

        key = cv2.waitKey(1)
        if key == 27:
            break

except KeyboardInterrupt:
    pass

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
