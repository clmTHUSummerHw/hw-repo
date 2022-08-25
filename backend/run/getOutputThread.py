import subprocess, threading, json
from subprocess import PIPE
import run

class getOutputThread(threading.Thread):
    def __init__(self, command1: str, command2: str, session: str):
        super().__init__()
        self.command1 = ['javac', command1] #编译命令
        self.command2 = ['java', command2] #运行命令
        self.usersession = session
    def run(self):
        
        compileSubprocess = subprocess.run(self.command1, stdout=PIPE) #编译
        executeSubprocess = subprocess.Popen(self.command2, stdout=PIPE) #运行
        while executeSubprocess.poll() is None: #子进程未结束
            array = bytearray()
            while True:
                if executeSubprocess.poll() is not None: #中间多检查一次进程是否结束，以便跳出循环
                    break
                currentByte = executeSubprocess.stdout.read(1)
                if currentByte != b'\n':
                    array += currentByte
                else:
                    #发送array
                    new_array = array[:-1].decode() #去除末尾'\r'，可能不需要
                    json_result = json.dumps(new_array)
                    run.run_api(self.usersession, 'new stdout', json_result) #发送事件
                    break
        #子进程结束


