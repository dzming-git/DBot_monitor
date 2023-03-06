# monitor_service.py
import time
from conf.route_info.route_info import RouteInfo
from conf.authority.authority import Authority
from conf.camera_list.camera_list import CameraList
from app.app import monitor_server_thread
from utils.tasks import task_thread

def load_conf():
    Authority.load_config('conf/authority/authority.yaml')
    CameraList.load_config('conf/camera_list/camera_list.yaml')
    RouteInfo.load_config('conf/route_info/route_info.yaml')

if __name__ == '__main__': 
    load_conf()
    monitor_server_thread.init()
    monitor_server_thread.start()
    task_thread.start()
    while True:
        time.sleep(10)
