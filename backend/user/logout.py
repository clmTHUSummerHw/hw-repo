from flask import request, jsonify
from user.user_dict import user_dict

def logout(): # 释放session

    if not request.is_json: # 若传入的不是json对象，返回-1（未知错误）
        return jsonify({'code': -1})

    session = request.json['session']

    if not isinstance(session): # 若request没有session，返回-1（未知错误）
        return jsonify({'code': -1})

    if session not in user_dict: # 如果登录名单里没找到此session，返回-1（未知错误）
        return jsonify({'code': -1})

    del user_dict[session]
    return jsonify({'code': 0})  # 返回0（退出登录成功）