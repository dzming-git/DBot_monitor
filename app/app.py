# app.py
from flask import Flask
import requests
import time
import json
from app.services.monitor_service import func_dict
from api.routes import route_registration
from conf.route_info.route_info import RouteInfo
from utils.service_discovery.consul_utils import register_consul, discover_api_gateway, discover_message_broker, deregister_service
from utils.service_discovery.consul_client import consul_client

def download_message_broker_endpoints(app: Flask):
    # 下载消息代理的endpoint
    message_broker_consul_key = RouteInfo.get_message_broker_consul_key('message_broker_endpoints')
    message_broker_endpoints_info_str = consul_client.download_key_value(message_broker_consul_key)
    dictionary = json.loads(message_broker_endpoints_info_str.replace("'", "\""))
    if dictionary:
        for endpoint, usage in dictionary.items():
            RouteInfo.add_message_broker_endpoint(usage=usage, endpoint=endpoint)
        return True
    return False

def upload_service_commands(app: Flask):
    # 注册支持的指令到消息代理程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('service_commands')
    service_name = RouteInfo.get_service_name()
    commands = list(func_dict.keys())
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'commands': commands})

def upload_service_endpoints(app: Flask):
    # 注册支持的endpoint到消息代理程序
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('service_endpoints')
    service_name = RouteInfo.get_service_name()
    endpoints_info = RouteInfo.get_service_endpoints_info()
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'endpoints_info': endpoints_info})

def create_monitor_app():
    monitor_app = Flask(__name__)
    success_connect = False
    while not success_connect:
        success_connect = \
            discover_api_gateway(RouteInfo.get_api_gateway_name()) and \
            discover_message_broker(RouteInfo.get_message_broker_name()) and \
            download_message_broker_endpoints(monitor_app)
        if not success_connect:
            print('连接DBot平台程序失败，正在重连')
            time.sleep(1)
    config = {
        **register_consul()
    }
    monitor_app.config.update(config)
    upload_service_commands(monitor_app)
    upload_service_endpoints(monitor_app)
    route_registration(monitor_app)
    return monitor_app

def destory_monitor_app(app):
    deregister_service(app)
