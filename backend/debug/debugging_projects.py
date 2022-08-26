from typing import Dict

from debug.debug_thread import DebugThread


class DebuggingProject:
    debug_thread: DebugThread


debugging_projects: Dict[str, DebuggingProject] = {}