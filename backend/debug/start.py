from debug import debug_api
from project.utils import get_root
from run.get_out_root import get_out_root
from run.run_thread import RunThread
from debug.debug_thread import DebugThread
from debug.debugging_projects import debugging_projects, DebuggingProject


def start(data):
    session = data['session']
    project = data['project']

    if not isinstance(session, str) or not isinstance(project, str):
        debug_api.emit('run_start', {'code': -1})
        return

    #获得项目文件Main.java路径并获得class文件名
    code, root = get_root(session, project)
    if code != 0:
        debug_api.emit('run_start', {'code': code})
        return

    _code, class_root = get_out_root(session, project)

    #新开一个线程进行java编译 & 运行
    run_thread = RunThread(root, class_root, data.session, debug_api ,debug=True)
    debug_thread = DebugThread(session, debug_api)
    debugging_projects[session] = DebuggingProject(run_thread, debug_thread)
    run_thread.start()
    debug_thread.start()