import os
from flask import request, jsonify
from db.models import User
from db import db
from user_dict import user_dict


def delete_project(): # 从数据库中删除项目，并删除项目文件夹

    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        return jsonify({'code': -1})

    session = request.json['session']
    name = request.json['name']

    if not isinstance(session, str) or not isinstance(name, str): # 若request没有username或password，返回-1（未知错误）
        return jsonify({'code': -1})
    
    if session not in user_dict: # 在用户名单里没有找到对应session，返回1（session无效）
        return jsonify({'code': 1})

    username = user_dict[session].username
    user = User.query.filter_by(username=username).first()
    project = user.projects.filter_by(name = name).first()

    if not project: # 若数据库中不能查询到该项目，返回2（项目不存在）
        return jsonify({'code': 2})
    
    db.session.delete(project)
    db.session.commite()

    dir_path = './project_storage/' + username + '/' + name
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for f_name in files:
            os.remove(os.path.join(root, f_name))
        for pro_name in dirs:
            os.rmdir(os.path.join(root, pro_name))
    os.rmdir(dir_path)

    return jsonify({'code': 0}) #返回0（删除成功）