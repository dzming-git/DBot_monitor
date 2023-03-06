# task.py
import threading
from queue import Queue
import time
from app.services.monitor_service import func_dict
from utils.message_sender import send_result_message_to_message_broker

class TaskThread(threading.Thread):
    def __init__(self):
        super().__init__(name='TaskThread')
        self._task_queue = Queue()
        self._stop = False

    def add_task(self, command, args, gid=None, qid=None):
        self._task_queue.put({
            'command': command,
            'args': args,
            'gid': gid,
            'qid': qid
        })
    
    def exe_task(self, task):
        command = task['command']
        gid = task['gid']
        qid = task['qid']
        args = task['args']
        message = func_dict[command](gid=gid, qid=qid, msg_list=args)
        send_result_message_to_message_broker(message=message, gid=gid, qid=qid)

    def run(self):
        while not self._stop:
            task = self._task_queue.get(block=True)
            command = task['command']
            single_task_thread = threading.Thread(target=self.exe_task, args=(task, ), name=f'ExeTask:{command}')
            single_task_thread.start()
            
    
    def stop(self):
        self._stop = False

task_thread = TaskThread()
