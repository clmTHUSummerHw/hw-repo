from flask import request, jsonify
from project.utils import add_log_with_session, get_dependency_root

def add_dependency():
    session = request.form['session']
    project_name = request.form['project']

    if not isinstance(session, str) or not isinstance(project_name, str):
        return jsonify({'code': -1})

    code, root = get_dependency_root(session, project_name)

    if code != 0:
        return jsonify({'code': code})

    file = request.files['file']
    file.save(root + '/' + file.filename)
    add_log_with_session(session, project_name, 9, file.filename)
    return jsonify({'code': 0})