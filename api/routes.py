from flask import request
from conf.route_info.route_info import RouteInfo
from conf.authority.authority import Authority
from utils.tasks import task

def route_registration(app):
    receive_command_endpoint = RouteInfo.get_service_endpoint('receive_command')
    @app.route(f'/{receive_command_endpoint}', methods=['POST'])
    def receive_command():
        data = request.get_json()
        command = data['command']
        args = data['args']
        gid = data['gid']
        qid = data['qid']
        permission = Authority.check_command_permission(command=command, group_id=gid, qq_id=qid)
        task.add_task(command=command, args=args, gid=gid, qid=qid)
        return {'permission': permission}
    
    @app.route('/health')
    def health_check():
        return 'OK'