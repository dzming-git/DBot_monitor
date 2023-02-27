import requests
from conf.route_info.route_info import RouteInfo

def send_message_to_main_program(message, gid=None, qid=None, at=False):
    ip = RouteInfo.get_message_broker_ip()
    port = RouteInfo.get_message_broker_port()
    endport = RouteInfo.get_message_broker_endpoint('server_results')
    url = f'http://{ip}:{port}/{endport}'
    response = requests.post(url, json={'message': message, 'gid': gid, 'qid': qid, 'at': at})
    return response.json()