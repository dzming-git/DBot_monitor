# service.py
from app.services.service import func_dict, KEYWORD
from conf.camera_list.camera_list import CameraList
from app import func_dict, KEYWORD
from dbot import DBot

if __name__ == '__main__': 
    dbot = DBot()
    dbot.set_authority_config('conf/authority/authority.yaml')
    dbot.set_route_info_config('conf/route_info/route_info.yaml')
    dbot.set_consul_info_config('conf/consul_info/consul_info.yaml')
    CameraList.load_config('conf/camera_list/camera_list.yaml')
    dbot.set_keyword(KEYWORD)
    dbot.set_func_dict(func_dict)
    dbot.start()
