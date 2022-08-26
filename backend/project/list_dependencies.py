import os
from flask import request, jsonify
from project.utils import get_dependency_root


def list_dependencies():
    if not request.is_json:
        return jsonify({'code': -1, 'dependencies': []})

    session = request.json['session']
    project_name = request.json['project']

    if not isinstance(session, str) or not isinstance(project_name, str):
        return jsonify({'code': -1, 'dependencies': []})

    code, root = get_dependency_root(session, project_name)
    if code != 0:
        return jsonify({'code': code, 'dependencies': []})

    files = os.listdir(root)
    return jsonify({'code': 0, 'dependencies': files})