from typing import Dict

from run.run_thread import RunThread
from debug.debug_thread import DebugThread


class DebuggingProject:
    run_thread: RunThread
    debug_thread: DebugThread
    def __init__(self, run_thread: RunThread, debug_thread: DebugThread) -> None:
        self.run_thread = run_thread
        self.debug_thread = debug_thread


debugging_projects: Dict[str, DebuggingProject] = {}