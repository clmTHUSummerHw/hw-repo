import os
import subprocess
from threading import Thread
import time
from typing import Optional


class DebugThread(Thread):
    debugger_process: Optional[subprocess.Popen] = None
    main_path: str = '.'
    last_line: bytearray = bytearray()
    in_init: bool = True

    def __init__(self, main_path) -> None:
        super().__init__()
        self.main_path = main_path

    def run(self):
        self.debugger_process = subprocess.Popen(
            ['jdb', '-classpath', self.main_path, 'Main'],
            stdin=subprocess.PIPE,
            stdout = subprocess.PIPE
        )

        while self.debugger_process.poll() is None:
            self.last_line.append(self.debugger_process.stdout.read(1)[0])
            if self.last_line.endswith(b'\n'):
                print(self.last_line.decode('gbk'))
                self.last_line = bytearray()

            if self.in_init and self.last_line.endswith(b'> '):
                print(self.last_line.decode('gbk'))
                self.last_line = bytearray()
                self.debugger_process.stdin.write(b'run\n')
                self.debugger_process.stdin.flush()
                self.in_init = False

            time.sleep(0.001)

        self.last_line.extend(self.debugger_process.stdout.read())
        print(self.last_line.decode('gbk'))


a = DebugThread('./local/test_java/out')

a.start()