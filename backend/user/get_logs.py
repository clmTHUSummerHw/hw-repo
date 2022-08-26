from flask import request, jsonify
from db.models import User, Log
from db.models import Log

def get_logs():
    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        print('not an instance!')
        return jsonify({'code': -1, 'log': []})

    username = request.json['username']
    projectname = request.json['projectname']

    if not isinstance(username, str) or not isinstance(projectname, str): # 若request没有username或projectname，返回-1（未知错误）
        print('more info!')
        return jsonify({'code': -1, 'log': []})

    user = User.query.filter_by(username=username).first()
    project = user.projects.filter_by(name = projectname).first()

    if user is None: # 若数据库中查询不到该用户，返回1（用户不存在）
        return jsonify({'code': 1, 'log': []})

    if project is None: # 若数据库中能查询到该项目，返回2（项目不存在）
        return jsonify({'code': 2, 'log': []})

    logs = []
    for log in project.log.order_by(Log.time.desc()).all():
        alone = {}
        alone['code'] = log.code
        alone['time'] = log.time.timestamp()*1000
        alone['extra_data'] = log.extra_data
        logs.append(alone)

    return jsonify({'code': 0, 'log': logs}) # 返回0（返回项目日志）