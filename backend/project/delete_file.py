import os
from flask import request, jsonify

from project.utils import add_log_with_session, get_root


def delete_file():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    file_full = request.json['name']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(file_full, str):
        return jsonify({'code': -1})

    code, root = get_root(session, project_name)

    if code != 0:
        return jsonify({'code': code})

    full = root + file_full

    if not os.path.exists(full):
        return jsonify({'code': 3})

    if os.path.isdir(full):
        return jsonify({'code': 4})

    try:
        os.remove(full)
    except Exception:
        return jsonify({'code': -1})

    add_log_with_session(session, project_name, 3, file_full)
    return jsonify({'code': 0})