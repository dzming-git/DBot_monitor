# monitor_server.py
import time
from conf.route_info.route_info import RouteInfo
from app.app import create_monitor_app, destory_monitor_app
from conf.authority.authority import Authority
from conf.camera_list.camera_list import CameraList

def load_conf():
    Authority._load_config('conf/authority/authority.yaml')
    CameraList._load_config('conf/camera_list/camera_list.yaml')
    RouteInfo._load_config('conf/route_info/route_info.yaml')

if __name__ == '__main__': 
    load_conf()

    monitor_app = None
    while not monitor_app:
        monitor_app = create_monitor_app()
        if not monitor_app:
            time.sleep(5)
    
    ip = RouteInfo.get_server_ip()
    server_port = RouteInfo.get_server_port()
    monitor_app.run(host=ip, port=server_port)
    destory_monitor_app(monitor_app)
