import yaml

class Conf:
    _server_conf = {}
    _bot_conf = {  }
    _message_broker_conf = {}

    @classmethod
    def _load_config(cls, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            cls._server_conf = config.get('server', {})
            cls._bot_conf = config.get('bot', {})
            cls._message_broker_conf = config.get('message_broker', {})

    # 服务程序配置方法
    @classmethod
    def get_bot_name(cls):
        return cls._bot_conf.get('name')

    # 服务程序配置方法
    @classmethod
    def get_server_name(cls):
        return cls._server_conf.get('name')

    @classmethod
    def get_server_ip(cls):
        return cls._server_conf.get('ip')

    @classmethod
    def get_server_port(cls):
        return cls._server_conf.get('port')

    @classmethod
    def get_server_tags(cls):
        return cls._server_conf.get('tags')

    # 消息代理配置方法
    @classmethod
    def get_message_broker_name(cls):
        return cls._message_broker_conf.get('name')
