import yaml

class Conf:
    _conf = {}

    @classmethod
    def _load_config(cls, config_path):
        with open(config_path) as f:
            cls._conf = yaml.safe_load(f)

    @classmethod
    def get_rob_name(cls):
        return cls._conf.get('rob_name')

    @classmethod
    def get_server_ip(cls):
        return cls._conf.get('server_ip')

    @classmethod
    def get_gocqhttp_port(cls):
        return cls._conf.get('gocqhttp', {}).get('port')

    @classmethod
    def get_gocqhttp_tags(cls):
        return cls._conf.get('gocqhttp', {}).get('tags')

    @classmethod
    def get_gocqhttp_message_recv_route(cls):
        return cls._conf.get('gocqhttp', {}).get('message_recv_route')

    @classmethod
    def get_service_port(cls):
        return cls._conf.get('service', {}).get('port')

    @classmethod
    def get_service_func_dict_route(cls):
        return cls._conf.get('service', {}).get('func_dict_route')

