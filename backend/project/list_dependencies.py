from flask import request, jsonify
from project.utils import get_dependency_root


def list_dependencies():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    dependency_name = request.json['dependency']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(dependency_name, str):
        return jsonify({'code': -1})

    code, root = get_dependency_root(session, project_name)