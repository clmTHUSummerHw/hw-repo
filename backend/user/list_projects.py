from flask import request, jsonify
from db.models import User
from user_dict import user_dict


def list_projects(): # 从数据库中查询用户的所有项目

    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        return jsonify({'code': -1, 'project': []})

    session = request.json['session']

    if not isinstance(session, str): # 若request没有username或password，返回-1（未知错误）
        return jsonify({'code': -1, 'project': []})
    
    if session not in user_dict: # 在用户名单里没有找到对应session，返回1（session无效）
        return jsonify({'code': 1, 'project': []})

    username = user_dict[session].username
    user = User.query.filter_by(username=username).first()

    names = []
    for project in user.projects.all():
        names.append(project.name)
    
    return jsonify({'code': 0, 'project': names}) # 返回0（获取成功）
