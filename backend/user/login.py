import random
import os
from flask import request, jsonify
from db.models import User
from user.user_dict import user_dict, joindict


def login(): # 处理登录请求，创建session

    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        return jsonify({'code': -1, 'session': 'QAQ'})

    username = request.json['username']
    password = request.json['password']

    if not isinstance(username, str) or not isinstance(password, str): # 若request没有username或password，返回-1（未知错误）
        return jsonify({'code': -1, 'session': 'QAQ'})


    user = User.query.filter_by(username=username).first()

    if user is None: # 若数据库中查询不到该用户，返回2（用户不存在）
        return jsonify({'code': 2, 'session': '@Y@'})

    if user.password != password: # 若用户密码错误，返回1
        return jsonify({'code': 1, 'session': 'Orz'})

    if not os.path.exists('./project_storage'): # 如果该工程没有《用户项目总存储文件夹》则生成一个
        os.makedirs('./project_storage')
    
    session = get_random_str()
    while session in user_dict:
        session = get_random_str()

    joindict(session, username)
    return jsonify({'code':0, 'session': session}) # 返回0（登录成功）



def get_random_str(): # 生成16字节长的session，仅包含字母和数字，且区分大小写
    random_str = ''

    digits = '0123456789'
    ascii_letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_list = [random.choice(digits + ascii_letters) for i in range(16)]
    random_str = random_str.join(str_list)

    return random_str