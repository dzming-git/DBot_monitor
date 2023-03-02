# route_info.yaml
import yaml

class RouteInfo:
    _service_conf = {}
    _api_gateway_conf = {
        'find': False
    }
    _message_broker_conf = {
        'find': False
    }

    @classmethod
    def _load_config(cls, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            cls._service_conf = config.get('service', {})
            cls._api_gateway_conf = config.get('api_gateway', {})
            cls._message_broker_conf = config.get('message_broker', {})

    # 机器人API网关配置方法
    @classmethod
    def get_api_gateway_name(cls):
        return cls._api_gateway_conf.get('name')
    
    @classmethod
    def is_api_gateway_find(cls):
        return cls._api_gateway_conf.get('find')
    
    @classmethod
    def update_api_gateway(cls, ip, port):
        cls._api_gateway_conf['find'] = True
        cls._api_gateway_conf['ip'] = ip
        cls._api_gateway_conf['port'] = port
    
    @classmethod
    def get_api_gateway_ip(cls):
        if cls._api_gateway_conf.get('find'):
            return cls._api_gateway_conf.get('ip')
        return None
    
    @classmethod
    def get_api_gateway_port(cls):
        if cls._api_gateway_conf.get('find'):
            return cls._api_gateway_conf.get('port')
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
        return cls._message_broker_conf.get('name')
    
    @classmethod
    def is_message_broker_find(cls):
        return cls._message_broker_conf.get('find')
    
    @classmethod
    def update_message_broker(cls, ip, port):
        cls._message_broker_conf['find'] = True
        cls._message_broker_conf['ip'] = ip
        cls._message_broker_conf['port'] = port
    
    @classmethod
    def get_message_broker_ip(cls):
        if cls._message_broker_conf.get('find'):
            return cls._message_broker_conf.get('ip')
        return None
    
    @classmethod
    def get_message_broker_port(cls):
        if cls._message_broker_conf.get('find'):
            return cls._message_broker_conf.get('port')
        return None
    
    @classmethod
    def add_message_broker_endpoint(cls, usage, endpoint):
        cls._message_broker_conf['endpoints'][usage] = endpoint
    
    @classmethod
    def get_message_broker_endpoint(cls, usage):
        return cls._message_broker_conf.get('endpoints')[usage]
    
    @classmethod
    def get_message_broker_consul_key(cls, usage):
        return cls._message_broker_conf.get('consul_key')[usage]
