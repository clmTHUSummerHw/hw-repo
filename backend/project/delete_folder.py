import os
from flask import request, jsonify

from project.utils import get_root


def recursive_delete(path: str):
    if os.path.isfile(path):
        os.remove(path)
        return
    children = os.listdir(path)

    for i in children:
        recursive_delete(path + '/' + i)

    os.rmdir(path)


def delete_folder():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    file_full = request.json['name']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(file_full, str):
        return jsonify({'code': -1})

    if file_full == '/' or file_full == '\\':
        return jsonify({'code': -1})

    code, root = get_root(session, project_name)

    if code != 0:
        return jsonify({'code': code})

    full = root + file_full

    if not os.path.exists(full):
        return jsonify({'code': 3})

    if os.path.isfile(full):
        return jsonify({'code': 4})

    try:
        recursive_delete(full)
    except Exception:
        return jsonify({'code': -1})

    return jsonify({'code': 0})