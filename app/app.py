# app.py
from flask import Flask
import requests
from app.services.monitor_service import func_dict
from api.routes import route_registration
from conf.route_info.route_info import RouteInfo
from utils.service_discovery.consul_utils import register_consul, discover_bot, discover_message_broker, deregister_service

def upload_service_commands(app: Flask):
    # 注册支持的指令到主程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('upload_commands')
    service_name = RouteInfo.get_service_name()
    commands = list(func_dict.keys())
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'commands': commands})

def upload_service_endpoints(app: Flask):
    # 注册支持的endpoint到主程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('upload_endpoints')
    service_name = RouteInfo.get_service_name()
    endpoints_info = RouteInfo.get_service_endpoints_info()
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'endpoints_info': endpoints_info})

def create_monitor_app():
    monitor_app = Flask(__name__)
    discover_bot(RouteInfo.get_bot_name())
    discover_message_broker(RouteInfo.get_message_broker_name())

    if RouteInfo.is_bot_find() and RouteInfo.is_message_broker_find():
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
