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

def discover_bot(service_name):
    """
    发现机器人主程序
    """
    services = consul_client.discover_services(service_name)
    if services:
        bot = services[0]
        RouteInfo.update_bot(ip=bot[0], port=bot[1])
        return True
    print('主程序未开启')
    return False
        
def discover_message_broker(service_name):
    """
    发现机器人主程序
    """
    services = consul_client.discover_services(service_name)
    if services:
        message_broker = services[0]
        RouteInfo.update_message_broker(ip=message_broker[0], port=message_broker[1])
        return True
    print('消息代理开启')
    return False
