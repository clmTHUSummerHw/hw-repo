import re
import os
from flask import request, jsonify
from db.models import User, Project
from db import db
from user_dict import user_dict

name_re = re.compile(r'\w{1,256}')

def new_project(): # 创建项目文件夹，并把项目信息加入数据库

    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        return jsonify({'code': -1})

    session = request.json['session']
    name = request.json['name']

    if not isinstance(session, str) or not isinstance(name, str): # 若request没有username或password，返回-1（未知错误）
        return jsonify({'code': -1})
    
    if session not in user_dict: # 在用户名单里没有找到对应session，返回1（session无效）
        return jsonify({'code': 1})

    if not name_re.match(name): # 通过正则表达式检查name是否符合规范，若不符合，返回2（项目名不符合规范）
        return jsonify({'code': 2})

    username = user_dict[session].username
    user = User.query.filter_by(username=username).first()
    project = user.projects.filter_by(name = name).first()

    if project is not None: # 若数据库中能查询到该项目，返回3（项目已存在）
        return jsonify({'code': 3})

    # 创建项目，并添加到数据库
    if not os.path.exists('./project_storage/'+ username): # 如果该工程没有《用户项目存储文件夹》则生成一个
        os.makedirs('./project_storage/' + username)

    os.makedirs('./project_storage/' + username + '/' + name)

    project = Project(name, user)
    db.session.add(project)
    db.session.commit()

    return jsonify({'code': 0}) # 返回0（创建成功）
