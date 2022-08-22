from flask import request, jsonify


def new_file():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    file_name = request.json['name']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(file_name, str):
        return jsonify({'code': -1})