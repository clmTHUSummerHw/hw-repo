import subprocess, threading
from subprocess import PIPE
from typing import Optional
from ws.ws_helper import WsHelper
from run.running_users import running_users
from debug.debugging_projects import debugging_projects

class RunThread(threading.Thread):
    execute_subprocess: Optional[subprocess.Popen] = None
    def __init__(self, source_root: str, class_root: str, session: str, ws: WsHelper, debug: bool = False):
        super().__init__()
        self.command1 = ['javac', source_root, '-d', class_root, '-g'] #编译命令
        if not debug:
            self.command2 = ['java', '-classpath', class_root, 'Main'] #运行命令
        else:
            self.command2 = [
                'java',
                '-agentlib:jdwp=transport=dt_shmem,address=%s,server=y,suspend=y' % session,
                '-classpath',
                class_root,
                'Main'
                ]
        self.user_session = session
        self.ws = ws
        self.array = bytearray()
        self.debug = debug
    def run(self):
        subprocess.run(self.command1, stdout=PIPE) #编译
        self.execute_subprocess = subprocess.Popen(self.command2, stdin=PIPE, stdout=PIPE) #运行
        while self.execute_subprocess.poll() is None: #子进程未结束
            currentByte = self.execute_subprocess.stdout.read(1)
            if currentByte != b'\n':
                self.array += currentByte
            else:
                #发送array
                text = self.array[:-1].decode() #去除末尾'\r'，可能不需要
                self.ws.emit(self.user_session, 'output', {'text': text}) #发送事件
                self.array = bytearray()

        last_outputs = self.execute_subprocess.stdout.read() # 子进程结束后，需要一次性读出所有未读完的输出
        self.ws.emit(self.user_session, 'output', {'text': last_outputs.decode()})
        self.ws.emit(self.user_session, 'run_complete')
        #子进程结束
        if not self.debug:
            del running_users[self.user_session]
        else:
            del debugging_projects[self.user_session]


