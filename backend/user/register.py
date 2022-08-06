import re
from flask import request, jsonify
from db.models import User
from db import db


username_re = re.compile(r'\w{2,16}')


def register():
    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        return jsonify({'code': -1})

    username = request.json['username']
    password = request.json['password']

    if not isinstance(username, str) or not isinstance(password, str): # 若request没有username或password，返回-1（未知错误）
        return jsonify({'code': -1})

    if not username_re.match(username): # 通过正则表达式检查username是否符合规范，若不符合，返回1（用户名不符合规范）
        return jsonify({'code': 1})

    user = User.query.filter_by(username=username).first()

    if user is not None: # 若数据库中能查询到该用户，返回2（用户已存在）
        return jsonify({'code': 2})

    # 创建用户并添加到数据库
    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'code': 0}) # 返回0（注册成功）