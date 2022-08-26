import base64
import os
from flask import request, jsonify

from project.utils import add_log_with_session, get_root


def download_file():
    if not request.is_json:
        return jsonify({'code': -1, 'file': ''})

    session = request.json['session']
    project_name = request.json['project']
    file_full = request.json['name']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(file_full, str):
        return jsonify({'code': -1, 'file': ''})

    code, root = get_root(session, project_name)

    if code != 0:
        return jsonify({'code': code, 'file': ''})

    full = root + file_full

    if not os.path.exists(full):
        return jsonify({'code': 3, 'file': ''})

    if os.path.isdir(full):
        return jsonify({'code': 4, 'file': ''})

    try:
        f = open(full, encoding='utf-8')
        content = f.read()
        f.close()
        out = base64.b64encode(content.encode()).decode()
        add_log_with_session(session, project_name, 6, file_full)
        return jsonify({'code': 0, 'file': out})
    except Exception:
        return jsonify({'code': -1, 'file': ''})
