# app.py
from flask import Flask
import requests
from app.services.monitor_service import func_dict
from api.routes import route_registration
from conf.route_info.route_info import RouteInfo
from utils.service_discovery.consul_utils import register_consul, discover_bot, discover_message_broker, deregister_service

def download_message_broker_endpoints(app: Flask):
    # 下载消息代理的endpoint到主程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('message_broker_endpoints')
    try:
        response = requests.get(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}')
        response.raise_for_status()
        message_broker_endpoints_info = response.json()
        for endpoint, usage in message_broker_endpoints_info.items():
            RouteInfo.add_message_broker_endpoint(usage=usage, endpoint=endpoint)
        return True
    except Exception as e:
        return False

def upload_service_commands(app: Flask):
    # 注册支持的指令到主程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('service_commands')
    service_name = RouteInfo.get_service_name()
    commands = list(func_dict.keys())
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'commands': commands})

def upload_service_endpoints(app: Flask):
    # 注册支持的endpoint到主程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('service_endpoints')
    service_name = RouteInfo.get_service_name()
    endpoints_info = RouteInfo.get_service_endpoints_info()
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'endpoints_info': endpoints_info})

def create_monitor_app():
    monitor_app = Flask(__name__)
    flag = \
        discover_bot(RouteInfo.get_bot_name()) and \
        discover_message_broker(RouteInfo.get_message_broker_name()) and \
        download_message_broker_endpoints(monitor_app)
    if flag:
        config = {
            **register_consul()
        }
        monitor_app.config.update(config)
        upload_service_commands(monitor_app)
        upload_service_endpoints(monitor_app)
        route_registration(monitor_app)
        return monitor_app
    return None

def destory_monitor_app(app):
    deregister_service(app)
