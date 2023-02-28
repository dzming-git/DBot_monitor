# route_info.yaml
import yaml

class RouteInfo:
    _service_conf = {}
    _bot_conf = {}
    _message_broker_conf = {}

    @classmethod
    def _load_config(cls, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            cls._service_conf = config.get('service', {})
            cls._bot_conf = config.get('bot', {})
            cls._bot_conf['find'] = False
            cls._message_broker_conf = config.get('message_broker', {})
            cls._message_broker_conf['find'] = False

    # 机器人主程序配置方法
    @classmethod
    def get_bot_name(cls):
        return cls._bot_conf.get('name')
    
    @classmethod
    def is_bot_find(cls):
        return cls._bot_conf.get('find')
    
    @classmethod
    def update_bot(cls, ip, port):
        cls._bot_conf['find'] = True
        cls._bot_conf['ip'] = ip
        cls._bot_conf['port'] = port
    
    @classmethod
    def get_bot_ip(cls):
        if cls._bot_conf.get('find'):
            return cls._bot_conf.get('ip')
        return None
    
    @classmethod
    def get_bot_port(cls):
        if cls._bot_conf.get('find'):
            return cls._bot_conf.get('port')
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
    def get_message_broker_endpoint(cls, usage):
        return cls._message_broker_conf.get('endpoints')[usage]
