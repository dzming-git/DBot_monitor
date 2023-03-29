import requests
import cv2
import os
from datetime import datetime
import numpy as np
from dzmicro import send_message
from conf.camera_list.camera_list import CameraList
from collections import OrderedDict

def help(task):
    from dzmicro import Authority
    authority = Authority()
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    gid, qid = source_id
    permission_level = authority.get_permission_level(source_id)
    permission = authority.get_permission_by_level(permission_level)
    if gid:
        message = f'[CQ:at,qq={qid}]\n'
    message = f'关键词 {KEYWORD}\n当前权限 {permission}\n可调用指令如下\n'
    for command in list(func_dict.keys()):
        if authority.check_command_permission(command, source_id):
            message += f'  - {command}\n'
    send_message(message.strip(), source_id, platform)

def send_current_camera_image(task):
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    gid, qid = source_id
    hotkeys = task.get('args', [])
    cameras = []
    for hotkey in hotkeys:
        # 海康威视摄像头信息
        ip_address, username, password = CameraList.get_camera_by_hotkey(hotkey)
        cameras.append((ip_address, username, password, hotkey))
    # 去除重复摄像头
    cameras = list(OrderedDict.fromkeys(cameras))
    
    for ip_address, username, password, hotkey in cameras:
        message_parts = []
        message_parts.append(f'热键 {hotkey}')
        if ip_address is None:
            message_parts.append('无效热键\n')
            continue
        message_parts.append(f'监控 {ip_address}')
        # 请求登录
        login_url = f"http://{ip_address}/ISAPI/Streaming/channels/101/picture"
        try:
            response = requests.get(login_url, auth=(username, password), stream=True, timeout=1)
        except:
            message_parts.append('无法连接\n')
            print("无法连接")
            continue
        if response.status_code != 200:
            message_parts.append(f'验证失败 {response.status_code}\n')
            continue
        else:
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
            message_parts.append(f"位置 {location}\n时间 {time_str_send}\n[CQ:image,file=monitor/{qid}_{gid}/{filename}]\n")
        message_send = '\n'.join(message_parts).rstrip('\n')
        send_message(message_send, source_id, platform)


def send_camera_list(task):
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    gid, qid = source_id
    message_parts = []
    if gid:
        message_parts.append(f'[CQ:at,qq={qid}]')
    for camera in CameraList._camera_list:
        message_parts.append(f"IP地址 {camera['ip']}\n位置 {camera['location']}\n")
    message_send = '\n'.join(message_parts).rstrip('\n')
    send_message(message_send, source_id, platform)

def add_camera(task):
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    args = task.get('args', [])
    gid, qid = source_id
    message_parts = []
    if gid:
        message_parts.append(f'[CQ:at,qq={qid}]')
    if len(args) != 3:
        message_parts.append('参数数量错误')
    else:
        ip_address , username, password = args
        ip_list = CameraList.get_camera_ip_list()
        if ip_address in ip_list:
            message_parts.append('该摄像头已存在')
        else:
            url = f"http://{ip_address }/ISAPI/System/deviceInfo"
            try:
                response = requests.get(url, auth=(username, password), timeout=1)
                if response.status_code != 200:
                    message_parts.append('验证失败')
                else:
                    CameraList.add_camera(ip_address , username, password)
                message_parts.append('添加成功')
            except:
                message_parts.append('无法连接')
    message_send = '\n'.join(message_parts).rstrip('\n')
    send_message(message_send, source_id, platform)

def set_hotkey(task):
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    gid, qid = source_id
    message_send = '#设置热键 开发中......'
    send_message(message_send, source_id, platform)

KEYWORD = '#监控'
func_dict = {
    '帮助':{
        'func': help,
        'permission': 'USER'
        },
    '调取': {
        'func': send_current_camera_image,
        'permission': 'USER'
        },
    '列表': {
        'func': send_camera_list,
        'permission': 'USER'
        },
    '添加': {
        'func': add_camera,
        'permission': 'MASTER'
        },
    '热键': {
        'func': set_hotkey,
        'permission': 'MASTER'
        },
    }