from flask import request, jsonify
from project.utils import get_dependency_root

def add_dependency():
    if not request.is_json:
        return jsonify({'code': -1, 'files': []})

    session = request.json['session']
    project_name = request.json['project']

    if not isinstance(session, str) or not isinstance(project_name, str):
        return jsonify({'code': -1, 'files': []})

    code, root = get_dependency_root(session, project_name)