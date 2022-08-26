import os
from flask import request, jsonify
from project.utils import add_log_with_session, get_dependency_root


def remove_dependency():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    dependency_name = request.json['dependency']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(dependency_name, str):
        return jsonify({'code': -1})

    code, root = get_dependency_root(session, project_name)
    if code != 0:
        return jsonify({'code': code})

    try:
        os.remove(root + '/' + dependency_name)
        add_log_with_session(session, project_name, 10, dependency_name)
        return jsonify({'code': 0})
    except Exception:
        return jsonify({'code': 3})