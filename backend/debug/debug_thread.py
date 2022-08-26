from queue import Queue
import re
import subprocess
from threading import Thread
import time
from typing import Optional
from ws.ws_helper import WsHelper


line_re = re.compile(r'行=([0-9]+) bci=[0-9]+')
var_re = re.compile(r'([\w]+) = (.+)')


class DebugThread(Thread):
    debugger_process: Optional[subprocess.Popen] = None
    session: str = ''
    last_line: bytearray = bytearray()
    in_init: bool = True
    input_queue: Queue[str] = Queue()
    ws: WsHelper

    def __init__(self, session: str, ws: WsHelper) -> None:
        super().__init__()
        self.session = session
        self.ws = ws

    def handle_full_line(self):
        to_handle = self.last_line.decode('gbk')
        try_line = line_re.search(to_handle)

        if try_line:
            line = try_line.group(1)
            self.ws.emit(self.session, 'stop_at_line', {'line': int(line)})

        try_var = var_re.search(to_handle)
        if try_var:
            var = try_var.group(1)
            value = try_var.group(2)
            self.ws.emit(self.session, 'var_value', {'var': var, 'value': value})
        self.last_line = bytearray()

    def handle_input(self):
        while self.input_queue.empty():
                time.sleep(0.01)

        input_str = self.input_queue.get()
        self.debugger_process.stdin.write(input_str + '\n')
        self.debugger_process.stdin.flush()
        self.last_line = bytearray()

    def handle_new_byte(self, new_byte: int):
        self.last_line.append(new_byte)
        if self.last_line.endswith(b'\n'):
            self.handle_full_line()
        elif self.last_line.endswith(b'main[1] '):
            self.handle_input()

    def run(self):
        time.sleep(0.1)
        self.debugger_process = subprocess.Popen(
            ['jdb', '-attach', self.session],
            stdin=subprocess.PIPE,
            stdout = subprocess.PIPE
        )

        while self.debugger_process.poll() is None:
            new_byte = self.debugger_process.stdout.read(1)[0]
            self.handle_new_byte(new_byte)

        last_bytes = self.debugger_process.stdout.read()
        for i in last_bytes:
            self.handle_new_byte(i)