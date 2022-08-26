from typing import Dict
from run.run_thread import RunThread

class RunningUser:
    run_thread: RunThread
    def __init__(self, run_thread: RunThread) -> None:
        self.run_thread = run_thread

running_users: Dict[str, RunningUser] = {}