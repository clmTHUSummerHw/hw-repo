import json
from run.getOutputThread import getOutputThread
from project.utils import get_root

def start(data): #TODO: 在一个新的线程中运行项目，并实时提供项目输出（注意，多个用户可能同时发起多个运行请求）

    #获得项目文件Main.java路径并获得class文件名
    code, root = get_root(data.session, data.projectname)
    java_file = root + '/Main.java'
    java_class = root + '/Main'

    #新开一个线程进行java编译 & 运行
    startProject = getOutputThread(java_file, java_class, data.session)
    startProject.start()