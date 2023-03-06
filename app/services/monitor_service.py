import requests
import cv2
import os
from datetime import datetime
import numpy as np
from conf.camera_list.camera_list import CameraList
from collections import OrderedDict

def send_current_camera_image(gid=None, qid=None, msg_list=[]):
    message_send = '\n'  # 避免和@xxx在同一行
    at = True
    hotkeys = msg_list
    cameras = []
    for hotkey in hotkeys:
        # 海康威视摄像头信息
        ip_address, username, password = CameraList.get_camera_by_hotkey(hotkey)
        cameras.append((ip_address, username, password, hotkey))
    # 去除重复摄像头
    cameras = list(OrderedDict.fromkeys(cameras))
    for ip_address, username, password, hotkey in cameras:
        message_send += f'热键 {hotkey}\n'
        if ip_address:
            message_send += f'监控 {ip_address}\n'
            # 请求登录
            login_url = f"http://{ip_address}/ISAPI/Streaming/channels/101/picture"
            response = requests.get(login_url, auth=(username, password), stream=True)
            if response.status_code == 401:
                message_send += "Authentication failed 401\n"
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
                time_now =  datetime.now()
                time_str_save = time_now.strftime("%Y-%m-%d-%H-%M-%S")
                filename = f"{ip_address}_{time_str_save}.jpg"
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
                location = CameraList.get_location_by_hotkey(hotkey)
                time_str_send = time_now.strftime("%Y-%m-%d %H:%M:%S")
                message_send += f"位置 {location}\n时间 {time_str_send}\n[CQ:image,file=monitor/{qid}_{gid}/{filename}]\n\n"  
            else:
                print("Failed to connect to camera")
                message_send += "Failed to connect to camera\n\n"
        else:
            message_send += "无效热键\n\n"
    return message_send.rstrip('\n'), at


def send_camera_list(gid=None, qid=None, msg_list=[]):
    message_send = ''
    for camera in CameraList._camera_list:
        message_send += f"IP地址 {camera['ip']}\n位置 {camera['location']}\n\n"
    return message_send.rstrip('\n'), False

def add_camera(gid=None, qid=None, msg_list=[]):
    message_send = ''
    if len(msg_list) != 3:
        message_send = '参数数量错误'
    else:
        ip_address , username, password = msg_list
        ip_list = CameraList.get_camera_ip_list()
        if ip_address in ip_list:
            message_send = '该摄像头已存在'
        else:
            url = f"http://{ip_address }/ISAPI/System/deviceInfo"
            try:
                response = requests.get(url, auth=(username, password))
                if response.status_code != 200:
                    message_send = '验证失败'
                else:
                    CameraList.add_camera(ip_address , username, password)
                message_send = '添加成功'
            except:
                message_send = '验证失败'
    return message_send, True




func_dict = {
    '#调取监控': lambda gid=None, qid=None, msg_list=[]: send_current_camera_image(gid, qid, msg_list),
    '#监控列表': lambda gid=None, qid=None, msg_list=[]: send_camera_list(gid, qid, msg_list),
    '#添加监控': lambda gid=None, qid=None, msg_list=[]: add_camera(gid, qid, msg_list)
}