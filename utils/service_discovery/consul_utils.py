from utils.service_discovery.consul_client import consul_client
from conf.route_info.route_info import RouteInfo

def register_consul():
    '''
    服务开启前,注册consul
    '''
    service_name = RouteInfo.get_service_name()
    port = RouteInfo.get_service_port()
    monitor_id = consul_client.register_service(service_name, port, [])
    config = {
            'monitor_id': monitor_id
        }
    return config

def deregister_service(app):
    '''
    服务结束后,注销consul
    '''
    monitor_id = app.config['monitor_id']
    consul_client.deregister_service(monitor_id)

def discover_api_gateway(service_name):
    """
    发现机器人API网关
    """
    services = consul_client.discover_services(service_name)
    if services:
        api_gateway = services[0]
        RouteInfo.update_api_gateway(ip=api_gateway[0], port=api_gateway[1])
        return True
    print('API网关未开启')
    return False
        
def discover_message_broker(service_name):
    """
    发现机器人消息代理
    """
    services = consul_client.discover_services(service_name)
    if services:
        message_broker = services[0]
        RouteInfo.update_message_broker(ip=message_broker[0], port=message_broker[1])
        return True
    print('消息代理未开启')
    return False
