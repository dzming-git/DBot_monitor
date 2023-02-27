import requests
import cv2
import os
from datetime import datetime
import numpy as np
from conf.camera_list.camera_list import CameraList

def send_current_camera_image(gid=None, qid=None, msg_list=[]):
    message_send = ''
    hotkey = msg_list[0]
    # 海康威视摄像头信息
    ip_address, username, password = CameraList.get_camera_by_hotkey(hotkey)
    if ip_address:
        # 请求登录
        login_url = f"http://{ip_address}/ISAPI/Streaming/channels/101/picture"
        response = requests.get(login_url, auth=(username, password), stream=True)
        if response.status_code == 401:
            message_send = "Authentication failed 401"
            print("Authentication failed")
        elif response.status_code == 200:
            print("Authentication success")

            # 读取数据并解码JPEG图像
            data = b""
            for chunk in response.iter_content(chunk_size=1024):
                data += chunk
                a = data.find(b'\xff\xd8')
                b = data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = data[a:b+2]
                    data = data[b+2:]
                    break
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            # 设置保存目录
            save_root_dir = CameraList.get_img_save_dir()
            save_dir = os.path.join(save_root_dir, f"{qid}_{gid}")
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # 获取当前时间，并将其格式化为指定字符串格式
            time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filename = f"{time_str}.jpg"
            filepath = f"{save_dir}/{filename}"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            # 压缩为JPEG并保存到本地
            quality = 95  # 设置压缩质量
            compressed = False
            while not compressed and quality >= 10:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
                _, buffer = cv2.imencode(".jpg", frame, encode_param)
                size = len(buffer)
                if size < 1e6:

                    with open(filepath, "wb") as f:
                        f.write(buffer)
                    compressed = True
                else:
                    quality -= 5
            message_send = f"[CQ:image,file=monitor/{qid}_{gid}/{filename}]"  
        else:
            print("Failed to connect to camera")
            message_send = "Failed to connect to camera"
    else:
        message_send = "无效热键"
    # msg_struct = Msg_struct(gid=gid, qid=qid, at=False, msg=message_send)
    # send_message(msg_struct)

def send_camera_list(gid=None, qid=None, msg_list=[]):
    message_send = ''
    for camera in CameraList._camera_list:
        message_send += f"IP地址 {camera['ip']}\n位置 {camera['location']}\n\n"
    # msg_struct = Msg_struct(gid=gid, qid=qid, at=False, msg=message_send)
    # send_message(msg_struct)
