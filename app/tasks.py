import threading
from queue import Queue
import time
from app.func_dict import func_dict
from api.message_sender import send_message_to_main_program

class Task:
    def __init__(cls):
        cls._task_queue = Queue()
        cls.t_exe_task = threading.Thread(target=cls.exe_task)
        cls.t_exe_task.start()

    def add_task(cls, command, args, gid=None, qid=None):
        cls._task_queue.put({
            'command': command,
            'args': args,
            'gid': gid,
            'qid': qid
        })
    
    def exe_task(cls):
        while True:
            task = cls._task_queue.get(block=True)
            command = task['command']
            gid = task['gid']
            qid = task['qid']
            args = task['args']
            message, at = func_dict[command](gid=gid, qid=qid, msg_list=args)
            send_message_to_main_program(message=message,gid=gid, qid=qid, at=at)
            time.sleep(0.1)

task = Task()
