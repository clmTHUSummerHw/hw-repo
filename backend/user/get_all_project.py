from os.path import abspath
from flask import jsonify
from db.models import Project
from project.utils import get_root_for_admin

def get_all_project():
    project_query = Project.query.all()
    projects = []
    for project in project_query:
        #获取用户名
        projectUsername = project.user.username
        #获取项目名
        projectName = project.name
        #获取项目时间
        projectCreateDate = str(project.create_time)
        #获取路径
        projectFileDir = get_root_for_admin(projectUsername, projectName) #相对路径
        projectDirectory = abspath(projectFileDir) #绝对路径
        #打包成字典
        alone = {}
        alone['projectUsername'] = projectUsername
        alone['projectName'] = projectName
        alone['projectCreateDate'] = projectCreateDate
        alone['projectDirectory'] = projectDirectory
        projects.append(alone)

    return jsonify({'code': 0, 'projects': projects})
        