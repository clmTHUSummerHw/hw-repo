from run.running_users import running_users, RunningUser
from run.run_thread import RunThread
from project.utils import get_root
from run.get_out_root import get_out_root
from run import run_api

def start(data): #TODO: 在一个新的线程中运行项目，并实时提供项目输出（注意，多个用户可能同时发起多个运行请求）

    session = data['session']
    project = data['project']

    if not isinstance(session, str) or not isinstance(project, str):
        run_api.emit('run_start', {'code': -1})
        return

    #获得项目文件Main.java路径并获得class文件名
    code, root = get_root(session, project)
    if code != 0:
        run_api.emit('run_start', {'code': code})
        return

    _code, class_root = get_out_root(session, project)

    #新开一个线程进行java编译 & 运行
    start_project = RunThread(root, class_root, data.session, run_api)
    running_users[data.session] = RunningUser(start_project)
    start_project.start()