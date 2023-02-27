# consul_client.py
import consul
import socket

class ConsulClient:
    def __init__(self, host='localhost', port=8500):
        self.consul = consul.Consul(host=host, port=port)

    def register_server(self, server_name, server_port, server_tags=None):
        """
        注册服务到Consul
        """
        server_id = f'{server_name}-{socket.gethostname()}'
        server_address = socket.gethostbyname(socket.gethostname())
        server_check = consul.Check.http(url=f'http://{server_address}:{server_port}/health', interval='10s')
        self.consul.agent.service.register(name=server_name, service_id=server_id, address=server_address, port=server_port, tags=server_tags, check=server_check)
        return server_id

    def deregister_server(self, server_id):
        """
        从Consul中注销服务
        """
        self.consul.agent.service.deregister(server_id)

    def discover_servers(self, server_name):
        """
        发现服务
        """
        servers = self.consul.catalog.service(server_name)[1]
        return [(server['ServiceAddress'], server['ServicePort']) for server in servers]

consul_client = ConsulClient()
