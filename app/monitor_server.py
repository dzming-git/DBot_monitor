# monitor_server.py
import time
from conf.conf import Conf
from app.route.monitor_routes import create_monitor_app, destory_monitor_app

CONF_PATH = './conf/conf.yaml'

if __name__ == '__main__': 
    Conf._load_config(CONF_PATH)

    monitor_app = None
    while not monitor_app:
        monitor_app = create_monitor_app()
        if not monitor_app:
            time.sleep(5)
    
    ip = Conf.get_server_ip()
    server_port = Conf.get_server_port()
    monitor_app.run(host=ip, port=server_port)
    destory_monitor_app(monitor_app)
