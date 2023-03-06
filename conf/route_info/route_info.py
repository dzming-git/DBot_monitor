# route_info.py
import yaml
from utils.watch_config import WatchDogThread
import copy
from utils.compare_dicts import compare_dicts

class RouteInfo:
    _config_path = ''
    _config = {}
    _watch_dog = None
    _service_conf = {}
    _api_gateway_find = False
    _message_broker_find = False
    _api_gateway_conf_from_file = {}
    _api_gateway_conf_from_consul = {}
    _message_broker_conf_from_file = {}
    _message_broker_conf_from_consul = {'endpoints': {}}

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        with open(config_path, 'r', encoding='utf-8') as f:
            cls._config = yaml.safe_load(f)
            cls._service_conf = cls._config.get('service', {})
            cls._api_gateway_conf_from_file = cls._config.get('api_gateway', {})
            cls._message_broker_conf_from_file = cls._config.get('message_broker', {})
            if not reload_flag:
                cls._config_path = config_path
                cls._watch_dog = WatchDogThread(config_path, cls.reload_config)
                cls._watch_dog.start()

    @classmethod
    def reload_config(cls):
        config_old = copy.deepcopy(cls._config)
        cls.load_config(config_path=cls._config_path, reload_flag=True)
        config_new = copy.deepcopy(cls._config)
        added_dict, deleted_dict, modified_dict = compare_dicts(config_old, config_new)
        if added_dict or deleted_dict or modified_dict:
            from app.app import monitor_server_thread
            monitor_server_thread.restart()

    # 机器人API网关配置方法
    @classmethod
    def get_api_gateway_name(cls):
        return cls._api_gateway_conf_from_file.get('name')
    
    @classmethod
    def is_api_gateway_find(cls):
        return cls._api_gateway_find
    
    @classmethod
    def update_api_gateway(cls, ip, port):
        cls._api_gateway_find = True
        cls._api_gateway_conf_from_consul['ip'] = ip
        cls._api_gateway_conf_from_consul['port'] = port
    
    @classmethod
    def get_api_gateway_ip(cls):
        if cls._api_gateway_find:
            return cls._api_gateway_conf_from_consul.get('ip')
        return None
    
    @classmethod
    def get_api_gateway_port(cls):
        if cls._api_gateway_find:
            return cls._api_gateway_conf_from_consul.get('port')
        return None

    # 服务程序配置方法
    @classmethod
    def get_service_name(cls):
        return cls._service_conf.get('name')

    @classmethod
    def get_service_ip(cls):
        return cls._service_conf.get('ip')

    @classmethod
    def get_service_port(cls):
        return cls._service_conf.get('port')

    @classmethod
    def get_service_tags(cls):
        return cls._service_conf.get('tags')
    
    @classmethod
    def get_service_endpoints_info(cls):
        return cls._service_conf.get('endpoints')
    
    @classmethod
    def get_service_endpoint(cls, usage):
        return cls._service_conf.get('endpoints')[usage]

    # 消息代理配置方法
    @classmethod
    def get_message_broker_name(cls):
        return cls._message_broker_conf_from_file.get('name')
    
    @classmethod
    def is_message_broker_find(cls):
        return cls._message_broker_find
    
    @classmethod
    def update_message_broker(cls, ip, port):
        cls._message_broker_find = True
        cls._message_broker_conf_from_consul['ip'] = ip
        cls._message_broker_conf_from_consul['port'] = port
    
    @classmethod
    def get_message_broker_ip(cls):
        if cls._message_broker_find:
            return cls._message_broker_conf_from_consul.get('ip')
        return None
    
    @classmethod
    def get_message_broker_port(cls):
        if cls._message_broker_find:
            return cls._message_broker_conf_from_consul.get('port')
        return None
    
    @classmethod
    def add_message_broker_endpoint(cls, usage, endpoint):
        cls._message_broker_conf_from_consul['endpoints'][usage] = endpoint
    
    @classmethod
    def get_message_broker_endpoint(cls, usage):
        return cls._message_broker_conf_from_consul.get('endpoints')[usage]
    
    @classmethod
    def get_message_broker_consul_key(cls, usage):
        return cls._message_broker_conf_from_file.get('consul_key')[usage]
