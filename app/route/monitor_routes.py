# monitor_routes.py
from flask import Flask, request
import requests
from app.message_handler import message_handler
from app.message_handler.func_dict import func_dict
from api.consul_client import consul_client
from conf.conf import Conf

def register_consul():
    '''
    服务开启前,注册consul
    '''
    server_name = Conf.get_server_name()
    port = Conf.get_server_port()
    monitor_id = consul_client.register_server(server_name, port, [])
    config = {
            'monitor_id': monitor_id
        }
    return config

def deregister_server(app):
    '''
    服务结束后,注销consul
    '''
    monitor_id = app.config['monitor_id']
    consul_client.deregister_server(monitor_id)

def discover_bot(server_name):
    """
    发现机器人主程序
    """
    servers = consul_client.discover_servers(server_name)
    if servers:
        bot = servers[0]
        config = {
            'bot_find': True,
            'bot_ip': bot[0],
            'bot_port': bot[1],
        }
    else:
        config = {
            'bot_find': False,
        }
        print('主程序未开启')
    return config
        
def discover_message_broker(server_name):
    """
    发现机器人主程序
    """
    servers = consul_client.discover_servers(server_name)
    if servers:
        message_broker = servers[0]
        config = {
            'message_broker_find': True,
            'message_broker_ip': message_broker[0],
            'message_broker_port': message_broker[1],
        }
    else:
        config = {
            'message_broker_find': False,
        }
        print('消息代理开启')
    return config

def upload_server_commands(app: Flask):
    # 注册支持的指令到主程序
    message_broker_ip = app.config['message_broker_ip']
    message_broker_port = app.config['message_broker_port']
    server_name = Conf.get_server_name()
    commands = list(func_dict.keys())
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/server_commands', json={'server_name': server_name, 'commands': commands})


def create_monitor_app():
    monitor_app = Flask(__name__)

    bot_config = discover_bot(Conf.get_bot_name())
    message_broker_config = discover_message_broker(Conf.get_message_broker_name())

    if bot_config['bot_find'] and message_broker_config['message_broker_find']:
        config = {
            **bot_config,
            **message_broker_config,
            **register_consul()
        }
        monitor_app.config.update(config)
        upload_server_commands(monitor_app)
        return monitor_app

    return None

def destory_monitor_app(app):
    deregister_server(app)